from .models import MenuItem, FoodOrder
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from django.views import View
import stripe
import json

# Create your views here.
class OrderView(View):
    def get(self, request, *args, **kwargs):
        # get every item from each category
        appetizers = MenuItem.objects.filter(category__name__contains='Appetizer')
        desserts = MenuItem.objects.filter(category__name__contains='Dessert')
        drinks = MenuItem.objects.filter(category__name__contains='Drink')
        # pass into context
        context = {
            'appetizers': appetizers,
            'desserts': desserts,
            'drinks': drinks,
        }
        # render the template
        return render(request, 'order.html', context)

    def post(self, request, *args, **kwargs):
        user = request.user
        person_name = user.first_name + user.last_name
        person_email = user.email
        
        order_items = {'items': []}
        items = request.POST.getlist('items[]')
        for item in items:
            menu_item = MenuItem.objects.get(pk__contains=int(item))
            item_data = {
                'id': menu_item.pk,
                'name': menu_item.name,
                'price': menu_item.price
            }
            order_items['items'].append(item_data)
        
        price = 0
        item_ids = []
        
        for item in order_items['items']:
            price += item['price']
            item_ids.append(item['id'])
        
        order = FoodOrder.objects.create(
            name=person_name,
            email=person_email,
            price=price
        )
        order.items.add(*item_ids)
        
        # After everything is done, send confirmation email to the user
        body = ('Thank you for your order! Your food is being made and will be available soon!\n'
                f'Your total: {price}\n'
                'Thank you again for your order!')
                
        send_mail(
            'Thank You For Your Order!',
            body,
            'example@example.com',
            [person_email],
            fail_silently=False
        )
        customer = stripe.Customer.create(
            name=person_name,
            email=person_email
        )
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url="http://127.0.0.1:8000/success",
                cancel_url="http://127.0.0.1:8000/cancel",
                payment_method_types=["card"],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': int(price)*100,
                            'product_data': {
                                'name': 'Food',
                            },
                        },
                        'quantity': 1
                    },
                ],
                mode="payment",
            )
            print('hihi')
            context = {
                'checkout_id': checkout_session.id,
                'pk': order.pk,
                'items': order.items,
                'price': price
            }
            return render(request, 'orderConfirmation.html', context)
        except Exception as e:
            print('failed , ', request.session)
            return render(request, 'failure.html', {'error': e})

class OrderConfirmation(View):
    def get(self, request, pk, *args, **kwargs):
        order = FoodOrder.objects.get(pk=pk)
        context = {
            'pk': order.pk,
            'items': order.items,
            'price': order.price,
        }
        return render(request, 'orderConfirmation.html', context)

    def post(self, request, pk, *args, **kwargs):
        data = json.loads(request.body)
        if data['isPaid']:
            order = FoodOrder.objects.get(pk=pk)
            order.is_paid = True
            order.save()

        return redirect('paymentConfirmation')

class OrderPayConfirmation(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'orderPayConfirmation.html')
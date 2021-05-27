from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import ListView, View, DeleteView
from django.urls import reverse, reverse_lazy
from .models import Room, Booking, Person,RoomCategory
from .forms import AvailabilityForm, PersonForm
from hotel.booking_functions.availability import check_availability
from django.contrib.auth.models import User
from hotel.booking_functions.find_total_room_charge import find_total_room_charge
from django.contrib.auth.decorators import login_required

# from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import stripe
stripe.api_key = 'sk_test_51IvCaFSC7JV9pI8OXxMGewXj7uiWzk1XKy7AuFB6MdPu35Lz2cvt3VDAj8JRw6EJoO05FiWNf39WXRPEXpCk7R1q00F6AyVmpO'

# Create your views here.

class BookingFormView(View):
    def get(self, request, *args, **kwargs):
        if "check_in" in request.session:
            s = request.session
            form_data = {
                "check_in": s['check_in'], "check_out": s['check_out'], "room_category": s['room_category']}
            form = AvailabilityForm(request.POST or None, initial=form_data)
        else:
            form = AvailabilityForm()
        return render(request, 'bookingform.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AvailabilityForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            request.session['check_in'] = data['check_in'].strftime(
                "%Y-%m-%dT%H:%M")
            request.session['check_out'] = data['check_out'].strftime(
                "%Y-%m-%dT%H:%M")
            request.session['room_category'] = data['room_category'].category
            request.session['amount'] = find_total_room_charge(
                data['check_in'], data['check_out'], data['room_category'])
            # return redirect(reverse('account_login'))
            return redirect('hotel:CheckoutView')
        return HttpResponse('form not valid', form.errors)


def RoomListView(request):
    rooms = Room.objects.all()
    context = {
        "room_list": rooms,
    }
    return render(request, 'allroom.html', context)


class BookingListView(ListView):
    model = Booking
    template_name = "booking_list_view.html"

    def get_queryset(self, *args, **kwargs):
        if self.request.user.is_staff:
            booking_list = Booking.objects.all()
            return booking_list
        else:
            booking_list = Booking.objects.filter(user=self.request.user)
            return booking_list

    # def get_context_data(self, **kwargs):
    #     room = Room.objects.all()[0]
    #     room_categories = dict(room.ROOM_CATEGORIES)
    #     context = super().get_context_data(**kwargs)
    #     context


class RoomDetailView(View):
    def get(self, request, *args, **kwargs):
        print(self.request.user)
        category = self.kwargs.get('category', None)
        print(category)
        form = AvailabilityForm()
        room_list = Room.objects.filter(category=category)

        if len(room_list) > 0:
            room = room_list[0]
            room_category = dict(room.ROOM_CATEGORIES).get(room.category, None)
            context = {
                'room_category': room_category,
                'form': form,
            }
            return render(request, 'room_detail_view.html', context)
        else:
            return HttpResponse('Category does not exist')


class CancelBookingView(DeleteView):
    model = Booking
    template_name = 'booking_cancel_view.html'
    success_url = reverse_lazy('hotel:BookingListView')


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('/accounts/login')
        person_form = PersonForm()
        context = {
            "person_form": person_form,
        }
        return render(request, 'checkout.html', context)

    def post(self, request, *args, **kwargs):
        person_name = request.POST['name']
        person_email = request.POST['email']
        room = RoomCategory.objects.get(category = request.session['room_category'])
        customer = stripe.Customer.create(
            name=person_name,
            email=person_email
        )
        person = Person.objects.create(
            name=person_name,
            email=person_email
        )
        person.save()
        try:
            stripe.api_key = 'sk_test_51IvCaFSC7JV9pI8OXxMGewXj7uiWzk1XKy7AuFB6MdPu35Lz2cvt3VDAj8JRw6EJoO05FiWNf39WXRPEXpCk7R1q00F6AyVmpO'
            checkout_session = stripe.checkout.Session.create(
                success_url="http://127.0.0.1:8000/success",
                cancel_url="http://127.0.0.1:8000/cancel",
                payment_method_types=["card"],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'inr',
                            'unit_amount': int(room.rate)*100,
                            'product_data': {
                                'name': request.session['room_category'],
                            },
                        },
                        'quantity': 1
                    },
                ],
                mode="payment",
            )
            # booking = Booking.objects.create(
            #     user = request.user,
            #     room = request.session['room_category'],
            #     check_in = request.session['check_in'],
            #     check_out = request.session['check_out'],
            #     payment_status = 'INC'
            # )
            # print(booking)
            # booking.save()
            context = {
                'person': person,
                'checkout_id': checkout_session.id,
                # 'amount':  request.session['amount'],
                'room_image': '',
                'room_name': request.session['room_category'],
                'amount': room.rate, #request.session['amount'],
                'check_in': request.session['check_in'],
                'check_out': request.session['check_out'],
            }

            print('chkout_context = ', context)
            return render(request, 'checkoutconfirm.html', context)
        except Exception as e:
            print('failed , ', request.session)
            return render(request, 'failure.html', {'error': e})

def HomeView(request):
    return render(request, 'home.html')

def AboutView(request):
    return render(request, 'about.html')

def success_view(request):
    return render(request, 'success.html')


def cancel_view(request):
    return render(request, 'cancel.html')


def ContactUsView(request):
    return render(request, 'contactus.html')
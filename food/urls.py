from django.urls import path
from .views import OrderView, OrderConfirmation, OrderPayConfirmation
app_name = 'food'

urlpatterns = [
    path('', OrderView.as_view(), name='order'),
    path('order-confirmation/<int:pk>', OrderConfirmation.as_view(), name='order-confirmation'),
    path('payment-confirmation/', OrderPayConfirmation.as_view(), name='payment-confirmation'),
]

from django.urls import path
from .views import HomeView, AboutView, RoomListView, ContactUsView, BookingListView, RoomDetailView, CancelBookingView, CheckoutView, success_view, cancel_view, BookingFormView
app_name = 'hotel'

urlpatterns = [
    path('', HomeView, name='HomeView'),
    path('about', AboutView, name='AboutView'),
    path('allrooms', RoomListView, name='RoomListView'),
    path('book/', BookingFormView.as_view(), name='BookingFormView'),
    path('booking_list/', BookingListView.as_view(), name='BookingListView'),
    path('room/<category>', RoomDetailView.as_view(), name='RoomDetailView'),
    path('booking/cancel/<pk>', CancelBookingView.as_view(),
         name='CancelBookingView'),
    path('checkout/', CheckoutView.as_view(), name='CheckoutView'),
    path('success/', success_view, name='success_view'),
    path('cancel/', cancel_view, name='cancel_view'),
    path('contact/', ContactUsView, name="ContactUsView")

]

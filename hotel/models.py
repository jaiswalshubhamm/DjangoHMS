from django.db import models
from django.conf import settings
from django.urls import reverse_lazy

# Create your models here.

class RoomCategory(models.Model):
    id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50)
    rate = models.FloatField()

    def __str__(self):
        return self.category


class Room(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    beds = models.IntegerField()
    capacity = models.IntegerField()
    category = models.ForeignKey(
        RoomCategory, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.number}. Beds = {self.beds} People = {self.capacity}'


class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    PAYMENT_STATUSES = (
        ('COM', 'PAYMENT_COMPLETE'),
        ('INC', 'PAYMENT_INCOMPLETE'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    payment_status = models.CharField(max_length=3, choices=PAYMENT_STATUSES)

    def __str__(self):
        return f'From = {self.check_in.strftime("%d-%b-%Y %H:%M")} To = {self.check_out.strftime("%d-%b-%Y %H:%M")}'

    def get_cancel_booking_url(self):
        return reverse_lazy('hotel:CancelBookingView', args=[self.pk])
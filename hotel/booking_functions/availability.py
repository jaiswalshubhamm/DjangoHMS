from datetime import datetime, tzinfo
from hotel.models import Booking

def check_availability(room, check_in, check_out):
    booking_list = Booking.objects.filter(room=room)
    chkin = datetime.strptime(check_in, '%Y-%m-%dT%H:%M')
    chkout = datetime.strptime(check_out, '%Y-%m-%dT%H:%M')
    if(len(booking_list)==0):
        return True
    for booking in booking_list:
        if booking.check_in.replace(tzinfo=None) > chkout or booking.check_out.replace(tzinfo=None) < chkin:
            continue
        else:
            return False
    return True
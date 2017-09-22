from django import template
from ..models import Guest

register = template.Library()


@register.filter
def countguests(guestlist):  # Only one argument.
    guests = Guest.objects.filter(guestlist=guestlist)
    guestcount = 0
    for guest in guests:
        guestcount += guest.plusones
    guestcount += len(guests)

    return guestcount

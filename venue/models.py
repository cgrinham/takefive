from django.db import models
from django.utils.timezone import now


class Company(models.Model):
    name = models.CharField(max_length=40)
    reference = models.CharField(max_length=40)
    created = models.DateTimeField(editable=False, default=now)

    def __unicode__(self):
        return self.name

# Holds all venues owned by all companies
class Venue(models.Model):
    created = models.DateTimeField(editable=False, default=now)
    owner = models.ForeignKey(Company)
    name = models.CharField(max_length=40)
    reference = models.CharField(max_length=40)
    capacity = models.PositiveIntegerField("Venue Capacity")

    def __unicode__(self):
        return self.name

"""
# Venue Layout for Area Reservation
class VenueLayout(models.Model):
    venue = models.ForeignKey(Venue)
    name = models.CharField(max_length=120, default="Default Layout")

    def __unicode__(self):
        return self.name

class VenueLayoutArea(models.Model):
    layout = models.ForeignKey(VenueLayout)
    name = models.CharField(max_length=40)
    notes = models.CharField(max_length=500)

    def __unicode__(self):
        return self.name
"""



# Holds all Events for all venues
class Event(models.Model):
    venue = models.ForeignKey(Venue)
    name = models.CharField("Event Name", max_length=120)
    description = models.TextField("Description")
    datestart = models.DateField("Event Start Date")
    timestart = models.TimeField("Event Start Time")
    dateend = models.DateField("Event End Date")
    timeend = models.TimeField("Event End Time")
    # Time slots needed
    recurring = models.BooleanField("Recurring event")

    def __unicode__(self): 
        return "%s - %s - %s" % (self.venue.name, self.datestart, self.name)

# Holds title of guest lists for all events
class GuestList(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField("Guest List Title", max_length=100)
    maxguests = models.PositiveIntegerField("Maximum number of guests", default=50)
    listopen = models.BooleanField("List Open?",default=True)

    def __unicode__(self):
        return "%s - %s - %s" % (self.event.name, self.event.datestart, self.name)

# Holds all guests for all guestlists
class Guest(models.Model):
    guestlist = models.ForeignKey(GuestList)
    firstname = models.CharField("First Name", max_length=50)
    lastname = models.CharField("Last Name", max_length=50)
    email = models.EmailField("Email", max_length=254)
    member = models.BooleanField("Member")
    timeslot = models.CharField("Time Slot", max_length=50)
    plusones = models.PositiveIntegerField("Plus Ones")
    notes = models.CharField("Additional information", max_length=140, blank=True)
    arrived = models.BooleanField("Arrived", default=False)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)

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

    def __unicode__(self):
        return self.name

# Holds all Events for all venues
class Event(models.Model):
    venue = models.ForeignKey(Venue)
    name = models.CharField(max_length=120)
    description = models.TextField()
    datestart = models.DateField()
    timestart = models.TimeField()
    dateend = models.DateField()
    timeend = models.TimeField()
    # Time slots needed
    recurring = models.BooleanField()

    def __unicode__(self):
        return self.name

# Holds title of guest lists for all events
class GuestList(models.Model):
    event = models.ForeignKey(Event)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

# Holds all guests for all guestlists
class Guest(models.Model):
    guestlist = models.ForeignKey(GuestList)
    firstname = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    member = models.BooleanField()
    timeslot = models.CharField(max_length=50)
    plusones = models.PositiveIntegerField()
    notes = models.CharField(max_length=140)
    arrived = models.BooleanField(default=False)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)

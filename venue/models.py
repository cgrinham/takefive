from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

class Company(models.Model):
    name = models.CharField(max_length=40)
    reference = models.CharField(max_length=40)
    created = models.DateTimeField(editable=False, default=now)

    def __unicode__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company)

    def __unicode__(self):
        return self.user.username

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

# Holds all venues owned by all companies
class Venue(models.Model):
    created = models.DateTimeField(editable=False, default=now)
    owner = models.ForeignKey(Company)
    name = models.CharField(max_length=40)
    reference = models.CharField(max_length=40)
    capacity = models.PositiveIntegerField("Venue Capacity")
    defaultplusones = models.PositiveIntegerField("Default max Plus Ones")

    def __unicode__(self):
        return self.name

# Venue Layout for Area Reservation
class VenueLayout(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    name = models.CharField(max_length=120, default="Default Layout")
    description = models.CharField(max_length=400, blank=True)

    def __unicode__(self):
        return self.name

class VenueLayoutArea(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    layout = models.ForeignKey(VenueLayout)
    name = models.CharField(max_length=40)
    capacity = models.PositiveIntegerField()
    notes = models.CharField(max_length=500)
    price = models.PositiveIntegerField()

    def __unicode__(self):
        return "%s %s" (self.venue.name, self.name)


# Holds all Events for all venues
class Event(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    name = models.CharField("Event Name", max_length=120)
    description = models.TextField("Description")
    datestart = models.DateField("Event Start Date")
    timestart = models.TimeField("Event Start Time")
    dateend = models.DateField("Event End Date")
    timeend = models.TimeField("Event End Time")
    #venuelayout = models.ForeignKey(VenueLayout)
    # Time slots needed
    recurring = models.BooleanField("Recurring event")

    def __unicode__(self): 
        return "%s - %s - %s" % (self.venue.name, self.datestart, self.name)

# Holds title of guest lists for all events
class GuestList(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    event = models.ForeignKey(Event)
    name = models.CharField("Guest List Title", max_length=100)
    maxguests = models.PositiveIntegerField("Maximum number of guests", default=50)
    maxplusones = models.PositiveIntegerField("Maximum plus ones a guest can bring", default=1)
    listopen = models.BooleanField("List Open?",default=True)

    def __unicode__(self):
        return "%s - %s - %s" % (self.event.name, self.event.datestart, self.name)

# Holds all guests for all guestlists
class Guest(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    guestlist = models.ForeignKey(GuestList)
    firstname = models.CharField("First Name", max_length=50)
    lastname = models.CharField("Last Name", max_length=50)
    email = models.EmailField("Email", max_length=254)
    member = models.BooleanField("Member")
    timeslot = models.CharField("Time Slot", max_length=50)
    plusones = models.PositiveIntegerField("Plus Ones", default=0)
    notes = models.CharField("Additional information", max_length=140, blank=True)
    arrived = models.BooleanField("Arrived", default=False)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)


class AreaHireBooking(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    area = models.ForeignKey(VenueLayoutArea)
    firstname = models.CharField("First Name", max_length=50)
    lastname = models.CharField("Last Name", max_length=50)
    email = models.EmailField("Email Address", max_length=254)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True, max_length=18)  # validators should be a list

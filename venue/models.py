from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator


class Company(models.Model):
    name = models.CharField(max_length=40, unique=True)
    reference = models.CharField(max_length=40, unique=True)
    created = models.DateTimeField(editable=False, default=now)

    def __unicode__(self):
        return self.reference


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, blank=True, null=True)

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
    logo = models.CharField("Venue logo", max_length=12, blank=True, null=True)
    background = models.CharField("Background for public pages such as guestlist sign up", max_length=12, blank=True, null=True)

    def __unicode__(self):
        return self.reference


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


class AreaHireBooking(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    area = models.ForeignKey(VenueLayoutArea)
    firstname = models.CharField("First Name", max_length=50)
    lastname = models.CharField("Last Name", max_length=50)
    email = models.EmailField("Email Address", max_length=254)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the "
                                         "format: '+999999999'. Up to 15 "
                                         "digits allowed.")
    phone = models.CharField(validators=[phone_regex], blank=True,
                             max_length=18)  # validators should be a list


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
    # venuelayout = models.ForeignKey(VenueLayout)
    # Time slots needed

    def __unicode__(self):
        return "%s - %s - %s" % (self.venue.name, self.datestart, self.name)


class RecurringEvent(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    name = models.CharField("Event Name", max_length=120)
    description = models.TextField("Description")
    firstevent = models.DateField("First Event Date")
    lastevent = models.DateField("Last Event Date")
    timestart = models.TimeField("Event Start Time")
    timeend = models.TimeField("Event End Time")
    recurrence = models.CharField("Weekly or Monthly", max_length=7)
    monday = models.BooleanField("Recurs on Mondays", default=False)
    tuesday = models.BooleanField("Recurs on Tuesdays", default=False)
    wednesday = models.BooleanField("Recurs on Wednesdays", default=False)
    thursday = models.BooleanField("Recurs on Thursdays", default=False)
    friday = models.BooleanField("Recurs on Fridays", default=False)
    saturday = models.BooleanField("Recurs on Saturdays", default=False)
    sunday = models.BooleanField("Recurs on Sundays", default=False)

    def __unicode__(self):
        return "%s - %s - %s" % (self.venue.name, self.firstevent, self.name)


class RecurringEventDate(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    event = models.ForeignKey(RecurringEvent)
    datestart = models.DateField("Event Start Date")
    timestart = models.TimeField("Event Start Time")
    dateend = models.DateField("Event End Date")
    timeend = models.TimeField("Event End Time")

    def __unicode__(self):
        return self.event.name


# Holds title of guest lists for all events
class GuestList(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    event = models.ForeignKey(Event, blank=True, null=True)
    recurringevent = models.ForeignKey(RecurringEventDate,
                                       blank=True,
                                       null=True)
    name = models.CharField("Guest List Title", max_length=100)
    maxguests = models.PositiveIntegerField("Maximum number of guests",
                                            default=50)
    maxplusones = models.PositiveIntegerField(
                "Maximum plus ones a guest can bring",
                default=1)
    listopen = models.BooleanField("List Open?", default=True)

    def __unicode__(self):
        if self.event:
            return "%s - %s - %s" % (self.event.name, self.event.datestart,
                                     self.name)
        else:
            return self.name


# Holds all guests for all guestlists
class Guest(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    guestlist = models.ForeignKey(GuestList)
    firstname = models.CharField("First Name", max_length=50)
    lastname = models.CharField("Last Name", max_length=50)
    email = models.EmailField("Email", max_length=254)
    member = models.BooleanField("Member", default=False)
    timeslot = models.CharField("Time Slot", max_length=50)
    plusones = models.PositiveIntegerField("Plus Ones", default=0)
    notes = models.CharField("Additional information", max_length=140,
                             blank=True)
    arrived = models.BooleanField("Arrived", default=False)
    source = models.CharField(default="internal", max_length=100)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)


class Member(models.Model):
    firstname = models.CharField("First Name", max_length=50)
    lastname = models.CharField("Last Name", max_length=50)
    email = models.EmailField("Email", max_length=254)
    dateofbirth = models.DateField("Date of Birth")
    appearances = models.PositiveIntegerField(default=0)

    def __unicode__(self):
        return "%s %s" % (self.firstname, self.lastname)


class MembershipType(models.Model):
    company = models.ForeignKey(Company)
    venue = models.ForeignKey(Venue)
    name = models.CharField(max_length=254)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    length = models.CharField(max_length=10)
    membershipopen = models.BooleanField(default=True)
    hidden = models.BooleanField("Hidden membership type", default=False)
    agerestriction = models.PositiveIntegerField(default=18)
    # Length notation
    # YMD (years, months, weeks or days) followed by number of
    # i.e. Y2 = 2 years, M3 = 3 Months

    def __unicode__(self):
        return self.name


class Membership(models.Model):
    """ Membership relationships """
    member = models.ForeignKey(Member)
    membershiptype = models.ForeignKey(MembershipType)
    starts = models.DateField("Date started")
    expires = models.DateField("Membership expiry date")
    paid = models.BooleanField("Membership paid", default=False)

    def __unicode__(self):
        return "%s %s" % (self.member.firstname, self.member.lastname)

from django import forms
from .models import Company, Venue, VenueLayout, Event, Guest, Member
from .models import Membership, MembershipType, GuestList, AreaHireBooking
from .models import VenueLayoutArea, RecurringEvent
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import datetime


class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )


class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']


class NewVenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'capacity', 'defaultplusones']


class NewVenueLayoutForm(forms.ModelForm):
    class Meta:
        model = VenueLayout
        exclude = ['company', 'venue']


class NewVenueLayoutAreaForm(forms.ModelForm):
    class Meta:
        model = VenueLayoutArea
        exclude = ['company', 'venue', 'layout']


class NewEventForm(forms.ModelForm):
    createguestlist = forms.BooleanField(initial=True, label="Create guestlist?")

    class Meta:
        model = Event
        fields = ['name', 'description', 'datestart', 'timestart',
                  'dateend', 'timeend']

    def clean(self):
        # Clean data
        cleaned_data = super(NewEventForm, self).clean()

        # Check event doesn't end before it starts
        datestart = self.cleaned_data.get("datestart")
        dateend = self.cleaned_data.get("dateend")
        if dateend < datestart:
            msg = u"Event can't end before it has started! Please change End Date."
            self._errors["dateend"] = self.error_class([msg])
        timestart = self.cleaned_data.get("timestart")
        timeend = self.cleaned_data.get("timeend")
        if (timeend < timestart) and (datestart == dateend):
            msg = u"Event can't end before it has started! Please change End Time."
            self._errors["timeend"] = self.error_class([msg])


    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(NewEventForm, self).__init__(*args, **kwargs)
        self.fields['datestart'].widget = forms.TextInput(attrs={
            'class': 'datepicker'})
        self.fields['dateend'].widget = forms.TextInput(attrs={
            'class': 'datepicker'})
        self.fields['timestart'].widget = forms.TextInput(attrs={
            'class': 'timepicker'})
        self.fields['timeend'].widget = forms.TextInput(attrs={
            'class': 'timepicker'})


class NewRecurringEventForm(forms.ModelForm):
    class Meta:
        model = RecurringEvent
        exclude = ['company', 'venue', 'recurrence']
        labels = {
            'name': 'What is your event called?',
            'description': '',
            'datestart': 'When will the first event be?',
            'timestart': 'What time will your events start?',
            'dateend': 'When will the last event be?',
            'timeend': 'What time will they finish?',
            'monday': 'mon',
            'tuesday': 'tue',
            'wednesday': 'wed',
            'thursday': 'thu',
            'friday': 'fri',
            'saturday': 'sat',
            'sunday': 'sun',
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('label_suffix', '')  # globally override the Django >=1.6 default of ':'
        super(NewRecurringEventForm, self).__init__(*args, **kwargs)
        self.fields['firstevent'].widget = forms.TextInput(attrs={
            'class': 'datepicker'})
        self.fields['lastevent'].widget = forms.TextInput(attrs={
            'class': 'datepicker'})
        self.fields['timestart'].widget = forms.TextInput(attrs={
            'class': 'timepicker'})
        self.fields['timeend'].widget = forms.TextInput(attrs={
            'class': 'timepicker'})


    def clean(self):
        # Clean data
        cleaned_data = super(NewRecurringEventForm, self).clean()

        # Check event doesn't end before it starts
        firstevent = self.cleaned_data.get("firstevent")
        lastevent = self.cleaned_data.get("lastevent")
        if lastevent < firstevent:
            msg = u"Event can't end before it has started! Please change End Date."
            self._errors["lastevent"] = self.error_class([msg])



class NewGuestListForm(forms.ModelForm):
    class Meta:
        model = GuestList
        fields = ['name', 'maxguests', 'maxplusones', 'listopen']


class AreaHireBookingForm(forms.ModelForm):
    class Meta:
        model = AreaHireBooking
        fields = ['area', 'firstname', 'lastname', 'email', 'phone']


class JoinGuestListForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['firstname', 'lastname',
                  'plusones', 'member', 'timeslot',  'email']
        labels = {
                  'firstname': _('What is your first name?'),
                  'lastname': _('Thanks, and what is your last?'),
                  'member': _('Are you a member?'),
                  'plusones': _('How many guests are you bringing?'),
                  'timeslot': _('What time can we be expecting you?'),
                  'email': _('To complete your request, please enter your email address'),
        }

    def __init__(self, *args, **kwargs):
        # Set up guestlist
        self.guestlistpk = kwargs.pop('guestlistpk')
        super(JoinGuestListForm, self).__init__(*args, **kwargs)

        """
        # Set up multiple choices
        timeslots = (
            (1, ("6-7pm")),
            (2, ("7-9pm")),
            (3, ("9-11pm")),
        )

        self.fields["timeslot"].widget = forms.CheckboxSelectMultiple()
        """

    def clean(self):
        # Clean data
        self.cleaned_data = super(JoinGuestListForm, self).clean()

        # Count guests
        guestlistobj = GuestList.objects.get(pk=self.guestlistpk)
        guests = Guest.objects.filter(guestlist=guestlistobj)
        guestcount = 0
        for guest in guests:
            guestcount += guest.plusones
        guestcount += len(guests)

        # Error if there is not enough space for additional guests
        if (guestcount + self.cleaned_data.get("plusones") + 1) > guestlistobj.maxguests:
            msg = u"Sorry, there is not enough space on the guest list for that many guests"
            self._errors["plusones"] = self.error_class([msg])

        # Error if exceeds max number of additional guests
        if self.cleaned_data.get("plusones") > guestlistobj.maxplusones:
            msg = u"Sorry, the maximum number of additional guests allowed is %d" % guestlistobj.maxplusones
            self._errors["plusones"] = self.error_class([msg])

class JoinRecurringGuestListForm(forms.ModelForm):
    class Meta:
        model = Guest
        fields = ['firstname', 'lastname',
                  'plusones', 'member', 'timeslot',  'email']
        labels = {
                  'firstname': _('What is your first name?'),
                  'lastname': _('Thanks, and what is your last?'),
                  'member': _('Are you a member?'),
                  'plusones': _('How many guests are you bringing?'),
                  'timeslot': _('What time can we be expecting you?'),
                  'email': _('To complete your request, please enter your email address'),
        }

class NewMembershipType(forms.ModelForm):
    class Meta:
        model = MembershipType
        exclude = ['company', 'venue']


class NewMemberForm(forms.Form):
    firstname = forms.CharField(label="What is your first name?",
                                max_length=40)  # Member
    lastname = forms.CharField(label="And your last?",
                               max_length=40)  # Member
    email = forms.EmailField(label="Please provide an email address so we can contact you",
                             max_length=254)  # Member
    dateofbirth = forms.DateField(label="What is your date of birth?", widget=forms.DateInput(attrs={'class': 'datepicker'}))  # Member


class MemberImportForm(forms.Form):
    file = forms.FileField()



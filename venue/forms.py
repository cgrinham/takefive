from django import forms
from .models import Company, Venue, VenueLayout, Event, Guest, Member
from .models import Membership, MembershipType, GuestList, AreaHireBooking
from django.utils.translation import gettext_lazy as _
import datetime


class NewCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['name']


class NewVenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['name', 'capacity']


class NewVenueLayoutForm(forms.ModelForm):
    class Meta:
        model = VenueLayout
        exclude = ['company', 'venue']


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

class NewRecurringEventForm(forms.Form):
    eventname = forms.CharField(label="What is your event called?", max_length=254)
    description = forms.CharField(widget=forms.Textarea, label="Give your event a description so people know what's going on")
    datestart = forms.DateField(initial=datetime.date.today)
    dateend = forms.DateField(initial=datetime.date.today)
    timestart = forms.DateField()
    timeend = forms.DateField()


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
    paid = forms.BooleanField()


"""
class JoinGuestListForm(forms.Form):
    guestlist = forms.ModelMultipleChoiceField(queryset=Event.objects.all())
    firstname = forms.CharField(label='First Name', max_length=50)
    lastname = forms.CharField(label='Last Name', max_length=50)
    email = forms.EmailField(max_length=254)
    member = forms.BooleanField(required=False)
    timeslot = forms.CharField(label='When would you like to attend?', max_length=50)
    plusones = forms.IntegerField()
    notes = forms.CharField(label='Any additional notes?', max_length=140)
"""



"""
class NewEventForm(forms.Form):
    venue = forms.ModelChoiceField(queryset=Venue.objects.all().order_by('name'))
    name = forms.CharField(label='Event Name', max_length=120)
    description = forms.CharField(widget=forms.Textarea, label='Provide a short description of the event')
    datestart = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    timestart = forms.TimeField(widget=forms.TimeInput)
    dateend = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))
    timeend = forms.TimeField(widget=forms.TimeInput)
    createguestlist = forms.BooleanField(label="Create a guestlist?")
"""

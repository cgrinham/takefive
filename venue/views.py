import csv
import re
import datetime
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from .models import Company, Venue, VenueLayout, VenueLayoutArea, Event, Guest
from .models import GuestList, Profile, Member, Membership, MembershipType
from .forms import NewCompanyForm, NewVenueForm, NewVenueLayoutForm
from .forms import NewGuestListForm, NewEventForm, JoinGuestListForm
from .forms import AreaHireBookingForm, NewMembershipType, NewMemberForm

# Tools

def countguests(guests):
    # Get total amount of guests
    # guests must be a Guest object
    guestcount = 0
    for guest in guests:
        guestcount += guest.plusones
    guestcount += len(guests)

    return guestcount



# Views


def index(request):
    company = Company.objects.get(pk=1)
    venues = Venue.objects.filter(owner=company)

    context = {
               'company': company,
               'venues': venues,
               }

    return render(request, 'venue/index.html', context)


@login_required
def company(request, company):

    # companyname = get_object_or_404(Company, reference=company)
    company = Company.objects.get(reference=company)

    # venues = get_object_or_404(Company, reference=company)
    venues = Venue.objects.filter(owner=company)

    context = {'company': company,
               'venues': venues
               }

    return render(request, 'venue/company.html', context)


@login_required
def venue(request, company, venue):
    # companyname = get_object_or_404(Company, reference=company)
    company = Company.objects.get(reference=company)

    # venues = get_object_or_404(Company, reference=company)
    venue = Venue.objects.get(reference=venue)
    events = Event.objects.filter(venue=venue).order_by('-datestart')

    pastevents = []
    futureevents = []

    for event in events:
        if event.dateend < datetime.datetime.now().date():
            pastevents.append(event)
        else:
            futureevents.append(event)

    context = {
               'venue': venue,
               'company': company,
               'pastevents': pastevents,
               'futureevents': futureevents
               }

    return render(request, 'venue/venue.html', context)


@login_required
def members(request, company, venue):

    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)

    membershiptypes = MembershipType.objects.filter(venue=venue)

    for membershiptype in membershiptypes:
        members = Membership.objects.filter(membershiptype=membershiptype)

    context = {
               'venue': venue,
               'company': company,
               'members': members,
               'membershiptypes': membershiptypes,
               }

    return render(request, 'venue/members.html', context)


def door(request, event):
    event = Event.objects.get(pk=event)

    if request.user.profile.company == event.company:
        guestlists = GuestList.objects.filter(event=event)

        allguests = {}

        for guestlist in guestlists:
            guests = Guest.objects.filter(guestlist=guestlist)
            allguests[guestlist] = guests

        #guests = [Guest.objects.get(pk=13), Guest.objects.get(pk=14)]

        context = {
                   'company': company,
                   'venue': venue,
                   'event': event,
                   'guests': allguests,
                   'guestlists': guestlists,
                   }

        return render(request, 'venue/door.html', context)
    else:
        context = {

        }
        return render(request, 'venue/venuelayout.html', context)


def doorajaxarrival(request):
    guest = request.GET.get("guest", None)
    guest = Guest.objects.get(pk=guest)
    if guest.arrived is False:
        guest.arrived = True
    else:
        guest.arrived = False
    guest.save()
    data = {
        'success': guest.pk
    }
    return JsonResponse(data)


@login_required
def venuelayout(request, company, venue):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)

    venuelayouts = VenueLayout.objects.filter(venue=venue)

    venuelayoutdict = {}

    for venuelayout in venuelayouts:
        venuelayoutarea = VenueLayoutArea.objects.filter(layout=venuelayout)
        venuelayoutdict[venuelayout.name] = [venuelayout, venuelayoutarea]

    print(venuelayoutdict)

    context = {'company': company,
               'venue': venue,
               'venuelayoutdict': venuelayoutdict
               }

    return render(request, 'venue/venuelayout.html', context)


@login_required
def newvenuelayout(request, company, venue):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewVenueLayoutForm(data=request.POST)

        if form.is_valid():
            # Create the company object but don't actually save it
            # So that we can add the reference
            form = form.save(commit=False)
            form.company = company
            form.venue = venue
            form.save()

            return HttpResponseRedirect('/venues/%s/%s/layout' %
                                        (company.reference, venue.reference))
    else:
        form = NewVenueLayoutForm()

    context = {'form': form,
               'venue': venue
               }

    return render(request, 'venue/newvenuelayout.html', context)


@login_required
def viewevent(request, company, venue, event):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    event = Event.objects.get(pk=event)
    print(event)

    guestlists = GuestList.objects.filter(event=event)

    print(guestlists)

    context = {
               'company': company,
               'venue': venue,
               'guestlists': guestlists,
               'event': event
               }

    return render(request, 'venue/viewevent.html', context)


@login_required
def viewguestlist(request, company, venue, guestlist):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    guestlist = GuestList.objects.get(pk=guestlist)

    event = guestlist.event

    guests = Guest.objects.filter(guestlist=guestlist).order_by('firstname')
    guestcount = countguests(guests)

    context = {
                'company': company,
                'venue': venue,
                'guests': guests,
                'guestcount': guestcount,
                'guestlist': guestlist,
                'event': event
               }

    return render(request, 'venue/viewguestlist.html', context)


@login_required
def exportcsv(request, guestlist):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guestlist.csv"'

    writer = csv.writer(response)
    writer.writerow(['firstname', 'lastname', 'email',
                    'member', 'timeslot', 'plusones', 'notes', 'arrived'])

    guestlist = GuestList.objects.get(pk=guestlist)
    guests = Guest.objects.filter(guestlist=guestlist).order_by('firstname')

    rows = []

    for guest in guests:
        row = [guest.firstname, guest.lastname, guest.email,
               guest.member, guest.timeslot, guest.plusones,
               guest.notes, guest.arrived]
        rows.append(row)

    print(rows)

    for row in rows:
        writer.writerow(row)

    return response


def testpage(request):
    print(GuestList.objects.all())

    """
    guestlist = GuestList.objects.filter(name=)
    guest = Guests(
        guestlist=,
        firstname="Christie",
        lastname="Grinham",
        email="christie@grinham.co.uk",
        member=False,
        timeslot="7-9pm",
        plusones=0,
        notes="",
                    )
    guest.save()"""

    return render(request, 'venue/test.html')


@login_required
def newcompany(request):

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewCompanyForm(data=request.POST)

        if form.is_valid():
            # Create the company object but don't actually save it
            # So that we can add the reference
            form = form.save(commit=False)

            print("Set reference!")
            form.reference = re.sub(r'\W+', '', form.name.lower())

            print(form.reference)
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = NewCompanyForm()

    context = {'form': form
               }

    return render(request, 'venue/newcompany.html', context)


@login_required
def newvenue(request, company):

    if request.method == 'POST':
        # Creat a form instance and populate it with data from the request
        form = NewVenueForm(data=request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            # Assign company from user's profile
            form.owner = request.user.profile.company
            # Assign reference
            form.reference = re.sub(r'\W+', '', form.name.lower())
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = NewVenueForm()

    context = {'form': form
               }

    return render(request, 'venue/newvenue.html', context)


@login_required
def newevent(request, company, venue):
    # Check if company owns a venue with this reference
    # Check user is allowed to create events for this venue
    company = Company.objects.get(reference=request.user.profile.company.reference)
    venue = Venue.objects.get(reference=venue)
    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewEventForm(request.POST)

        if form.is_valid():
            newevent = form.save(commit=False)
            newevent.company = company
            newevent.venue = venue
            newevent.save()
            if form.cleaned_data["createguestlist"] is True:
                print("Let's make a guestlist!")
                newguestlist = GuestList(company=company, venue=venue,
                                         event=newevent,
                                         name="%s Guestlist" %
                                              form.cleaned_data["name"],
                                         maxguests=newevent.venue.capacity)
                newguestlist.save()
            return HttpResponseRedirect('/venues/%s/%s' %
                                        (company.reference, venue.reference))
    else:
        form = NewEventForm()

    events = Event.objects.order_by('name')
    context = {
               'events': events,
               'venue': venue,
               'form': form
               }

    return render(request, 'venue/newevent.html', context)


@login_required
def newguestlist(request, event):

    eventobj = Event.objects.get(pk=event)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = NewGuestListForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.company = Company.objects.get(reference=request.user.profile.company.reference)
            form.venue = eventobj.venue
            form.event = eventobj
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = NewGuestListForm()

    context = {'event': eventobj,
               'form': form
               }

    return render(request, 'venue/newguestlist.html', context)


def newmembershiptype(request, company, venue):
    # Check if company owns a venue with this reference
    # Check user is allowed to create events for this venue
    company = Company.objects.get(reference=request.user.profile.company.reference)
    venue = Venue.objects.get(reference=venue)
    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewMembershipType(request.POST)

        if form.is_valid():
            newevent = form.save(commit=False)
            newevent.company = company
            newevent.venue = venue
            newevent.save()

            return HttpResponseRedirect('/venues/%s/%s' %
                                        (company.reference, venue.reference))
    else:
        form = NewMembershipType()

    context = {
               'venue': venue,
               'form': form
               }

    return render(request, 'venue/newmembershiptype.html', context)


def newmember(request, membershiptype):
    mt = MembershipType.objects.get(pk=membershiptype)

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewMemberForm(request.POST)

        if form.is_valid():

            m = Member(
                       firstname=form.cleaned_data['firstname'],
                       lastname=form.cleaned_data['lastname'],
                       email=form.cleaned_data['email'],
                       dateofbirth=form.cleaned_data['dateofbirth']
                       )
            m.save()

            ms = Membership(
                            member=m,
                            membershiptype=mt,
                            starts=datetime.date.today(),
                            expires=(datetime.date.today() +
                                     relativedelta(years=1)),
                            paid=form.cleaned_data['paid'],
                            )

            ms.save()

            context = {
                       'thankyou': True,
                       'membershiptype': mt,
                       }

            return render(request, 'venue/newmember.html', context)
    else:
        form = NewMemberForm()

    context = {
               'form': form,
               'membershiptype': mt,
               }

    return render(request, 'venue/newmember.html', context)

def joinguestlist(request, guestlist):
    guestlistobj = GuestList.objects.get(pk=guestlist)

    # Could check guestlist open here to skip other logic for speed

    # Count guests
    guests = Guest.objects.filter(guestlist=guestlistobj)
    guestcount = 0
    for guest in guests:
        guestcount += guest.plusones
    guestcount += len(guests)

    # If at capacity, closed guestlist
    if guestcount > guestlistobj.maxguests:
        guestlistobj.listopen = False
        guestlistobj.save()

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = JoinGuestListForm(request.POST, guestlistpk=guestlist)

        if form.is_valid():
            form = form.save(commit=False)
            form.guestlist = guestlistobj
            form.company = guestlistobj.company
            form.venue = guestlistobj.venue
            form.save()

            send_mail('Thankyou for joining the guest list',
                      """Dear %s,\n Thankyou for joining the guest list for %s,\n
                       We looking forward to seeing you.\n
                       Piano Bar Soho Team""" % (form.firstname, guestlistobj.event.name),
                      'tf@christiegrinham.co.uk',
                      [form.email],
                      fail_silently=False,
                      )

            context = {'guestlistobj': guestlistobj,
                       'thankyou': True
                       }

            return render(request, 'venue/joinguestlist.html', context)
    else:
        form = JoinGuestListForm(guestlistpk=guestlist)

    context = {'guestlistobj': guestlistobj,
               'guests': guestcount,
               'form': form
               }

    return render(request, 'venue/joinguestlist.html', context)


def areahire(request):

    form = AreaHireBookingForm()

    context = {
               'form': form
               }

    return render(request, 'venue/areahire.html', context)
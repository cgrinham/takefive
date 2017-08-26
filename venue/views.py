import csv
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Company, Venue, Event, Guest, GuestList
from .forms import NewCompanyForm, NewVenueForm, NewGuestListForm, NewEventForm, JoinGuestListForm

# Views

def index(request):
    loggedin = True

    company = Company.objects.get(pk=1)
    venues = Venue.objects.filter(owner=company)
    print(venues)

    context = {'loggedin': loggedin,
               'company': company,
               'venues': venues
               }

    return render(request, 'venue/index.html', context)


def company(request, company):
    loggedin = True

    #companyname = get_object_or_404(Company, reference=company)
    company = Company.objects.get(reference=company)
    print(company)

    #venues = get_object_or_404(Company, reference=company)
    venues = Venue.objects.filter(owner=company)

    context = {'loggedin': loggedin,
               'company': company,
               'venues': venues
               }

    return render(request, 'venue/company.html', context)

def venue(request, company, venue):
    loggedin = True

    #companyname = get_object_or_404(Company, reference=company)
    company = Company.objects.get(reference=company)

    #venues = get_object_or_404(Company, reference=company)
    venue = Venue.objects.get(reference=venue)
    events = Event.objects.filter(venue=venue)

    context = {'loggedin': loggedin,
               'companyname': company,
               'venue': venue,
               'events': events
               }

    return render(request, 'venue/venue.html', context)

def viewevent(request, event):
    loggedin = False
    event = Event.objects.get(pk=event)
    print(event)

    guestlists = GuestList.objects.filter(event=event)
    print(guestlists)

    context = {'loggedin': loggedin,
                'guestlists': guestlists,
                'event': event
               }

    return render(request, 'venue/viewevent.html', context)

def viewguestlist(request, guestlist):
    loggedin = False

    guestlist = GuestList.objects.get(pk=guestlist)

    event = guestlist.event

    guests = Guest.objects.filter(guestlist=guestlist)

    # Get total amount of guests
    guestcount = 0
    for guest in guests:
        guestcount += guest.plusones
    guestcount += len(guests)

    context = {'loggedin': loggedin,
                'guests': guests,
                'guestcount': guestcount,
                'guestlist': guestlist,
                'event': event
               }

    return render(request, 'venue/viewguestlist.html', context)

def exportcsv(request, guestlist):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guestlist.csv"'

    writer = csv.writer(response)
    writer.writerow(['firstname', 'lastname', 'email',
                    'member', 'timeslot', 'plusones', 'notes', 'arrived'])

    guestlist = GuestList.objects.get(pk=1)
    guests = Guest.objects.filter(guestlist=guestlist)

    rows = []

    for guest in guests:
        row = [guest.firstname, guest.lastname, guest.email,
               guest.member, guest.timeslot, guest.plusones, guest.notes, guest.arrived]
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


def newcompany(request):

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewCompanyForm(data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = NewCompanyForm()

    loggedin = False
    context = {'loggedin': loggedin,
               'form': form
               }

    return render(request, 'venue/newcompany.html', context)


def newvenue(request):

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewVenueForm(data=request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = NewVenueForm()

    loggedin = False
    context = {'loggedin': loggedin,
               'form': form
               }

    return render(request, 'venue/newvenue.html', context)

def newevent(request):
    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewEventForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/venues')
    else:
        form = NewEventForm()

    loggedin = False
    events = Event.objects.order_by('name')
    context = {'events': events,
               'loggedin': loggedin,
               'form': form
               }

    return render(request, 'venue/newevent.html', context)

def newguestlist(request):

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewGuestListForm(request.POST)

        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = NewGuestListForm()

    loggedin = False
    context = {'loggedin': loggedin,
               'form': form
               }

    return render(request, 'venue/newguestlist.html', context)

def joinguestlist(request):

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = JoinGuestListForm(request.POST)

        if form.is_valid():
            # process the data in form.cleaned_data as required
            # redirect to new URL
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = JoinGuestListForm()

    loggedin = False
    events = Event.objects.order_by('name')
    context = {'events': events,
               'loggedin': loggedin,
               'form': form
               }

    return render(request, 'venue/joinguestlist.html', context)

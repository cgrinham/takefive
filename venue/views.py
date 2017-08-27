import csv, re
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from .models import Company, Venue, Event, Guest, GuestList
from .forms import NewCompanyForm, NewVenueForm, NewGuestListForm, NewEventForm, JoinGuestListForm

# Views

def index(request):
    loggedin = True

    company = Company.objects.get(pk=1)
    venues = Venue.objects.filter(owner=company)

    context = {'loggedin': loggedin,
               'company': company,
               'venues': venues
               }

    return render(request, 'venue/index.html', context)


def company(request, company):
    loggedin = True

    #companyname = get_object_or_404(Company, reference=company)
    company = Company.objects.get(reference=company)

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

    guestlist = GuestList.objects.get(pk=guestlist)
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
            form = form.save(commit=False)
            form.reference = re.sub(r'\W+', '', form.name.lower())
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
            newevent = form.save()
            if form.cleaned_data["createguestlist"] == True:
                print("Let's make a guestlist!")
                newguestlist = GuestList(event=newevent, name="%s Guestlist" % form.cleaned_data["name"], maxguests=newevent.venue.capacity)
                newguestlist.save()
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

def newguestlist(request, event):

    eventobj = Event.objects.get(pk=event)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = NewGuestListForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.event = eventobj
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = NewGuestListForm()

    loggedin = False
    context = {'loggedin': loggedin,
               'event': eventobj,
               'form': form
               }

    return render(request, 'venue/newguestlist.html', context)

def joinguestlist(request, guestlist):
    loggedin = False
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
        form = JoinGuestListForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.guestlist = guestlistobj
            form.save()

            return HttpResponseRedirect('/venues')
    else:
        form = JoinGuestListForm()

    context = {'guestlistobj': guestlistobj,
               'guests': guestcount,
               'loggedin': loggedin,
               'form': form
               }

    return render(request, 'venue/joinguestlist.html', context)
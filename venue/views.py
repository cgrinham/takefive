import os
import csv
import re
import datetime
import stripe
import string
import random
from django.http import JsonResponse
from dateutil.relativedelta import relativedelta
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.conf import settings
from .models import Company, Venue, VenueLayout, VenueLayoutArea, Event, Guest
from .models import GuestList, Member, Membership, MembershipType
from .models import RecurringEvent, RecurringEventDate
from .forms import NewCompanyForm, NewVenueForm, NewVenueLayoutForm
from .forms import NewGuestListForm, NewEventForm, JoinGuestListForm
from .forms import AreaHireBookingForm, NewMembershipType, NewMemberForm
from .forms import NewRecurringEventForm, NewVenueLayoutAreaForm
from .forms import JoinRecurringGuestListForm, SignUpForm, MemberImportForm
from .forms import VenueSettingsForm
from .decorators import user_owns_company_and_venue


# Set up stripe
stripe_keys = settings.STRIPE_KEYS
stripe.api_key = stripe_keys['secret_key']


# Tools


def count_guests(guests):
    # Also available as a template filter
    # Get total amount of guests
    # guests must be a Guest object
    guestcount = 0
    for guest in guests:
        guestcount += guest.plusones
    guestcount += guests.count()

    return guestcount


def get_event_days(recurringevent):
    """ Get dates for recurring days """
    dayslist = [
        (recurringevent.monday, 'Monday'),
        (recurringevent.tuesday, 'Tuesday'),
        (recurringevent.wednesday, 'Wednesday'),
        (recurringevent.thursday, 'Thursday'),
        (recurringevent.friday, 'Friday'),
        (recurringevent.saturday, 'Saturday'),
        (recurringevent.sunday, 'Sunday'),
        ]

    days = []
    for day in dayslist:
        if day[0] is True:
            days.append(day[1])

    return days


def sort_dates(events):
    """ Sort events into past and future """
    pastevents = []
    futureevents = []

    for event in events:
        if event.dateend < datetime.datetime.now().date():
            pastevents.append(event)
        else:
            futureevents.append(event)

    return futureevents, pastevents


def handle_uploaded_file(f):
    filename = "%s.csv" % ''.join(random.choice(
        string.ascii_uppercase +
        string.digits) for _ in range(8))
    with open(filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return filename

# Views


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # load the profile instance created by the signal
            user.refresh_from_db()
            # user.profile.birth_date = form.cleaned_data.get('birth_date')
            user.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
        context = {
            'form': form,
        }

    return render(request, 'venue/signup.html', context)


def index(request):
    if request.user.is_authenticated():
        print("Is is_authenticated")
        try:
            company = Company.objects.get(
                reference=request.user.profile.company.reference)
        except:
            return HttpResponseRedirect('/venues/newcompany/')
    else:
        return HttpResponseRedirect('/signup')

    venues = Venue.objects.filter(owner=company)

    context = {
               'company': company,
               'venues': venues,
               }

    return render(request, 'venue/index.html', context)


""" COMPANY """


@login_required
def company(request, company):
    return HttpResponseRedirect('/venues/')


@login_required
def new_company(request):
    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewCompanyForm(data=request.POST)

        if form.is_valid():
            # Create the company object but don't actually save it
            # So that we can add the reference
            form = form.save(commit=False)

            form.reference = re.sub(r'\W+', '', form.name.lower())

            print(form.reference)
            form.save()

            request.user.profile.company = Company.objects.get(
                reference=form.reference)
            request.user.profile.save()

            return HttpResponseRedirect('/venues')
    else:
        form = NewCompanyForm()

    context = {'form': form
               }

    return render(request, 'venue/newcompany.html', context)


""" VENUE """


@login_required
@user_owns_company_and_venue
def venue(request, company, venue):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    events = Event.objects.filter(venue=venue).order_by('-datestart')

    # Guest metrics
    guests = Guest.objects.filter(venue=venue)
    arrivedguests = guests.filter(arrived=True)

    guestcount = count_guests(guests)
    arrivedguestcount = count_guests(arrivedguests)

    # Avoid divide by zero
    if guestcount != 0:
        attendance = float(arrivedguestcount) / guestcount * 100
    else:
        attendance = 0

    # Count members
    membershiptypes = MembershipType.objects.filter(venue=venue)
    members = []
    for membershiptype in membershiptypes:
        members += Membership.objects.filter(membershiptype=membershiptype)

    # Sort events into past and future
    pastevents = []
    futureevents = []

    for event in events:
        if event.dateend < datetime.datetime.now().date():
            pastevents.append(event)
        else:
            futureevents.append(event)

    recurringevents = RecurringEvent.objects.filter(company=company,
                                                    venue=venue)
    redict = {}

    for event in recurringevents:
        lists = RecurringEventDate.objects.filter(event=event)
        pre = []
        fre = []

        for redate in lists:
            if redate.dateend < datetime.datetime.now().date():
                pre.append(event)
            else:
                fre.append(redate)

        redict[event.name] = (event, fre[0])

    context = {
               'venue': venue,
               'company': company,
               'pastevents': pastevents,
               'recurringevents': redict,
               'futureevents': futureevents,
               'arrived': arrivedguestcount,
               'attendance': attendance,
               'membercount': len(members)
               }

    return render(request, 'venue/venue.html', context)


@login_required
@user_owns_company_and_venue
def venue_settings(request, company, venue):
    # Get models
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)

    if request.method == "POST":
        form = VenueSettingsForm(data=request.POST)
        if form.is_valid():
            venue.defaultplusones = form.cleaned_data['defaultplusones']
            venue.capacity = form.cleaned_data['capacity']
            venue.address = form.cleaned_data['address']
            venue.stripesecretkey = form.cleaned_data['stripesecretkey']
            venue.stripepubkey = form.cleaned_data['stripepubkey']
            venue.save()
        return HttpResponseRedirect('/venues')
    else:
        form = VenueSettingsForm(initial={
                'defaultplusones': venue.defaultplusones,
                'capacity': venue.capacity,
                'address': venue.address,
                'stripesecretkey': venue.stripesecretkey,
                'stripepubkey': venue.stripepubkey,
            })

        context = {'company': company,
                   'venue': venue,
                   'form': form,
                   }

        return render(request, 'venue/venuesettings.html', context)


@login_required
def new_venue(request, company):
    # companyname = get_object_or_404(Company, reference=company)
    company = Company.objects.get(reference=company)

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

    context = {
               'company': company,
               'form': form,
               }

    return render(request, 'venue/newvenue.html', context)


""" VENUE LAYOUT """


@login_required
@user_owns_company_and_venue
def venue_layout(request, company, venue):
    # Get models
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    venuelayouts = VenueLayout.objects.filter(venue=venue)

    venuelayoutdict = {}

    for venuelayout in venuelayouts:
        venuelayoutarea = VenueLayoutArea.objects.filter(layout=venuelayout)
        venuelayoutdict[venuelayout.name] = [venuelayout, venuelayoutarea]

    context = {'company': company,
               'venue': venue,
               'venuelayoutdict': venuelayoutdict,
               }

    return render(request, 'venue/venuelayout.html', context)


@login_required
def delete_layout(request):
    try:
        venuelayout = VenueLayout.objects.get(pk=request.GET.get("venuelayout",
                                                                 None))
        VenueLayoutArea.objects.filter(layout=venuelayout).delete()
        venuelayout.delete()
        data = {
            'success': 'success'
        }
    except:
        data = {
            'success': 'error'
        }

    return JsonResponse(data)


@login_required
@user_owns_company_and_venue
def new_venue_layout(request, company, venue):
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
@user_owns_company_and_venue
def new_venue_layout_area(request, company, venue, layout):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)

    if request.method == 'POST':
        form = NewVenueLayoutAreaForm(data=request.POST)

        if form.is_valid():
            # Create the company object but don't actually save it
            # So that we can add the reference
            form = form.save(commit=False)
            form.company = company
            form.venue = venue
            form.layout = VenueLayout.objects.get(pk=layout)
            form.save()

            return HttpResponseRedirect('/venues/%s/%s/layout' %
                                        (company.reference, venue.reference))
    else:
        form = NewVenueLayoutAreaForm()

    context = {
               'company': company,
               'venue': venue,
               'form': form,
               'layout': layout,
               }

    return render(request, 'venue/newvenuelayoutarea.html', context)


# Public View
def area_hire(request):
    form = AreaHireBookingForm()

    context = {
               'form': form
               }

    return render(request, 'venue/areahire.html', context)


""" MEMBERS/MEMBERSHIP """


@login_required
@user_owns_company_and_venue
def members(request, company, venue):
    # Get models for view
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    membershiptypes = MembershipType.objects.filter(venue=venue)
    members = []

    for membershiptype in membershiptypes:
        members += Membership.objects.filter(membershiptype=membershiptype)

    context = {
               'venue': venue,
               'company': company,
               'members': members,
               'membershiptypes': membershiptypes,
               }

    return render(request, 'venue/members.html', context)


@login_required
@user_owns_company_and_venue
def new_membership_type(request, company, venue):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)

    if request.method == 'POST':
        # Create a form instance and populate it with data from teh request
        form = NewMembershipType(request.POST)

        if form.is_valid():
            newevent = form.save(commit=False)
            newevent.company = company
            newevent.venue = venue
            newevent.save()

            return HttpResponseRedirect('/venues/%s/%s/members/' %
                                        (company.reference, venue.reference))
    else:
        form = NewMembershipType()

    context = {
               'company': company,
               'venue': venue,
               'form': form
               }

    return render(request, 'venue/newmembershiptype.html', context)


# Public View
def new_member(request, membershiptype):
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
                expires=(datetime.date.today() + relativedelta(years=1)),
                paid=False,
                )
            ms.save()

            return HttpResponseRedirect('/venues/payment/%s/' % ms.pk)
    else:
        form = NewMemberForm()

    context = {
               'form': form,
               'membershiptype': mt,
               }

    return render(request, 'venue/newmember.html', context)


@login_required
@user_owns_company_and_venue
def import_members(request, company, venue):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)

    if request.method == 'POST':
        if request.FILES:
            form = MemberImportForm(request.POST, request.FILES)
            newfile = handle_uploaded_file(request.FILES['file'])

            with open(newfile) as f:
                rdr = csv.reader(f)

                uploadfields = []
                count = 0
                for item in next(rdr):
                    uploadfields.append((count, item))
                    count += 1

                context = {
                    'company': company,
                    'venue': venue,
                    'data': True,
                    'modelfields': Member._meta.fields,
                    'uploadfields': uploadfields,
                    'csv': newfile,
                }

            return render(request, 'venue/importmembers.html', context)
        else:
            with open(request.POST['csvfile']) as f:
                rdr = csv.reader(f)
                count = 0
                for line in rdr:
                    if count > 0:
                        newmember = Member(
                            firstname=line[int(request.POST['venue.Member.firstname'])],
                            lastname=line[int(request.POST['venue.Member.lastname'])],
                            dateofbirth=line[int(request.POST['venue.Member.dateofbirth'])],
                            email=line[int(request.POST['venue.Member.email'])],
                            )
                        newmember.save()
                        newmembership = Membership(
                                member=newmember,
                                membershiptype=MembershipType.objects.get(pk=2),
                                starts=datetime.date.today(),
                                expires=(datetime.date.today() + relativedelta(years=1)),
                                paid=True,
                            )
                        newmembership.save()
                    count += 1

            os.remove(request.POST['csvfile'])
            print(request.POST)
            context = {
                'message': "Hello",
                'thankyou': True,
            }
            return render(request, 'venue/importmembers.html', context)

    else:
        form = MemberImportForm()

    context = {
               'company': company,
               'venue': venue,
               'form': form
               }

    return render(request, 'venue/importmembers.html', context)

""" END MEMBERS """
""" EVENTS """


@login_required
@user_owns_company_and_venue
def view_event(request, company, venue, event):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    event = get_object_or_404(Event, pk=event)

    # Get guestlist
    guestlists = GuestList.objects.filter(event=event)

    # check if an event is in the past
    if event.datestart < datetime.date.today():
        past_event = True
    else:
        past_event = False

    context = {
               'company': company,
               'venue': venue,
               'guestlists': guestlists,
               'event': event,
               'past_event': past_event,
               }

    return render(request, 'venue/viewevent.html', context)


@login_required
def ajax_event_delete(request):
    event = Event.objects.get(pk=request.GET.get("event", None))
    event.delete()
    data = {
        'success': True
    }
    return JsonResponse(data)


@login_required
@user_owns_company_and_venue
def view_recurring_event(request, company, venue, event):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    event = RecurringEvent.objects.get(pk=event)
    dates = RecurringEventDate.objects.filter(event=event)

    # guestlists = GuestList.objects.filter(event=event)

    # print(guestlists)

    daylist = get_event_days(event)
    days = ""
    count = 0

    for day in daylist:
        if count < (len(daylist) - 1):
            days += "%s, " % day
        else:
            days += day
        count += 1

    # Sort dates into past and future
    pastdates = []
    futuredates = []

    for date in dates:
        if date.dateend < datetime.datetime.now().date():
            pastdates.append(date)
        else:
            futuredates.append(date)

    context = {
               'company': company,
               'venue': venue,
               # 'guestlists': guestlists,
               'event': event,
               'futuredates': futuredates,
               'pastdates': pastdates,
               'days': days,
               }

    return render(request, 'venue/viewrecurringevent.html', context)


@login_required
def ajax_recc_event_delete_all(request):
    event = RecurringEvent.objects.get(pk=request.GET.get("event", None))
    dates = RecurringEventDate.objects.filter(event=event)
    dates.delete()

    event.delete()
    data = {
        'success': True
    }
    return JsonResponse(data)


@login_required
def ajax_recc_event_delete_date(request):
    event = RecurringEventDate.objects.get(pk=request.GET.get("event", None))
    guestlist = GuestList.objects.get(recurringevent=event)

    event.delete()
    guestlist.delete()
    data = {
        'success': True
    }
    return JsonResponse(data)


@login_required
@user_owns_company_and_venue
def new_event(request, company, venue):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    oneoffform = NewEventForm()
    recurringform = NewRecurringEventForm()

    context = {
               'company': company,
               'venue': venue,
               'oneoffform': oneoffform,
               'recurringform': recurringform,
               }

    return render(request, 'venue/newevent.html', context)


@login_required
@user_owns_company_and_venue
def new_one_off_event(request, company, venue):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    error = False
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
            error = True
    else:
        error = True

    context = {
               'venue': venue,
               'company': company,
               'error': error,
               }

    return render(request, 'venue/newoneoffevent.html', context)


@login_required
@user_owns_company_and_venue
def new_recurring_event(request, company, venue):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    error = False
    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = NewRecurringEventForm(data=request.POST)

        if form.is_valid():
            print("That form's valid")
            newevent = form.save(commit=False)
            newevent.company = company
            newevent.venue = venue
            newevent.recurrence = "weekly"

            newevent.save()

            # Create event dates
            d1 = newevent.firstevent
            d2 = newevent.lastevent
            days = get_event_days(newevent)
            delta = d2 - d1         # timedelta

            for i in range(delta.days + 1):
                thisdate = d1 + datetime.timedelta(days=i)
                if thisdate.strftime('%A') in days:
                    if thisdate.strftime('%d'):
                        newdate = RecurringEventDate(
                            company=company,
                            venue=venue,
                            event=newevent,
                            datestart=thisdate,
                            dateend=thisdate + datetime.timedelta(days=1),
                            timestart=newevent.timestart,
                            timeend=newevent.timeend,
                            )
                        newdate.save()

                        guestlistname = "%s - %s" % (newevent.name,
                                                     thisdate.strftime(
                                                        '%d/%m/%Y'))

                        newguestlist = GuestList(
                            company=company,
                            venue=venue,
                            recurringevent=newdate,
                            name=guestlistname,
                            maxguests=venue.capacity,
                            )
                        newguestlist.save()
                else:
                    pass

            # Create guestlists for all events
            # print("Let's make a guestlist!")
            # newguestlist = GuestList(company=company, venue=venue,
            #                          event=newevent,
            #                          name="%s Guestlist" %
            #                               form.cleaned_data["name"],
            #                          maxguests=newevent.venue.capacity)
            # newguestlist.save()
            return HttpResponseRedirect('/venues/%s/%s' %
                                        (company.reference, venue.reference))
    else:
        form = NewRecurringEventForm()

    context = {
               'venue': venue,
               'company': company,
               'form': form,
               'error': error,
               }

    return render(request, 'venue/newrecurringevent.html', context)


""" GUESTLISTS """


@login_required
@user_owns_company_and_venue
def view_guestlist(request, company, venue, guestlist):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    guestlist = GuestList.objects.get(pk=guestlist)

    event = guestlist.event

    guests = Guest.objects.filter(guestlist=guestlist).order_by('firstname')
    guestcount = count_guests(guests)

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
@user_owns_company_and_venue
def new_guestlist(request, company, venue, event):
    company = Company.objects.get(reference=company)
    venue = Venue.objects.get(reference=venue)
    eventobj = Event.objects.get(pk=event)

    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = NewGuestListForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.company = Company.objects.get(
                reference=request.user.profile.company.reference)
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


def join_guestlist(request, guestlist):
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
                       Piano Bar Soho Team""" % (form.firstname,
                                                 guestlistobj.event.name),
                      'tf@christiegrinham.co.uk',
                      [form.email],
                      fail_silently=False,
                      )

            context = {'guestlistobj': guestlistobj,
                       'thankyou': True,
                       'pagetitle': "Thank you...",
                       }

            return render(request, 'venue/joinguestlist.html', context)
    else:
        form = JoinGuestListForm(guestlistpk=guestlist)

    context = {
               'guestlistobj': guestlistobj,
               'guests': guestcount,
               'form': form,
               'pagetitle': "Join the guestlist",
               }

    return render(request, 'venue/joinguestlist.html', context)


def join_recurring_guestlist(request, event):
    event = RecurringEvent.objects.get(pk=event)
    dates = RecurringEventDate.objects.filter(event=event)

    futuredates, pastdates = sort_dates(dates)

    if request.method == 'POST':
        # Creat a form instance and populate it with data from teh request
        form = JoinRecurringGuestListForm(request.POST)

        if form.is_valid():
            form = form.save(commit=False)
            form.guestlist = event
            form.company = event.company
            form.venue = event.venue
            form.save()

            send_mail('Thankyou for joining the guest list',
                      """Dear %s,\n Thankyou for joining the guest list for %s,\n
                       We looking forward to seeing you.\n
                       Piano Bar Soho Team""" % (form.firstname,
                                                 event.event.name),
                      'tf@christiegrinham.co.uk',
                      [form.email],
                      fail_silently=False,
                      )

            context = {
                       'event': event,
                       'thankyou': True,
                       'pagetitle': "Thank you...",
                       }

            return render(request, 'venue/joinguestlist.html', context)
    else:
        form = JoinRecurringGuestListForm()

    context = {
               'event': event,
               'dates': futuredates,
               'form': form,
               'pagetitle': "Join the guestlist",
               }

    return render(request, 'venue/joinrecurringguestlist.html', context)


def toggle_guestlist_open(request):
    guestlistpk = request.GET.get("guestlist", None)
    guestlist = GuestList.objects.get(pk=guestlistpk)
    if guestlist.listopen is False:
        colour = "green"
        guestlist.listopen = True
    else:
        guestlist.listopen = False
        colour = "red"
    guestlist.save()
    data = {
        'success': guestlist.pk,
        'colour': colour
    }
    return JsonResponse(data)


""" DOOR """


def door(request, event):
    event = Event.objects.get(pk=event)

    if request.user.profile.company == event.company:
        guestlists = GuestList.objects.filter(event=event)

        allguests = {}

        for guestlist in guestlists:
            guests = Guest.objects.filter(guestlist=guestlist)
            allguests[guestlist] = guests

        # guests = [Guest.objects.get(pk=13), Guest.objects.get(pk=14)]

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


@login_required
def door_ajax_arrival(request):
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


""" misc pages """


def payment(request, membership):
    membership = Membership.objects.get(pk=membership)
    membershiptype = membership.membershiptype
    venue = membershiptype.venue

    if venue.stripepubkey is not None:
        amount = int(membershiptype.price * 100)  # amount in GBP pence

        if membership.paid is False:
            if request.method == 'POST':

                customer = stripe.Customer.create(
                    email=request.POST['stripeEmail'],
                    source=request.POST['stripeToken'],
                    )

                charge = stripe.Charge.create(
                    customer=customer.id,
                    amount=amount,
                    currency='gbp',
                    description=membershiptype.name,
                    )

                membership.paid = True
                membership.save()

                context = {
                    'pagetitle': "make a payment - %s" % membershiptype.venue.name,
                    'thankyou': True,
                    'membership': membership,
                }
            else:
                context = {
                    'pagetitle': "make a payment - %s" % membershiptype.venue.name,
                    'key': venue.stripepubkey,
                    'mt': membershiptype,
                    'membership': membership,
                    'price': amount,
                }
        else:
            context = {
                'pagetitle': "make a payment - %s" % membershiptype.venue.name,
                'membership': membership,
                'mt': membershiptype,
                'paid': True
            }

        return render(request, 'venue/payment.html', context)
    else:
        context = {
            'error': "Sorry, this venue's payment details aren't set up correclty",
        }
        return render(request, 'venue/error.html', context)


@login_required
def export_csv(request, guestlist):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="guestlist.csv"'

    writer = csv.writer(response)
    writer.writerow(['firstname', 'lastname', 'email',
                    'member', 'timeslot', 'plusones', 'notes', 'listopen'])

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

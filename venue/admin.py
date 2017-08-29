from django.contrib import admin
from .models import Company, Venue, Event, GuestList, Guest, Profile
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    fields = ['name', 'reference']

class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'company']

class VenueAdmin(admin.ModelAdmin):
    fields = ['owner', 'name', 'reference', 'capacity']


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
                ('Event', {'fields': ['venue', 'name', 'description']}),
                ('Date & Time', {'fields': ['datestart', 'timestart',
                                 'dateend', 'timeend']}),
                ('Recurrance', {'fields': ['recurring']})
    ]

class GuestListAdmin(admin.ModelAdmin):
    fields = ['event', 'name', 'maxguests', 'maxplusones', 'listopen']

class GuestAdmin(admin.ModelAdmin):
    fields = ['guestlist', 'firstname', 'lastname', 'email',
              'member', 'timeslot', 'plusones', 'notes', 'arrived']

admin.site.register(Company, CompanyAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(GuestList, GuestListAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Profile, ProfileAdmin)
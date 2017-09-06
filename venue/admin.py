from django.contrib import admin
from .models import Company, Venue, VenueLayout, VenueLayoutArea, Event
from .models import GuestList, Guest, Profile, Member, Membership, MembershipType
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    fields = ['name', 'reference']


class ProfileAdmin(admin.ModelAdmin):
    fields = ['user', 'company']


class VenueAdmin(admin.ModelAdmin):
    fields = ['owner', 'name', 'reference', 'capacity', 'defaultplusones']


class VenueLayoutAdmin(admin.ModelAdmin):
    fields = ['venue', 'name', 'description']


class VenueLayoutAreaAdmin(admin.ModelAdmin):
    fields = ['company', 'venue', 'layout', 'name', 'capacity', 'notes', 'price']


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
                ('Event', {'fields': ['company', 'venue', 'name', 'description']}),
                ('Date & Time', {'fields': ['datestart', 'timestart',
                                 'dateend', 'timeend']}),
                ('Recurrance', {'fields': ['recurring']})
    ]


class MemberAdmin(admin.ModelAdmin):
    fields = ['firstname', 'lastname', 'email', 'dateofbirth', 'appearances']


class MembershipTypeAdmin(admin.ModelAdmin):
    fields = ['company', 'venue', 'name', 'price', 'length']


class MembershipAdmin(admin.ModelAdmin):
    fields = ['member', 'membershiptype', 'starts', 'expires', 'paid']


class GuestListAdmin(admin.ModelAdmin):
    fields = ['company', 'venue', 'event', 'name', 'maxguests',
              'maxplusones', 'listopen']


class GuestAdmin(admin.ModelAdmin):
    fields = ['company', 'venue', 'guestlist', 'firstname', 'lastname',
              'email', 'member', 'timeslot', 'plusones', 'notes', 'arrived']

admin.site.register(Company, CompanyAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(VenueLayout, VenueLayoutAdmin)
admin.site.register(VenueLayoutArea, VenueLayoutAreaAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(GuestList, GuestListAdmin)
admin.site.register(Guest, GuestAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Member, MemberAdmin)
admin.site.register(Membership, MembershipAdmin)
admin.site.register(MembershipType, MembershipTypeAdmin)

from django.contrib import admin
from .models import Company, Venue, Event
# Register your models here.


class CompanyAdmin(admin.ModelAdmin):
    fields = ['name']


class VenueAdmin(admin.ModelAdmin):
    fields = ['owner', 'name']


class EventAdmin(admin.ModelAdmin):
    fieldsets = [
                ('Event', {'fields': ['venue', 'name', 'description']}),
                ('Date & Time', {'fields': ['datestart', 'timestart',
                                 'dateend', 'timeend']}),
                ('Recurrance', {'fields': ['recurring']})
    ]


admin.site.register(Company, CompanyAdmin)
admin.site.register(Venue, VenueAdmin)
admin.site.register(Event, EventAdmin)

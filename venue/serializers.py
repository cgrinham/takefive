from venue.models import Event, Member, Venue, Company
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    venue = serializers.StringRelatedField()

    class Meta:
        # model = Member
        # fields = ('firstname', 'lastname', 'email')
        model = Event
        fields = ('venue', 'name', 'datestart', 'timestart')

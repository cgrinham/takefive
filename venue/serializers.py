from venue.models import Event, Member, Venue, Company, GuestList, Guest
from rest_framework import serializers


class GuestListSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.StringRelatedField()
    venue = serializers.StringRelatedField()
    event = serializers.StringRelatedField()
    recurringevent = serializers.StringRelatedField()

    class Meta:
        model = GuestList
        fields = ('company', 'venue', 'event', 'recurringevent', 'name', 'maxguests', 'maxplusones', 'listopen')


class GuestSerializer(serializers.HyperlinkedModelSerializer):
    company = serializers.StringRelatedField()
    venue = serializers.StringRelatedField()
    guestlist = serializers.StringRelatedField()

    class Meta:
        model = Guest
        fields = (
            'company',
            'venue',
            'guestlist',
            'firstname',
            'lastname',
            'email',
            'member',
            'timeslot',
            'plusones',
            'notes',
            'arrived',
            'source',
            )


class EventSerializer(serializers.HyperlinkedModelSerializer):
    venue = serializers.StringRelatedField()

    class Meta:
        # model = Member
        # fields = ('firstname', 'lastname', 'email')
        model = Event
        fields = ('venue', 'name', 'datestart', 'timestart')

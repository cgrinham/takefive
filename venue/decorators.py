from django.core.exceptions import PermissionDenied
from models import Company, Venue


def user_owns_company_and_venue(function):
    def wrap(request, *args, **kwargs):
        company = Company.objects.get(reference=kwargs['company'])
        venue = Venue.objects.get(reference=kwargs['venue'])

        if request.user.profile.company == company and venue.owner == company:
            return function(request, *args, **kwargs)
        else:
            raise PermissionDenied

    wrap.__doc__ = function.__doc__
    wrap.__name__ = function.__name__
    return wrap

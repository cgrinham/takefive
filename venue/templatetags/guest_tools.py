from django import template

register = template.Library()


@register.filter
def countguests(guests):  # Only one argument.
    return len(guests)

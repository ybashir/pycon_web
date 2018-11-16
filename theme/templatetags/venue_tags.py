from theme.models import Venue
from django import template


register = template.Library()


@register.simple_tag
def featured_venue(limit=4):
    return list(Venue.objects.filter(featured=True)[:limit])


@register.simple_tag
def all_venue():
    return list(Venue.objects.all())

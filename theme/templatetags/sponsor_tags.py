from theme.models import Sponsor
from django import template


register = template.Library()


@register.simple_tag
def featured_sponsors(limit=4):
    return list(Sponsor.objects.filter(featured=True)[:limit])


@register.simple_tag
def all_sponsors():
    return list(Sponsor.objects.all())

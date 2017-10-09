from theme.models import Speaker
from django import template


register = template.Library()


@register.simple_tag
def featured_speakers(limit=3):
    return list(Speaker.objects.filter(featured=True)[:limit])


@register.simple_tag
def all_speakers():
    return list(Speaker.objects.all())

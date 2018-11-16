from theme.models import Media
from django import template


register = template.Library()


@register.simple_tag
def featured_media(limit=4):
    return list(Media.objects.filter(featured=True)[:limit])


@register.simple_tag
def all_media():
    return list(Media.objects.all())

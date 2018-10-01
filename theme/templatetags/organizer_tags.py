from theme.models import Organizer
from django import template


register = template.Library()



@register.simple_tag
def all_organizers():
    return list(Organizer.objects.all())

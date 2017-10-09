from theme.models import HomePageSlide
from django import template


register = template.Library()


@register.simple_tag
def all_slides():
    return list(HomePageSlide.objects.all())

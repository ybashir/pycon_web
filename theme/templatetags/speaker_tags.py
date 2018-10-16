from theme.models import Speaker
from django import template
from django.db.models import Q
from mezzanine.blog.models import BlogPost
from mezzanine.forms.models import Field, FieldEntry


register = template.Library()


@register.simple_tag
def featured_speakers(limit=3):
    return list(Speaker.objects.filter(featured=True)[:limit])


@register.simple_tag
def speaker_count(year):
    return Speaker.objects.filter(conference_year=year).count()


@register.simple_tag
def total_passes_booked():
    return FieldEntry.objects.filter(
        field_id__in=Field.objects.filter(label__icontains='cnic number'), entry__entry_time__year=2018
    ).count()


@register.simple_tag
def blog_post_count():
    return BlogPost.objects.count()

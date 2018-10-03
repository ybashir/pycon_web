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
def speaker_count():
    return Speaker.objects.count()


@register.simple_tag
def total_passes_booked():
    entries = FieldEntry.objects.filter(field_id__in=Field.objects.filter(Q(label__icontains='student pass') | Q(
        label__icontains='professional pass') | Q(label__icontains='speaker pass')))

    total_passes = 0
    for entry in entries:
        total_passes += int(entry.value)

    return total_passes


@register.simple_tag
def blog_post_count():
    return BlogPost.objects.count()

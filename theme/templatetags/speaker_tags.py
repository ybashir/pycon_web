from theme.models import Speaker
from django import template
from django.db.models import Q, Sum
from mezzanine.forms.models import Field, FieldEntry


register = template.Library()


@register.simple_tag
def featured_speakers(limit=3):
    return list(Speaker.objects.filter(featured=True)[:limit])


@register.simple_tag
def all_speakers():
    return list(Speaker.objects.all())


@register.simple_tag
def speaker_count():
    return Speaker.objects.count()


@register.simple_tag
def passes_booked_except_speakers():
    return FieldEntry.objects.filter(field_id__in=Field.objects.filter(
        Q(label__icontains='student pass') | Q(label__icontains='professional pass') | Q(label__icontains='speaker pass'))).aggregate(Sum('value'))[
        'value__sum']

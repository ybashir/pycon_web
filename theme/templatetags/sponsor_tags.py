from theme.models import Sponsor
from django import template
from collections import OrderedDict


register = template.Library()

def preprocess_sponsors(sponsors):
    sponsors_dict = OrderedDict()
    for sponsor in sponsors:
        key = sponsor.sponsor_type.title if sponsor.sponsor_type else ""
        
        if sponsors_dict.get(key) == None:
            sponsors_dict[key] = [sponsor]
        else:
            sponsors_dict[key].append(sponsor)

    return sponsors_dict

@register.simple_tag
def featured_sponsors(limit=4):
    return preprocess_sponsors(list(Sponsor.objects.filter(featured=True).order_by('sponsor_type__order', 'title')[:limit]))

@register.simple_tag
def all_sponsors():
    return preprocess_sponsors(list(Sponsor.objects.all().order_by('sponsor_type__order', 'title')))

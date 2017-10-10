from theme.models import GalleryImage
from django import template


register = template.Library()


@register.simple_tag
def featured_gallery_images(limit=9):
    return list(GalleryImage.objects.filter(featured=True)[:limit])

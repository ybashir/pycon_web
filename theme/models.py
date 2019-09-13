from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.pages.models import RichText
from mezzanine.core.fields import FileField, RichTextField
from mezzanine.pages.models import Displayable
from mezzanine.utils.models import upload_to
from orderable.models import Orderable


class Speaker(Orderable):
    name = models.CharField(max_length=500)
    designation = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    bio = models.TextField()
    conference_year = models.IntegerField(null=True, blank=True)
    profile_image = FileField(verbose_name=_("Profile Image"),
                              upload_to=upload_to("", "teacher"),
                              format="Image", max_length=255, null=True, blank=True)
    featured = models.BooleanField(default=False)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linked_in_link = models.URLField(blank=True, null=True)
    dribble_link = models.URLField(blank=True, null=True)
    github_link = models.URLField(blank=True, null=True)
    personal_web_link = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        return '/speakers/'


class Organizer(Displayable):
    designation = models.CharField(max_length=100)
    organization = models.CharField(max_length=100)
    profile_image = FileField(verbose_name=_("Profile Image"),
                              upload_to=upload_to("", "teacher"),
                              format="Image", max_length=255, null=True, blank=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linked_in_link = models.URLField(blank=True, null=True)
    dribble_link = models.URLField(blank=True, null=True)
    personal_web_link = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        return '/organizers/'


class HomePageSlide(Displayable, RichText):
    def get_absolute_url(self):
        pass

    background_image = FileField(verbose_name=_("Background Image"),
                                 upload_to=upload_to("", "slider"),
                                 format="Image", max_length=255)
    sub_text = models.CharField(max_length=300)
    links = RichTextField()


class Gallery(Displayable):
    gallery_description = models.TextField(null=True, blank=True)
    thumbnail = FileField(verbose_name=_("Thumbnail"), upload_to=upload_to("", "gallery_thumbs"),
                          format="Image", max_length=255)
    is_video = models.BooleanField(default=False)
    video_link = models.CharField(null=True, blank=True, max_length=300)

    def get_absolute_url(self):
        return reverse('gallery_detail', args=[self.slug])


class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, on_delete=models.CASCADE)
    featured = models.BooleanField(default=False)
    image = FileField(verbose_name=_("Image"), upload_to=upload_to("", "gallery"), format="Image", max_length=255)

    def __unicode__(self):
        return self.gallery.title

class SponsorType(Displayable):
    title = models.CharField(null=True, blank=True, max_length=100)
    order = models.IntegerField(default=0)

class Sponsor(Displayable):
    def get_absolute_url(self):
        pass

    logo = FileField(verbose_name=_("Logo"), upload_to=upload_to("", "sponsors"),
                     format="Image", max_length=255)
    link = models.URLField()
    featured = models.BooleanField(default=False)
    sponsor_type = models.ForeignKey(SponsorType, null=True, blank=True, on_delete=models.SET_NULL)

class Media(Displayable):
    def get_absolute_url(self):
        pass

    logo = FileField(verbose_name=_("Logo"), upload_to=upload_to("", "media"),
                     format="Image", max_length=255)
    link = models.URLField()
    featured = models.BooleanField(default=False)


class Venue(Displayable):
    def get_absolute_url(self):
        pass

    logo = FileField(verbose_name=_("Logo"), upload_to=upload_to("", "venue"),
                     format="Image", max_length=255)
    link = models.URLField()
    featured = models.BooleanField(default=False)

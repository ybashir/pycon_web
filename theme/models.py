from django.db import models
from django.utils.translation import ugettext_lazy as _
from mezzanine.core.fields import FileField
from mezzanine.pages.models import Displayable
from mezzanine.utils.models import upload_to


class Speaker(Displayable):
    designation = models.CharField(max_length=20)
    organization = models.CharField(max_length=30)
    bio = models.TextField()
    profile_image = FileField(verbose_name=_("Profile Image"),
                              upload_to=upload_to("", "teacher"),
                              format="Image", max_length=255, null=True, blank=True)
    facebook_link = models.URLField(blank=True, null=True)
    twitter_link = models.URLField(blank=True, null=True)
    linked_in_link = models.URLField(blank=True, null=True)
    dribble_link = models.URLField(blank=True, null=True)

    def get_absolute_url(self):
        return '/speakers/'

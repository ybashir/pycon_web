from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin
from theme.models import Speaker, HomePageSlide


class SpeakerAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'designation', 'organization', 'featured', 'bio', 'profile_image',
                                    'facebook_link', 'twitter_link', 'linked_in_link', 'dribble_link')}),)
    list_display = ('title', 'status', 'designation', 'organization')


class HomePageSlideAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'sub_text', 'background_image', 'links')}),)
    list_display = ('title', 'status')


admin.site.register(HomePageSlide, HomePageSlideAdmin)
admin.site.register(Speaker, SpeakerAdmin)

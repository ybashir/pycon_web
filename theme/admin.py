from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin
from theme.models import Speaker, HomePageSlide, Gallery, GalleryImage, Sponsor


class SpeakerAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'designation', 'organization', 'featured', 'bio', 'profile_image',
                                    'facebook_link', 'twitter_link', 'linked_in_link', 'dribble_link')}),)
    list_display = ('title', 'status', 'designation', 'organization')


class HomePageSlideAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'sub_text', 'background_image', 'links')}),)
    list_display = ('title', 'status')


class GalleryImageInline(TabularDynamicInlineAdmin):
    model = GalleryImage


class GalleryAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'thumbnail', 'gallery_description')}),)
    list_display = ('title', 'status')
    inlines = [GalleryImageInline]


class SponsorAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'logo', 'link', 'featured')}),)
    list_display = ('title', 'status', 'featured')

admin.site.register(HomePageSlide, HomePageSlideAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Sponsor, SponsorAdmin)

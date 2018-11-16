from django.contrib import admin
from mezzanine.core.admin import DisplayableAdmin, TabularDynamicInlineAdmin
from orderable.admin import OrderableAdmin

from theme.models import Speaker, HomePageSlide, Gallery, GalleryImage, Sponsor, Organizer, Media, Venue


class SpeakerAdmin(OrderableAdmin):
    fieldsets = ((None, {'fields': ('name', 'designation', 'organization', 'featured', 'bio', 'profile_image',
                                    'conference_year', 'facebook_link', 'twitter_link', 'linked_in_link',
                                    'dribble_link', 'github_link', 'personal_web_link')}),)
    list_display = ('name', 'featured', 'designation', 'organization', 'sort_order_display')


class OrganizerAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'designation', 'organization', 'profile_image',
                                    'facebook_link', 'twitter_link', 'linked_in_link', 'dribble_link',
                                    'personal_web_link')}),)
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


class MediaAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'logo', 'link', 'featured')}),)
    list_display = ('title', 'status', 'featured')


class VenueAdmin(DisplayableAdmin):
    fieldsets = ((None, {'fields': ('title', 'logo', 'link', 'featured')}),)
    list_display = ('title', 'status', 'featured')


admin.site.register(HomePageSlide, HomePageSlideAdmin)
admin.site.register(Speaker, SpeakerAdmin)
admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(Organizer, OrganizerAdmin)
admin.site.register(Media, MediaAdmin)
admin.site.register(Venue, VenueAdmin)

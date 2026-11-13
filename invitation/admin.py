from django.contrib import admin
from django.utils.html import format_html
from .models import WeddingDetails, Event, StoryMilestone, GalleryMedia, RSVP, GuestWish


@admin.register(WeddingDetails)
class WeddingDetailsAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'wedding_date', 'wedding_location', 'hashtag', 'preview_couple_photo')
    fieldsets = (
        ("Couple Details", {
            'fields': (
                ('groom_name', 'bride_name'),
                ('groom_parents', 'bride_parents'),
                ('groom_bio', 'bride_bio'),
                ('groom_photo', 'bride_photo', 'couple_photo'),
            )
        }),
        ("Ceremony & Date", {
            'fields': (
                ('wedding_date', 'wedding_location'),
                ('hero_title', 'hero_tagline', 'hashtag'),
                'invitation_quote',
                'hero_image',
            )
        }),
        ("Media & Background Music", {
            'fields': (
                'background_music',
                'highlight_video_url',
            )
        }),
        ("Contact & RSVP Info", {
            'fields': (
                ('rsvp_deadline', 'contact_phone', 'contact_email'),
            )
        }),
    )

    def preview_couple_photo(self, obj):
        if obj.couple_photo:
            return format_html('<img src="{}" style="height: 50px; border-radius: 6px; object-fit: cover;" />', obj.couple_photo.url)
        return "No Photo"
    preview_couple_photo.short_description = "Couple Photo"


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_date', 'start_time', 'venue_name', 'dress_code', 'order')
    list_editable = ('order',)
    list_filter = ('event_date',)
    search_fields = ('title', 'venue_name', 'venue_address')


@admin.register(StoryMilestone)
class StoryMilestoneAdmin(admin.ModelAdmin):
    list_display = ('title', 'milestone_date', 'order', 'preview_photo')
    list_editable = ('order',)

    def preview_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="height: 45px; border-radius: 4px; object-fit: cover;" />', obj.photo.url)
        return "No Photo"
    preview_photo.short_description = "Photo"


@admin.register(GalleryMedia)
class GalleryMediaAdmin(admin.ModelAdmin):
    list_display = ('title', 'media_type', 'category', 'is_featured', 'order', 'media_preview')
    list_filter = ('media_type', 'category', 'is_featured')
    list_editable = ('order', 'is_featured', 'category')
    search_fields = ('title', 'caption')

    def media_preview(self, obj):
        if obj.media_type == 'photo' and obj.image:
            return format_html('<img src="{}" style="height: 50px; border-radius: 4px; object-fit: cover;" />', obj.image.url)
        elif obj.media_type == 'video_file' and obj.video_file:
            return format_html('<span style="color:#2563eb; font-weight:bold;">🎬 Video File ({})</span>', obj.video_file.name.split('/')[-1])
        elif obj.video_embed_url:
            return format_html('<a href="{}" target="_blank" style="color:#b45309; text-decoration:underline;">🔗 Video Link</a>', obj.video_embed_url)
        return "None"
    media_preview.short_description = "Preview"


@admin.register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('guest_name', 'phone', 'email', 'attending', 'guest_count', 'events_attending', 'submitted_at')
    list_filter = ('attending', 'submitted_at')
    search_fields = ('guest_name', 'email', 'phone')
    readonly_fields = ('submitted_at',)


@admin.register(GuestWish)
class GuestWishAdmin(admin.ModelAdmin):
    list_display = ('name', 'relation_or_city', 'is_approved', 'created_at', 'short_message')
    list_filter = ('is_approved', 'created_at')
    list_editable = ('is_approved',)
    search_fields = ('name', 'relation_or_city', 'message')

    def short_message(self, obj):
        return obj.message[:60] + ("..." if len(obj.message) > 60 else "")
    short_message.short_description = "Message"

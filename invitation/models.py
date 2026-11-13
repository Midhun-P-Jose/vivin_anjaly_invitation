from django.db import models
from django.utils import timezone


class WeddingDetails(models.Model):
    groom_name = models.CharField(max_length=100, default="Vivin")
    bride_name = models.CharField(max_length=100, default="Anjaly")
    groom_parents = models.CharField(max_length=250, blank=True, default="Son of Mr. & Mrs. Jose")
    bride_parents = models.CharField(max_length=250, blank=True, default="Daughter of Mr. & Mrs. Thomas")
    groom_bio = models.TextField(blank=True, default="A gentle heart, an adventurous spirit, and ready to embark on a lifetime of love.")
    bride_bio = models.TextField(blank=True, default="Graceful, kind-hearted, with a smile that brightens every room and completes Vivin's world.")
    
    wedding_date = models.DateTimeField(help_text="Primary wedding ceremony date and time")
    wedding_location = models.CharField(max_length=200, default="Kochi, Kerala, India")
    
    hero_title = models.CharField(max_length=200, default="We Are Getting Married!")
    hero_tagline = models.CharField(max_length=250, default="Two Souls, One Heart, An Eternal Promise")
    hashtag = models.CharField(max_length=100, default="#VivinWedsAnjaly")
    
    invitation_quote = models.TextField(
        default="As love brings us together, we invite you to share this sacred beginning of our new chapter. Your presence, love, and prayers will make our special day complete."
    )
    
    # Media
    hero_image = models.ImageField(upload_to="hero/", blank=True, null=True)
    groom_photo = models.ImageField(upload_to="couple/", blank=True, null=True)
    bride_photo = models.ImageField(upload_to="couple/", blank=True, null=True)
    couple_photo = models.ImageField(upload_to="couple/", blank=True, null=True)
    background_music = models.FileField(upload_to="music/", blank=True, null=True, help_text="Upload MP3 for ambient background music")
    highlight_video_url = models.CharField(max_length=500, blank=True, null=True, help_text="YouTube / Vimeo / MP4 link for pre-wedding teaser")
    
    rsvp_deadline = models.DateField(blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, default="+91 98765 43210")
    contact_email = models.EmailField(blank=True, default="wedding@example.com")
    
    class Meta:
        verbose_name = "Wedding Details"
        verbose_name_plural = "Wedding Details"

    def __str__(self):
        return f"{self.groom_name} & {self.bride_name}'s Wedding"

    @classmethod
    def get_details(cls):
        """Retrieve the active wedding details or return the first entry"""
        return cls.objects.first()


class Event(models.Model):
    ICON_CHOICES = [
        ('church', 'Church / Ceremony'),
        ('rings', 'Wedding Rings / Vows'),
        ('glass-cheers', 'Reception / Toast'),
        ('music', 'Sangeet / Music Party'),
        ('sparkles', 'Haldi / Mehendi'),
        ('heart', 'Blessings / Engagement'),
    ]

    title = models.CharField(max_length=150)
    subtitle = models.CharField(max_length=200, blank=True)
    event_date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(blank=True, null=True)
    venue_name = models.CharField(max_length=200)
    venue_address = models.TextField()
    google_maps_url = models.URLField(blank=True, max_length=500)
    dress_code = models.CharField(max_length=150, blank=True, help_text="e.g. Traditional Festive / Formal Pastel / Elegance")
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=30, choices=ICON_CHOICES, default='church')
    cover_image = models.ImageField(upload_to="events/", blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order', 'event_date', 'start_time']

    def __str__(self):
        return f"{self.title} - {self.event_date}"


class StoryMilestone(models.Model):
    title = models.CharField(max_length=150)
    milestone_date = models.CharField(max_length=100, help_text="e.g. October 2022, The First Date")
    description = models.TextField()
    photo = models.ImageField(upload_to="story/", blank=True, null=True)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.title}"


class GalleryMedia(models.Model):
    MEDIA_TYPES = [
        ('photo', 'Photo'),
        ('video_file', 'Video File (MP4/WebM)'),
        ('video_embed', 'Video Link (YouTube / Vimeo / Direct URL)'),
    ]
    
    CATEGORY_CHOICES = [
        ('all', 'All Highlights'),
        ('engagement', 'Engagement'),
        ('pre_wedding', 'Pre-Wedding Shoot'),
        ('candid', 'Moments & Candids'),
    ]

    title = models.CharField(max_length=150, blank=True)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES, default='photo')
    image = models.ImageField(upload_to="gallery/photos/", blank=True, null=True)
    video_file = models.FileField(upload_to="gallery/videos/", blank=True, null=True)
    video_embed_url = models.CharField(max_length=500, blank=True, help_text="YouTube URL, Vimeo URL, or CDN video URL")
    caption = models.CharField(max_length=300, blank=True)
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES, default='all')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title or f"Media #{self.id} ({self.media_type})"


class RSVP(models.Model):
    ATTENDANCE_CHOICES = [
        ('yes', 'Joyfully Accept (Attending)'),
        ('no', 'Regretfully Decline'),
    ]

    guest_name = models.CharField(max_length=150)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=30)
    attending = models.CharField(max_length=10, choices=ATTENDANCE_CHOICES, default='yes')
    guest_count = models.PositiveIntegerField(default=1)
    events_attending = models.CharField(max_length=300, blank=True, default="All Events")
    notes_or_dietary = models.TextField(blank=True, verbose_name="Wishes or Dietary Notes")
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-submitted_at']
        verbose_name = "RSVP"
        verbose_name_plural = "RSVPs"

    def __str__(self):
        return f"{self.guest_name} ({self.get_attending_display()}) - {self.guest_count} guest(s)"


class GuestWish(models.Model):
    name = models.CharField(max_length=120)
    relation_or_city = models.CharField(max_length=120, blank=True, help_text="e.g. College Friend, Cousin, Kochi")
    message = models.TextField()
    is_approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Guest Wish"
        verbose_name_plural = "Guest Wishes"

    def __str__(self):
        return f"Wish by {self.name}"

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import datetime, date, time, timedelta
from invitation.models import WeddingDetails, Event, StoryMilestone, GalleryMedia, RSVP, GuestWish


class Command(BaseCommand):
    help = "Seeds initial sample data for Vivin & Anjaly's wedding invitation website"

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding wedding details for Vivin & Anjaly..."))

        # Future wedding date: e.g. 45 days from today at 10:30 AM
        wedding_datetime = timezone.now() + timedelta(days=45)
        wedding_datetime = wedding_datetime.replace(hour=10, minute=30, second=0, microsecond=0)

        # 1. Wedding Details
        details, created = WeddingDetails.objects.get_or_create(id=1, defaults={
            'groom_name': 'Vivin',
            'bride_name': 'Anjaly',
            'groom_parents': 'Son of Mr. P.J. Jose & Mrs. Mary Jose',
            'bride_parents': 'Daughter of Mr. K.T. Thomas & Mrs. Leelamma Thomas',
            'groom_bio': 'A kind soul, avid traveler, and passionate engineer, who found his true companion and greatest adventure in Anjaly.',
            'bride_bio': 'Graceful, compassionate, and full of life, whose infectious smile and warmth illuminate Vivin’s world every day.',
            'wedding_date': wedding_datetime,
            'wedding_location': 'Kochi, Kerala, India',
            'hero_title': 'WE ARE GETTING MARRIED',
            'hero_tagline': 'Two souls, one heart, an eternal promise.',
            'hashtag': '#VivinWedsAnjaly',
            'invitation_quote': 'With joyful hearts and the blessings of our families, we cordially invite you to join us as we celebrate our love and exchange our vows in Holy Matrimony.',
            'highlight_video_url': 'https://www.youtube.com/watch?v=ScMzIvxBSi4',
            'rsvp_deadline': (wedding_datetime - timedelta(days=14)).date(),
            'contact_phone': '+91 98470 12345',
            'contact_email': 'vivin.anjaly.wedding@gmail.com',
        })
        if not created:
            details.wedding_date = wedding_datetime
            details.save()
        self.stdout.write(self.style.SUCCESS("✓ Wedding Details ready!"))

        # 2. Events
        Event.objects.all().delete()
        
        event1 = Event.objects.create(
            title="Holy Matrimony",
            subtitle="The Sacred Vows & Nuptial Blessing",
            event_date=wedding_datetime.date(),
            start_time=time(10, 30),
            end_time=time(12, 30),
            venue_name="St. Mary's Cathedral Basilica",
            venue_address="Marine Drive, Ernakulam, Kochi, Kerala 682031",
            google_maps_url="https://maps.google.com/?q=St+Marys+Cathedral+Basilica+Ernakulam+Kochi",
            dress_code="Traditional Kerala Festive / Elegant Formal",
            description="Join us in prayer and joy as we unite our lives before God, our families, and dearest friends in the sacred sacrament of marriage.",
            icon="church",
            order=1
        )

        event2 = Event.objects.create(
            title="Grand Wedding Reception",
            subtitle="Dinner, Toasts & Celebrations",
            event_date=wedding_datetime.date(),
            start_time=time(18, 0),
            end_time=time(22, 30),
            venue_name="Grand Hyatt Kochi Bolgatty",
            venue_address="Mulavukad, Kochi, Kerala 682504",
            google_maps_url="https://maps.google.com/?q=Grand+Hyatt+Kochi+Bolgatty",
            dress_code="Formal Evening Attire / Suits & Sarees",
            description="An enchanting evening overlooking the backwaters with fine dining, music, cake cutting, and cheerful memories.",
            icon="glass-cheers",
            order=2
        )

        event3 = Event.objects.create(
            title="Haldi & Sangeet Evening",
            subtitle="Colors, Rhythms & Family Fun",
            event_date=(wedding_datetime - timedelta(days=1)).date(),
            start_time=time(17, 30),
            end_time=time(21, 0),
            venue_name="The Avenue Center Hotel",
            venue_address="Panampilly Nagar, Kochi, Kerala 682036",
            google_maps_url="https://maps.google.com/?q=The+Avenue+Center+Hotel+Panampilly+Nagar",
            dress_code="Vibrant Yellows, Pastels & Ethnic Festive",
            description="A pre-wedding celebration filled with music, turmeric blessings, sweet laughter, and lively dances.",
            icon="sparkles",
            order=3
        )
        self.stdout.write(self.style.SUCCESS("✓ 3 Wedding Events created!"))

        # 3. Love Story Milestones
        StoryMilestone.objects.all().delete()
        StoryMilestone.objects.create(
            title="A Serendipitous Meeting",
            milestone_date="October 2021",
            description="A casual coffee in Fort Kochi turned into four unforgettable hours of laughing, sharing dreams, and an instant, effortless connection.",
            order=1
        )
        StoryMilestone.objects.create(
            title="First Journey Together",
            milestone_date="November 2022",
            description="Exploring the misty hills of Munnar, enjoying sunrise walks, and realizing that every road in life felt better traveled together.",
            order=2
        )
        StoryMilestone.objects.create(
            title="The Proposal By The Waters 💍",
            milestone_date="December 2023",
            description="With the golden sunset reflecting over the Vembanad Lake, Vivin got down on one knee. With happy tears and smiling eyes, Anjaly said YES!",
            order=3
        )
        StoryMilestone.objects.create(
            title="The Sacred Vow",
            milestone_date="The Big Day",
            description="Stepping into a lifetime of love, trust, and shared dreams surrounded by the people who mean the absolute most to us.",
            order=4
        )
        self.stdout.write(self.style.SUCCESS("✓ Love Story timeline created!"))

        # 4. Gallery Media
        GalleryMedia.objects.all().delete()
        GalleryMedia.objects.create(
            title="Sunset Over The Backwaters",
            media_type="photo",
            caption="Where the sky meets our dreams.",
            category="pre_wedding",
            is_featured=True,
            order=1
        )
        GalleryMedia.objects.create(
            title="Wedding Teaser Trailer",
            media_type="video_embed",
            video_embed_url="https://www.youtube.com/watch?v=ScMzIvxBSi4",
            caption="A sneak peek into our love story.",
            category="pre_wedding",
            is_featured=True,
            order=2
        )
        GalleryMedia.objects.create(
            title="Unconditional Smiles",
            media_type="photo",
            caption="The sweetest candids are never staged.",
            category="candid",
            is_featured=False,
            order=3
        )
        GalleryMedia.objects.create(
            title="The Ring Ceremony",
            media_type="photo",
            caption="Two rings, one promise of a lifetime.",
            category="engagement",
            is_featured=True,
            order=4
        )
        self.stdout.write(self.style.SUCCESS("✓ Gallery media placeholders created!"))

        # 5. Wishes
        if not GuestWish.objects.exists():
            GuestWish.objects.create(
                name="Uncle George & Family",
                relation_or_city="Dallas, TX",
                message="Heartiest congratulations Vivin and Anjaly! May your married life be filled with abundant blessings, peace, and eternal joy.",
                is_approved=True
            )
            GuestWish.objects.create(
                name="Sneha & Rahul",
                relation_or_city="Bangalore",
                message="You two are the sweetest couple ever! Can't wait to dance at the reception and celebrate your big day with you!",
                is_approved=True
            )
            GuestWish.objects.create(
                name="Fr. Mathew & Parish Community",
                relation_or_city="Kochi",
                message="Praying for God's grace and blessings upon both of you as you embark upon this holy sacrament of matrimony.",
                is_approved=True
            )
            self.stdout.write(self.style.SUCCESS("✓ Sample guestbook wishes created!"))

        self.stdout.write(self.style.SUCCESS("\n🎉 Wedding database successfully seeded for Vivin & Anjaly!"))


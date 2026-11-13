import json
from datetime import datetime
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import WeddingDetails, Event, StoryMilestone, GalleryMedia, RSVP, GuestWish


def index(request):
    details = WeddingDetails.get_details()
    events = Event.objects.all()
    stories = StoryMilestone.objects.all()
    gallery_items = GalleryMedia.objects.all()
    wishes = GuestWish.objects.filter(is_approved=True)

    # Categories present in gallery for filter tabs
    categories = [
        ('all', 'All Moments'),
        ('pre_wedding', 'Pre-Wedding'),
        ('engagement', 'Engagement'),
        ('candid', 'Candids & Memories'),
    ]

    # Format wedding date ISO for JavaScript countdown
    # Fixed: Jan 4 2027 at 10:00 AM IST (UTC+5:30)
    countdown_iso = "2027-01-04T10:00:00+05:30"
    if details and details.wedding_date:
        import pytz
        ist = pytz.timezone('Asia/Kolkata')
        wd = details.wedding_date.astimezone(ist)
        countdown_iso = wd.isoformat()

    context = {
        'details': details,
        'events': events,
        'stories': stories,
        'gallery_items': gallery_items,
        'wishes': wishes,
        'categories': categories,
        'countdown_iso': countdown_iso,
    }
    return render(request, 'invitation/index.html', context)


@require_POST
def submit_rsvp(request):
    try:
        # Handle both JSON request and standard form POST
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        guest_name = data.get('guest_name', '').strip()
        phone = data.get('phone', '').strip()
        email = data.get('email', '').strip()
        attending = data.get('attending', 'yes')
        guest_count = int(data.get('guest_count', 1))
        events_attending = data.get('events_attending', 'All Events')
        notes_or_dietary = data.get('notes_or_dietary', '').strip()

        if not guest_name or not phone:
            return JsonResponse({'status': 'error', 'message': 'Please provide your name and phone number.'}, status=400)

        rsvp = RSVP.objects.create(
            guest_name=guest_name,
            phone=phone,
            email=email,
            attending=attending,
            guest_count=max(1, guest_count),
            events_attending=events_attending,
            notes_or_dietary=notes_or_dietary
        )

        return JsonResponse({
            'status': 'success',
            'message': f"Thank you, {guest_name}! Your RSVP has been received with joy."
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@require_POST
def submit_wish(request):
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST

        name = data.get('name', '').strip()
        relation_or_city = data.get('relation_or_city', '').strip()
        message = data.get('message', '').strip()

        if not name or not message:
            return JsonResponse({'status': 'error', 'message': 'Please enter both your name and a heartfelt message.'}, status=400)

        wish = GuestWish.objects.create(
            name=name,
            relation_or_city=relation_or_city,
            message=message,
            is_approved=True
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Thank you for your warm wishes and blessings!',
            'wish': {
                'name': wish.name,
                'relation_or_city': wish.relation_or_city,
                'message': wish.message,
                'created_at': wish.created_at.strftime('%b %d, %Y')
            }
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


def download_ics(request, event_id=None):
    """Generate .ics calendar file for the wedding or specific event"""
    details = WeddingDetails.get_details()
    events = Event.objects.all()
    if event_id:
        events = events.filter(id=event_id)

    title_prefix = f"{details.groom_name} & {details.bride_name}'s Wedding" if details else "Vivin & Anjaly's Wedding"

    ics_content = [
        "BEGIN:VCALENDAR",
        "VERSION:2.0",
        "PRODID:-//Vivin & Anjaly Wedding Invitation//EN",
        "CALSCALE:GREGORIAN",
        "METHOD:PUBLISH"
    ]

    for ev in events:
        dt_start = datetime.combine(ev.event_date, ev.start_time)
        dt_end = datetime.combine(ev.event_date, ev.end_time) if ev.end_time else (dt_start + timezone.timedelta(hours=3))
        
        fmt = "%Y%m%dT%H%M%SZ"
        start_str = dt_start.strftime(fmt)
        end_str = dt_end.strftime(fmt)

        summary = f"{title_prefix} - {ev.title}"
        description = f"{ev.description}\\nDress Code: {ev.dress_code}".replace("\n", "\\n")
        location = f"{ev.venue_name}, {ev.venue_address}".replace("\n", ", ")

        ics_content.extend([
            "BEGIN:VEVENT",
            f"UID:wedding-event-{ev.id}@{request.get_host()}",
            f"DTSTAMP:{timezone.now().strftime(fmt)}",
            f"DTSTART:{start_str}",
            f"DTEND:{end_str}",
            f"SUMMARY:{summary}",
            f"DESCRIPTION:{description}",
            f"LOCATION:{location}",
            "STATUS:CONFIRMED",
            "END:VEVENT"
        ])

    ics_content.append("END:VCALENDAR")
    response = HttpResponse("\r\n".join(ics_content), content_type="text/calendar")
    response['Content-Disposition'] = f'attachment; filename="wedding_invitation.ics"'
    return response

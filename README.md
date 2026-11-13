# 💍 Vivin & Anjaly - Luxury Wedding Invitation Website

A wedding invitation website built with **Django 5**, HTML5, CSS3, and JavaScript, designed with an editorial aesthetic for **Vivin & Anjaly**.

---

## ✨ Features

- **Luxury Editorial Design**: Tailored typography (Playfair Display, Alex Brush, Cormorant Garamond, Montserrat) with champagne gold and warm ivory aesthetics.
- **Live Countdown Timer**: Real-time ticker counting down Days, Hours, Minutes, and Seconds until the wedding vows.
- **Meet the Couple**: Dedicated spotlight cards for the Groom and Bride with parent blessings and bios.
- **Interactive Love Story**: Romantic timeline tracking milestones from how they first met to the proposal and wedding day.
- **Wedding Itinerary & Events**:
  - Detailed cards for the ceremony (Holy Matrimony), Reception, Haldi/Sangeet.
  - Direct 1-tap **Google Maps navigation**.
  - **1-Click "Add to Calendar"** (.ics file download compatible with Google Calendar, Apple Calendar, and Outlook).
- **Photo & Video Gallery**:
  - Filterable tabs for Photos, Videos, Pre-Wedding shoots, and Candids.
  - Full-screen **Lightbox viewer** for high-resolution images.
  - **Video Modal Player** supporting both direct uploaded MP4 files and embedded YouTube/Vimeo links.
- **Interactive Online RSVP**:
  - Instant AJAX RSVP form (Full Name, Phone/WhatsApp, Email, Guest count, Attending status, Event choices, Dietary notes).
  - Stored directly in the Django database with admin moderation and review.
- **Live Wishes & Blessings Wall (Guestbook)**:
  - Real-time guestbook where loved ones can write blessings that display on the website.
- **Background Romantic Music Player**:
  - Floating vinyl audio controller with play/pause and animated equalizer soundbars.
- **Travel & Stay Guide**:
  - Helpful travel tips (Nearest Airport COK, Railway stations, nearby hotels, family contact info).
- **Mobile-First & Responsive**:
  - Designed for mobile phones (where 90%+ of wedding guests view invitations on WhatsApp/Instagram).

---

## 🚀 How to Run the Website

### 1. Start the Django Server
Open your terminal in this folder (`vivin_anjaly`) and run:
```powershell
python manage.py runserver
```
Then open your browser and navigate to:
👉 **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)**

---

## 📸 How to Add Your Photos and Videos

You can add pictures and videos using either of the two easy methods below:

### Method 1: Using the Django Admin Dashboard (Recommended)
1. Go to **[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)** in your browser.
2. Sign in with the credentials:
   - **Username**: `admin`
   - **Password**: `admin123`
3. Click on:
   - **Wedding Details**: Upload Hero Background image, Groom photo, Bride photo, Couple photo, and background music MP3.
   - **Gallery Media**: Click **"Add Gallery Media"** to upload your high-resolution photos, MP4 video files, or paste YouTube/Vimeo links.
   - **Events**: Upload cover images for the Church, Reception, or Sangeet.
   - **Story Milestones**: Upload photos for each milestone in your love story.

### Method 2: Providing Files in the Workspace
You can drop your media files directly into the project folders:
- `media/hero/` - Main banner background photo or video poster
- `media/couple/` - Groom, Bride, and Couple portraits
- `media/photos/` - High-resolution gallery photos
- `media/videos/` - Pre-wedding MP4 video files
- `media/music/` - Background romantic instrumental MP3
- `media/story/` - Love story milestone photos
- `media/events/` - Event cards cover photos

Whenever you share the files here in the chat, I can also place, configure, and optimize them for you automatically!

---

## 📋 Managing RSVPs & Wishes

From the **Django Admin** (`/admin/`):
- View full guest list under **RSVPs** with guest counts and contact details.
- Approve or moderate guest wishes under **Guest Wishes**.
- Update event dates, times, dress codes, or venues anytime.

---

## 🛠️ Project Structure
```text
vivin_anjaly/
├── manage.py
├── db.sqlite3
├── wedding_project/       # Project configuration
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── invitation/            # Wedding invitation application
│   ├── models.py          # Wedding, Event, Gallery, RSVP, Wish models
│   ├── views.py           # Views & AJAX handlers
│   ├── urls.py
│   ├── admin.py           # Customized Django admin
│   └── management/
│       └── commands/
│           └── seed_wedding.py # Initial demo data seed
├── templates/
│   └── invitation/
│       ├── base.html      # Base layout, navbar, audio player, modals
│       └── index.html     # Full wedding invitation landing page
├── static/
│   ├── css/style.css      # Luxury gold & champagne styling
│   └── js/main.js         # Countdown, audio, filter, RSVP/Wish AJAX
└── media/                 # Upload directory for photos & videos
```


/**
 * VIVIN & ANJALY - WEDDING INVITATION INTERACTIVE SCRIPTS
 */

document.addEventListener('DOMContentLoaded', function () {
    initNavbar();
    initCountdown();
    initAudioPlayer();
    initGallery();
    initCoupleLetter();
    initModals();
    initRSVPForm();
    initWishForm();
    initAmbientCanvas();
});

/* ==========================================================================
   1. STICKY NAVBAR & MOBILE MENU
   ========================================================================== */
function initNavbar() {
    const navbar = document.getElementById('navbar');
    const toggle = document.getElementById('mobileNavToggle');
    const navLinks = document.getElementById('navLinks');

    // Sticky header on scroll
    window.addEventListener('scroll', () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Mobile nav toggle
    if (toggle && navLinks) {
        toggle.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            const icon = toggle.querySelector('i');
            if (icon) {
                icon.classList.toggle('fa-bars');
                icon.classList.toggle('fa-xmark');
            }
        });

        // Close on link click
        navLinks.querySelectorAll('.nav-item').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                const icon = toggle.querySelector('i');
                if (icon) {
                    icon.classList.add('fa-bars');
                    icon.classList.remove('fa-xmark');
                }
            });
        });
    }
}

/* ==========================================================================
   2. LIVE COUNTDOWN TIMER
   ========================================================================== */
function initCountdown() {
    const targetDateStr = window.WEDDING_CONFIG?.countdownDate;
    if (!targetDateStr) return;

    const targetTime = new Date(targetDateStr).getTime();
    if (isNaN(targetTime)) return;

    const countDays = document.getElementById('countDays');
    const countHours = document.getElementById('countHours');
    const countMinutes = document.getElementById('countMinutes');
    const countSeconds = document.getElementById('countSeconds');
    const container = document.getElementById('countdownContainer');

    function update() {
        const now = new Date().getTime();
        const difference = targetTime - now;

        if (difference <= 0) {
            if (container) {
                container.innerHTML = `
                    <div style="font-family:'Playfair Display', serif; font-size:1.8rem; color:#FFFFFF; padding:15px 25px; background:rgba(197,168,128,0.3); border-radius:12px; border:1px solid rgba(197,168,128,0.5);">
                        💍 Celebrating Today &amp; Forever! 🥂
                    </div>
                `;
            }
            return;
        }

        const days = Math.floor(difference / (1000 * 60 * 60 * 24));
        const hours = Math.floor((difference % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((difference % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((difference % (1000 * 60)) / 1000);

        if (countDays) countDays.textContent = String(days).padStart(2, '0');
        if (countHours) countHours.textContent = String(hours).padStart(2, '0');
        if (countMinutes) countMinutes.textContent = String(minutes).padStart(2, '0');
        if (countSeconds) countSeconds.textContent = String(seconds).padStart(2, '0');
    }

    update();
    setInterval(update, 1000);
}

/* ==========================================================================
   3. BACKGROUND AUDIO PLAYER
   ========================================================================== */
function initAudioPlayer() {
    const audio = document.getElementById('weddingAudio');
    const toggleBtn = document.getElementById('musicToggleBtn');
    const controlPill = document.getElementById('audio-control');
    if (!audio || !toggleBtn) return;

    function playAudio() {
        try {
            const attempt = audio.play();
            if (attempt && typeof attempt.catch === 'function') {
                attempt.catch(() => {});
            }
        } catch (err) {
            /* playback was blocked */
        }
    }

    function pauseAudio() {
        audio.pause();
    }

    // Keep the pill UI in sync with the real playback state
    audio.addEventListener('play', () => {
        controlPill.classList.add('playing');
        clearFallback();
    });
    audio.addEventListener('pause', () => controlPill.classList.remove('playing'));

    // Toggle button: pause <-> resume
    toggleBtn.addEventListener('click', () => {
        if (audio.paused) {
            playAudio();
        } else {
            pauseAudio();
        }
    });

    // Start on the very first interaction anywhere on the page.
    // Register these listeners immediately (not only after the autoplay
    // promise rejects) so no gesture is ever missed while it resolves.
    const interactionEvents = ['pointerdown', 'click', 'touchstart', 'touchend', 'keydown', 'scroll'];
    let fallbackActive = true;

    function clearFallback() {
        if (!fallbackActive) return;
        fallbackActive = false;
        interactionEvents.forEach(evt => {
            document.removeEventListener(evt, startOnFirstInteraction);
            window.removeEventListener(evt, startOnFirstInteraction);
        });
    }

    function startOnFirstInteraction(event) {
        if (!fallbackActive) return;
        // The toggle button handles its own logic; ignore gestures on it.
        if (toggleBtn.contains(event.target)) {
            clearFallback();
            return;
        }
        if (audio.paused) {
            playAudio();
        }
        clearFallback();
    }

    interactionEvents.forEach(evt => {
        document.addEventListener(evt, startOnFirstInteraction, { passive: true });
        window.addEventListener(evt, startOnFirstInteraction, { passive: true });
    });

    // Try to play the song as soon as the visitor enters the page.
    // If the browser blocks autoplay, the interaction listeners above
    // will start it on the visitor's first gesture instead.
    try {
        const attempt = audio.play();
        if (attempt && typeof attempt.catch === 'function') {
            attempt.catch(() => { /* will start on first interaction */ });
        }
    } catch (err) {
        /* will start on first interaction */
    }
}

/* ==========================================================================
   4. PHOTO & VIDEO GALLERY FILTER
   ========================================================================== */
function initGallery() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const items = document.querySelectorAll('.gallery-card');

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            const filter = btn.getAttribute('data-filter');

            items.forEach(item => {
                if (filter === 'all') {
                    item.style.display = 'block';
                } else if (filter === 'photos') {
                    item.style.display = item.getAttribute('data-type') === 'photo' ? 'block' : 'none';
                } else if (filter === 'videos') {
                    const type = item.getAttribute('data-type');
                    item.style.display = (type === 'video_file' || type === 'video_embed') ? 'block' : 'none';
                } else {
                    item.style.display = item.classList.contains(filter) ? 'block' : 'none';
                }
            });
        });
    });
}

/* ==========================================================================
   5. VIDEO MODAL & IMAGE LIGHTBOX
   ========================================================================== */
function initModals() {
    // Video Modal
    const videoModal = document.getElementById('videoModal');
    const closeVideo = document.getElementById('closeVideoModal');
    const videoContainer = document.getElementById('videoContainer');
    const videoModalTitle = document.getElementById('videoModalTitle');

    function openVideo(url, isEmbed, title) {
        if (!videoContainer) return;
        videoModalTitle.textContent = title || "Wedding Video";

        if (isEmbed) {
            // YouTube or embed URL formatting
            let embedUrl = url;
            if (url.includes('youtube.com/watch?v=')) {
                const vidId = url.split('v=')[1]?.split('&')[0];
                embedUrl = `https://www.youtube.com/embed/${vidId}?autoplay=1`;
            } else if (url.includes('youtu.be/')) {
                const vidId = url.split('youtu.be/')[1]?.split('?')[0];
                embedUrl = `https://www.youtube.com/embed/${vidId}?autoplay=1`;
            }
            videoContainer.innerHTML = `<iframe src="${embedUrl}" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>`;
        } else {
            videoContainer.innerHTML = `<video controls autoplay playsinline style="width:100%; height:100%;"><source src="${url}" type="video/mp4">Your browser does not support video playback.</video>`;
        }

        videoModal.classList.add('active');
    }

    function closeVideoModalFunc() {
        if (!videoModal) return;
        videoModal.classList.remove('active');
        if (videoContainer) videoContainer.innerHTML = '';
    }

    if (closeVideo) closeVideo.addEventListener('click', closeVideoModalFunc);
    if (videoModal) {
        videoModal.querySelector('.modal-backdrop')?.addEventListener('click', closeVideoModalFunc);
    }

    // Teaser button in Hero
    document.querySelectorAll('.play-video-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const url = btn.getAttribute('data-video-url');
            const title = btn.getAttribute('data-video-title');
            if (url) openVideo(url, true, title);
        });
    });

    // Image Modal with Slideshow Navigation
    const imageModal = document.getElementById('imageModal');
    const closeImage = document.getElementById('closeImageModal');
    const lightboxImage = document.getElementById('lightboxImage');
    const imageModalCaption = document.getElementById('imageModalCaption');
    const lightboxPrev = document.getElementById('lightboxPrev');
    const lightboxNext = document.getElementById('lightboxNext');
    const lightboxCounter = document.getElementById('lightboxCounter');

    // Collect all photo cards into an array for slideshow
    let photoCards = [];
    let currentPhotoIndex = 0;

    function buildPhotoList() {
        photoCards = Array.from(document.querySelectorAll('.gallery-card[data-type="photo"]'));
    }

    function showPhoto(index) {
        if (!photoCards.length) return;
        // Clamp index with wrap-around
        currentPhotoIndex = (index + photoCards.length) % photoCards.length;
        const card = photoCards[currentPhotoIndex];
        const src = card.getAttribute('data-img-src');
        const caption = card.getAttribute('data-caption') || card.getAttribute('data-title') || '';

        // Fade transition
        lightboxImage.style.opacity = '0';
        setTimeout(() => {
            lightboxImage.src = src;
            lightboxImage.onload = () => { lightboxImage.style.opacity = '1'; };
            // Also handle cached images
            if (lightboxImage.complete) lightboxImage.style.opacity = '1';
        }, 150);

        if (imageModalCaption) imageModalCaption.textContent = caption;
        if (lightboxCounter) lightboxCounter.textContent = `${currentPhotoIndex + 1} / ${photoCards.length}`;
    }

    function openImage(startIndex) {
        if (!imageModal) return;
        buildPhotoList();
        imageModal.classList.add('active');
        lightboxImage.style.transition = 'opacity 0.15s ease';
        showPhoto(startIndex);
    }

    function closeImageModalFunc() {
        if (!imageModal) return;
        imageModal.classList.remove('active');
        if (lightboxImage) lightboxImage.src = '';
    }

    if (closeImage) closeImage.addEventListener('click', closeImageModalFunc);
    if (imageModal) {
        imageModal.querySelector('.modal-backdrop')?.addEventListener('click', closeImageModalFunc);
    }

    // Prev / Next buttons
    if (lightboxPrev) lightboxPrev.addEventListener('click', (e) => {
        e.stopPropagation();
        showPhoto(currentPhotoIndex - 1);
    });
    if (lightboxNext) lightboxNext.addEventListener('click', (e) => {
        e.stopPropagation();
        showPhoto(currentPhotoIndex + 1);
    });

    // Gallery cards click
    document.querySelectorAll('.gallery-card').forEach((card, idx) => {
        card.addEventListener('click', () => {
            const type = card.getAttribute('data-type');
            const title = card.getAttribute('data-title');
            const caption = card.getAttribute('data-caption');

            if (type === 'photo') {
                buildPhotoList();
                // Find this card's index among photo cards
                const photoIdx = photoCards.indexOf(card);
                openImage(photoIdx >= 0 ? photoIdx : 0);
            } else if (type === 'video_file') {
                const src = card.getAttribute('data-video-src');
                if (src) openVideo(src, false, title);
            } else if (type === 'video_embed') {
                const embed = card.getAttribute('data-video-embed');
                if (embed) openVideo(embed, true, title);
            }
        });
    });

    // Keyboard arrow navigation
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeVideoModalFunc();
            closeImageModalFunc();
        }
        if (imageModal && imageModal.classList.contains('active')) {
            if (e.key === 'ArrowLeft') showPhoto(currentPhotoIndex - 1);
            if (e.key === 'ArrowRight') showPhoto(currentPhotoIndex + 1);
        }
    });

    // Touch/swipe support for mobile
    let touchStartX = 0;
    if (imageModal) {
        imageModal.addEventListener('touchstart', (e) => { touchStartX = e.changedTouches[0].clientX; }, { passive: true });
        imageModal.addEventListener('touchend', (e) => {
            const diff = touchStartX - e.changedTouches[0].clientX;
            if (Math.abs(diff) > 50) {
                diff > 0 ? showPhoto(currentPhotoIndex + 1) : showPhoto(currentPhotoIndex - 1);
            }
        }, { passive: true });
    }
}

/* ==========================================================================
   6. INTERACTIVE RSVP FORM (AJAX)
   ========================================================================== */
function initCoupleLetter() {
    const openButton = document.getElementById('openCoupleLetter');
    const letterDialog = document.getElementById('coupleLetterDialog');
    const closeButton = document.getElementById('closeCoupleLetter');

    if (!openButton || !letterDialog) return;

    function openLetter() {
        if (typeof letterDialog.showModal === 'function') {
            letterDialog.showModal();
        } else {
            letterDialog.classList.add('letter-dialog-visible');
        }
        closeButton?.focus();
    }

    function closeLetter() {
        if (typeof letterDialog.close === 'function' && letterDialog.open) {
            letterDialog.close();
        }
        letterDialog.classList.remove('letter-dialog-visible');
        openButton.focus();
    }

    openButton.addEventListener('click', openLetter);
    closeButton?.addEventListener('click', closeLetter);
    letterDialog.addEventListener('click', event => {
        if (event.target === letterDialog && letterDialog.classList.contains('letter-dialog-visible')) {
            closeLetter();
        } else if (event.target === letterDialog && typeof letterDialog.close === 'function') {
            letterDialog.close();
        }
    });
    letterDialog.addEventListener('cancel', event => {
        event.preventDefault();
        closeLetter();
    });
}

function initRSVPForm() {
    const form = document.getElementById('rsvpForm');
    const alertBox = document.getElementById('rsvpAlert');
    const submitBtn = document.getElementById('rsvpSubmitBtn');
    const successCard = document.getElementById('rsvpSuccessCard');
    const resetBtn = document.getElementById('resetRsvpBtn');

    if (!form) return;

    // Attendance Radio Pill toggling
    document.querySelectorAll('.attendance-pill').forEach(pill => {
        const radio = pill.querySelector('input[type="radio"]');
        if (radio) {
            radio.addEventListener('change', () => {
                document.querySelectorAll('.attendance-pill').forEach(p => p.classList.remove('active'));
                pill.classList.add('active');

                // If declined, optional: hide events checkboxes
                const eventsGroup = document.getElementById('eventsCheckboxGroup');
                if (eventsGroup) {
                    eventsGroup.style.display = radio.value === 'no' ? 'none' : 'block';
                }
            });
        }
    });

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const guestName = document.getElementById('rsvpName').value.trim();
        const phone = document.getElementById('rsvpPhone').value.trim();
        const email = document.getElementById('rsvpEmail').value.trim();
        const guestCount = document.getElementById('rsvpGuests').value;
        const attending = form.querySelector('input[name="attending"]:checked')?.value || 'yes';
        const notes = document.getElementById('rsvpNotes').value.trim();

        // Collect events
        const selectedEvents = [];
        form.querySelectorAll('input[name="event_choice"]:checked').forEach(cb => {
            selectedEvents.push(cb.value);
        });

        if (!guestName || !phone) {
            showAlert(alertBox, "Please fill in your name and phone number.", "error");
            return;
        }

        // Show spinner
        setBtnLoading(submitBtn, true);
        alertBox.classList.add('hidden');

        const payload = {
            guest_name: guestName,
            phone: phone,
            email: email,
            guest_count: guestCount,
            attending: attending,
            events_attending: selectedEvents.join(', ') || 'All Events',
            notes_or_dietary: notes
        };

        fetch(window.WEDDING_CONFIG.rsvpUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.WEDDING_CONFIG.csrfToken
            },
            body: JSON.stringify(payload)
        })
        .then(res => res.json())
        .then(data => {
            setBtnLoading(submitBtn, false);
            if (data.status === 'success') {
                form.classList.add('hidden');
                if (successCard) {
                    const msgEl = document.getElementById('rsvpSuccessMsg');
                    if (msgEl) msgEl.textContent = data.message;
                    successCard.classList.remove('hidden');
                }
            } else {
                showAlert(alertBox, data.message || "Failed to submit RSVP. Please try again.", "error");
            }
        })
        .catch(() => {
            setBtnLoading(submitBtn, false);
            showAlert(alertBox, "A network error occurred. Please try again or message the family directly.", "error");
        });
    });

    if (resetBtn) {
        resetBtn.addEventListener('click', () => {
            form.reset();
            form.classList.remove('hidden');
            if (successCard) successCard.classList.add('hidden');
            alertBox.classList.add('hidden');
        });
    }
}

/* ==========================================================================
   7. WISHES / GUESTBOOK FORM (AJAX)
   ========================================================================== */
function initWishForm() {
    const form = document.getElementById('wishForm');
    const alertBox = document.getElementById('wishAlert');
    const submitBtn = document.getElementById('wishSubmitBtn');
    const wishesBoard = document.getElementById('wishesBoard');

    if (!form) return;

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        const name = document.getElementById('wishName').value.trim();
        const relation = document.getElementById('wishRelation').value.trim();
        const message = document.getElementById('wishMessage').value.trim();

        if (!name || !message) {
            showAlert(alertBox, "Please provide your name and your blessings message.", "error");
            return;
        }

        setBtnLoading(submitBtn, true);
        alertBox.classList.add('hidden');

        fetch(window.WEDDING_CONFIG.wishUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': window.WEDDING_CONFIG.csrfToken
            },
            body: JSON.stringify({
                name: name,
                relation_or_city: relation,
                message: message
            })
        })
        .then(res => res.json())
        .then(data => {
            setBtnLoading(submitBtn, false);
            if (data.status === 'success') {
                form.reset();
                showAlert(alertBox, "Your blessings have been added to the Wishes Wall! ❤️", "success");

                // Prepend new wish note to the board
                if (wishesBoard && data.wish) {
                    const newCard = document.createElement('div');
                    newCard.className = 'wish-note';
                    newCard.innerHTML = `
                        <div class="wish-quote-icon"><i class="fa-solid fa-quote-left"></i></div>
                        <p class="wish-text">${escapeHtml(data.wish.message)}</p>
                        <div class="wish-footer">
                            <span class="wish-author">${escapeHtml(data.wish.name)}</span>
                            ${data.wish.relation_or_city ? `<span class="wish-meta">&bull; ${escapeHtml(data.wish.relation_or_city)}</span>` : ''}
                            <span class="wish-time">${escapeHtml(data.wish.created_at)}</span>
                        </div>
                    `;
                    wishesBoard.prepend(newCard);
                }
            } else {
                showAlert(alertBox, data.message || "Failed to post message.", "error");
            }
        })
        .catch(() => {
            setBtnLoading(submitBtn, false);
            showAlert(alertBox, "Could not post wish. Please try again.", "error");
        });
    });
}

/* ==========================================================================
   8. AMBIENT GOLDEN FLOATING SPARKLES CANVAS
   ========================================================================== */
function initAmbientCanvas() {
    const canvas = document.getElementById('ambientCanvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let width = canvas.width = window.innerWidth;
    let height = canvas.height = window.innerHeight;

    window.addEventListener('resize', () => {
        width = canvas.width = window.innerWidth;
        height = canvas.height = window.innerHeight;
    });

    const particles = [];
    const count = 28;

    for (let i = 0; i < count; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            radius: Math.random() * 2.2 + 0.8,
            speedY: Math.random() * 0.4 + 0.2,
            speedX: (Math.random() - 0.5) * 0.3,
            opacity: Math.random() * 0.5 + 0.2,
            pulseSpeed: Math.random() * 0.02 + 0.01
        });
    }

    function render() {
        ctx.clearRect(0, 0, width, height);

        for (let p of particles) {
            p.y -= p.speedY;
            p.x += p.speedX;
            p.opacity += Math.sin(Date.now() * 0.002) * 0.005;

            // Reset when leaving top
            if (p.y < -10) {
                p.y = height + 10;
                p.x = Math.random() * width;
            }
            if (p.x < -10) p.x = width + 10;
            if (p.x > width + 10) p.x = -10;

            ctx.beginPath();
            ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(212, 175, 55, ${Math.max(0.1, Math.min(0.6, p.opacity))})`;
            ctx.fill();
        }

        requestAnimationFrame(render);
    }

    render();
}

/* Helper Functions */
function showAlert(box, msg, type) {
    if (!box) return;
    box.className = `form-alert alert-${type}`;
    box.textContent = msg;
    box.classList.remove('hidden');
}

function setBtnLoading(btn, isLoading) {
    if (!btn) return;
    const textSpan = btn.querySelector('.btn-text');
    const spinnerSpan = btn.querySelector('.btn-spinner');

    btn.disabled = isLoading;
    if (isLoading) {
        if (textSpan) textSpan.classList.add('hidden');
        if (spinnerSpan) spinnerSpan.classList.remove('hidden');
    } else {
        if (textSpan) textSpan.classList.remove('hidden');
        if (spinnerSpan) spinnerSpan.classList.add('hidden');
    }
}

function escapeHtml(string) {
    if (!string) return "";
    return String(string).replace(/[&<>"']/g, function (s) {
        return {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#39;'
        }[s];
    });
}

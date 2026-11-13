from django.urls import path
from . import views

app_name = 'invitation'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/rsvp/', views.submit_rsvp, name='submit_rsvp'),
    path('api/wish/', views.submit_wish, name='submit_wish'),
    path('calendar/download/', views.download_ics, name='download_all_calendar'),
    path('calendar/download/<int:event_id>/', views.download_ics, name='download_event_calendar'),
]


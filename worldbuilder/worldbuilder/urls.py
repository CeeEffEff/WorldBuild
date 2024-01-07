from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path("", views.request, name="request"),
    path("about/", views.about, name="about"),
    path("accounts/profile/", views.profile, name="profile"),
    path("dash_map/", views.dash_map, name="dash_map"),
    path("maps/", views.maps, name="maps"),
    path("session_screen_size/", views.session_screen_size, name="session_screen_size")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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
    path("session_screen_size/", views.session_screen_size, name="session_screen_size"),
    path("lists/npc", views.list_npcs, name="list_npcs"),
    path("lists/faction", views.list_factions, name="list_factions"),
    path("lists/map", views.list_maps, name="list_maps"),
    path("lists/point_of_interest", views.list_points_of_interest, name="list_points_of_interest"),
    path("lists/quest", views.list_quests, name="list_quests"),
    path("lists", views.lists, name="lists"),
    path("search/", views.search, name="search"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

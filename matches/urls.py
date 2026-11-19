
from django.urls import path

from . import views

urlpatterns = [
    path("nuova/", views.create_match, name="create_match"),
    path("<uuid:token>/", views.match_detail, name="match_detail"),
]
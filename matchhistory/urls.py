from django.urls import path
from . import views

# Main url.py points paths including 'matchhistory' to this url.py
urlpatterns = [
    path('', views.search_summoner, name='search_summoner'),
    path('<str:summoner_name>/', views.display_match_history, name='display_match_history'),
    # other URL patterns
]
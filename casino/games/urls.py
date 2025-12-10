from django.urls import path
from . import views

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('coin/', views.coin_flip, name='coin_flip'),
    path("guess/", views.guess_number, name="guess_number"),
    path('coin/history/', views.coin_history, name='coin_history'),
    path('slots/', views.slots_game, name='slots'),

    
]

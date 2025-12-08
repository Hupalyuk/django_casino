from django.urls import path
from . import views

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('coin/', views.coin_flip, name='coin_flip'),
    path('coin/history/', views.coin_history, name='coin_history'),
]

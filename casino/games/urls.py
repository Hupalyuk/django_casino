from django.urls import path
from . import views
from .views import slots, update_balance

urlpatterns = [
    path('', views.games_list, name='games_list'),
    path('coin/', views.coin_flip, name='coin_flip'),
    path("guess/", views.guess_number, name="guess_number"),
    path('coin/history/', views.coin_history, name='coin_history'),
    path("slots/", slots, name="slots"),
    path("update-balance/", update_balance, name="update_balance"),
    
]

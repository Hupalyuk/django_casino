from django.shortcuts import render
import random
from django.contrib.auth.decorators import login_required
from .models import CoinFlipResult

def games_list(request):
    games = [
        {"title": "Random Number Game", "url": "/games/random/"},
        {"title": "Coin Flip", "url": "/games/coin/"},
        {"title": "Slots (Demo)", "url": "/games/slots/"},
    ]

    return render(request, "games/games_list.html", {"games": games})

@login_required
def coin_flip(request):
    result = None

    if request.method == "POST":
        result = random.choice(["Орёл", "Решка"])

        # зберігаємо результат у базу
        CoinFlipResult.objects.create(
            user=request.user,
            result=result
        )

    return render(request, "games/coin_flip.html", {"result": result})


@login_required
def coin_history(request):
    history = CoinFlipResult.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "games/coin_history.html", {"history": history})

def games_list(request):
    games = [
        {"title": "Random Number Game", "url": "/games/random/"},
        {"title": "Coin Flip", "url": "/games/coin/"},
        {"title": "Slots (Demo)", "url": "/games/slots/"},
    ]
    return render(request, "games/games_list.html", {"games": games})
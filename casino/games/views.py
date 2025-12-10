from django.shortcuts import render
import random
from django.contrib.auth.decorators import login_required
from .models import CoinFlipResult

def games_list(request):
    return render(request, "games/games_list.html")

from django.http import HttpResponse

def slots(request):
    return render(request, 'games/slots.html')


@login_required
def coin_flip(request):
    result = None
    win = None
    user_choice = None

    if request.method == "POST":
        # Вибір користувача ("Орёл" або "Решка")
        user_choice = request.POST.get("choice")
        
        # Реальний результат
        result = random.choice(["Орёл", "Решка"])

        profile = request.user.profile

        if user_choice == result:
            profile.balance += 100
            win = True
        else:
            profile.balance -= 50
            win = False

        profile.save()

        CoinFlipResult.objects.create(
            user=request.user,
            result=result
        )

    return render(request, "games/coin_flip.html", {
        "result": result,
        "user_choice": user_choice,
        "win": win
    })

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json

@login_required
def update_balance(request):
    data = json.loads(request.body)
    amount = int(data.get("amount", 0))

    profile = request.user.profile
    profile.balance += amount
    profile.save()

    return JsonResponse({"balance": profile.balance})


@login_required
def coin_history(request):
    history = CoinFlipResult.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "games/coin_history.html", {"history": history})

@login_required
def guess_number(request):
    profile = request.user.profile
    initial_balance = profile.balance  # баланс до ставки
    bet_amount = 0
    win_amount = 0
    message = None
    result_number = None
    user_choice = None

    if request.method == "POST":
        try:
            user_choice = int(request.POST.get("number"))
            bet_amount = int(request.POST.get("bet"))
            multiplier = float(request.POST.get("multiplier"))
        except:
            return render(request, "games/guess.html", {
                "error": "Невірні дані!",
                "balance": profile.balance
            })

        if user_choice < 1 or user_choice > 6:
            return render(request, "games/guess.html", {
                "error": "Число повинно бути від 1 до 6!",
                "balance": profile.balance
            })

        if bet_amount > profile.balance:
            return render(request, "games/guess.html", {
                "error": "Недостатньо коштів",
                "balance": profile.balance
            })

        # Віднімаємо ставку від балансу
        profile.balance -= bet_amount

        # Генеруємо випадкове число
        result_number = random.randint(1, 6)

        if user_choice == result_number:
            win_amount = int(bet_amount * multiplier)
            profile.balance += win_amount
            message = f"Ви вгадали! Ви виграли {win_amount} 💰"
        else:
            message = f"Не вгадали! Було число {result_number}. Ви програли {bet_amount} 💸"

        profile.save()

    return render(request, "games/guess.html", {
        "balance": profile.balance,
        "initial_balance": initial_balance,
        "bet_amount": bet_amount,
        "win_amount": win_amount,
        "message": message,
        "result_number": result_number,
        "user_choice": user_choice
    })
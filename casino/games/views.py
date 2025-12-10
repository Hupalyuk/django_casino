from django.shortcuts import render
import random
from django.contrib.auth.decorators import login_required
from .models import CoinFlipResult

def games_list(request):
    games = [
        {"title": "Random Number Game", "url": "/games/guess/"},
        {"title": "Coin Flip", "url": "/games/coin/"},
        {"title": "Slots (Demo)", "url": "/games/slots/"},
    ]

    return render(request, "games/games_list.html", {"games": games})

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



@login_required
def coin_history(request):
    history = CoinFlipResult.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "games/coin_history.html", {"history": history})

@login_required
def guess_number(request):
    message = None
    result_number = None
    win_amount = 0

    if request.method == "POST":
        try:
            user_number = int(request.POST.get("number"))
            bet = int(request.POST.get("bet"))
            multiplier = float(request.POST.get("multiplier"))
        except:
            return render(request, "games/guess.html", {
                "error": "Невірні дані!"
            })

        if user_number < 1 or user_number > 6:
            return render(request, "games/guess.html", {
                "error": "Число повинно бути від 1 до 6!"
            })

        profile = request.user.profile

        if bet > profile.balance:
            return render(request, "games/guess.html", {
                "error": "Недостатньо коштів",
            })

        # знімаємо ставку
        profile.balance -= bet

        # генеруємо число
        result_number = random.randint(1, 6)

        if user_number == result_number:
            win_amount = int(bet * multiplier)
            profile.balance += win_amount
            message = f"Ви вгадали! Ви виграли {win_amount} грн."
        else:
            message = f"Не вгадали! Було число {result_number}."

        profile.save()

    return render(request, "games/guess.html", {
        "message": message,
        "result_number": result_number,
        "win_amount": win_amount
    })
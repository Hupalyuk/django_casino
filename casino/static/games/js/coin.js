const coin = document.getElementById("coin");
const statusEl = document.getElementById("status");
const balanceEl = document.getElementById("balance");
const betInput = document.getElementById("bet");
const flipBtn = document.getElementById("flipBtn");
const choiceBtns = document.querySelectorAll(".choice-btn");

let selectedChoice = null;
let balance = parseInt(balanceEl.textContent);

// Вибір орел/решка
choiceBtns.forEach(btn => {
    btn.addEventListener("click", () => {
        choiceBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        selectedChoice = btn.dataset.choice;
    });
});

// CSRF helper
function getCookie(name){
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if(parts.length === 2) return parts.pop().split(';').shift();
}

// Оновлення балансу через Django
function updateBalance(amount){
    fetch(updateBalanceUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ amount: amount })
    })
    .then(r => r.json())
    .then(data => {
        balance = data.balance;
        balanceEl.textContent = balance;
    });
}

// Клік на кидок монети
flipBtn.addEventListener("click", () => {
    if (!selectedChoice) {
        statusEl.textContent = "Вибери сторону!";
        return;
    }

    let bet = parseInt(betInput.value);
    if (isNaN(bet) || bet < 1) {
        statusEl.textContent = "Введи ставку!";
        return;
    }

    if (bet > balance) {
        statusEl.textContent = "Недостатньо грошей!";
        return;
    }

    statusEl.textContent = "Крутиться...";
    flipBtn.disabled = true;

    // Анімація кидка
    coin.classList.add("flipping");

    // Декілька обертів
    setTimeout(() => {
        coin.classList.remove("flipping");

        // Випадково вибираємо результат
        const result = Math.random() < 0.5 ? "heads" : "tails";
        coin.textContent = result === "heads" ? "🦅" : "🪙";

        // Множник виграшу (можна змінювати)
        const multiplier = 2;

        if (result === selectedChoice) {
            const win = bet * multiplier;
            statusEl.textContent = `Виграш! +$${win}`;
            updateBalance(+win);
        } else {
            statusEl.textContent = `Програш (-$${bet})`;
            updateBalance(-bet);
        }

        flipBtn.disabled = false;
    }, 1000); // Тривалість анімації
});

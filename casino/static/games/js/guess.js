const dice = document.getElementById("dice");
const statusEl = document.getElementById("status");
const balanceEl = document.getElementById("balance");
const betInput = document.getElementById("bet");
const rollBtn = document.getElementById("rollBtn");

let selectedNumber = null;
let balance = parseInt(balanceEl.textContent);

// Створюємо точки кубика
function createDots() {
  dice.innerHTML = "";
  for (let i = 0; i < 9; i++) {
    const d = document.createElement("div");
    d.className = "dot";
    dice.appendChild(d);
  }
}

// Відображення числа на кубику
function showNumber(n) {
  const pattern = {
    1: [4],
    2: [0, 8],
    3: [0, 4, 8],
    4: [0, 2, 6, 8],
    5: [0, 2, 4, 6, 8],
    6: [0, 2, 3, 5, 6, 8]
  };
  createDots();
  const dots = document.querySelectorAll(".dot");
  pattern[n].forEach(i => dots[i].style.opacity = "1");
}

// Вибір числа
document.querySelectorAll(".num").forEach(b => {
  b.addEventListener("click", () => {
    document.querySelectorAll(".num").forEach(x => x.classList.remove("active"));
    b.classList.add("active");
    selectedNumber = parseInt(b.dataset.n);
  });
});

// AJAX для оновлення балансу на сервері
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

// CSRF cookie helper
function getCookie(name){
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if(parts.length === 2) return parts.pop().split(';').shift();
}

// Клік на кидок кубика
rollBtn.addEventListener("click", () => {
  if (!selectedNumber) {
    statusEl.textContent = "Вибери число!";
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
  dice.style.transform = "rotate(0deg)";

  // Анімація кубика (спін)
  let spins = 20;
  let duration = 1500; // 1.5 сек анімації
  let start = Date.now();

  const interval = setInterval(() => {
    const elapsed = Date.now() - start;
    const num = Math.floor(Math.random() * 6) + 1;
    showNumber(num);
    dice.style.transform = `rotate(${elapsed * 0.5}deg)`;
    if (elapsed >= duration) clearInterval(interval);
  }, 50);

  setTimeout(() => {
    const rolled = Math.floor(Math.random() * 6) + 1;
    showNumber(rolled);

    // Множник: можна регулювати
    let multiplier = rolled <= 2 ? 2 : rolled <= 4 ? 4 : 6;

    if (rolled === selectedNumber) {
      let win = bet * multiplier;
      statusEl.textContent = `Виграш! +$${win}`;
      updateBalance(+win);
    } else {
      statusEl.textContent = `Програш (-$${bet})`;
      updateBalance(-bet);
    }
  }, duration + 50);
});

// init
createDots();
showNumber(1);

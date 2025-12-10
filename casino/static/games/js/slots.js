const symbols = ['🍒','🍋','🔔','7️⃣','🍊','🍇','⭐','💎'];
const REELS = 3;
const REPEAT = 20;
const symbolSize = 90;

const reelsEl = document.getElementById('reels');
const btn = document.getElementById('spin');
const msg = document.getElementById('msg');
const balanceEl = document.getElementById('balance');
let balance = parseInt(balanceEl.textContent);
let spinning = false;

// ---- CREATE REELS ----
for (let i = 0; i < REELS; i++) {
    const reel = document.createElement('div'); reel.className = 'reel';
    const windowEl = document.createElement('div'); windowEl.className = 'window';
    const strip = document.createElement('div'); strip.className = 'strip';

    for (let r = 0; r < REPEAT; r++) {
        for (const s of symbols) {
            const el = document.createElement('div');
            el.className = 'symbol';
            el.textContent = s;
            strip.appendChild(el);
        }
    }

    windowEl.appendChild(strip);
    reel.appendChild(windowEl);
    reelsEl.appendChild(reel);
    reel.strip = strip;

    const totalSymbols = symbols.length * REPEAT;
    const midIndex = Math.floor(totalSymbols / 2);
    strip.style.transform = `translateY(${-midIndex * symbolSize}px)`;
}

// ---- SPIN ----
btn.addEventListener('click', () => {
    if (spinning) return;
    spinning = true;
    btn.disabled = true;
    msg.textContent = 'Крутиться...';

    const finalSymbols = [];
    const totalSymbols = symbols.length * REPEAT;
    const midIndex = Math.floor(totalSymbols / 2);
    const spinsFull = 6; // скільки символів крутимо спочатку

    for (let i = 0; i < REELS; i++) {
        const reel = reelsEl.children[i];
        const strip = reel.strip;
        const stopSymbol = Math.floor(Math.random() * symbols.length);
        finalSymbols.push(symbols[stopSymbol]);

        // --- Анімація ---
        const initialOffset = -midIndex * symbolSize;
        const finalOffset = - (midIndex + spinsFull * symbols.length + stopSymbol) * symbolSize;

        // Початковий швидкий спін (імітую багато рядків)
        strip.style.transition = `transform 0.6s cubic-bezier(.15,.9,.2,1)`;
        strip.style.transform = `translateY(${initialOffset - 20*symbolSize}px)`;

        // Потім плавно сповільнюємося до кінцевого символу
        setTimeout(() => {
            strip.style.transition = `transform 2s cubic-bezier(.25,.1,.25,1)`;
            strip.style.transform = `translateY(${finalOffset}px)`;
        }, 600 + i*200); // невеликий зсув для кожного барабана
    }

    // Очікуємо поки всі transition завершаться
    const totalTime = 600 + 2_000 + (REELS - 1) * 200 + 50; // 50ms запас
    setTimeout(() => {
        spinning = false;
        btn.disabled = false;

        const win = finalSymbols.every(s => s === finalSymbols[0]);
        if (win) {
            msg.textContent = `Виграш! 🎉 ${finalSymbols[0]}`;
            balance += 50;
        } else {
            msg.textContent = 'Спробуй ще!';
            balance -= 10;
        }
        balanceEl.textContent = balance;
    }, totalTime);
});

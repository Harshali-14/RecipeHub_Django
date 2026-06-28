// Star rating
function initStarRating(recipeId, userScore) {
  const container = document.getElementById('star-rating');
  if (!container) return;
  const stars = container.querySelectorAll('.star-btn');
  
  function setActive(n) {
    stars.forEach((s, i) => s.classList.toggle('active', i < n));
  }
  setActive(userScore || 0);

  stars.forEach((star, idx) => {
    star.addEventListener('mouseenter', () => setActive(idx + 1));
    star.addEventListener('mouseleave', () => setActive(userScore || 0));
    star.addEventListener('click', async () => {
      const score = idx + 1;
      const res = await fetch(`/recipes/${recipeId}/rate/`, {
        method: 'POST',
        headers: {'Content-Type': 'application/x-www-form-urlencoded', 'X-CSRFToken': getCookie('csrftoken')},
        body: `score=${score}`
      });
      const data = await res.json();
      userScore = score;
      setActive(score);
      document.getElementById('avg-rating').textContent = data.avg || '—';
      document.getElementById('rating-count').textContent = `(${data.count})`;
      showToast('Rating saved!');
    });
  });
}

// Save toggle
async function toggleSave(recipeId) {
  const btn = document.getElementById('save-btn');
  const res = await fetch(`/recipes/${recipeId}/save/`, {
    method: 'POST',
    headers: {'X-CSRFToken': getCookie('csrftoken')}
  });
  const data = await res.json();
  btn.textContent = data.saved ? '🔖' : '🏷️';
  showToast(data.saved ? 'Recipe saved!' : 'Removed from saved');
}

// Servings scaler
function initServingsScaler(baseServings, baseIngredients) {
  let current = baseServings;
  const countEl = document.getElementById('serving-count');
  const ingredientEls = document.querySelectorAll('.ingredient-qty');
  
  function update() {
    if (countEl) countEl.textContent = current;
    const ratio = current / baseServings;
    ingredientEls.forEach((el, i) => {
      const base = parseFloat(el.dataset.base);
      if (!isNaN(base)) {
        const scaled = base * ratio;
        el.textContent = scaled % 1 === 0 ? scaled : scaled.toFixed(1);
      }
    });
  }
  
  document.getElementById('serve-plus')?.addEventListener('click', () => { current++; update(); });
  document.getElementById('serve-minus')?.addEventListener('click', () => { if (current > 1) { current--; update(); } });
}

// Cook timer
let timerInterval = null;
let timerSeconds = 0;

function initTimer(cookMinutes) {
  timerSeconds = cookMinutes * 60;
  updateTimerDisplay();
}

function updateTimerDisplay() {
  const m = Math.floor(timerSeconds / 60).toString().padStart(2, '0');
  const s = (timerSeconds % 60).toString().padStart(2, '0');
  const el = document.getElementById('timer-display');
  if (el) el.textContent = `${m}:${s}`;
}

function startTimer() {
  if (timerInterval) return;
  timerInterval = setInterval(() => {
    if (timerSeconds <= 0) {
      clearInterval(timerInterval);
      timerInterval = null;
      showToast('⏰ Timer done! Check your dish!');
      return;
    }
    timerSeconds--;
    updateTimerDisplay();
  }, 1000);
}

function pauseTimer() {
  clearInterval(timerInterval);
  timerInterval = null;
}

function resetTimer(cookMinutes) {
  pauseTimer();
  timerSeconds = cookMinutes * 60;
  updateTimerDisplay();
}

// Toast
function showToast(msg) {
  const t = document.createElement('div');
  t.textContent = msg;
  t.style.cssText = 'position:fixed;bottom:24px;right:24px;background:#2C2416;color:#fff;padding:0.7rem 1.2rem;border-radius:10px;font-size:0.88rem;z-index:999;box-shadow:0 4px 20px rgba(0,0,0,0.2);animation:fadeIn 0.3s ease';
  document.body.appendChild(t);
  setTimeout(() => t.remove(), 2500);
}

// CSRF
function getCookie(name) {
  let v = null;
  document.cookie.split(';').forEach(c => {
    const [k, val] = c.trim().split('=');
    if (k === name) v = decodeURIComponent(val);
  });
  return v;
}

// Search autocomplete debounce
let searchTimeout;
document.getElementById('search-input')?.addEventListener('input', function() {
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(() => {
    this.closest('form')?.submit();
  }, 600);
});

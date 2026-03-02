// --- Конфигурация ---
const API_URL = '/roll';
const STORAGE_KEY = 'dice_omnissiah_history';
const MAX_HISTORY = 20;

// --- DOM Элементы ---
const input = document.getElementById('diceInput');
const rollBtn = document.getElementById('rollBtn');
const resultValue = document.getElementById('resultValue');
const resultRange = document.getElementById('resultRange');
const errorMsg = document.getElementById('errorMsg');
const historyList = document.getElementById('historyList');
const clearHistoryBtn = document.getElementById('clearHistoryBtn');

// --- Логика Цветовой Дифференциации ---
function getColorForTier(result, min, max) {
    if (min === max) return 'var(--text-primary)';
    
    const range = max - min;
    const third = range / 3;
    const lowThreshold = min + third;
    const highThreshold = min + 2 * third;

    if (result <= lowThreshold) {
        return 'var(--tier-low)';
    } else if (result <= highThreshold) {
        return 'var(--tier-mid)';
    } else {
        return 'var(--tier-high)';
    }
}

// --- Сетевые Запросы ---
async function performRoll(query) {
    rollBtn.disabled = true;
    errorMsg.style.display = 'none';
    resultValue.textContent = '...';
    resultValue.style.color = 'var(--text-secondary)';

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query: query })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.details || data.error || 'Ошибка протокола связи');
        }

        const { result, min, max, query: normalizedQuery } = data;
        
        const color = getColorForTier(result, min, max);
        resultValue.textContent = result;
        resultValue.style.color = color;
        resultRange.textContent = `[${min} : ${max}]`;

        saveToHistory(normalizedQuery, result, min, max);

    } catch (err) {
        console.error('Ошибка броска:', err);
        resultValue.textContent = 'ERR';
        resultRange.textContent = '';
        errorMsg.textContent = err.message;
        errorMsg.style.display = 'block';
    } finally {
        rollBtn.disabled = false;
        input.focus();
    }
}

// --- Управление Историей ---
function saveToHistory(query, result, min, max) {
    let history = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    history = history.filter(item => item.query !== query);
    
    const entry = {
        query: query,
        result: result,
        min: min,
        max: max,
        timestamp: Date.now()
    };
    
    history.unshift(entry);
    
    if (history.length > MAX_HISTORY) {
        history = slice(0, MAX_HISTORY);
    }
    
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
    renderHistory();
}

function clearHistory() {
    if(confirm('Подтвердите очистку кэша памяти. Это действие необратимо.')) {
        localStorage.removeItem(STORAGE_KEY);
        renderHistory();
    }
}

function renderHistory() {
    const history = JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]');
    historyList.innerHTML = '';

    if (history.length === 0) {
        // Можно добавить заглушку, если история пуста
        return;
    }

    history.forEach(item => {
        const el = document.createElement('div');
        el.className = 'history-item';
        
        const date = new Date(item.timestamp);
        const timeStr = date.toLocaleTimeString('ru-RU', { hour: '2-digit', minute: '2-digit' });

        el.innerHTML = `
            <span class="history-query">${escapeHtml(item.query)}</span>
            <span class="history-meta">= ${item.result} <small style="opacity:0.6">[${item.min}-${item.max}] ${timeStr}</small></span>
        `;
        
        el.addEventListener('click', () => {
            input.value = item.query;
            performRoll(item.query);
        });
        
        historyList.appendChild(el);
    });
}

function escapeHtml(text) {
    const map = { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#039;' };
    return text.replace(/[&<>"']/g, m => map[m]);
}

// --- Обработчики Событий ---
function handleRoll() {
    const query = input.value.trim();
    if (query) {
        performRoll(query);
    }
}

rollBtn.addEventListener('click', handleRoll);
clearHistoryBtn.addEventListener('click', clearHistory);

input.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') handleRoll();
});

// --- Инициализация ---
renderHistory();
if (!input.value) input.value = "2d6+3";

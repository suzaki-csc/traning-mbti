/**
 * タイマー機能
 */

let timerInterval = null;
let remainingSeconds = 0;

/**
 * タイマーを開始
 * @param {number} seconds - タイマーの秒数
 * @param {function} onTimeout - 時間切れ時のコールバック
 */
function startTimer(seconds, onTimeout) {
    remainingSeconds = seconds;
    updateTimerDisplay();
    
    // 既存のタイマーをクリア
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    // タイマーを開始
    timerInterval = setInterval(function() {
        remainingSeconds--;
        updateTimerDisplay();
        
        if (remainingSeconds <= 0) {
            clearInterval(timerInterval);
            if (onTimeout) {
                onTimeout();
            }
        }
    }, 1000);
}

/**
 * タイマー表示を更新
 */
function updateTimerDisplay() {
    const display = document.getElementById('timer-display');
    if (display) {
        const minutes = Math.floor(remainingSeconds / 60);
        const seconds = remainingSeconds % 60;
        display.textContent = `${minutes}:${seconds.toString().padStart(2, '0')}`;
        
        // 残り時間が少ない場合は警告色に変更
        if (remainingSeconds <= 10) {
            display.classList.remove('bg-warning');
            display.classList.add('bg-danger');
        } else if (remainingSeconds <= 20) {
            display.classList.remove('bg-danger');
            display.classList.add('bg-warning');
        }
    }
}

/**
 * タイマーを停止
 */
function stopTimer() {
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
}


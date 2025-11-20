/**
 * タイマー機能モジュール
 * 
 * クイズの問題ごとに制限時間を管理し、時間切れの処理を行います。
 */

class QuizTimer {
    constructor(duration, onTimeout, onTick) {
        this.duration = duration; // 制限時間（秒）
        this.remaining = duration; // 残り時間（秒）
        this.onTimeout = onTimeout; // 時間切れ時のコールバック
        this.onTick = onTick; // 1秒ごとのコールバック
        this.intervalId = null;
        this.isRunning = false;
    }
    
    /**
     * タイマーを開始
     */
    start() {
        if (this.isRunning) {
            return;
        }
        
        this.isRunning = true;
        this.intervalId = setInterval(() => {
            this.remaining--;
            
            // 残り時間を更新
            if (this.onTick) {
                this.onTick(this.remaining);
            }
            
            // 時間切れチェック
            if (this.remaining <= 0) {
                this.stop();
                if (this.onTimeout) {
                    this.onTimeout();
                }
            }
        }, 1000);
    }
    
    /**
     * タイマーを停止
     */
    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
        this.isRunning = false;
    }
    
    /**
     * タイマーをリセット
     */
    reset() {
        this.stop();
        this.remaining = this.duration;
    }
    
    /**
     * 残り時間を取得
     */
    getRemaining() {
        return this.remaining;
    }
}

// グローバルにタイマーインスタンスを保持
let quizTimer = null;

/**
 * タイマーを初期化
 */
function initTimer(duration, onTimeout) {
    const timerDisplay = document.getElementById('timer-display');
    const timerBar = document.getElementById('timer-bar');
    const timerProgress = document.getElementById('timer-progress');
    
    // タイマーの更新コールバック
    const onTick = (remaining) => {
        if (timerDisplay) {
            timerDisplay.textContent = remaining;
        }
        
        if (timerBar && timerProgress) {
            const percentage = (remaining / duration) * 100;
            timerBar.style.width = percentage + '%';
            timerBar.setAttribute('aria-valuenow', remaining);
            timerProgress.setAttribute('aria-valuenow', remaining);
            
            // 残り時間が少なくなったら色を変更
            if (remaining <= 5) {
                timerBar.classList.remove('bg-primary', 'bg-warning');
                timerBar.classList.add('bg-danger');
            } else if (remaining <= 10) {
                timerBar.classList.remove('bg-primary', 'bg-danger');
                timerBar.classList.add('bg-warning');
            }
        }
    };
    
    // タイマーインスタンスを作成
    quizTimer = new QuizTimer(duration, onTimeout, onTick);
    
    // タイマーを開始
    quizTimer.start();
    
    return quizTimer;
}

/**
 * タイマーを停止
 */
function stopTimer() {
    if (quizTimer) {
        quizTimer.stop();
    }
}

/**
 * タイマーをリセット
 */
function resetTimer() {
    if (quizTimer) {
        quizTimer.reset();
    }
}


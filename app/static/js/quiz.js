/**
 * クイズアプリ JavaScript
 * クイズのロジック、タイマー、効果音などを制御
 */

// グローバル変数
let currentQuestion = null;
let timerInterval = null;
let timeRemaining = 30;
let soundEnabled = true;

/**
 * ページ読み込み時の初期化
 */
document.addEventListener('DOMContentLoaded', function() {
    // ローカルストレージから効果音設定を読み込み
    const savedSoundSetting = localStorage.getItem('soundEnabled');
    if (savedSoundSetting !== null) {
        soundEnabled = savedSoundSetting === 'true';
    }
    document.getElementById('sound-toggle').checked = soundEnabled;
    
    // 効果音トグルのイベントリスナー
    document.getElementById('sound-toggle').addEventListener('change', function(e) {
        soundEnabled = e.target.checked;
        localStorage.setItem('soundEnabled', soundEnabled);
    });
    
    // キーボードショートカット（1-4キーで選択）
    document.addEventListener('keydown', handleKeyPress);
    
    // 最初の問題を読み込み
    loadCurrentQuestion();
});

/**
 * 現在の問題を読み込む
 */
async function loadCurrentQuestion() {
    try {
        const response = await fetch('/api/question/current');
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        if (data.finished) {
            // クイズ終了
            window.location.href = '/result';
            return;
        }
        
        if (data.error) {
            throw new Error(data.error);
        }
        
        currentQuestion = data;
        displayQuestion(data);
        startTimer();
        
    } catch (error) {
        console.error('問題の読み込みエラー:', error);
        alert('問題の読み込みに失敗しました。ページを再読み込みしてください。');
    }
}

/**
 * 問題を画面に表示
 * @param {Object} data - 問題データ
 */
function displayQuestion(data) {
    // 問題番号と進捗を更新
    document.getElementById('current-number').textContent = data.question_number;
    document.getElementById('total-number').textContent = data.total;
    
    const progress = (data.question_number / data.total) * 100;
    const progressBar = document.getElementById('progress-bar');
    progressBar.style.width = progress + '%';
    progressBar.setAttribute('aria-valuenow', progress);
    
    // 問題文を表示
    document.getElementById('question-text').textContent = data.question_text;
    
    // 選択肢を生成
    const optionsContainer = document.getElementById('options-container');
    optionsContainer.innerHTML = '';
    
    ['A', 'B', 'C', 'D'].forEach((key, index) => {
        const button = document.createElement('button');
        button.className = 'btn btn-outline-primary btn-lg text-start';
        button.setAttribute('data-answer', key);
        button.setAttribute('aria-label', `選択肢${key}: ${data.options[key]}`);
        button.setAttribute('type', 'button');
        button.innerHTML = `<strong>${key}.</strong> ${data.options[key]}`;
        button.innerHTML += ` <span class="badge bg-secondary ms-2">${index + 1}</span>`;
        button.onclick = () => selectAnswer(key);
        
        optionsContainer.appendChild(button);
    });
    
    // 解説カードを非表示
    document.getElementById('explanation-card').classList.add('d-none');
}

/**
 * タイマーを開始
 */
function startTimer() {
    timeRemaining = 30;
    updateTimerDisplay();
    
    // 既存のタイマーをクリア
    if (timerInterval) {
        clearInterval(timerInterval);
    }
    
    timerInterval = setInterval(() => {
        timeRemaining--;
        updateTimerDisplay();
        
        if (timeRemaining <= 0) {
            clearInterval(timerInterval);
            // 時間切れ: 自動的に不正解として次へ
            selectAnswer('');
        }
    }, 1000);
}

/**
 * タイマー表示を更新
 */
function updateTimerDisplay() {
    const timerElement = document.getElementById('timer');
    timerElement.textContent = timeRemaining;
    
    // 残り時間に応じて色を変更
    if (timeRemaining <= 5) {
        timerElement.className = 'badge bg-danger fs-4';
    } else if (timeRemaining <= 10) {
        timerElement.className = 'badge bg-warning fs-4';
    } else {
        timerElement.className = 'badge bg-primary fs-4';
    }
}

/**
 * 回答を選択
 * @param {string} answer - 選択された回答（'A', 'B', 'C', 'D' または空文字）
 */
async function selectAnswer(answer) {
    // タイマーを停止
    if (timerInterval) {
        clearInterval(timerInterval);
        timerInterval = null;
    }
    
    // 選択肢ボタンを無効化
    const buttons = document.querySelectorAll('#options-container button');
    buttons.forEach(btn => btn.disabled = true);
    
    try {
        const response = await fetch('/api/question/answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ answer: answer })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const result = await response.json();
        
        if (result.error) {
            throw new Error(result.error);
        }
        
        displayResult(result, answer);
        
    } catch (error) {
        console.error('回答送信エラー:', error);
        alert('回答の送信に失敗しました。ページを再読み込みしてください。');
    }
}

/**
 * 回答結果を表示
 * @param {Object} result - 回答結果データ
 * @param {string} userAnswer - ユーザーが選択した回答
 */
function displayResult(result, userAnswer) {
    const explanationCard = document.getElementById('explanation-card');
    const resultMessage = document.getElementById('result-message');
    const explanationText = document.getElementById('explanation-text');
    
    // 正解/不正解メッセージ
    if (result.correct) {
        resultMessage.className = 'alert alert-success mb-3';
        resultMessage.innerHTML = '<strong><i class="bi bi-check-circle me-2"></i>正解！</strong>';
        playSound('correct');
    } else {
        resultMessage.className = 'alert alert-danger mb-3';
        const timeUpMessage = userAnswer === '' ? '（時間切れ）' : '';
        resultMessage.innerHTML = `<strong><i class="bi bi-x-circle me-2"></i>不正解${timeUpMessage}</strong><br>正解は <strong>${result.correct_answer}</strong> です。`;
        playSound('incorrect');
    }
    
    // 解説を表示
    explanationText.textContent = result.explanation;
    
    // スコアを更新
    document.getElementById('current-score').textContent = result.score;
    
    // 正解の選択肢をハイライト
    const buttons = document.querySelectorAll('#options-container button');
    buttons.forEach(btn => {
        const answer = btn.getAttribute('data-answer');
        if (answer === result.correct_answer) {
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-success');
        } else if (answer === userAnswer && !result.correct && userAnswer !== '') {
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-danger');
        }
    });
    
    // 解説カードを表示
    explanationCard.classList.remove('d-none');
    
    // スクリーンリーダー用にアナウンス
    resultMessage.setAttribute('aria-live', 'polite');
}

/**
 * 効果音を再生
 * @param {string} type - 音の種類（'correct' または 'incorrect'）
 */
function playSound(type) {
    if (!soundEnabled) return;
    
    const soundId = type === 'correct' ? 'correct-sound' : 'incorrect-sound';
    const audio = document.getElementById(soundId);
    
    if (audio) {
        audio.currentTime = 0;
        audio.play().catch(err => {
            // 効果音の再生に失敗してもエラーを表示しない（ユーザー体験を損なわない）
            console.warn('効果音の再生に失敗しました:', err);
        });
    }
}

/**
 * 次の問題へ
 */
function nextQuestion() {
    // ボタンを再有効化
    const buttons = document.querySelectorAll('#options-container button');
    buttons.forEach(btn => {
        btn.disabled = false;
        btn.className = 'btn btn-outline-primary btn-lg text-start';
    });
    
    // 次の問題を読み込み
    loadCurrentQuestion();
}

/**
 * キーボードショートカット処理
 * @param {KeyboardEvent} event - キーボードイベント
 */
function handleKeyPress(event) {
    // 入力フィールドにフォーカスがある場合は無視
    if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
        return;
    }
    
    // 解説表示中はEnterキーで次へ
    const explanationCard = document.getElementById('explanation-card');
    if (!explanationCard.classList.contains('d-none')) {
        if (event.key === 'Enter') {
            event.preventDefault();
            nextQuestion();
        }
        return;
    }
    
    // 数字キー1-4で選択
    const keyMap = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'};
    if (keyMap[event.key]) {
        event.preventDefault();
        selectAnswer(keyMap[event.key]);
    }
}


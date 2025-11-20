/**
 * 復習モード用JavaScript
 * 
 * 復習モードでのクイズ進行を管理します。
 * quiz.jsとほぼ同じですが、復習モード用のエンドポイントを使用します。
 */

// グローバル変数
let currentQuestionId = null;
let currentQuestionStartTime = null;
let isAnswered = false;

/**
 * ページ読み込み時の初期化
 */
document.addEventListener('DOMContentLoaded', function() {
    // 問題データの取得
    currentQuestionId = questionData.id;
    currentQuestionStartTime = Date.now();
    
    // タイマーの初期化
    initTimer(timerDuration, handleTimeout);
    
    // オーディオマネージャーの初期化
    initAudioManager();
    
    // 選択肢ボタンのイベントリスナーを設定
    setupOptionButtons();
    
    // 次へボタンのイベントリスナーを設定
    setupNextButton();
});

/**
 * 選択肢ボタンのイベントリスナーを設定
 */
function setupOptionButtons() {
    const optionButtons = document.querySelectorAll('.option-btn');
    
    optionButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (isAnswered) {
                return;
            }
            
            const userAnswer = this.getAttribute('data-answer');
            handleAnswer(userAnswer);
        });
        
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !isAnswered) {
                e.preventDefault();
                this.click();
            }
        });
    });
}

/**
 * 回答処理
 */
async function handleAnswer(userAnswer) {
    if (isAnswered) {
        return;
    }
    
    isAnswered = true;
    stopTimer();
    
    const timeTaken = Math.floor((Date.now() - currentQuestionStartTime) / 1000);
    
    const optionButtons = document.querySelectorAll('.option-btn');
    optionButtons.forEach(btn => {
        btn.disabled = true;
        btn.classList.add('disabled');
    });
    
    try {
        const response = await fetch('/review/answer', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                question_id: currentQuestionId,
                answer: userAnswer,
                time_taken: timeTaken
            })
        });
        
        if (!response.ok) {
            throw new Error('回答の送信に失敗しました');
        }
        
        const result = await response.json();
        displayResult(userAnswer, result);
        
        if (result.is_correct) {
            playCorrectSound();
        } else {
            playIncorrectSound();
        }
        
    } catch (error) {
        console.error('エラー:', error);
        alert('回答の送信に失敗しました。ページを再読み込みしてください。');
        isAnswered = false;
    }
}

/**
 * 結果を表示
 */
function displayResult(userAnswer, result) {
    const optionButtons = document.querySelectorAll('.option-btn');
    const explanationBox = document.getElementById('explanation-box');
    const resultTitle = document.getElementById('result-title');
    const explanationText = document.getElementById('explanation-text');
    const nextButtonContainer = document.getElementById('next-button-container');
    
    optionButtons.forEach(btn => {
        const answer = btn.getAttribute('data-answer');
        
        if (answer === result.correct_answer) {
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-success', 'correct');
        } else if (answer === userAnswer && !result.is_correct) {
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-danger', 'incorrect');
        } else {
            btn.classList.add('disabled');
        }
    });
    
    if (explanationBox && resultTitle && explanationText) {
        if (result.is_correct) {
            resultTitle.textContent = '✓ 正解！';
            explanationBox.classList.remove('alert-danger');
            explanationBox.classList.add('alert-success', 'show');
        } else {
            resultTitle.textContent = '✗ 不正解';
            explanationBox.classList.remove('alert-success');
            explanationBox.classList.add('alert-danger', 'show');
        }
        explanationText.textContent = result.explanation;
    }
    
    if (nextButtonContainer) {
        nextButtonContainer.style.display = 'block';
        nextButtonContainer.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
}

/**
 * 次へボタンのイベントリスナーを設定
 */
function setupNextButton() {
    const nextButton = document.getElementById('next-button');
    
    if (nextButton) {
        nextButton.addEventListener('click', async function() {
            try {
                const response = await fetch('/review/next');
                
                if (!response.ok) {
                    throw new Error('次の問題の取得に失敗しました');
                }
                
                const data = await response.json();
                
                if (data.finished) {
                    window.location.href = data.redirect_url;
                } else {
                    window.location.reload();
                }
            } catch (error) {
                console.error('エラー:', error);
                alert('次の問題の取得に失敗しました。ページを再読み込みしてください。');
            }
        });
    }
}

/**
 * 時間切れ処理
 */
function handleTimeout() {
    if (isAnswered) {
        return;
    }
    
    const firstButton = document.querySelector('.option-btn');
    if (firstButton) {
        handleAnswer('A');
    }
}


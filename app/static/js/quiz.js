/**
 * クイズ機能
 */

// グローバル変数
let currentQuestionNum = 0;
let isReviewMode = false;

/**
 * 回答ボタンのイベントリスナーを設定
 */
document.addEventListener('DOMContentLoaded', function() {
    const answerButtons = document.querySelectorAll('.answer-btn');
    
    answerButtons.forEach(function(button) {
        button.addEventListener('click', function() {
            const answer = parseInt(this.getAttribute('data-answer'));
            handleAnswer(answer);
        });
    });
    
    // キーボード操作対応（アクセシビリティ）
    document.addEventListener('keydown', function(event) {
        if (event.key >= '1' && event.key <= '4') {
            const answer = parseInt(event.key);
            const button = document.querySelector(`.answer-btn[data-answer="${answer}"]`);
            if (button && !button.disabled) {
                button.click();
            }
        }
    });
});

/**
 * 回答を処理
 * @param {number} answer - 選択した回答（1-4）
 */
function handleAnswer(answer) {
    // すべてのボタンを無効化
    const buttons = document.querySelectorAll('.answer-btn');
    buttons.forEach(function(btn) {
        btn.disabled = true;
    });
    
    // タイマーを停止
    if (typeof stopTimer === 'function') {
        stopTimer();
    }
    
    // 回答をサーバーに送信
    const categoryId = quizConfig.categoryId;
    const questionNum = quizConfig.questionNum;
    
    fetch(`/quiz/${categoryId}/answer`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            question_num: questionNum,
            answer: answer
        })
    })
    .then(response => response.json())
    .then(data => {
        // 正解/不正解の視覚的フィードバック
        const selectedButton = document.querySelector(`.answer-btn[data-answer="${answer}"]`);
        const correctButton = document.querySelector(`.answer-btn[data-answer="${data.correct_answer}"]`);
        
        if (data.correct) {
            selectedButton.classList.remove('btn-outline-primary');
            selectedButton.classList.add('btn-success');
            if (typeof playSound === 'function') {
                playSound('correct');
            }
        } else {
            selectedButton.classList.remove('btn-outline-primary');
            selectedButton.classList.add('btn-danger');
            if (correctButton) {
                correctButton.classList.remove('btn-outline-primary');
                correctButton.classList.add('btn-success');
            }
            if (typeof playSound === 'function') {
                playSound('incorrect');
            }
        }
        
        // 進捗バーを更新
        updateProgressBar(questionNum, data.correct);
        
        // 少し待ってから解説ページへ遷移
        setTimeout(function() {
            if (isReviewMode) {
                // 復習モードの場合は別の処理
                window.location.href = `/quiz/${categoryId}/review/explanation/${questionNum}`;
            } else {
                window.location.href = `/quiz/${categoryId}/explanation/${questionNum}`;
            }
        }, 1500);
    })
    .catch(error => {
        console.error('Error:', error);
        alert('エラーが発生しました。ページを再読み込みしてください。');
    });
}

/**
 * 進捗バーを更新
 * @param {number} questionNum - 問題番号
 * @param {boolean} isCorrect - 正解かどうか
 */
function updateProgressBar(questionNum, isCorrect) {
    const progressItem = document.querySelectorAll('.progress-item')[questionNum];
    if (progressItem) {
        progressItem.classList.remove('pending', 'current');
        progressItem.classList.add(isCorrect ? 'correct' : 'incorrect');
    }
}


/**
 * クイズアプリケーションのメインロジック
 */

class QuizApp {
    constructor(sessionKey, totalQuestions, timerSeconds, soundEnabled) {
        this.sessionKey = sessionKey;
        this.totalQuestions = totalQuestions;
        this.timerSeconds = timerSeconds;
        this.soundEnabled = soundEnabled;
        this.currentQuestion = 1;
        this.currentQuestionId = null;  // 現在の問題ID
        this.timer = null;
        this.selectedChoiceId = null;
    }

    async init() {
        await this.loadQuestion(this.currentQuestion);
        this.setupEventListeners();
    }

    async loadQuestion(questionNumber) {
        try {
            const response = await fetch(`/api/quiz/${this.sessionKey}/question/${questionNumber}`);
            if (!response.ok) throw new Error('問題の読み込みに失敗しました');
            
            const data = await response.json();
            this.displayQuestion(data);
            
            if (this.timerSeconds > 0) {
                this.startTimer();
            }
        } catch (error) {
            console.error(error);
            alert('エラーが発生しました: ' + error.message);
        }
    }

    displayQuestion(data) {
        // 現在の問題IDを保存
        this.currentQuestionId = data.question_id;
        
        // 問題番号と進捗を更新
        document.getElementById('current-question').textContent = data.question_number;
        document.getElementById('question-number').textContent = data.question_number;
        document.getElementById('question-text').textContent = data.question_text;
        
        const progress = (data.question_number / data.total_questions) * 100;
        const progressBar = document.getElementById('progress-bar');
        progressBar.style.width = progress + '%';
        progressBar.setAttribute('aria-valuenow', progress);
        
        // 選択肢を表示
        const choicesContainer = document.getElementById('choices-container');
        choicesContainer.innerHTML = '';
        
        data.choices.forEach((choice, index) => {
            const div = document.createElement('div');
            div.className = 'form-check choice-option';
            div.innerHTML = `
                <input class="form-check-input" type="radio" name="choice" 
                       id="choice-${choice.choice_id}" value="${choice.choice_id}"
                       aria-describedby="choice-text-${choice.choice_id}">
                <label class="form-check-label w-100" for="choice-${choice.choice_id}" 
                       id="choice-text-${choice.choice_id}">
                    ${choice.choice_text}
                </label>
            `;
            choicesContainer.appendChild(div);
        });
        
        // 解説エリアをリセット
        document.getElementById('explanation-area').classList.add('d-none');
        document.getElementById('submit-btn').disabled = true;
        this.selectedChoiceId = null;
        
        // フォーカスを問題タイトルに移動
        document.getElementById('question-title').focus();
        announceToScreenReader(`問題${data.question_number}を読み込みました`);
    }

    setupEventListeners() {
        // 選択肢の選択
        document.addEventListener('change', (e) => {
            if (e.target.name === 'choice') {
                this.selectedChoiceId = parseInt(e.target.value);
                document.getElementById('submit-btn').disabled = false;
            }
        });
        
        // 回答ボタン
        document.getElementById('submit-btn').addEventListener('click', () => {
            this.submitAnswer();
        });
        
        // 次の問題ボタン
        document.getElementById('next-btn').addEventListener('click', () => {
            this.nextQuestion();
        });
        
        // 結果を見るボタン
        document.getElementById('finish-btn').addEventListener('click', () => {
            this.finishQuiz();
        });
    }

    startTimer() {
        let remaining = this.timerSeconds;
        const timerDisplay = document.getElementById('timer-display');
        
        const updateTimer = () => {
            const minutes = Math.floor(remaining / 60);
            const seconds = remaining % 60;
            timerDisplay.innerHTML = `
                <i class="bi bi-clock"></i> 
                残り ${minutes}:${seconds.toString().padStart(2, '0')}
            `;
            
            if (remaining <= 10) {
                timerDisplay.classList.add('text-danger');
            }
            
            if (remaining <= 0) {
                clearInterval(this.timer);
                this.timeoutAnswer();
            }
            
            remaining--;
        };
        
        updateTimer();
        this.timer = setInterval(updateTimer, 1000);
    }

    stopTimer() {
        if (this.timer) {
            clearInterval(this.timer);
            this.timer = null;
        }
    }

    async submitAnswer() {
        this.stopTimer();
        
        if (!this.selectedChoiceId) {
            alert('選択肢を選んでください');
            return;
        }
        
        if (!this.currentQuestionId) {
            alert('問題データが読み込まれていません');
            return;
        }
        
        const submitBtn = document.getElementById('submit-btn');
        submitBtn.disabled = true;
        
        try {
            const response = await fetch(`/api/quiz/${this.sessionKey}/answer`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question_id: this.currentQuestionId,
                    choice_id: this.selectedChoiceId,
                    time_spent_seconds: this.timerSeconds
                })
            });
            
            if (!response.ok) throw new Error('回答の送信に失敗しました');
            
            const data = await response.json();
            this.showResult(data);
        } catch (error) {
            console.error(error);
            alert('エラーが発生しました: ' + error.message);
            submitBtn.disabled = false;
        }
    }

    async timeoutAnswer() {
        announceToScreenReader('時間切れです');
        
        if (!this.currentQuestionId) {
            console.error('問題IDが見つかりません');
            return;
        }
        
        try {
            const response = await fetch(`/api/quiz/${this.sessionKey}/answer`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    question_id: this.currentQuestionId,
                    choice_id: null,
                    time_spent_seconds: this.timerSeconds
                })
            });
            
            if (!response.ok) throw new Error('回答の送信に失敗しました');
            
            const data = await response.json();
            this.showResult(data, true);
        } catch (error) {
            console.error(error);
            alert('エラーが発生しました: ' + error.message);
        }
    }

    showResult(data, isTimeout = false) {
        const resultBadge = document.getElementById('result-badge');
        const explanationArea = document.getElementById('explanation-area');
        const explanationText = document.getElementById('explanation-text');
        
        if (data.is_correct) {
            resultBadge.innerHTML = '<div class="alert alert-success"><i class="bi bi-check-circle-fill"></i> <strong>正解です！</strong></div>';
            announceToScreenReader('正解です');
            if (this.soundEnabled) this.playSound('correct');
        } else {
            if (isTimeout) {
                resultBadge.innerHTML = '<div class="alert alert-danger"><i class="bi bi-clock-history"></i> <strong>時間切れ</strong></div>';
                announceToScreenReader('時間切れです');
            } else {
                resultBadge.innerHTML = '<div class="alert alert-danger"><i class="bi bi-x-circle-fill"></i> <strong>不正解です</strong></div>';
                announceToScreenReader('不正解です');
            }
            if (this.soundEnabled) this.playSound('incorrect');
        }
        
        explanationText.textContent = data.explanation;
        explanationArea.classList.remove('d-none');
        
        // ボタンの表示切り替え
        document.getElementById('submit-btn').classList.add('d-none');
        
        if (this.currentQuestion < this.totalQuestions) {
            document.getElementById('next-btn').classList.remove('d-none');
        } else {
            document.getElementById('finish-btn').classList.remove('d-none');
        }
    }

    nextQuestion() {
        this.currentQuestion++;
        
        // ボタンをリセット
        document.getElementById('next-btn').classList.add('d-none');
        document.getElementById('submit-btn').classList.remove('d-none');
        
        this.loadQuestion(this.currentQuestion);
    }

    async finishQuiz() {
        try {
            const response = await fetch(`/api/quiz/${this.sessionKey}/complete`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (!response.ok) throw new Error('クイズの完了処理に失敗しました');
            
            const data = await response.json();
            window.location.href = data.result_url;
        } catch (error) {
            console.error(error);
            alert('エラーが発生しました: ' + error.message);
        }
    }

    getCurrentQuestionId() {
        // 現在の問題IDを返す
        return this.currentQuestionId;
    }

    playSound(type) {
        try {
            const audio = new Audio(`/static/sounds/${type}.mp3`);
            audio.play().catch(e => console.log('音声再生エラー:', e));
        } catch (error) {
            console.log('音声ファイルが見つかりません');
        }
    }
}

// スクリーンリーダー用の通知関数
function announceToScreenReader(message) {
    const announcer = document.getElementById('sr-announce');
    if (announcer) {
        announcer.textContent = message;
        setTimeout(() => {
            announcer.textContent = '';
        }, 1000);
    }
}


# クイズアプリ設計書

## 概要

セキュリティ、IT基礎、プログラミングなどの技術用語を学習できる4択クイズアプリケーションです。
Python/Flask/Bootstrapを使用したWebアプリケーションとして実装します。

## 主要機能

### 1. カテゴリ選択
- 初期カテゴリ: 「セキュリティ」「IT基礎」「プログラミング」
- ユーザーは開始前にカテゴリを選択可能
- 各カテゴリに最大20問の問題プールを保持

### 2. クイズ出題
- 4択形式
- 問題プールからランダムに10問を出題
- 出題順序はシャッフル
- 問題数が10問以下の場合は重複出題を許可

### 3. タイマー機能
- 1問あたり30秒（設定変更可能）
- タイマー表示は視覚的にわかりやすく
- 時間切れで次の問題へ自動遷移

### 4. 効果音
- 正解時・不正解時で異なる効果音
- ON/OFF切り替え可能
- ローカルストレージで設定を保存

### 5. 解説表示
- 各問題の正解後に解説を日本語で表示
- 大学3年生向けのやさしい記述

### 6. 結果表示
- 最終スコア（正答率）
- 間違えた問題の一覧
- 復習リスト

### 7. 復習モード
- 間違えた問題のみを再度出題
- 通常モードと同じUI

### 8. スコア共有
- スコア文字列をクリップボードにコピー
- SNS共有用フォーマット

## アクセシビリティ配慮

- セマンティックHTML（`<main>`, `<nav>`, `<button>`等）の使用
- キーボード操作対応（Tab、Enter、数字キー1-4で選択）
- 十分なコントラスト比（WCAG AA基準）
- `aria-label`や`aria-live`属性の適切な使用
- フォントサイズ調整機能
- 色だけに依存しない情報伝達（アイコンとテキストの併用）

## システム構成

```
quiz-app/
├── app.py                  # メインアプリケーション
├── models.py               # データベースモデル
├── config.py               # 設定ファイル
├── requirements.txt        # 依存関係（poetryの場合はpyproject.toml）
├── static/
│   ├── css/
│   │   └── style.css      # カスタムスタイル
│   ├── js/
│   │   └── quiz.js        # クイズロジック
│   └── sounds/
│       ├── correct.mp3    # 正解音
│       └── incorrect.mp3  # 不正解音
├── templates/
│   ├── base.html          # ベーステンプレート
│   ├── index.html         # トップページ
│   ├── category.html      # カテゴリ選択
│   ├── quiz.html          # クイズ画面
│   ├── result.html        # 結果画面
│   └── review.html        # 復習モード
└── data/
    └── init_questions.py  # 初期問題データ
```

## データベース設計

### Categoryテーブル
```sql
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Questionテーブル
```sql
CREATE TABLE question (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    option_a VARCHAR(200) NOT NULL,
    option_b VARCHAR(200) NOT NULL,
    option_c VARCHAR(200) NOT NULL,
    option_d VARCHAR(200) NOT NULL,
    correct_answer CHAR(1) NOT NULL, -- 'A', 'B', 'C', 'D'
    explanation TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);
```

### QuizSessionテーブル（オプション: 履歴保存用）
```sql
CREATE TABLE quiz_session (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category_id INTEGER NOT NULL,
    score INTEGER NOT NULL,
    total_questions INTEGER NOT NULL,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES category(id)
);
```

## 主要コード例

### app.py（メインアプリケーション）

```python
from flask import Flask, render_template, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random
import os

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///quiz.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# トップページ: カテゴリ一覧を表示
@app.route('/')
def index():
    """
    トップページを表示
    利用可能なカテゴリ一覧を取得して表示
    """
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

# カテゴリ選択
@app.route('/category/<int:category_id>')
def select_category(category_id):
    """
    選択されたカテゴリのクイズを開始
    
    Args:
        category_id: カテゴリID
    
    Returns:
        クイズ画面またはエラーページ
    """
    category = Category.query.get_or_404(category_id)
    
    # カテゴリに属する全問題を取得
    all_questions = Question.query.filter_by(category_id=category_id).all()
    
    # 問題数の確認
    if len(all_questions) == 0:
        return render_template('error.html', 
                             message='この問題カテゴリには問題が登録されていません。')
    
    # ランダムに10問選択（重複を許可）
    if len(all_questions) <= 10:
        # 10問以下の場合は重複を許可して10問にする
        selected_questions = random.choices(all_questions, k=10)
    else:
        # 10問以上の場合は重複なしで10問選択
        selected_questions = random.sample(all_questions, 10)
    
    # 順番をシャッフル
    random.shuffle(selected_questions)
    
    # セッションに問題IDリストを保存
    session['question_ids'] = [q.id for q in selected_questions]
    session['current_index'] = 0
    session['score'] = 0
    session['wrong_questions'] = []
    session['category_id'] = category_id
    
    return render_template('quiz.html', 
                         category=category,
                         total_questions=len(selected_questions))

# クイズAPI: 現在の問題を取得
@app.route('/api/question/current')
def get_current_question():
    """
    現在の問題を取得するAPI
    
    Returns:
        JSON: 問題データ（問題文、選択肢）
    """
    question_ids = session.get('question_ids', [])
    current_index = session.get('current_index', 0)
    
    if current_index >= len(question_ids):
        return jsonify({'finished': True})
    
    question_id = question_ids[current_index]
    question = Question.query.get(question_id)
    
    return jsonify({
        'finished': False,
        'question_number': current_index + 1,
        'total': len(question_ids),
        'question_text': question.question_text,
        'options': {
            'A': question.option_a,
            'B': question.option_b,
            'C': question.option_c,
            'D': question.option_d
        }
    })

# クイズAPI: 回答を送信
@app.route('/api/question/answer', methods=['POST'])
def submit_answer():
    """
    ユーザーの回答を受け取り、正誤判定を行う
    
    Request Body:
        answer: 選択された回答（A, B, C, D）
    
    Returns:
        JSON: 正誤結果と解説
    """
    data = request.get_json()
    user_answer = data.get('answer', '').upper()
    
    question_ids = session.get('question_ids', [])
    current_index = session.get('current_index', 0)
    
    if current_index >= len(question_ids):
        return jsonify({'error': 'Invalid question index'}), 400
    
    question_id = question_ids[current_index]
    question = Question.query.get(question_id)
    
    # 正誤判定
    is_correct = (user_answer == question.correct_answer)
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    else:
        # 間違えた問題を記録
        wrong_questions = session.get('wrong_questions', [])
        wrong_questions.append(question_id)
        session['wrong_questions'] = wrong_questions
    
    # 次の問題へ
    session['current_index'] = current_index + 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'score': session.get('score', 0)
    })

# 結果表示
@app.route('/result')
def show_result():
    """
    クイズ終了後の結果を表示
    スコアと間違えた問題の一覧を表示
    """
    score = session.get('score', 0)
    question_ids = session.get('question_ids', [])
    wrong_question_ids = session.get('wrong_questions', [])
    category_id = session.get('category_id')
    
    category = Category.query.get(category_id)
    total = len(question_ids)
    percentage = int((score / total) * 100) if total > 0 else 0
    
    # 間違えた問題の詳細を取得
    wrong_questions = Question.query.filter(
        Question.id.in_(wrong_question_ids)
    ).all() if wrong_question_ids else []
    
    # スコア共有用テキスト生成
    share_text = f"クイズ「{category.name}」の結果: {score}/{total}問正解 ({percentage}%) #クイズアプリ"
    
    return render_template('result.html',
                         category=category,
                         score=score,
                         total=total,
                         percentage=percentage,
                         wrong_questions=wrong_questions,
                         share_text=share_text)

# 復習モード
@app.route('/review')
def review_mode():
    """
    間違えた問題のみを復習するモード
    """
    wrong_question_ids = session.get('wrong_questions', [])
    
    if not wrong_question_ids:
        return render_template('error.html', 
                             message='復習する問題がありません。')
    
    # 復習用セッションを設定
    random.shuffle(wrong_question_ids)
    session['question_ids'] = wrong_question_ids
    session['current_index'] = 0
    session['score'] = 0
    session['is_review_mode'] = True
    
    category_id = session.get('category_id')
    category = Category.query.get(category_id)
    
    return render_template('quiz.html',
                         category=category,
                         total_questions=len(wrong_question_ids),
                         is_review=True)

if __name__ == '__main__':
    app.run(debug=True)
```

### models.py（データベースモデル）

```python
from app import db
from datetime import datetime

class Category(db.Model):
    """
    クイズのカテゴリを管理するモデル
    """
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーション: このカテゴリに属する問題
    questions = db.relationship('Question', backref='category', lazy=True)
    
    def __repr__(self):
        return f'<Category {self.name}>'

class Question(db.Model):
    """
    クイズの問題を管理するモデル
    """
    __tablename__ = 'question'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(200), nullable=False)
    option_b = db.Column(db.String(200), nullable=False)
    option_c = db.Column(db.String(200), nullable=False)
    option_d = db.Column(db.String(200), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)  # 'A', 'B', 'C', 'D'
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Question {self.id}: {self.question_text[:30]}...>'

class QuizSession(db.Model):
    """
    クイズセッションの履歴を保存するモデル（オプション）
    """
    __tablename__ = 'quiz_session'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    completed_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QuizSession {self.id}: {self.score}/{self.total_questions}>'
```

### templates/quiz.html（クイズ画面）

```html
{% extends "base.html" %}

{% block title %}クイズ - {{ category.name }}{% endblock %}

{% block content %}
<main class="container mt-5" role="main">
    <div class="row justify-content-center">
        <div class="col-lg-8">
            <!-- 進捗表示 -->
            <div class="mb-4">
                <div class="d-flex justify-content-between mb-2">
                    <span id="question-counter" aria-live="polite">
                        問題 <span id="current-number">1</span> / <span id="total-number">{{ total_questions }}</span>
                    </span>
                    <span id="score-display" aria-live="polite">
                        スコア: <span id="current-score">0</span>
                    </span>
                </div>
                <div class="progress" style="height: 10px;">
                    <div id="progress-bar" class="progress-bar" role="progressbar" 
                         style="width: 0%;" aria-valuenow="0" 
                         aria-valuemin="0" aria-valuemax="100">
                    </div>
                </div>
            </div>

            <!-- タイマー表示 -->
            <div class="card mb-3 text-center">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">残り時間</h5>
                        <div>
                            <span id="timer" class="badge bg-primary fs-4" aria-live="polite">30</span>
                            <span class="ms-2">秒</span>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 問題カード -->
            <div class="card shadow-sm">
                <div class="card-body">
                    <h2 id="question-text" class="card-title mb-4" aria-live="polite">
                        <!-- 問題文がJavaScriptで挿入されます -->
                    </h2>
                    
                    <!-- 選択肢 -->
                    <div id="options-container" class="d-grid gap-2">
                        <!-- 選択肢がJavaScriptで挿入されます -->
                    </div>
                </div>
            </div>

            <!-- 解説表示エリア（正解後に表示） -->
            <div id="explanation-card" class="card mt-3 d-none">
                <div class="card-body">
                    <div id="result-message" class="alert mb-3" role="alert">
                        <!-- 正解/不正解メッセージ -->
                    </div>
                    <h5 class="card-title">解説</h5>
                    <p id="explanation-text" class="card-text">
                        <!-- 解説文 -->
                    </p>
                    <button id="next-button" class="btn btn-primary w-100" onclick="nextQuestion()">
                        次の問題へ
                    </button>
                </div>
            </div>

            <!-- 設定パネル -->
            <div class="card mt-3">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <label for="sound-toggle" class="form-label mb-0">効果音</label>
                        <div class="form-check form-switch">
                            <input class="form-check-input" type="checkbox" 
                                   id="sound-toggle" checked 
                                   aria-label="効果音のオン・オフを切り替え">
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</main>

<!-- 効果音 -->
<audio id="correct-sound" preload="auto">
    <source src="{{ url_for('static', filename='sounds/correct.mp3') }}" type="audio/mpeg">
</audio>
<audio id="incorrect-sound" preload="auto">
    <source src="{{ url_for('static', filename='sounds/incorrect.mp3') }}" type="audio/mpeg">
</audio>

<script src="{{ url_for('static', filename='js/quiz.js') }}"></script>
{% endblock %}
```

### static/js/quiz.js（クイズロジック）

```javascript
// グローバル変数
let currentQuestion = null;
let timerInterval = null;
let timeRemaining = 30;
let soundEnabled = true;

// ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', function() {
    // ローカルストレージから効果音設定を読み込み
    soundEnabled = localStorage.getItem('soundEnabled') !== 'false';
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
        const data = await response.json();
        
        if (data.finished) {
            // クイズ終了
            window.location.href = '/result';
            return;
        }
        
        currentQuestion = data;
        displayQuestion(data);
        startTimer();
        
    } catch (error) {
        console.error('問題の読み込みエラー:', error);
        alert('問題の読み込みに失敗しました。');
    }
}

/**
 * 問題を画面に表示
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
        button.innerHTML = `<strong>${key}.</strong> ${data.options[key]}`;
        button.onclick = () => selectAnswer(key);
        
        // キーボードショートカット表示
        button.innerHTML += ` <span class="badge bg-secondary ms-2">${index + 1}</span>`;
        
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
 */
async function selectAnswer(answer) {
    // タイマーを停止
    clearInterval(timerInterval);
    
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
        
        const result = await response.json();
        displayResult(result, answer);
        
    } catch (error) {
        console.error('回答送信エラー:', error);
        alert('回答の送信に失敗しました。');
    }
}

/**
 * 回答結果を表示
 */
function displayResult(result, userAnswer) {
    const explanationCard = document.getElementById('explanation-card');
    const resultMessage = document.getElementById('result-message');
    const explanationText = document.getElementById('explanation-text');
    
    // 正解/不正解メッセージ
    if (result.correct) {
        resultMessage.className = 'alert alert-success mb-3';
        resultMessage.innerHTML = '<strong>✓ 正解！</strong>';
        playSound('correct');
    } else {
        resultMessage.className = 'alert alert-danger mb-3';
        resultMessage.innerHTML = `<strong>✗ 不正解</strong><br>正解は <strong>${result.correct_answer}</strong> です。`;
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
        } else if (answer === userAnswer && !result.correct) {
            btn.classList.remove('btn-outline-primary');
            btn.classList.add('btn-danger');
        }
    });
    
    // 解説カードを表示
    explanationCard.classList.remove('d-none');
}

/**
 * 効果音を再生
 */
function playSound(type) {
    if (!soundEnabled) return;
    
    const soundId = type === 'correct' ? 'correct-sound' : 'incorrect-sound';
    const audio = document.getElementById(soundId);
    
    if (audio) {
        audio.currentTime = 0;
        audio.play().catch(err => {
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
 */
function handleKeyPress(event) {
    // 解説表示中は無視
    if (!document.getElementById('explanation-card').classList.contains('d-none')) {
        if (event.key === 'Enter') {
            nextQuestion();
        }
        return;
    }
    
    // 数字キー1-4で選択
    const keyMap = {'1': 'A', '2': 'B', '3': 'C', '4': 'D'};
    if (keyMap[event.key]) {
        selectAnswer(keyMap[event.key]);
    }
}
```

## 初期データ

### data/init_questions.py（セキュリティカテゴリの問題例）

```python
"""
初期問題データを登録するスクリプト
セキュリティカテゴリの問題20問を登録
"""
from app import app, db
from models import Category, Question

def init_security_questions():
    """セキュリティカテゴリの問題を登録"""
    
    # カテゴリを作成
    security_cat = Category(
        name='セキュリティ',
        description='情報セキュリティに関する基礎的な用語と概念を学習します'
    )
    db.session.add(security_cat)
    db.session.commit()
    
    # 問題リスト
    questions = [
        {
            'question_text': 'XSS（クロスサイトスクリプティング）とは何ですか？',
            'option_a': 'データベースに不正なSQLを送信する攻撃',
            'option_b': 'Webサイトに悪意のあるスクリプトを埋め込む攻撃',
            'option_c': 'パスワードを総当たりで解読する攻撃',
            'option_d': 'ネットワーク通信を傍受する攻撃',
            'correct_answer': 'B',
            'explanation': 'XSSは、攻撃者が悪意のあるスクリプト（主にJavaScript）をWebページに埋め込み、他のユーザーのブラウザで実行させる攻撃です。これにより、セッション情報の盗取やフィッシングなどが可能になります。'
        },
        {
            'question_text': 'SQLインジェクションを防ぐ最も効果的な方法は？',
            'option_a': 'ファイアウォールを導入する',
            'option_b': 'パスワードを複雑にする',
            'option_c': 'プリペアドステートメントを使用する',
            'option_d': 'HTTPSを使用する',
            'correct_answer': 'C',
            'explanation': 'プリペアドステートメント（パラメータ化クエリ）を使用することで、SQLとデータを分離し、SQLインジェクション攻撃を防ぐことができます。これは最も基本的で効果的な対策方法です。'
        },
        {
            'question_text': 'CSRF（クロスサイトリクエストフォージェリ）攻撃の説明として正しいものは？',
            'option_a': 'ユーザーの意図しない操作を強制的に実行させる攻撃',
            'option_b': 'パスワードを盗み取る攻撃',
            'option_c': 'ウイルスをダウンロードさせる攻撃',
            'option_d': 'ネットワークを過負荷にする攻撃',
            'correct_answer': 'A',
            'explanation': 'CSRFは、ログイン中のユーザーに対して、本人の意図しない送金や設定変更などの操作を強制的に実行させる攻撃です。CSRFトークンを使用することで防ぐことができます。'
        },
        {
            'question_text': 'パスワードリスト攻撃とは何ですか？',
            'option_a': '辞書にある単語を順番に試す攻撃',
            'option_b': '他サイトから流出したID/パスワードを使い回す攻撃',
            'option_c': 'ランダムな文字列を総当たりで試す攻撃',
            'option_d': 'パスワード管理ソフトを攻撃する手法',
            'correct_answer': 'B',
            'explanation': 'パスワードリスト攻撃は、他のサービスから流出したIDとパスワードのリストを使って不正ログインを試みる攻撃です。多くのユーザーが複数のサービスで同じパスワードを使い回していることを悪用します。'
        },
        {
            'question_text': 'レインボーテーブルとは何ですか？',
            'option_a': '様々な文字列とそのハッシュ値を事前計算したテーブル',
            'option_b': 'ネットワーク通信を色分けして表示するツール',
            'option_c': 'セキュリティリスクを評価する表',
            'option_d': 'パスワードの強度を表示する表',
            'correct_answer': 'A',
            'explanation': 'レインボーテーブルは、パスワードとそのハッシュ値を大量に事前計算して保存したテーブルです。これを使うとハッシュ値からパスワードを高速に逆算できます。ソルトを使用することで対策できます。'
        },
        {
            'question_text': 'ゼロトラストセキュリティモデルの基本原則は？',
            'option_a': '社内ネットワークは全て信頼する',
            'option_b': 'VPNさえ使えば安全',
            'option_c': '全てのアクセスを検証し、何も信頼しない',
            'option_d': 'ファイアウォールだけで防御する',
            'correct_answer': 'C',
            'explanation': 'ゼロトラストは「決して信頼せず、常に検証する」という原則に基づくセキュリティモデルです。社内外を問わず、全てのアクセスを毎回検証することで、より高いセキュリティを実現します。'
        },
        {
            'question_text': '多要素認証（MFA）で使われる「要素」として正しくないものは？',
            'option_a': '知識要素（パスワードなど）',
            'option_b': '所有要素（スマホなど）',
            'option_c': '生体要素（指紋など）',
            'option_d': '時間要素（ログイン時刻など）',
            'correct_answer': 'D',
            'explanation': '多要素認証の3要素は、知識要素（知っているもの）、所有要素（持っているもの）、生体要素（その人自身）です。時間要素は一般的な要素ではありません。'
        },
        {
            'question_text': 'DPIA（データ保護影響評価）の主な目的は？',
            'option_a': 'システムの処理速度を評価する',
            'option_b': '個人データ処理によるプライバシーリスクを評価する',
            'option_c': 'ネットワーク帯域を評価する',
            'option_d': 'データベースの容量を評価する',
            'correct_answer': 'B',
            'explanation': 'DPIAは、個人データの処理活動がプライバシーに与える影響とリスクを事前に評価する手法です。GDPRなどのプライバシー規制で要求されることがあります。'
        },
        {
            'question_text': 'SASTとDASTの違いとして正しいものは？',
            'option_a': 'SASTはソースコード解析、DASTは実行時テスト',
            'option_b': 'SASTは動的解析、DASTは静的解析',
            'option_c': 'SASTは手動テスト、DASTは自動テスト',
            'option_d': 'SASTは本番環境、DASTは開発環境',
            'correct_answer': 'A',
            'explanation': 'SAST（Static Application Security Testing）はソースコードを解析する静的テスト、DAST（Dynamic Application Security Testing）は実際にアプリを動かして脆弱性を探す動的テストです。'
        },
        {
            'question_text': 'CVEとは何を表しますか？',
            'option_a': '暗号化アルゴリズムの略称',
            'option_b': '脆弱性に付与される共通識別子',
            'option_c': 'セキュリティ製品の認証規格',
            'option_d': 'ネットワークプロトコルの名称',
            'correct_answer': 'B',
            'explanation': 'CVE（Common Vulnerabilities and Exposures）は、公開されている脆弱性に付与される共通の識別子です。CVE番号により、脆弱性を一意に特定し、情報共有が容易になります。'
        },
        {
            'question_text': 'CVSSの主な用途は？',
            'option_a': 'ネットワーク速度の測定',
            'option_b': '脆弱性の深刻度を数値化する',
            'option_c': 'データ容量の計算',
            'option_d': 'パスワードの強度評価',
            'correct_answer': 'B',
            'explanation': 'CVSS（Common Vulnerability Scoring System）は、脆弱性の深刻度を0.0〜10.0のスコアで評価する標準的な指標です。優先的に対処すべき脆弱性を判断するのに役立ちます。'
        },
        {
            'question_text': 'フィッシング攻撃の説明として最も適切なものは？',
            'option_a': '偽のWebサイトやメールで個人情報を騙し取る',
            'option_b': 'ネットワークを監視して情報を盗む',
            'option_c': 'ウイルスを使ってファイルを暗号化する',
            'option_d': 'システムに大量のリクエストを送る',
            'correct_answer': 'A',
            'explanation': 'フィッシングは、本物そっくりの偽サイトやメールを使って、ユーザーをだましてパスワードやクレジットカード情報などを入力させる攻撃手法です。'
        },
        {
            'question_text': 'スミッシングとは何ですか？',
            'option_a': 'SMSを使ったフィッシング攻撃',
            'option_b': 'スマートフォンのウイルス',
            'option_c': 'SNSでの誹謗中傷',
            'option_d': 'スパムメールのフィルタリング技術',
            'correct_answer': 'A',
            'explanation': 'スミッシングは、SMS（ショートメッセージ）を使ったフィッシング攻撃です。SMS + Phishing = Smishingという造語で、宅配業者などを装ったメッセージが多く見られます。'
        },
        {
            'question_text': 'スピアフィッシングの特徴は？',
            'option_a': '不特定多数に送信される',
            'option_b': '特定の個人や組織を狙う',
            'option_c': 'ウイルスを添付しない',
            'option_d': '必ず電話で確認される',
            'correct_answer': 'B',
            'explanation': 'スピアフィッシングは、特定の個人や組織を標的にした精巧なフィッシング攻撃です。事前に標的の情報を収集し、信憑性の高いメールを作成するため、見破るのが困難です。'
        },
        {
            'question_text': 'ランサムウェアの主な特徴は？',
            'option_a': 'ファイルを暗号化して身代金を要求する',
            'option_b': 'パスワードを盗み出す',
            'option_c': 'Webサイトを改ざんする',
            'option_d': 'ネットワークを監視する',
            'correct_answer': 'A',
            'explanation': 'ランサムウェアは、感染したコンピュータのファイルを暗号化し、復号のために身代金（Ransom）を要求するマルウェアです。定期的なバックアップが重要な対策となります。'
        },
        {
            'question_text': 'サプライチェーン攻撃とは？',
            'option_a': '物流システムを停止させる攻撃',
            'option_b': '信頼されているソフトウェアや業者を経由した攻撃',
            'option_c': 'ネットワーク機器を直接攻撃する手法',
            'option_d': 'ECサイトのカート機能を狙う攻撃',
            'correct_answer': 'B',
            'explanation': 'サプライチェーン攻撃は、標的企業が信頼している外部ベンダーやソフトウェアを侵害し、それを足がかりに本来の標的を攻撃する手法です。防御が難しい高度な攻撃です。'
        },
        {
            'question_text': 'ソーシャルエンジニアリングとは？',
            'option_a': '人の心理的な隙を突いて情報を得る手法',
            'option_b': 'SNSの機能を開発する技術',
            'option_c': 'ソフトウェアの脆弱性を突く攻撃',
            'option_d': '社会インフラを管理する技術',
            'correct_answer': 'A',
            'explanation': 'ソーシャルエンジニアリングは、技術的な手段ではなく、人間の心理的な隙や信頼関係を悪用して機密情報を入手する手法です。技術的な対策だけでは防げないため、教育が重要です。'
        },
        {
            'question_text': 'セキュアコーディングの主な目的は？',
            'option_a': 'コードの実行速度を上げる',
            'option_b': 'セキュリティ脆弱性を作り込まない',
            'option_c': 'コードの行数を減らす',
            'option_d': 'デザインパターンを適用する',
            'correct_answer': 'B',
            'explanation': 'セキュアコーディングは、開発段階からセキュリティを考慮し、脆弱性を作り込まないようにするプログラミング手法です。入力値の検証やエラー処理などが含まれます。'
        },
        {
            'question_text': '侵入テスト（ペネトレーションテスト）の目的は？',
            'option_a': 'システムの処理速度を測定する',
            'option_b': '実際に攻撃を試してセキュリティの弱点を発見する',
            'option_c': 'ユーザビリティを評価する',
            'option_d': 'データベースの整合性を確認する',
            'correct_answer': 'B',
            'explanation': '侵入テストは、実際の攻撃者の視点でシステムに侵入を試み、セキュリティ上の弱点を発見する手法です。脆弱性診断よりも実践的なアプローチです。'
        },
        {
            'question_text': 'WAF（Web Application Firewall）の主な機能は？',
            'option_a': 'Webアプリケーションへの攻撃を検知・防御する',
            'option_b': 'Webページの表示速度を上げる',
            'option_c': 'データベースをバックアップする',
            'option_d': 'HTTPSを自動設定する',
            'correct_answer': 'A',
            'explanation': 'WAFは、Webアプリケーションへの攻撃（SQLインジェクション、XSSなど）を検知・防御する専用のファイアウォールです。アプリケーション層での防御を提供します。'
        }
    ]
    
    # 問題を登録
    for q_data in questions:
        question = Question(
            category_id=security_cat.id,
            **q_data
        )
        db.session.add(question)
    
    db.session.commit()
    print(f'セキュリティカテゴリに{len(questions)}問を登録しました。')

def init_it_basics_questions():
    """IT基礎カテゴリの問題を登録（サンプル）"""
    it_cat = Category(
        name='IT基礎',
        description='ITの基礎的な知識と用語を学習します'
    )
    db.session.add(it_cat)
    db.session.commit()
    print('IT基礎カテゴリを作成しました。（問題は後で追加してください）')

def init_programming_questions():
    """プログラミングカテゴリの問題を登録（サンプル）"""
    prog_cat = Category(
        name='プログラミング',
        description='プログラミングの基本概念を学習します'
    )
    db.session.add(prog_cat)
    db.session.commit()
    print('プログラミングカテゴリを作成しました。（問題は後で追加してください）')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        init_security_questions()
        init_it_basics_questions()
        init_programming_questions()
```

## テスト手順

### 全問正解の再現手順

1. カテゴリを選択してクイズを開始
2. 開発者ツール（F12）を開く
3. Consoleタブで以下を実行：

```javascript
// 全問正解用スクリプト
async function autoCorrectAnswer() {
    // 現在の問題を取得
    const response = await fetch('/api/question/current');
    const data = await response.json();
    
    if (data.finished) {
        console.log('クイズ終了');
        return;
    }
    
    // バックエンドから正解を取得（本番環境では削除すべき）
    const questionId = data.question_id; // APIに追加が必要
    
    // ここでは手動で正解を選択
    // または、データベースから直接取得する管理者用APIを用意
}
```

**推奨方法**: 問題データをあらかじめ確認し、正解を選択してテスト

### 全問不正解の再現手順

1. カテゴリを選択してクイズを開始
2. 各問題で正解以外の選択肢を選ぶ
3. または、開発者ツールで：

```javascript
// 全問不正解用スクリプト（わざと空文字を送信）
selectAnswer('');  // 各問題で実行
```

### 復習モードのテスト

1. クイズを実施し、意図的に数問間違える
2. 結果画面で「復習モード」ボタンをクリック
3. 間違えた問題のみが出題されることを確認

### タイマーのテスト

1. クイズ開始
2. 30秒間何も選択せずに待つ
3. 自動的に次の問題に移ることを確認

### 効果音のテスト

1. 効果音ONの状態で問題に回答
2. 正解時と不正解時で異なる音が再生されることを確認
3. 効果音トグルをOFFにして音が鳴らないことを確認

## 今後の拡張案

### 1. 問題管理機能

- **管理画面の実装**
  - 問題の追加・編集・削除
  - カテゴリの管理
  - 一括インポート（CSV/JSON）
  
- **問題のレビュー機能**
  - 問題の評価（わかりやすさ、難易度）
  - コメント機能

### 2. 難易度調整

- **難易度レベルの追加**
  - 初級・中級・上級の3段階
  - 難易度別の出題設定
  
- **適応型学習**
  - 正答率に応じて難易度を自動調整
  - 弱点分野の重点出題

### 3. 検索機能

- **問題検索**
  - キーワードで問題を検索
  - タグ機能の追加
  
- **学習履歴の検索**
  - 過去のスコア検索
  - 間違えた問題の一覧表示

### 4. ユーザー管理

- **ログイン機能**
  - ユーザー登録・認証
  - 学習履歴の保存
  
- **進捗管理**
  - カテゴリ別の習熟度表示
  - 学習カレンダー

### 5. ソーシャル機能

- **ランキング**
  - スコアランキング
  - 週間・月間ランキング
  
- **チャレンジモード**
  - 他のユーザーとのスコア競争
  - チーム対戦機能

### 6. 学習支援

- **統計機能**
  - カテゴリ別の正答率グラフ
  - 学習時間の記録
  
- **推奨問題**
  - AIによる次に学ぶべき問題の推薦
  - 復習タイミングの通知

### 7. モバイル対応

- **PWA化**
  - オフライン対応
  - ホーム画面への追加
  
- **レスポンシブデザインの強化**
  - タブレット最適化
  - スマートフォンUI改善

### 8. 多言語対応

- **UI・問題の多言語化**
  - 英語、中国語などへの対応
  - 翻訳管理機能

### 9. アクセシビリティ強化

- **スクリーンリーダー対応の強化**
- **キーボードナビゲーションの改善**
- **ハイコントラストモード**
- **音声読み上げ機能**

### 10. ゲーミフィケーション

- **バッジ・実績システム**
  - 連続ログイン報酬
  - スコア達成バッジ
  
- **ポイントシステム**
  - 学習ポイントの付与
  - ポイントランキング

## 用語の参考リンク集

### セキュリティ用語

- **XSS（クロスサイトスクリプティング）**: [#]
- **CSRF（クロスサイトリクエストフォージェリ）**: [#]
- **SQLインジェクション**: [#]
- **パスワードリスト攻撃**: [#]
- **レインボーテーブル**: [#]
- **ゼロトラスト**: [#]
- **多要素認証（MFA）**: [#]
- **DPIA（データ保護影響評価）**: [#]
- **SAST（静的アプリケーションセキュリティテスト）**: [#]
- **DAST（動的アプリケーションセキュリティテスト）**: [#]
- **CVE（共通脆弱性識別子）**: [#]
- **CVSS（共通脆弱性評価システム）**: [#]
- **フィッシング**: [#]
- **スミッシング**: [#]
- **スピアフィッシング**: [#]
- **ランサムウェア**: [#]
- **サプライチェーン攻撃**: [#]
- **ソーシャルエンジニアリング**: [#]
- **セキュアコーディング**: [#]
- **侵入テスト（ペネトレーションテスト）**: [#]
- **WAF（Webアプリケーションファイアウォール）**: [#]
- **IAM（アイデンティティ・アクセス管理）**: [#]

### IT基礎用語

- **プロトコル**: [#]
- **HTTP/HTTPS**: [#]
- **DNS**: [#]
- **IP アドレス**: [#]
- **TCP/IP**: [#]
- **クラウドコンピューティング**: [#]
- **API**: [#]
- **データベース**: [#]
- **サーバー**: [#]
- **クライアント**: [#]

### プログラミング用語

- **変数**: [#]
- **関数**: [#]
- **ループ**: [#]
- **条件分岐**: [#]
- **オブジェクト指向**: [#]
- **配列**: [#]
- **デバッグ**: [#]
- **バージョン管理**: [#]
- **Git**: [#]
- **フレームワーク**: [#]

## 技術スタック詳細

### バックエンド
- **Python 3.12+**
- **Flask 3.1+**: Webフレームワーク
- **Flask-SQLAlchemy**: ORM
- **Flask-Migrate**: データベースマイグレーション

### フロントエンド
- **Bootstrap 5**: UIフレームワーク
- **Vanilla JavaScript**: クイズロジック
- **HTML5/CSS3**: マークアップ

### データベース
- **SQLite**: 開発環境用
- **MySQL/PostgreSQL**: 本番環境推奨

### 開発ツール
- **Poetry**: パッケージ管理
- **pytest**: テストフレームワーク
- **Black**: コードフォーマッター
- **Flake8**: リンター

## 起動方法

### 前提条件

#### Dockerを使用する場合（推奨）

- Docker Desktop または Docker Engine
- Docker Compose（Docker Desktopに含まれています）

Dockerのインストール方法:
- **macOS/Windows**: [Docker Desktop](https://www.docker.com/products/docker-desktop/) をダウンロードしてインストール
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/) をインストール

#### ローカル環境を使用する場合

- Python 3.12以上
- Poetry（パッケージ管理ツール）

Poetryのインストール方法:
```bash
# macOS/Linux
curl -sSL https://install.python-poetry.org | python3 -

# Windows (PowerShell)
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

### 方法1: Docker Composeを使用（推奨）

Docker Composeを使用することで、環境の違いを気にせずにアプリケーションを起動できます。

#### macOS/Linux

```bash
# 起動
./run.sh

# 停止（別のターミナルから）
./stop.sh
```

#### Windows

```cmd
REM 起動
run.bat

REM 停止（別のコマンドプロンプトから）
stop.bat
```

ラッパースクリプトは以下の処理を自動的に実行します:
1. DockerとDocker Composeのインストール確認
2. コンテナのビルド（初回のみ）
3. データベースの初期化（存在しない場合）
4. アプリケーションの起動

#### 手動でDocker Composeを操作する場合

```bash
# コンテナをビルドして起動
docker compose up --build

# バックグラウンドで起動
docker compose up -d

# ログを確認
docker compose logs -f

# 停止
docker compose down

# 停止してボリュームも削除
docker compose down -v
```

#### 初回起動時のデータベース初期化

初回起動時は自動的に初期化されますが、手動で実行する場合:

```bash
docker compose exec web poetry run python data/init_questions.py
```

### 方法2: ローカル環境で起動（Dockerを使用しない場合）

ローカル環境で直接起動する場合の手順です。

#### ステップ1: 依存関係のインストール

#### ステップ1: 依存関係のインストール

```bash
poetry install
```

#### ステップ2: 仮想環境の有効化

```bash
poetry shell
```

#### ステップ3: データベースの初期化（初回のみ）

```bash
poetry run python data/init_questions.py
```

これにより、以下のカテゴリと問題が登録されます:
- **セキュリティ**: 20問
- **IT基礎**: カテゴリのみ（問題は後で追加可能）
- **プログラミング**: カテゴリのみ（問題は後で追加可能）

#### ステップ4: アプリケーションの起動

```bash
poetry run python app.py
```

または

```bash
flask run
```

アプリケーションは `http://localhost:5000` で起動します。

### アクセス方法

ブラウザで以下のURLにアクセス:

```
http://localhost:5000
```

### トラブルシューティング

#### Docker関連

##### ポートが既に使用されている場合

`docker-compose.yml` の `ports` セクションを編集:

```yaml
ports:
  - "5001:5000"  # ホストの5001ポートを使用
```

##### コンテナが起動しない場合

```bash
# ログを確認
docker compose logs

# コンテナを再ビルド
docker compose build --no-cache
docker compose up
```

##### データベースをリセットする場合

```bash
# コンテナを停止してデータベースファイルを削除
docker compose down
rm quiz.db  # macOS/Linux
# del quiz.db  # Windows

# 再起動（自動的に初期化されます）
./run.sh  # または docker compose up
```

##### イメージを再ビルドする場合

```bash
docker compose build --no-cache
docker compose up
```

#### ローカル環境関連

##### ポートが既に使用されている場合

`app.py` の最後の行を編集して、別のポートを指定:

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

##### データベースエラーが発生する場合

データベースファイルを削除して再初期化:

```bash
# macOS/Linux
rm quiz.db
poetry run python data/init_questions.py

# Windows
del quiz.db
poetry run python data/init_questions.py
```

##### 仮想環境の問題

仮想環境を再作成:

```bash
poetry env remove python
poetry install
```

#### 共通

##### 効果音が再生されない場合

効果音ファイル（`static/sounds/correct.mp3` と `static/sounds/incorrect.mp3`）が存在しない可能性があります。
効果音がなくてもアプリケーションは正常に動作します（音が鳴らないだけです）。

効果音ファイルを追加する場合は、`static/sounds/` ディレクトリに配置してください。
詳細は `static/sounds/README.md` を参照してください。

### 開発モードでの起動

デバッグモードで起動する場合（コード変更が自動反映されます）:

```bash
export FLASK_ENV=development  # macOS/Linux
set FLASK_ENV=development     # Windows
poetry run python app.py
```

## まとめ

このクイズアプリは、セキュリティ、IT基礎、プログラミングの学習を支援する教育ツールです。
アクセシビリティに配慮し、ゲーム感覚で楽しく学習できる設計となっています。

今後の拡張により、より高機能な学習プラットフォームへと発展させることが可能です。


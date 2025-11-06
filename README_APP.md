# クイズアプリ設計書

## 概要
大学3年生向けのIT・セキュリティ用語学習Webアプリケーション。4択クイズ形式で、カテゴリ別に用語を学習できます。

---

## 要件定義

### 基本要件
- **言語**: 日本語UI
- **アクセシビリティ**: WCAG 2.1 Level AA準拠を目指す
- **クイズ形式**: 4択（ラジオボタン）
- **出題方式**: 各カテゴリ20問プールからランダム10問を出題（順番シャッフル）
  - 全問題数が10問以下の場合は重複出題を許可
- **フィードバック**: 正解後に解説を表示
- **結果表示**: 終了時にスコアと復習リストを提示

### カテゴリ
初期設定として以下の3カテゴリを用意：
1. **セキュリティ**
2. **IT基礎**
3. **プログラミング**

### 主要機能
1. **タイマー機能**: 1問あたり30秒（設定で可変）
2. **効果音**: 正誤で異なる効果音、ON/OFF切替可能
3. **復習モード**: 間違えた問題のみを再出題
4. **スコア共有**: スコア文字列をクリップボードにコピー

---

## システム構成

### 技術スタック
- **バックエンド**: Python 3.12 + Flask 3.1.2
- **フロントエンド**: Bootstrap 5 + Vanilla JavaScript
- **データベース**: MySQL 8.0（開発時はSQLite可）
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **マイグレーション**: Flask-Migrate
- **環境管理**: Poetry + pyenv

### アーキテクチャ
```
quiz-app/
├── app/
│   ├── __init__.py           # Flaskアプリケーション初期化
│   ├── models.py             # データモデル定義
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── main.py           # メインページ（トップ、カテゴリ選択）
│   │   ├── quiz.py           # クイズ実行ロジック
│   │   └── api.py            # API（スコア取得、設定保存など）
│   ├── services/
│   │   ├── __init__.py
│   │   ├── quiz_service.py   # クイズロジック（問題選択、採点）
│   │   └── result_service.py # 結果集計、復習リスト生成
│   ├── templates/
│   │   ├── base.html         # 共通レイアウト
│   │   ├── index.html        # トップページ
│   │   ├── category.html     # カテゴリ選択
│   │   ├── quiz.html         # クイズ実行画面
│   │   ├── result.html       # 結果表示
│   │   ├── review.html       # 復習モード
│   │   └── reference.html    # 用語参考リンク集
│   └── static/
│       ├── css/
│       │   └── style.css     # カスタムスタイル
│       ├── js/
│       │   ├── quiz.js       # クイズロジック（タイマー、効果音）
│       │   ├── settings.js   # 設定管理
│       │   └── accessibility.js # アクセシビリティ機能
│       └── sounds/
│           ├── correct.mp3   # 正解音
│           └── incorrect.mp3 # 不正解音
├── migrations/               # データベースマイグレーション
├── tests/
│   ├── test_models.py
│   ├── test_quiz_service.py
│   └── test_routes.py
├── config.py                 # 設定ファイル
├── run.py                    # アプリケーション起動スクリプト
├── pyproject.toml            # Poetry設定
└── README.md
```

---

## データベース設計

### ERD概要
```
Category (カテゴリ)
    ↓ 1:N
Question (問題)
    ↓ 1:N
Choice (選択肢)

QuizSession (クイズセッション) ←→ N:M → Question
    ↓ 1:N
UserAnswer (回答履歴)
```

### テーブル定義

#### 1. categories（カテゴリテーブル）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | INTEGER | PK, AUTO_INCREMENT | カテゴリID |
| name | VARCHAR(100) | NOT NULL, UNIQUE | カテゴリ名 |
| description | TEXT | NULL | カテゴリ説明 |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | 表示順 |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | 有効フラグ |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

#### 2. questions（問題テーブル）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 問題ID |
| category_id | INTEGER | FK(categories.id), NOT NULL | カテゴリID |
| question_text | TEXT | NOT NULL | 問題文 |
| explanation | TEXT | NOT NULL | 解説 |
| difficulty | INTEGER | NOT NULL, DEFAULT 1 | 難易度（1-5） |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | 有効フラグ |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

#### 3. choices（選択肢テーブル）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 選択肢ID |
| question_id | INTEGER | FK(questions.id), NOT NULL | 問題ID |
| choice_text | TEXT | NOT NULL | 選択肢テキスト |
| is_correct | BOOLEAN | NOT NULL, DEFAULT FALSE | 正解フラグ |
| display_order | INTEGER | NOT NULL | 表示順（ランダム化前の順序） |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

#### 4. quiz_sessions（クイズセッションテーブル）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | INTEGER | PK, AUTO_INCREMENT | セッションID |
| category_id | INTEGER | FK(categories.id), NOT NULL | カテゴリID |
| session_key | VARCHAR(64) | UNIQUE, NOT NULL | セッション識別キー |
| total_questions | INTEGER | NOT NULL | 総問題数 |
| correct_count | INTEGER | NOT NULL, DEFAULT 0 | 正解数 |
| is_review_mode | BOOLEAN | NOT NULL, DEFAULT FALSE | 復習モードフラグ |
| timer_seconds | INTEGER | NOT NULL, DEFAULT 30 | タイマー秒数 |
| sound_enabled | BOOLEAN | NOT NULL, DEFAULT TRUE | 効果音有効フラグ |
| started_at | DATETIME | NOT NULL | 開始日時 |
| completed_at | DATETIME | NULL | 完了日時 |
| created_at | DATETIME | NOT NULL | 作成日時 |

#### 5. user_answers（回答履歴テーブル）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | INTEGER | PK, AUTO_INCREMENT | 回答ID |
| session_id | INTEGER | FK(quiz_sessions.id), NOT NULL | セッションID |
| question_id | INTEGER | FK(questions.id), NOT NULL | 問題ID |
| choice_id | INTEGER | FK(choices.id), NULL | 選択した選択肢ID |
| is_correct | BOOLEAN | NOT NULL | 正誤フラグ |
| time_spent_seconds | INTEGER | NOT NULL | 回答時間（秒） |
| answered_at | DATETIME | NOT NULL | 回答日時 |

#### 6. term_references（用語参考リンクテーブル）
| カラム名 | 型 | 制約 | 説明 |
|---------|-----|------|------|
| id | INTEGER | PK, AUTO_INCREMENT | リンクID |
| term_name | VARCHAR(200) | NOT NULL | 用語名 |
| description | TEXT | NULL | 説明 |
| url | VARCHAR(500) | NOT NULL | 参考URL |
| category_id | INTEGER | FK(categories.id), NULL | 関連カテゴリID |
| display_order | INTEGER | NOT NULL, DEFAULT 0 | 表示順 |
| created_at | DATETIME | NOT NULL | 作成日時 |
| updated_at | DATETIME | NOT NULL | 更新日時 |

---

## 画面設計

### 1. トップページ（`/`）
**目的**: アプリケーションの説明とカテゴリ選択への導線

**構成要素**:
- ヘッダー: アプリタイトル、ナビゲーション
- メインエリア:
  - アプリケーション説明（簡潔に）
  - 「クイズを始める」ボタン → カテゴリ選択画面へ
  - 「用語参考リンク集」ボタン
- フッター: 設定（効果音ON/OFF、タイマー設定）

**アクセシビリティ対応**:
- `<h1>`でページタイトル
- ランドマーク（`<main>`, `<nav>`, `<footer>`）の適切な使用
- ボタンに`aria-label`付与

### 2. カテゴリ選択画面（`/category`）
**目的**: クイズのカテゴリを選択

**構成要素**:
- カテゴリカード（Bootstrap Card）
  - カテゴリ名
  - カテゴリ説明
  - 問題数表示
  - 「このカテゴリで始める」ボタン
- 設定パネル（開閉可能）
  - タイマー: ON/OFF、秒数設定（スライダー: 15-60秒）
  - 効果音: ON/OFF

**アクセシビリティ対応**:
- カードはフォーカス可能
- キーボード操作（Enter/Spaceで選択）
- スライダーに適切な`aria-label`

### 3. クイズ実行画面（`/quiz/<session_key>`）
**目的**: クイズを実施

**構成要素**:
- プログレスバー: 現在の問題番号 / 総問題数
- タイマー表示: 残り時間（円形プログレスバー）
- 問題文エリア:
  - 問題番号
  - 問題文（大きめのフォント）
- 選択肢エリア:
  - 4つのラジオボタン + ラベル
  - ホバー時にハイライト
- 操作ボタン:
  - 「回答する」ボタン（選択後に有効化）
  - 「次の問題へ」ボタン（回答後に表示）
  - 「中断する」ボタン
- 解説エリア（回答後に表示）:
  - 正誤判定アイコン
  - 解説テキスト

**JavaScript処理**:
- タイマーカウントダウン
- 時間切れ時の自動回答処理
- 効果音再生（正誤）
- アニメーション効果

**アクセシビリティ対応**:
- ラジオボタングループに`fieldset`と`legend`
- スクリーンリーダー向けライブリージョン（`aria-live="polite"`）
- キーボード操作（矢印キーで選択肢移動）
- 色だけに依存しない正誤表示（アイコン併用）

### 4. 結果表示画面（`/result/<session_key>`）
**目的**: クイズの結果を表示

**構成要素**:
- スコア表示:
  - 正解数 / 総問題数
  - 正解率（パーセンテージ）
  - グラフ（円グラフまたはバー）
- 評価メッセージ（スコアに応じて変化）
- 間違えた問題リスト:
  - 問題文
  - 選択した回答 vs 正解
  - 解説（折りたたみ可能）
- 操作ボタン:
  - 「スコアをコピー」ボタン
  - 「間違えた問題を復習」ボタン
  - 「別のカテゴリで挑戦」ボタン
  - 「トップに戻る」ボタン

**スコア共有フォーマット例**:
```
【クイズ結果】
カテゴリ: セキュリティ
スコア: 8/10 (80%)
#ITクイズアプリ
```

**アクセシビリティ対応**:
- スコアを`aria-live`で通知
- グラフに代替テキスト
- リストはセマンティックな`<dl>`または`<ul>`

### 5. 復習モード画面（`/review/<session_key>`）
**目的**: 間違えた問題のみを再出題

**構成要素**:
- クイズ実行画面と同様の構成
- ヘッダーに「復習モード」バッジ表示
- タイマーはデフォルトで無効化（有効化も可能）

### 6. 用語参考リンク集（`/reference`）
**目的**: 学習に役立つ用語の参考リンクを提供

**構成要素**:
- カテゴリタブ（Bootstrap Tabs）
- 各タブ内に用語リスト:
  - 用語名
  - 簡潔な説明
  - 参考リンク（現時点では`#`）
- 検索フィルター（将来実装）

**初期設定用語（セキュリティカテゴリ）**:
- XSS（クロスサイトスクリプティング）
- CSRF（クロスサイトリクエストフォージェリ）
- SQLインジェクション
- パスワードリスト攻撃
- レインボーテーブル
- ゼロトラスト
- 多要素認証
- DPIA（データ保護影響評価）
- SAST/DAST
- CVE/CVSS
- フィッシング
- スミッシング
- スピアフィッシング
- ランサムウェア
- サプライチェーン攻撃
- ソーシャルエンジニアリング
- セキュアコーディング
- 侵入テスト
- WAF（Web Application Firewall）
- IAM（Identity and Access Management）

**アクセシビリティ対応**:
- タブに適切な`role="tablist"`、`role="tab"`
- リンクに説明的なテキスト

---

## API設計

### エンドポイント一覧

#### 1. クイズ開始
```
POST /api/quiz/start
```
**リクエストボディ**:
```json
{
  "category_id": 1,
  "timer_seconds": 30,
  "sound_enabled": true,
  "is_review_mode": false,
  "parent_session_key": null  // 復習モード時に元セッションキー
}
```
**レスポンス**:
```json
{
  "session_key": "abc123...",
  "total_questions": 10,
  "questions": [
    {
      "question_id": 5,
      "question_number": 1
    },
    // ...10問分
  ]
}
```

#### 2. 問題取得
```
GET /api/quiz/<session_key>/question/<question_number>
```
**レスポンス**:
```json
{
  "question_id": 5,
  "question_number": 1,
  "total_questions": 10,
  "question_text": "XSSとは何の略ですか？",
  "choices": [
    {
      "choice_id": 17,
      "choice_text": "Cross-Site Scripting"
    },
    // ...4つの選択肢（ランダム順）
  ]
}
```

#### 3. 回答送信
```
POST /api/quiz/<session_key>/answer
```
**リクエストボディ**:
```json
{
  "question_id": 5,
  "choice_id": 17,
  "time_spent_seconds": 12
}
```
**レスポンス**:
```json
{
  "is_correct": true,
  "correct_choice_id": 17,
  "explanation": "XSSはCross-Site Scriptingの略で..."
}
```

#### 4. 結果取得
```
GET /api/quiz/<session_key>/result
```
**レスポンス**:
```json
{
  "session_key": "abc123...",
  "category_name": "セキュリティ",
  "total_questions": 10,
  "correct_count": 8,
  "accuracy_rate": 80.0,
  "completed_at": "2025-11-06T10:30:00Z",
  "incorrect_questions": [
    {
      "question_id": 7,
      "question_text": "...",
      "user_choice_text": "...",
      "correct_choice_text": "...",
      "explanation": "..."
    }
  ],
  "share_text": "【クイズ結果】\nカテゴリ: セキュリティ\nスコア: 8/10 (80%)\n#ITクイズアプリ"
}
```

#### 5. 設定保存
```
POST /api/settings
```
**リクエストボディ**:
```json
{
  "timer_seconds": 30,
  "sound_enabled": true
}
```
**レスポンス**:
```json
{
  "message": "設定を保存しました"
}
```
※ クッキーまたはlocalStorageで管理

---

## 実装詳細

### 主要ロジック

#### 1. 問題選択アルゴリズム（`quiz_service.py`）
```python
def select_questions(category_id: int, num_questions: int = 10) -> list:
    """
    指定カテゴリから問題をランダムに選択
    
    Args:
        category_id: カテゴリID
        num_questions: 出題数（デフォルト10問）
    
    Returns:
        選択された問題IDのリスト
    """
    # カテゴリ内の有効な問題を取得
    available_questions = Question.query.filter_by(
        category_id=category_id, 
        is_active=True
    ).all()
    
    question_ids = [q.id for q in available_questions]
    
    # 問題数が足りない場合は重複を許可
    if len(question_ids) < num_questions:
        # 重複を許可してランダムサンプリング
        selected = random.choices(question_ids, k=num_questions)
    else:
        # 重複なしでランダムサンプリング
        selected = random.sample(question_ids, num_questions)
    
    # 順番をシャッフル
    random.shuffle(selected)
    
    return selected
```

#### 2. 選択肢シャッフル（`quiz_service.py`）
```python
def get_shuffled_choices(question_id: int) -> list:
    """
    問題の選択肢をシャッフルして返す
    
    Args:
        question_id: 問題ID
    
    Returns:
        シャッフルされた選択肢のリスト
    """
    choices = Choice.query.filter_by(question_id=question_id).all()
    choices_list = list(choices)
    random.shuffle(choices_list)
    
    return choices_list
```

#### 3. タイマー機能（`quiz.js`）
```javascript
class QuizTimer {
    constructor(seconds, onTimeout) {
        this.totalSeconds = seconds;
        this.remainingSeconds = seconds;
        this.onTimeout = onTimeout;
        this.intervalId = null;
    }
    
    start() {
        this.intervalId = setInterval(() => {
            this.remainingSeconds--;
            this.updateDisplay();
            
            if (this.remainingSeconds <= 0) {
                this.stop();
                this.onTimeout();
            }
        }, 1000);
    }
    
    stop() {
        if (this.intervalId) {
            clearInterval(this.intervalId);
            this.intervalId = null;
        }
    }
    
    updateDisplay() {
        // 円形プログレスバーの更新
        const percentage = (this.remainingSeconds / this.totalSeconds) * 100;
        document.getElementById('timer-progress').style.strokeDashoffset = 
            100 - percentage;
        document.getElementById('timer-text').textContent = 
            this.remainingSeconds;
    }
}
```

#### 4. 効果音再生（`quiz.js`）
```javascript
class SoundManager {
    constructor() {
        this.enabled = true;
        this.correctSound = new Audio('/static/sounds/correct.mp3');
        this.incorrectSound = new Audio('/static/sounds/incorrect.mp3');
    }
    
    playCorrect() {
        if (this.enabled) {
            this.correctSound.currentTime = 0;
            this.correctSound.play();
        }
    }
    
    playIncorrect() {
        if (this.enabled) {
            this.incorrectSound.currentTime = 0;
            this.incorrectSound.play();
        }
    }
    
    setEnabled(enabled) {
        this.enabled = enabled;
        localStorage.setItem('sound_enabled', enabled);
    }
}
```

#### 5. スコアコピー機能（`quiz.js`）
```javascript
async function copyScoreToClipboard(shareText) {
    try {
        await navigator.clipboard.writeText(shareText);
        // 成功メッセージ表示
        showToast('スコアをクリップボードにコピーしました', 'success');
    } catch (err) {
        // フォールバック: テキストエリアを使った方法
        const textarea = document.createElement('textarea');
        textarea.value = shareText;
        document.body.appendChild(textarea);
        textarea.select();
        document.execCommand('copy');
        document.body.removeChild(textarea);
        showToast('スコアをクリップボードにコピーしました', 'success');
    }
}
```

### アクセシビリティ実装

#### 1. キーボードナビゲーション（`accessibility.js`）
```javascript
// 選択肢の矢印キー操作
document.addEventListener('keydown', (e) => {
    const choices = document.querySelectorAll('input[name="choice"]');
    const currentIndex = Array.from(choices).findIndex(c => c === document.activeElement);
    
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
        e.preventDefault();
        const nextIndex = (currentIndex + 1) % choices.length;
        choices[nextIndex].focus();
        choices[nextIndex].checked = true;
    } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        e.preventDefault();
        const prevIndex = (currentIndex - 1 + choices.length) % choices.length;
        choices[prevIndex].focus();
        choices[prevIndex].checked = true;
    }
});
```

#### 2. スクリーンリーダー対応
```html
<!-- 問題表示エリア -->
<div role="region" aria-live="polite" aria-atomic="true">
    <h2 id="question-title">問題 <span id="question-number">1</span> / 10</h2>
    <p id="question-text" class="question-text">...</p>
</div>

<!-- 選択肢 -->
<fieldset>
    <legend class="sr-only">回答選択</legend>
    <div class="choices">
        <div class="choice-item">
            <input type="radio" id="choice-1" name="choice" value="1" 
                   aria-describedby="choice-1-text">
            <label for="choice-1" id="choice-1-text">選択肢1</label>
        </div>
        <!-- ... -->
    </div>
</fieldset>

<!-- 結果通知 -->
<div role="status" aria-live="assertive" aria-atomic="true" class="sr-only">
    <span id="result-announce"></span>
</div>
```

#### 3. フォーカス管理
```javascript
// 問題遷移時にフォーカスをリセット
function moveToNextQuestion() {
    // 問題タイトルにフォーカスを移動
    document.getElementById('question-title').focus();
    
    // スクリーンリーダーに通知
    announceToScreenReader('次の問題に移動しました');
}

function announceToScreenReader(message) {
    const announcer = document.getElementById('result-announce');
    announcer.textContent = message;
    
    // 短時間後にクリア
    setTimeout(() => {
        announcer.textContent = '';
    }, 1000);
}
```

### セキュリティ対策

#### 1. CSRF対策
```python
# Flask-WTFを使用したCSRF保護
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# テンプレートでCSRFトークンを埋め込み
# <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
```

#### 2. XSS対策
```python
# Jinjaテンプレートでの自動エスケープ（デフォルトで有効）
# 明示的にHTMLを挿入する場合は |safe フィルターを使用
# ユーザー入力は常にエスケープ
```

#### 3. SQLインジェクション対策
```python
# SQLAlchemyのパラメータ化クエリを使用
# ORM経由でのアクセスを基本とする
questions = Question.query.filter_by(category_id=category_id).all()

# 生SQLを使う場合はパラメータバインディング
db.session.execute(text("SELECT * FROM questions WHERE id = :id"), {"id": question_id})
```

---

## 初期データ設定

### 1. カテゴリ初期データ
```python
# migrations/seeds/categories.py
categories = [
    {
        "name": "セキュリティ",
        "description": "情報セキュリティに関する用語や概念を学習します",
        "display_order": 1
    },
    {
        "name": "IT基礎",
        "description": "ITの基礎知識やネットワーク、ハードウェアについて学習します",
        "display_order": 2
    },
    {
        "name": "プログラミング",
        "description": "プログラミング言語やアルゴリズム、データ構造について学習します",
        "display_order": 3
    }
]
```

### 2. セキュリティカテゴリの問題例

#### 問題1: XSS
```python
{
    "question_text": "XSS（クロスサイトスクリプティング）攻撃を防ぐために最も効果的な対策はどれですか？",
    "explanation": """
    XSS攻撃を防ぐには、ユーザー入力を適切にエスケープ処理することが重要です。
    HTMLエスケープにより、<script>タグなどの特殊文字が無害な文字列に変換され、
    ブラウザで実行されることを防ぎます。大学3年生の皆さんは、Webアプリケーション開発時に
    必ずユーザー入力をエスケープする習慣をつけましょう。
    """,
    "choices": [
        {"text": "ユーザー入力を適切にエスケープする", "is_correct": True},
        {"text": "HTTPSを使用する", "is_correct": False},
        {"text": "データベースを暗号化する", "is_correct": False},
        {"text": "ファイアウォールを設置する", "is_correct": False}
    ]
}
```

#### 問題2: SQLインジェクション
```python
{
    "question_text": "SQLインジェクション攻撃のリスクを最小化する最良の方法はどれですか？",
    "explanation": """
    SQLインジェクション対策には、プリペアドステートメント（パラメータ化クエリ）の使用が
    最も効果的です。これにより、ユーザー入力がSQL文として解釈されることを防ぎます。
    例えば、PythonではSQLAlchemyのようなORMを使うことで、自動的にパラメータバインディングが
    行われます。直接SQL文を組み立てることは避けましょう。
    """,
    "choices": [
        {"text": "プリペアドステートメントを使用する", "is_correct": True},
        {"text": "データベースのポートを変更する", "is_correct": False},
        {"text": "ユーザー入力の文字数を制限する", "is_correct": False},
        {"text": "データベースを読み取り専用にする", "is_correct": False}
    ]
}
```

#### 問題3: 多要素認証
```python
{
    "question_text": "多要素認証（MFA）の「3つの要素」に含まれないものはどれですか？",
    "explanation": """
    多要素認証の3要素は、「知識要素（パスワードなど知っているもの）」「所持要素（スマホなど
    持っているもの）」「生体要素（指紋など自分自身）」です。メールアドレスは知識要素の
    一部ですが、それ自体は要素の分類には含まれません。MFAはセキュリティを大幅に向上させる
    重要な技術なので、可能な限り有効にすることをお勧めします。
    """,
    "choices": [
        {"text": "メールアドレス", "is_correct": True},
        {"text": "知識要素（パスワード）", "is_correct": False},
        {"text": "所持要素（スマートフォン）", "is_correct": False},
        {"text": "生体要素（指紋）", "is_correct": False}
    ]
}
```

※ 実際には各カテゴリに20問以上のデータを用意

---

## テスト設計

### 単体テスト

#### 1. モデルテスト（`test_models.py`）
```python
def test_question_choices_relationship():
    """問題と選択肢のリレーションシップをテスト"""
    question = Question(question_text="テスト問題", category_id=1)
    db.session.add(question)
    db.session.commit()
    
    choice1 = Choice(question_id=question.id, choice_text="選択肢1", is_correct=True)
    choice2 = Choice(question_id=question.id, choice_text="選択肢2", is_correct=False)
    db.session.add_all([choice1, choice2])
    db.session.commit()
    
    assert len(question.choices) == 2
    assert question.choices[0].choice_text == "選択肢1"
```

#### 2. サービスロジックテスト（`test_quiz_service.py`）
```python
def test_select_questions_with_sufficient_pool():
    """問題プールが十分にある場合のテスト"""
    # 20問の問題を作成
    for i in range(20):
        q = Question(question_text=f"問題{i}", category_id=1)
        db.session.add(q)
    db.session.commit()
    
    selected = select_questions(category_id=1, num_questions=10)
    
    assert len(selected) == 10
    assert len(set(selected)) == 10  # 重複なし

def test_select_questions_with_insufficient_pool():
    """問題プールが不足している場合のテスト"""
    # 5問の問題を作成
    for i in range(5):
        q = Question(question_text=f"問題{i}", category_id=1)
        db.session.add(q)
    db.session.commit()
    
    selected = select_questions(category_id=1, num_questions=10)
    
    assert len(selected) == 10
    # 重複が発生するはず
    assert len(set(selected)) < 10
```

### 統合テスト

#### 3. ルートテスト（`test_routes.py`）
```python
def test_quiz_start_api(client):
    """クイズ開始APIのテスト"""
    response = client.post('/api/quiz/start', json={
        'category_id': 1,
        'timer_seconds': 30,
        'sound_enabled': True
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'session_key' in data
    assert data['total_questions'] == 10

def test_answer_submission(client):
    """回答送信のテスト"""
    # セッション開始
    start_response = client.post('/api/quiz/start', json={'category_id': 1})
    session_key = start_response.get_json()['session_key']
    
    # 回答送信
    response = client.post(f'/api/quiz/{session_key}/answer', json={
        'question_id': 1,
        'choice_id': 1,
        'time_spent_seconds': 10
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert 'is_correct' in data
    assert 'explanation' in data
```

### E2Eテスト手順

#### シナリオ1: 全問正解の再現手順
1. トップページにアクセス
2. 「クイズを始める」をクリック
3. 「セキュリティ」カテゴリを選択
4. **テストモード有効化**: URLに`?test_mode=all_correct`を追加
   - または管理画面から「テストモード: 全問正解」を選択
5. 各問題で任意の選択肢を選択（自動的に正解として処理される）
6. 10問すべて回答
7. 結果画面で「10/10 (100%)」と表示されることを確認

#### シナリオ2: 全問不正解の再現手順
1. トップページにアクセス
2. 「クイズを始める」をクリック
3. 「IT基礎」カテゴリを選択
4. **テストモード有効化**: URLに`?test_mode=all_incorrect`を追加
   - または管理画面から「テストモード: 全問不正解」を選択
5. 各問題で任意の選択肢を選択（自動的に不正解として処理される）
6. 10問すべて回答
7. 結果画面で「0/10 (0%)」と表示されることを確認
8. 「間違えた問題を復習」ボタンが表示されることを確認
9. 復習モードで10問すべてが再出題されることを確認

#### シナリオ3: 復習モードのテスト
1. 通常モードで意図的に3問間違える（7問正解）
2. 結果画面で「間違えた問題を復習」をクリック
3. 復習モードで3問のみが出題されることを確認
4. 復習モードの結果が別途記録されることを確認

#### テストモード実装例
```python
# routes/quiz.py
@quiz_bp.route('/quiz/<session_key>/answer', methods=['POST'])
def submit_answer(session_key):
    data = request.get_json()
    question_id = data['question_id']
    choice_id = data['choice_id']
    
    # テストモードチェック
    test_mode = session.get('test_mode')
    
    if test_mode == 'all_correct':
        # 強制的に正解扱い
        correct_choice = Choice.query.filter_by(
            question_id=question_id, 
            is_correct=True
        ).first()
        is_correct = True
        explanation = "【テストモード】正解として処理されました。" + correct_choice.explanation
    elif test_mode == 'all_incorrect':
        # 強制的に不正解扱い
        correct_choice = Choice.query.filter_by(
            question_id=question_id, 
            is_correct=True
        ).first()
        is_correct = False
        explanation = "【テストモード】不正解として処理されました。" + correct_choice.explanation
    else:
        # 通常モード
        selected_choice = Choice.query.get(choice_id)
        is_correct = selected_choice.is_correct
        # ...
    
    # 回答を記録
    # ...
```

---

## 用語参考リンク集

### セキュリティカテゴリ

#### XSS（クロスサイトスクリプティング）
Webアプリケーションの脆弱性の一つで、攻撃者が悪意のあるスクリプトをWebページに挿入する攻撃。ユーザーの入力値を適切にエスケープすることで防ぐことができます。  
参考: [#](#)

#### CSRF（クロスサイトリクエストフォージェリ）
ログイン中のユーザーが意図しない操作を実行させられる攻撃。CSRFトークンを使用することで防御できます。  
参考: [#](#)

#### SQLインジェクション
不正なSQL文を挿入してデータベースを操作する攻撃。プリペアドステートメントを使用することで防止できます。  
参考: [#](#)

#### パスワードリスト攻撃
他サービスから流出したIDとパスワードのリストを使ってログインを試みる攻撃。多要素認証が有効な対策です。  
参考: [#](#)

#### レインボーテーブル
事前計算されたハッシュ値の一覧表。ソルトを使用することで攻撃を防げます。  
参考: [#](#)

#### ゼロトラスト
「信頼しない、常に検証する」という考え方に基づくセキュリティモデル。ネットワークの内外を問わず、すべてのアクセスを検証します。  
参考: [#](#)

#### 多要素認証（MFA）
パスワードに加えて、スマートフォンや生体認証など複数の認証要素を組み合わせる方法。セキュリティが大幅に向上します。  
参考: [#](#)

#### DPIA（データ保護影響評価）
個人データの処理がプライバシーに与える影響を評価する手法。GDPRで要求される場合があります。  
参考: [#](#)

#### SAST（Static Application Security Testing）
ソースコードを静的に解析して脆弱性を検出する手法。開発の早い段階で問題を発見できます。  
参考: [#](#)

#### DAST（Dynamic Application Security Testing）
実行中のアプリケーションを動的にテストして脆弱性を検出する手法。実際の攻撃をシミュレートします。  
参考: [#](#)

#### CVE（Common Vulnerabilities and Exposures）
公開されている脆弱性の識別番号システム。CVE-2021-XXXXX のような形式で表現されます。  
参考: [#](#)

#### CVSS（Common Vulnerability Scoring System）
脆弱性の深刻度を数値化する標準的な評価手法。0.0〜10.0のスコアで表されます。  
参考: [#](#)

#### フィッシング
正規のサービスを装ったメールやWebサイトで個人情報を盗む詐欺。URLを必ず確認する習慣が重要です。  
参考: [#](#)

#### スミッシング
SMSを使ったフィッシング攻撃。宅配業者などを装ったメッセージに注意が必要です。  
参考: [#](#)

#### スピアフィッシング
特定の個人や組織を標的にした精巧なフィッシング攻撃。標的型攻撃とも呼ばれます。  
参考: [#](#)

#### ランサムウェア
データを暗号化して身代金を要求するマルウェア。定期的なバックアップが重要な対策です。  
参考: [#](#)

#### サプライチェーン攻撃
ソフトウェアの供給網（ライブラリやツールなど）を経由した攻撃。信頼できるソースからのみインストールしましょう。  
参考: [#](#)

#### ソーシャルエンジニアリング
人間の心理的な隙をついて情報を盗み取る手法。技術的な対策だけでなく、教育も重要です。  
参考: [#](#)

#### セキュアコーディング
セキュリティを考慮したプログラミング手法。入力検証、エラー処理、最小権限の原則などが含まれます。  
参考: [#](#)

#### 侵入テスト（ペネトレーションテスト）
実際に攻撃を試みてシステムの脆弱性を発見する手法。専門家による定期的な実施が推奨されます。  
参考: [#](#)

#### WAF（Web Application Firewall）
Webアプリケーションへの攻撃を検出・遮断する防御システム。SQLインジェクションやXSSを防ぎます。  
参考: [#](#)

#### IAM（Identity and Access Management）
ユーザーのアイデンティティとアクセス権限を管理するシステム。適切な権限管理がセキュリティの基本です。  
参考: [#](#)

### IT基礎カテゴリ
（今後追加予定）

### プログラミングカテゴリ
（今後追加予定）

---

## 今後の拡張案

### 1. 問題管理機能
**目的**: 管理者が簡単に問題を追加・編集できるようにする

**機能**:
- 管理者ログイン機能
- 問題CRUD（作成・読取・更新・削除）画面
- カテゴリ管理画面
- 問題のインポート/エクスポート（CSV, JSON形式）
- 問題のプレビュー機能
- バージョン管理（問題の変更履歴）

**実装時の考慮点**:
- 認証・認可の実装（Flask-Loginなど）
- 管理画面用のUIフレームワーク（Flask-Adminなど）
- バリデーション強化

### 2. 難易度調整機能
**目的**: 学習者のレベルに応じた出題を可能にする

**機能**:
- 問題に難易度レベル（1-5）を設定
- ユーザーレベル別の出題フィルター
  - 初級: 難易度1-2
  - 中級: 難易度2-4
  - 上級: 難易度3-5
- アダプティブ学習（正答率に応じて難易度を自動調整）
- 難易度別の統計表示

**実装時の考慮点**:
- 問題データへの難易度カラム追加（既に設計済み）
- ユーザープロファイル機能（レベル保存）
- アダプティブアルゴリズムの設計

### 3. 検索機能
**目的**: 特定の用語や分野の問題を素早く見つける

**機能**:
- キーワード検索（問題文、解説、用語名）
- タグ機能（複数タグを問題に付与）
- カテゴリ横断検索
- 検索結果のフィルタリング（難易度、正答率など）
- 検索履歴の保存

**実装時の考慮点**:
- 全文検索エンジンの導入（Elasticsearch、PostgreSQL Full Text Searchなど）
- タグテーブルの追加
- 検索パフォーマンスの最適化（インデックス）

### 4. 学習履歴・統計機能
**目的**: 学習の進捗を可視化し、モチベーションを向上させる

**機能**:
- ユーザー登録/ログイン機能
- 過去の成績グラフ（折れ線グラフ、レーダーチャート）
- カテゴリ別の正答率
- 苦手分野の分析
- 学習時間の記録
- バッジ・実績システム（連続ログイン、100問達成など）

**実装時の考慮点**:
- ユーザーテーブルの追加
- セッションとユーザーの紐付け
- グラフライブラリ（Chart.js、D3.jsなど）
- GDPR対応（データ削除機能）

### 5. ソーシャル機能
**目的**: 学習者同士のコミュニケーションを促進

**機能**:
- スコアランキング（日次、週次、月次）
- 問題へのコメント機能
- 解説の評価（いいね、役立った）
- 問題の共有（SNS連携）
- 学習グループ機能

**実装時の考慮点**:
- コメント管理（スパム対策）
- リアルタイム更新（WebSocket）
- プライバシー設定
- SNS API連携（Twitter、Facebookなど）

### 6. モバイルアプリ化
**目的**: スマートフォンでの学習体験を向上

**技術選択肢**:
- PWA（Progressive Web App）: 既存のWeb技術を活用
- React Native / Flutter: ネイティブアプリとして配信

**機能**:
- オフライン学習（Service Workerでキャッシュ）
- プッシュ通知（学習リマインダー）
- ホーム画面への追加
- タッチジェスチャー最適化

### 7. 多言語対応
**目的**: 国際的な利用を可能にする

**機能**:
- UI多言語化（英語、中国語など）
- 問題コンテンツの多言語版
- 言語切り替え機能

**実装時の考慮点**:
- Flask-Babelの導入
- 翻訳ファイル管理（.po形式）
- データベース設計（問題の多言語対応）

### 8. AI機能の統合
**目的**: AIを活用した学習支援

**機能**:
- 問題の自動生成（GPT-4など）
- 解説の自動改善（わかりやすさの向上）
- チャットボット（学習サポート）
- 問題の難易度自動判定

**実装時の考慮点**:
- OpenAI API連携
- プロンプトエンジニアリング
- コスト管理
- 生成コンテンツの品質チェック

### 9. アクセシビリティの更なる向上
**目的**: より多くの人が利用できるようにする

**機能**:
- ハイコントラストモード
- フォントサイズ調整
- 音声読み上げ機能の強化
- ダークモード
- ディスレクシア対応フォント

**実装時の考慮点**:
- CSS変数での色管理
- ARIA属性の徹底
- 自動テストツール（axe、Lighthouse）

### 10. ゲーミフィケーション要素の強化
**目的**: 学習の継続性を高める

**機能**:
- レベルアップシステム
- 連続学習ボーナス
- デイリーチャレンジ
- タイムアタックモード
- 対戦モード（2人プレイ）
- リーダーボード

**実装時の考慮点**:
- ポイント計算ロジック
- 不正防止（チート対策）
- バランス調整

---

## 開発スケジュール（例）

### フェーズ1: MVP開発（4週間）
- Week 1: データベース設計、モデル実装、初期データ作成
- Week 2: 基本画面実装（トップ、カテゴリ選択、クイズ実行）
- Week 3: API実装、JavaScript機能実装（タイマー、効果音）
- Week 4: 結果画面、復習モード、テスト、バグ修正

### フェーズ2: 機能拡張（2週間）
- Week 5: アクセシビリティ強化、UI/UX改善
- Week 6: 用語参考リンク集、スコア共有機能、ドキュメント整備

### フェーズ3: 運用準備（1週間）
- Week 7: 本番環境構築（Docker）、デプロイ、監視設定

---

## デプロイ構成

### 開発環境
```yaml
# docker-compose.yml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DATABASE_URL=mysql+pymysql://user:password@db:3306/quiz_app
    volumes:
      - .:/app
    depends_on:
      - db
  
  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=quiz_app
      - MYSQL_USER=user
      - MYSQL_PASSWORD=password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### 本番環境
- **Webサーバー**: Gunicorn + Nginx
- **データベース**: MySQL 8.0（Amazon RDS または Cloud SQLなど）
- **ストレージ**: 静的ファイル用（AWS S3 または Cloud Storageなど）
- **監視**: Sentry（エラートラッキング）、Google Analytics（アクセス解析）

---

## アプリケーションの起動方法

### 前提条件
- Docker Desktop がインストールされていること
- Docker Desktop が起動していること
- ポート5000と3306が使用可能であること

### クイックスタート

#### 1. 起動用シェルスクリプトを使用（推奨）

プロジェクトルートディレクトリで以下のコマンドを実行します：

```bash
# アプリケーションを起動
./start.sh
```

初回起動時は、データベースの初期化が必要です：

```bash
# データベースを初期化（初回のみ）
./init_db.sh
```

その他の便利なコマンド：

```bash
# アプリケーションを停止
./stop.sh

# アプリケーションを再起動
./restart.sh

# ログをリアルタイムで表示
./logs.sh
```

#### 2. Docker Composeを直接使用

シェルスクリプトを使用しない場合は、以下のコマンドで起動できます：

```bash
# コンテナをビルドして起動
docker-compose up -d

# データベースの初期化（初回のみ）
# データベースの起動を待つ（10秒程度）
sleep 10
docker-compose exec web python migrations/seeds/init_data.py

# ログを確認
docker-compose logs -f

# コンテナを停止
docker-compose down
```

### アクセス方法

起動後、以下のURLでアクセスできます：

- **アプリケーション**: http://localhost:5000
- **MySQL**: localhost:3306
  - ユーザー: `quiz_user`
  - パスワード: `quiz_password`
  - データベース: `quiz_db`

### トラブルシューティング

#### ポートが使用中の場合

```bash
# ポート5000を使用しているプロセスを確認
lsof -i :5000

# ポート3306を使用しているプロセスを確認
lsof -i :3306
```

#### コンテナが起動しない場合

```bash
# コンテナの状態を確認
docker-compose ps

# ログを確認
docker-compose logs web
docker-compose logs db

# すべてのコンテナを削除して再起動
docker-compose down -v
docker-compose up -d --build
```

#### データベースの再初期化

```bash
# データベースをリセット
./stop.sh
docker volume rm traning-mbti_mysql_data
./start.sh
./init_db.sh
```

### 開発モード

コードを変更すると自動的に再読み込みされます（Flask の開発モード）。
ただし、テンプレートやJavaScriptファイルの変更は、ブラウザのリロードが必要です。

```bash
# ファイルを変更後、Webコンテナのみ再起動
docker-compose restart web

# またはブラウザでスーパーリロード
# macOS: Cmd + Shift + R
# Windows/Linux: Ctrl + Shift + R
```

### 利用可能なシェルスクリプト一覧

| スクリプト | 説明 |
|----------|------|
| `start.sh` | アプリケーションを起動します |
| `stop.sh` | アプリケーションを停止します |
| `restart.sh` | アプリケーションを再起動します |
| `init_db.sh` | データベースを初期化します（既存データは削除されます） |
| `logs.sh` | アプリケーションのログをリアルタイムで表示します |

すべてのスクリプトは実行権限が付与されており、プロジェクトルートディレクトリから実行できます。

---

## まとめ

本設計書では、大学3年生向けのIT用語学習クイズアプリケーションの全体像を示しました。

**主な特徴**:
- アクセシブルで使いやすい日本語UI
- カテゴリ別の効率的な学習
- タイマーや効果音でゲーム感覚の学習
- 復習機能で苦手分野を克服
- 拡張性の高い設計

**技術的なポイント**:
- Flask + Bootstrap によるモダンなWebアプリケーション
- SQLAlchemyによる保守性の高いデータ管理
- アクセシビリティを考慮したHTML/CSS/JavaScript
- セキュリティベストプラクティスの適用

この設計書を基に実装を進めることで、教育的価値の高いWebアプリケーションを構築できます。

---

**作成日**: 2025年11月6日  
**バージョン**: 1.0  
**ドキュメント形式**: Markdown


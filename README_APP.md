# クイズアプリケーション 要件定義・設計書

## 1. システム概要

本アプリケーションは、IT関連の知識を学習するためのWebベースのクイズアプリケーションです。
ユーザーはカテゴリを選択し、4択形式のクイズに回答することで、セキュリティ、IT基礎、プログラミングなどの知識を習得できます。

### 1.1 主な特徴

- 日本語UIによる直感的な操作
- アクセシビリティに配慮した設計
- カテゴリ別のクイズ出題
- タイマー機能による時間制限
- 効果音によるフィードバック
- 復習モードによる学習効率の向上
- スコア共有機能

## 2. 機能要件

### 2.1 クイズ機能

#### 2.1.1 カテゴリ選択
- **初期カテゴリ**: 以下の3カテゴリが初期設定として用意される
  - セキュリティ
  - IT基礎
  - プログラミング
- ユーザーは開始前にカテゴリを選択可能

#### 2.1.2 出題ロジック
- **出題数**: 各カテゴリから最大20問のプールからランダムに10問を出題
- **順番**: 出題順序はシャッフルされる
- **重複出題**: カテゴリ内の問題数が10問以下の場合、重複出題を許可
  - 例: カテゴリに8問しかない場合、10問出題するために一部の問題が重複して出題される

#### 2.1.3 問題形式
- **形式**: 4択問題
- **表示内容**:
  - 問題文（日本語）
  - 4つの選択肢（A, B, C, D）
  - 正解後の解説（日本語、大学3年生向けのやさしい記述）

#### 2.1.4 回答処理
- ユーザーが選択肢をクリックすると即座に正誤判定
- 正解時: 正解の表示と解説を表示
- 不正解時: 不正解の表示、正解の表示、解説を表示
- 次の問題へ進むボタンで次問へ遷移

### 2.2 タイマー機能

- **デフォルト時間**: 1問あたり30秒
- **可変設定**: タイマー時間は設定で変更可能（将来的な拡張）
- **時間切れ**: 制限時間内に回答がない場合、自動的に不正解として処理
- **表示**: 残り時間を視覚的に表示（プログレスバーまたはカウントダウン表示）

### 2.3 効果音機能

- **ON/OFF切り替え**: ユーザーが効果音の有効/無効を切り替え可能
- **正解音**: 正解時に再生される効果音
- **不正解音**: 不正解時に再生される効果音
- **設定の永続化**: ブラウザのローカルストレージに設定を保存

### 2.4 復習モード

- **対象問題**: 間違えた問題のみを対象とする
- **機能**: クイズ終了後、間違えた問題のみを再度出題
- **出題順序**: 復習モードでも順番はシャッフルされる
- **タイマー**: 復習モードでもタイマー機能は有効

### 2.5 スコア表示・共有機能

#### 2.5.1 スコア表示
- **表示タイミング**: クイズ終了時に表示
- **表示内容**:
  - 正解数 / 総問題数
  - 正答率（パーセンテージ）
  - かかった時間（合計）

#### 2.5.2 復習リスト
- **表示内容**: 間違えた問題の一覧
  - 問題文
  - 選択した回答
  - 正解
  - 解説

#### 2.5.3 スコア共有
- **共有用文字列**: スコア情報をテキスト形式で生成
  - 例: "セキュリティクイズ: 8/10問正解 (80%)"
- **コピー機能**: ワンクリックでクリップボードにコピー
- **用途**: SNSやメッセージアプリでの共有

### 2.6 アクセシビリティ配慮

- **キーボード操作**: すべての機能をキーボードで操作可能
- **スクリーンリーダー対応**: 適切なARIAラベルとセマンティックHTML
- **色覚多様性への配慮**: 色だけでなく、アイコンやテキストでも情報を伝達
- **フォーカス表示**: キーボードフォーカスが視覚的に明確
- **コントラスト比**: WCAG 2.1 AA基準を満たすコントラスト比

## 3. データモデル設計

### 3.1 データベーススキーマ

#### 3.1.1 カテゴリテーブル (Category)

```sql
CREATE TABLE categories (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE COMMENT 'カテゴリ名（例: セキュリティ）',
    description TEXT COMMENT 'カテゴリの説明',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

#### 3.1.2 問題テーブル (Question)

```sql
CREATE TABLE questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    category_id INT NOT NULL,
    question_text TEXT NOT NULL COMMENT '問題文',
    option_a VARCHAR(255) NOT NULL COMMENT '選択肢A',
    option_b VARCHAR(255) NOT NULL COMMENT '選択肢B',
    option_c VARCHAR(255) NOT NULL COMMENT '選択肢C',
    option_d VARCHAR(255) NOT NULL COMMENT '選択肢D',
    correct_answer ENUM('A', 'B', 'C', 'D') NOT NULL COMMENT '正解',
    explanation TEXT NOT NULL COMMENT '解説',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_category_id (category_id)
);
```

#### 3.1.3 クイズ結果テーブル (QuizResult)

```sql
CREATE TABLE quiz_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT COMMENT 'ユーザーID（ログイン機能実装時に使用）',
    category_id INT NOT NULL,
    total_questions INT NOT NULL COMMENT '総問題数',
    correct_answers INT NOT NULL COMMENT '正解数',
    score_percentage DECIMAL(5,2) NOT NULL COMMENT '正答率',
    time_taken INT COMMENT 'かかった時間（秒）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_category_id (category_id),
    INDEX idx_created_at (created_at)
);
```

#### 3.1.4 回答詳細テーブル (AnswerDetail)

```sql
CREATE TABLE answer_details (
    id INT PRIMARY KEY AUTO_INCREMENT,
    quiz_result_id INT NOT NULL,
    question_id INT NOT NULL,
    user_answer ENUM('A', 'B', 'C', 'D') NOT NULL COMMENT 'ユーザーの回答',
    is_correct BOOLEAN NOT NULL COMMENT '正解かどうか',
    time_taken INT COMMENT '回答にかかった時間（秒）',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (quiz_result_id) REFERENCES quiz_results(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE,
    INDEX idx_quiz_result_id (quiz_result_id),
    INDEX idx_question_id (question_id)
);
```

### 3.2 SQLAlchemyモデル設計

#### 3.2.1 Categoryモデル

```python
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # リレーション
    questions = db.relationship('Question', backref='category', lazy=True, cascade='all, delete-orphan')
```

#### 3.2.2 Questionモデル

```python
class Question(db.Model):
    __tablename__ = 'questions'
    
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.String(255), nullable=False)
    option_b = db.Column(db.String(255), nullable=False)
    option_c = db.Column(db.String(255), nullable=False)
    option_d = db.Column(db.String(255), nullable=False)
    correct_answer = db.Column(db.Enum('A', 'B', 'C', 'D'), nullable=False)
    explanation = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

#### 3.2.3 QuizResultモデル

```python
class QuizResult(db.Model):
    __tablename__ = 'quiz_results'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)  # 将来的に使用
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False)
    total_questions = db.Column(db.Integer, nullable=False)
    correct_answers = db.Column(db.Integer, nullable=False)
    score_percentage = db.Column(db.Numeric(5, 2), nullable=False)
    time_taken = db.Column(db.Integer)  # 秒単位
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # リレーション
    answer_details = db.relationship('AnswerDetail', backref='quiz_result', lazy=True, cascade='all, delete-orphan')
```

#### 3.2.4 AnswerDetailモデル

```python
class AnswerDetail(db.Model):
    __tablename__ = 'answer_details'
    
    id = db.Column(db.Integer, primary_key=True)
    quiz_result_id = db.Column(db.Integer, db.ForeignKey('quiz_results.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    user_answer = db.Column(db.Enum('A', 'B', 'C', 'D'), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    time_taken = db.Column(db.Integer)  # 秒単位
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
```

## 4. 画面設計

### 4.1 画面一覧

1. **トップページ** (`/`)
   - カテゴリ選択画面
   - アプリの説明
   - 設定（効果音ON/OFF、タイマー設定）

2. **クイズ画面** (`/quiz/<category_id>`)
   - 問題表示エリア
   - 選択肢ボタン（4つ）
   - タイマー表示
   - 進捗バー（現在の問題番号 / 総問題数）
   - 効果音設定ボタン

3. **結果表示画面** (`/result/<quiz_result_id>`)
   - スコア表示
   - 復習リスト
   - スコアコピーボタン
   - 復習モード開始ボタン
   - トップに戻るボタン

4. **復習モード画面** (`/review/<quiz_result_id>`)
   - クイズ画面と同様のレイアウト
   - 間違えた問題のみを出題

### 4.2 UI/UX設計

#### 4.2.1 レイアウト
- **フレームワーク**: Bootstrap 5.x
- **レスポンシブデザイン**: モバイル、タブレット、デスクトップに対応
- **カラースキーム**: 
  - プライマリカラー: 青系（信頼感）
  - 成功: 緑（正解時）
  - 警告: 赤（不正解時）
  - 背景: 白またはライトグレー

#### 4.2.2 コンポーネント

**カテゴリカード**
- カテゴリ名
- 問題数表示
- カテゴリ説明
- 開始ボタン

**問題カード**
- 問題番号表示
- 問題文（大きなフォント）
- 4つの選択肢ボタン（等幅、大きなクリック領域）
- タイマー表示（プログレスバー形式）

**結果カード**
- スコア表示（大きな数字）
- 正答率（円グラフまたはプログレスバー）
- 復習リスト（アコーディオン形式）

## 5. 技術スタック

### 5.1 バックエンド
- **言語**: Python 3.12
- **フレームワーク**: Flask 3.1.2
- **ORM**: SQLAlchemy (Flask-SQLAlchemy 3.1.1)
- **データベースマイグレーション**: Flask-Migrate 4.1.0
- **データベース**: MySQL (PyMySQL 1.1.2)
- **環境変数管理**: python-dotenv 1.1.1
- **本番サーバー**: Gunicorn 23.0.0
- **暗号化**: cryptography 46.0.3

### 5.2 フロントエンド
- **CSSフレームワーク**: Bootstrap 5.x (CDN)
- **JavaScript**: バニラJavaScript（フレームワーク不使用）
- **効果音**: Web Audio API または HTML5 Audio

### 5.3 インフラ
- **コンテナ**: Docker
- **オーケストレーション**: Docker Compose
- **データベース**: MySQL 8.0

## 6. ファイル構成

```
traning-mbti/
├── app/
│   ├── __init__.py                 # Flaskアプリケーション初期化
│   ├── models.py                    # SQLAlchemyモデル定義
│   ├── routes.py                    # ルーティング定義
│   ├── forms.py                     # WTFormsフォーム定義（将来的に使用）
│   ├── utils.py                     # ユーティリティ関数
│   ├── templates/
│   │   ├── base.html                # ベーステンプレート
│   │   ├── index.html               # トップページ（カテゴリ選択）
│   │   ├── quiz.html                # クイズ画面
│   │   ├── result.html              # 結果表示画面
│   │   └── review.html              # 復習モード画面
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css            # カスタムCSS
│   │   ├── js/
│   │   │   ├── quiz.js              # クイズ画面のJavaScript
│   │   │   ├── timer.js             # タイマー機能
│   │   │   └── audio.js             # 効果音管理
│   │   └── audio/
│   │       ├── correct.mp3          # 正解音
│   │       └── incorrect.mp3        # 不正解音
│   └── data/
│       └── initial_data.py          # 初期データ投入スクリプト
├── docker/
│   ├── Dockerfile                   # アプリケーション用Dockerfile
│   └── docker-compose.yml           # Docker Compose設定
├── scripts/
│   ├── init_db.py                   # データベース初期化スクリプト
│   ├── seed_data.py                 # 初期データ投入スクリプト
│   └── start.sh                     # 起動用ラッパーシェル
├── migrations/                      # Flask-Migrateマイグレーションファイル
├── tests/                           # テストファイル
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_routes.py
│   └── test_utils.py
├── .env.example                     # 環境変数テンプレート
├── .gitignore
├── pyproject.toml                   # Poetry設定
├── poetry.lock                      # Poetry依存関係ロック
├── README.md                        # プロジェクト説明
└── README_APP.md                    # 本設計書
```

## 7. ルーティング設計

### 7.1 ルート定義

| メソッド | パス | 関数名 | 説明 |
|---------|------|--------|------|
| GET | `/` | `index()` | トップページ（カテゴリ選択） |
| GET | `/quiz/<int:category_id>` | `start_quiz(category_id)` | クイズ開始（問題をランダム選択してセッションに保存） |
| POST | `/quiz/answer` | `submit_answer()` | 回答送信（AJAX） |
| GET | `/quiz/next` | `next_question()` | 次の問題へ（AJAX） |
| GET | `/result/<int:quiz_result_id>` | `show_result(quiz_result_id)` | 結果表示 |
| GET | `/review/<int:quiz_result_id>` | `review_quiz(quiz_result_id)` | 復習モード開始 |
| POST | `/api/copy-score` | `copy_score()` | スコア文字列をコピー用に返す（AJAX） |

### 7.2 セッション管理

クイズ進行中は以下の情報をセッションに保存：

```python
session['quiz'] = {
    'category_id': int,
    'question_ids': [int, ...],  # 出題される問題IDのリスト（シャッフル済み）
    'current_index': int,         # 現在の問題インデックス
    'answers': {                  # 回答履歴
        question_id: {
            'user_answer': 'A'|'B'|'C'|'D',
            'is_correct': bool,
            'time_taken': int
        }
    },
    'start_time': datetime,       # クイズ開始時刻
    'timer_duration': int         # タイマー時間（秒）
}
```

## 8. 主要な処理フロー

### 8.1 クイズ開始フロー

1. ユーザーがカテゴリを選択
2. `/quiz/<category_id>` にアクセス
3. バックエンドで以下を実行：
   - カテゴリに紐づく問題を全件取得
   - 問題IDリストをシャッフル
   - 最大10問を選択（問題数が10問以下の場合は重複を許可して10問にする）
   - セッションに問題IDリストを保存
4. 最初の問題を表示

### 8.2 回答処理フロー

1. ユーザーが選択肢をクリック
2. JavaScriptで選択を取得
3. AJAXで `/quiz/answer` にPOST送信
   - 問題ID、選択肢、経過時間を送信
4. バックエンドで以下を実行：
   - 正誤判定
   - セッションに回答を保存
   - 正解/不正解、解説を返却
5. フロントエンドで結果を表示
   - 正解/不正解の視覚的フィードバック
   - 解説の表示
   - 効果音の再生（設定がONの場合）
6. 「次へ」ボタンで次の問題へ

### 8.3 クイズ終了フロー

1. 最後の問題に回答後、「結果を見る」ボタンをクリック
2. バックエンドで以下を実行：
   - セッションから回答履歴を取得
   - スコアを計算
   - データベースに結果を保存（QuizResult, AnswerDetail）
   - クイズ結果IDを返却
3. `/result/<quiz_result_id>` にリダイレクト
4. 結果画面を表示

### 8.4 復習モードフロー

1. 結果画面で「復習モード」ボタンをクリック
2. `/review/<quiz_result_id>` にアクセス
3. バックエンドで以下を実行：
   - クイズ結果から間違えた問題IDを取得
   - 問題IDリストをシャッフル
   - セッションに保存
4. クイズ画面と同様のフローで出題

## 9. 初期データ

### 9.1 カテゴリデータ

```python
INITIAL_CATEGORIES = [
    {
        'name': 'セキュリティ',
        'description': '情報セキュリティに関する基礎知識を学びます'
    },
    {
        'name': 'IT基礎',
        'description': 'ITの基礎的な知識を学びます'
    },
    {
        'name': 'プログラミング',
        'description': 'プログラミングの基礎知識を学びます'
    }
]
```

### 9.2 セキュリティカテゴリの問題例

以下の用語をテーマにした問題を最大20問作成：

- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- SQLインジェクション
- パスワードリスト攻撃
- レインボーテーブル
- ゼロトラスト
- 多要素認証
- DPIA (Data Protection Impact Assessment)
- SAST/DAST (Static/Dynamic Application Security Testing)
- CVE/CVSS (Common Vulnerabilities and Exposures / Common Vulnerability Scoring System)
- フィッシング
- スミッシング
- スピアフィッシング
- ランサムウェア
- サプライチェーン攻撃
- ソーシャルエンジニアリング
- セキュアコーディング
- 侵入テスト
- WAF (Web Application Firewall)
- IAM (Identity and Access Management)

**問題作成の指針**:
- 大学3年生向けのやさしい説明
- 4択形式
- 各問題に解説を付与
- 実務で役立つ知識を重視

## 10. 用語の参考リンク集

以下の用語について、学習者がさらに詳しく調べられるよう、参考リンク集をアプリケーション内に用意する。
（実際のリンクは実装時に適切な公式ドキュメントや信頼できる情報源を設定）

### セキュリティ関連

- **XSS (Cross-Site Scripting)**: #
- **CSRF (Cross-Site Request Forgery)**: #
- **SQLインジェクション**: #
- **パスワードリスト攻撃**: #
- **レインボーテーブル**: #
- **ゼロトラスト**: #
- **多要素認証 (MFA)**: #
- **DPIA (Data Protection Impact Assessment)**: #
- **SAST (Static Application Security Testing)**: #
- **DAST (Dynamic Application Security Testing)**: #
- **CVE (Common Vulnerabilities and Exposures)**: #
- **CVSS (Common Vulnerability Scoring System)**: #
- **フィッシング**: #
- **スミッシング**: #
- **スピアフィッシング**: #
- **ランサムウェア**: #
- **サプライチェーン攻撃**: #
- **ソーシャルエンジニアリング**: #
- **セキュアコーディング**: #
- **侵入テスト (Penetration Testing)**: #
- **WAF (Web Application Firewall)**: #
- **IAM (Identity and Access Management)**: #

### IT基礎関連

（IT基礎カテゴリの問題作成時に追加）

### プログラミング関連

（プログラミングカテゴリの問題作成時に追加）

## 11. テスト方法

### 11.1 全問正解の再現手順

1. **テストデータの準備**
   - テスト用のカテゴリと問題を作成
   - すべての問題の正解を事前に把握

2. **テスト実行**
   - アプリケーションを起動
   - テスト用カテゴリを選択
   - クイズを開始
   - すべての問題で正解を選択
   - クイズを完了

3. **検証項目**
   - スコアが 10/10 (100%) と表示されること
   - 復習リストが空であること
   - データベースの `quiz_results` テーブルに正しいスコアが保存されていること
   - データベースの `answer_details` テーブルにすべて `is_correct = true` で保存されていること

### 11.2 全問不正解の再現手順

1. **テストデータの準備**
   - テスト用のカテゴリと問題を作成
   - すべての問題の正解を事前に把握

2. **テスト実行**
   - アプリケーションを起動
   - テスト用カテゴリを選択
   - クイズを開始
   - すべての問題で不正解を選択（正解以外の選択肢を選択）
   - クイズを完了

3. **検証項目**
   - スコアが 0/10 (0%) と表示されること
   - 復習リストにすべての問題が表示されること
   - データベースの `quiz_results` テーブルに正しいスコアが保存されていること
   - データベースの `answer_details` テーブルにすべて `is_correct = false` で保存されていること

### 11.3 その他のテストケース

- **タイマー機能**: 制限時間内に回答しない場合、自動的に不正解として処理されること
- **効果音機能**: ON/OFF設定が正しく動作すること
- **重複出題**: 問題数が10問以下の場合、重複して出題されること
- **復習モード**: 間違えた問題のみが復習モードで出題されること
- **スコアコピー**: スコア文字列が正しくクリップボードにコピーされること
- **アクセシビリティ**: キーボード操作で全機能が使用可能であること

## 12. 今後の拡張案

### 12.1 問題追加機能

- **管理画面**: 管理者が問題を追加・編集・削除できる機能
- **バルクインポート**: CSVファイルから一括で問題をインポート
- **問題のバージョン管理**: 問題の編集履歴を保持

### 12.2 難易度調整機能

- **難易度レベル**: 各問題に難易度（初級・中級・上級）を設定
- **難易度別出題**: ユーザーが難易度を選択してクイズを受ける
- **適応的出題**: ユーザーの正答率に応じて難易度を自動調整

### 12.3 検索機能

- **問題検索**: キーワードで問題を検索
- **カテゴリ検索**: カテゴリ名で検索
- **用語検索**: 解説文内の用語で検索

### 12.4 その他の拡張案

- **ユーザー認証**: ログイン機能により、個人の学習履歴を管理
- **ランキング機能**: スコアランキングの表示
- **学習進捗**: ユーザーの学習進捗を可視化
- **問題のブックマーク**: 後で復習したい問題をブックマーク
- **カスタムクイズ**: ユーザーが問題を選択してクイズを作成
- **統計機能**: カテゴリ別の正答率、苦手分野の分析
- **多言語対応**: 英語版の追加
- **API提供**: 外部アプリケーションから問題データにアクセス可能なAPI

## 13. 実装時の注意事項

### 13.1 セキュリティ

- **SQLインジェクション対策**: SQLAlchemyのORMを使用することで対策済み
- **XSS対策**: Flaskのテンプレートエンジン（Jinja2）の自動エスケープ機能を活用
- **CSRF対策**: 重要な操作にはCSRFトークンを実装（将来的に）

### 13.2 パフォーマンス

- **データベースクエリの最適化**: N+1問題を避けるため、`joinedload` などを使用
- **セッション管理**: セッションサイズを適切に管理
- **静的ファイルのキャッシュ**: 本番環境では適切なキャッシュヘッダーを設定

### 13.3 コード品質

- **コメント**: すべての関数とクラスに適切なdocstringを記述
- **エラーハンドリング**: 適切な例外処理とエラーメッセージ
- **ログ出力**: 重要な操作にはログを出力

## 14. 起動方法

### 14.1 環境変数の設定

`.env.example`を`.env`にコピーし、必要に応じて編集してください。

```bash
cp .env.example .env
```

### 14.2 Docker Composeを使用する場合（推奨）

```bash
# 起動用スクリプトを実行
./scripts/start.sh

# または、直接Docker Composeを使用
cd docker
docker-compose up --build
```

アプリケーションは `http://localhost:5000` でアクセスできます。

### 14.3 ローカル環境で起動する場合

1. **環境変数の設定**
   ```bash
   export USE_DOCKER=false
   ```

2. **データベースの起動**
   MySQLをローカルで起動し、`.env`で指定したデータベースとユーザーを作成してください。

3. **依存関係のインストール**
   ```bash
   poetry install
   ```

4. **データベースの初期化**
   ```bash
   poetry run python scripts/init_db.py
   ```

5. **アプリケーションの起動**
   ```bash
   poetry run python wsgi.py
   ```

### 14.4 停止方法

Docker Composeを使用している場合:
```bash
cd docker
docker-compose down
```

データベースのボリュームも削除する場合:
```bash
cd docker
docker-compose down -v
```

### 14.5 効果音ファイルについて

効果音機能を使用するには、以下のファイルを配置してください：
- `app/static/audio/correct.mp3` - 正解時の効果音
- `app/static/audio/incorrect.mp3` - 不正解時の効果音

これらのファイルが存在しない場合でも、アプリケーションは正常に動作しますが、効果音は再生されません。
効果音ファイルは、適切なライセンスの下で使用可能な音声ファイルを用意してください。

---

**作成日**: 2024年
**バージョン**: 1.0
**作成者**: システム設計チーム


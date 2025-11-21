# クイズアプリケーション 設計書

## クイックスタート

### 簡単な起動方法

```bash
# 起動スクリプトを実行（推奨）
./scripts/start.sh
```

起動後、ブラウザで `http://localhost:5000` にアクセスしてください。

**デフォルト管理者アカウント：**
- ユーザーID: `admin`
- パスワード: `admin123`

詳細な起動方法は「[13. 起動方法](#13-起動方法)」を参照してください。

---

## 1. システム概要

本アプリケーションは、IT関連の知識を学習するためのWebベースのクイズアプリケーションです。ユーザーはカテゴリを選択して4択クイズに回答し、学習を進めることができます。管理者はクイズやカテゴリの管理、ユーザー管理を行うことができます。

### 1.1 主な特徴

- 日本語UIによる直感的な操作
- アクセシビリティに配慮した設計
- リアルタイムタイマー機能
- 効果音によるフィードバック
- 復習モードによる学習効率の向上
- スコア共有機能

## 2. 機能要件

### 2.1 クイズ機能

#### 2.1.1 クイズ形式
- **形式**: 4択問題
- **カテゴリ選択**: ユーザーは複数のカテゴリから選択可能
- **初期カテゴリ**:
  - セキュリティ
  - IT基礎
  - プログラミング

#### 2.1.2 出題ロジック
- **出題数**: 最大20問のプールからランダムに10問を選択
- **順番**: 選択された問題はシャッフルして出題
- **重複出題**: 全問題数が10問以下の場合、重複出題を許可（同じ問題が複数回出題される可能性がある）

#### 2.1.3 解説機能
- 各問題の正解後、日本語による解説を表示
- 解説は大学3年生向けのやさしい記述で提供

#### 2.1.4 結果表示
- クイズ終了時にスコア（正解数/総問題数、正答率）を表示
- 間違えた問題のリスト（復習リスト）を提示
- 復習リストから直接復習モードに移行可能

### 2.2 タイマー機能

- **デフォルト時間**: 1問あたり30秒
- **可変設定**: タイマー時間は設定で変更可能
- **時間切れ処理**: 時間切れの場合は自動的に次の問題へ進む（不正解として扱う）

### 2.3 効果音機能

- **ON/OFF切り替え**: ユーザーが効果音の有効/無効を切り替え可能
- **正解音**: 正解時に再生される効果音
- **不正解音**: 不正解時に再生される効果音
- **設定の永続化**: ブラウザのローカルストレージに設定を保存

### 2.4 復習モード

- **対象問題**: 間違えた問題のみを対象
- **出題順序**: 間違えた問題を順番に再出題
- **解説表示**: 復習モードでも解説を表示
- **スコア記録**: 復習モードの結果は通常のクイズ結果とは別に記録

### 2.5 スコア共有機能

- **スコア文字列生成**: クイズ結果を共有用の文字列として生成
- **コピー機能**: ワンクリックでクリップボードにコピー
- **フォーマット例**: 「セキュリティクイズ: 8/10問正解 (80%)」

### 2.6 ユーザー認証機能

#### 2.6.1 ログイン/ログアウト
- **ログイン**: ユーザーIDとパスワードによる認証
- **ログアウト**: セッションを終了
- **セッション管理**: Flaskのセッション機能を使用

#### 2.6.2 ユーザー登録
- **必須項目**:
  - ユーザーID（一意である必要がある）
  - メールアドレス（一意である必要がある）
  - パスワード（適切な強度チェック）
- **バリデーション**: フロントエンドとバックエンドの両方で検証

### 2.7 ユーザーロール機能

#### 2.7.1 一般ユーザー
- 自分のクイズ履歴の確認
- レビューの投稿・閲覧
- クイズの実施

#### 2.7.2 管理者
- 全ユーザーのクイズ履歴の確認
- レビューの管理（一覧表示、詳細表示、削除）
- ユーザー管理（一覧表示、詳細表示、情報・ロール変更、削除）
- クイズ管理（カテゴリの作成・修正・削除、クイズの作成・修正・削除）

#### 2.7.3 デフォルト管理者
- **ユーザーID**: admin
- **メールアドレス**: admin@example.com
- **パスワード**: admin123
- 初回起動時に自動的に作成される

### 2.8 レビュー機能

- **投稿**: ログイン済みユーザーがレビューを投稿可能
- **表示**: 全ユーザーがレビューを閲覧可能
- **管理**: 管理者がレビューの削除が可能

## 3. 非機能要件

### 3.1 アクセシビリティ

- **キーボード操作**: すべての機能をキーボードで操作可能
- **スクリーンリーダー対応**: 適切なARIAラベルとセマンティックHTMLを使用
- **色のコントラスト**: WCAG 2.1 AAレベル以上のコントラスト比を確保
- **フォーカス表示**: キーボードフォーカスが視覚的に明確
- **代替テキスト**: 画像には適切な代替テキストを設定

### 3.2 パフォーマンス

- **レスポンス時間**: ページ遷移は1秒以内
- **クイズ開始**: カテゴリ選択からクイズ開始まで2秒以内
- **データベースクエリ**: 最適化されたクエリを使用

### 3.3 セキュリティ

- **パスワードハッシュ化**: bcrypt等を使用した安全なパスワード保存
- **SQLインジェクション対策**: パラメータ化クエリの使用
- **XSS対策**: ユーザー入力の適切なエスケープ
- **CSRF対策**: CSRFトークンの実装
- **セッション管理**: 安全なセッション管理

### 3.4 ブラウザ対応

- **対応ブラウザ**: 
  - Chrome（最新版）
  - Firefox（最新版）
  - Safari（最新版）
  - Edge（最新版）

## 4. データベース設計

### 4.1 テーブル構成

#### 4.1.1 users（ユーザーテーブル）
```sql
- id: INT PRIMARY KEY AUTO_INCREMENT
- user_id: VARCHAR(50) UNIQUE NOT NULL
- email: VARCHAR(255) UNIQUE NOT NULL
- password_hash: VARCHAR(255) NOT NULL
- role: ENUM('user', 'admin') DEFAULT 'user'
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- updated_at: DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

#### 4.1.2 categories（カテゴリテーブル）
```sql
- id: INT PRIMARY KEY AUTO_INCREMENT
- name: VARCHAR(100) NOT NULL
- description: TEXT
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- updated_at: DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
```

#### 4.1.3 quizzes（クイズテーブル）
```sql
- id: INT PRIMARY KEY AUTO_INCREMENT
- category_id: INT NOT NULL
- question: TEXT NOT NULL
- option1: VARCHAR(255) NOT NULL
- option2: VARCHAR(255) NOT NULL
- option3: VARCHAR(255) NOT NULL
- option4: VARCHAR(255) NOT NULL
- correct_answer: INT NOT NULL (1-4)
- explanation: TEXT NOT NULL
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- updated_at: DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
- FOREIGN KEY (category_id) REFERENCES categories(id)
```

#### 4.1.4 quiz_results（クイズ結果テーブル）
```sql
- id: INT PRIMARY KEY AUTO_INCREMENT
- user_id: INT NOT NULL
- category_id: INT NOT NULL
- score: INT NOT NULL
- total_questions: INT NOT NULL
- is_review_mode: BOOLEAN DEFAULT FALSE
- completed_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- FOREIGN KEY (user_id) REFERENCES users(id)
- FOREIGN KEY (category_id) REFERENCES categories(id)
```

#### 4.1.5 quiz_answers（回答詳細テーブル）
```sql
- id: INT PRIMARY KEY AUTO_INCREMENT
- quiz_result_id: INT NOT NULL
- quiz_id: INT NOT NULL
- user_answer: INT NOT NULL (1-4)
- is_correct: BOOLEAN NOT NULL
- answered_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- FOREIGN KEY (quiz_result_id) REFERENCES quiz_results(id)
- FOREIGN KEY (quiz_id) REFERENCES quizzes(id)
```

#### 4.1.6 reviews（レビューテーブル）
```sql
- id: INT PRIMARY KEY AUTO_INCREMENT
- user_id: INT NOT NULL
- title: VARCHAR(255) NOT NULL
- content: TEXT NOT NULL
- rating: INT (1-5)
- created_at: DATETIME DEFAULT CURRENT_TIMESTAMP
- updated_at: DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
- FOREIGN KEY (user_id) REFERENCES users(id)
```

### 4.2 初期データ

#### 4.2.1 カテゴリ初期データ
- セキュリティ
- IT基礎
- プログラミング

#### 4.2.2 クイズ初期データ
各カテゴリに最大20問のクイズを用意

**セキュリティカテゴリの用語例**:
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- SQLインジェクション
- パスワードリスト攻撃
- レインボーテーブル
- ゼロトラスト
- 多要素認証
- DPIA (Data Protection Impact Assessment)
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
- WAF (Web Application Firewall)
- IAM (Identity and Access Management)

## 5. 画面設計

### 5.1 画面一覧

#### 5.1.1 未認証ユーザー向け画面
1. **トップページ** (`/`)
   - アプリケーションの説明
   - ログイン/新規登録へのリンク
   - クイズ開始ボタン（ログイン必須）

2. **ログインページ** (`/login`)
   - ユーザーID入力欄
   - パスワード入力欄
   - ログインボタン
   - 新規登録へのリンク

3. **新規登録ページ** (`/register`)
   - ユーザーID入力欄
   - メールアドレス入力欄
   - パスワード入力欄
   - パスワード確認入力欄
   - 登録ボタン

#### 5.1.2 認証済みユーザー向け画面
4. **ダッシュボード** (`/dashboard`)
   - ユーザー情報表示
   - 最近のクイズ結果
   - クイズ開始ボタン

5. **カテゴリ選択ページ** (`/quiz/select`)
   - カテゴリ一覧表示
   - 各カテゴリの説明
   - カテゴリ選択ボタン

6. **クイズ実施ページ** (`/quiz/<category_id>`)
   - 進捗バー（現在位置/総数、正解/不正解で色分け）
   - 問題文表示
   - 4つの選択肢ボタン
   - タイマー表示
   - 効果音ON/OFF切り替えボタン
   - スキップボタン（時間切れ時）

7. **解説ページ** (`/quiz/<category_id>/explanation`)
   - 問題文再表示
   - 選択した答えと正解の表示
   - 解説テキスト
   - 次の問題へボタン

8. **結果ページ** (`/quiz/<category_id>/result`)
   - スコア表示（正解数/総問題数、正答率）
   - 復習リスト（間違えた問題一覧）
   - 復習モード開始ボタン
   - スコアコピーボタン
   - ダッシュボードへ戻るボタン

9. **履歴ページ** (`/history`)
   - 自分のクイズ履歴一覧
   - カテゴリ別フィルタ
   - 詳細表示リンク

10. **レビュー一覧ページ** (`/reviews`)
    - レビュー一覧表示
    - レビュー投稿ボタン

11. **レビュー投稿ページ** (`/reviews/new`)
    - タイトル入力欄
    - 内容入力欄
    - 評価選択（1-5）
    - 投稿ボタン

#### 5.1.3 管理者向け画面
12. **管理ダッシュボード** (`/admin`)
    - 統計情報表示
    - 各管理機能へのリンク

13. **ユーザー管理ページ** (`/admin/users`)
    - ユーザー一覧表示
    - 検索機能
    - ユーザー詳細表示
    - ユーザー情報編集
    - ユーザー削除

14. **クイズ管理ページ** (`/admin/quizzes`)
    - カテゴリ一覧
    - カテゴリ作成・編集・削除
    - クイズ一覧（カテゴリ別）
    - クイズ作成・編集・削除

15. **レビュー管理ページ** (`/admin/reviews`)
    - レビュー一覧表示
    - レビュー詳細表示
    - レビュー削除

16. **全ユーザー履歴ページ** (`/admin/history`)
    - 全ユーザーのクイズ履歴一覧
    - ユーザー別フィルタ
    - カテゴリ別フィルタ

### 5.2 UI/UX設計

#### 5.2.1 デザイン原則
- **シンプルで直感的**: 迷わず操作できるUI
- **視覚的フィードバック**: 操作に対する明確な反応
- **レスポンシブデザイン**: モバイル・タブレット・PCに対応
- **Bootstrap**: Bootstrap 5を使用した統一されたデザイン

#### 5.2.2 カラースキーム
- **プライマリカラー**: Bootstrapのデフォルト（青系）
- **成功**: 緑（正解時）
- **警告**: オレンジ（時間切れ）
- **危険**: 赤（不正解時）
- **情報**: 青（解説表示時）

#### 5.2.3 進捗バー
- **正解時**: 緑色で表示
- **不正解時**: 赤色で表示
- **未回答**: グレーで表示
- **現在位置**: ハイライト表示

## 6. API設計

### 6.1 エンドポイント一覧

#### 6.1.1 認証関連
- `POST /api/login` - ログイン
- `POST /api/logout` - ログアウト
- `POST /api/register` - 新規登録

#### 6.1.2 クイズ関連
- `GET /api/categories` - カテゴリ一覧取得
- `GET /api/quiz/<category_id>/questions` - クイズ問題取得（10問）
- `POST /api/quiz/<category_id>/answer` - 回答送信
- `POST /api/quiz/<category_id>/result` - 結果保存
- `GET /api/quiz/<category_id>/review` - 復習モード用問題取得

#### 6.1.3 履歴関連
- `GET /api/history` - 自分の履歴取得
- `GET /api/history/<result_id>` - 履歴詳細取得

#### 6.1.4 レビュー関連
- `GET /api/reviews` - レビュー一覧取得
- `POST /api/reviews` - レビュー投稿
- `DELETE /api/reviews/<review_id>` - レビュー削除（管理者のみ）

#### 6.1.5 管理機能関連（管理者のみ）
- `GET /api/admin/users` - ユーザー一覧取得
- `GET /api/admin/users/<user_id>` - ユーザー詳細取得
- `PUT /api/admin/users/<user_id>` - ユーザー情報更新
- `DELETE /api/admin/users/<user_id>` - ユーザー削除
- `POST /api/admin/categories` - カテゴリ作成
- `PUT /api/admin/categories/<category_id>` - カテゴリ更新
- `DELETE /api/admin/categories/<category_id>` - カテゴリ削除
- `POST /api/admin/quizzes` - クイズ作成
- `PUT /api/admin/quizzes/<quiz_id>` - クイズ更新
- `DELETE /api/admin/quizzes/<quiz_id>` - クイズ削除
- `GET /api/admin/history` - 全ユーザー履歴取得

## 7. 技術スタック

### 7.1 バックエンド
- **言語**: Python 3.12
- **フレームワーク**: Flask 3.1.2
- **ORM**: SQLAlchemy (Flask-SQLAlchemy 3.1.1)
- **マイグレーション**: Flask-Migrate 4.1.0
- **データベースドライバ**: PyMySQL 1.1.2
- **環境変数管理**: python-dotenv 1.1.1
- **WSGIサーバー**: Gunicorn 23.0.0
- **暗号化**: cryptography 46.0.3

### 7.2 フロントエンド
- **CSSフレームワーク**: Bootstrap 5
- **JavaScript**: バニラJavaScript（必要に応じて）
- **音声**: Web Audio API

### 7.3 インフラ
- **コンテナ**: Docker
- **オーケストレーション**: Docker Compose
- **データベース**: MySQL 8.0

### 7.4 開発ツール
- **パッケージ管理**: Poetry
- **Python環境**: pyenv
- **テスト**: pytest 8.4.2, pytest-flask 1.3.0
- **リンター**: flake8 7.3.0
- **フォーマッター**: black 25.9.0

## 8. ディレクトリ構成

```
traning-mbti/
├── app/                          # アプリケーション本体
│   ├── __init__.py              # Flaskアプリケーション初期化
│   ├── models.py                # データベースモデル
│   ├── routes/                   # ルーティング
│   │   ├── __init__.py
│   │   ├── auth.py              # 認証関連ルート
│   │   ├── quiz.py              # クイズ関連ルート
│   │   ├── history.py           # 履歴関連ルート
│   │   ├── review.py            # レビュー関連ルート
│   │   └── admin.py             # 管理機能関連ルート
│   ├── templates/                # Jinja2テンプレート
│   │   ├── base.html            # ベーステンプレート
│   │   ├── auth/
│   │   │   ├── login.html
│   │   │   └── register.html
│   │   ├── quiz/
│   │   │   ├── select.html
│   │   │   ├── question.html
│   │   │   ├── explanation.html
│   │   │   └── result.html
│   │   ├── history/
│   │   │   └── list.html
│   │   ├── review/
│   │   │   ├── list.html
│   │   │   └── new.html
│   │   └── admin/
│   │       ├── dashboard.html
│   │       ├── users.html
│   │       ├── quizzes.html
│   │       └── reviews.html
│   ├── static/                   # 静的ファイル
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── quiz.js
│   │   │   ├── timer.js
│   │   │   └── sound.js
│   │   └── sounds/
│   │       ├── correct.mp3
│   │       └── incorrect.mp3
│   ├── utils/                    # ユーティリティ
│   │   ├── __init__.py
│   │   ├── auth.py              # 認証関連ユーティリティ
│   │   └── quiz.py              # クイズ関連ユーティリティ
│   └── data/                     # 初期データ
│       └── initial_data.py      # 初期データ投入スクリプト
├── scripts/                      # スクリプト
│   ├── start.sh                 # 起動スクリプト
│   ├── stop.sh                  # 停止スクリプト
│   ├── init_db.sh               # データベース初期化スクリプト
│   └── seed_data.py             # 初期データ投入
├── docker/                       # Docker関連ファイル
│   ├── Dockerfile               # アプリケーション用Dockerfile
│   ├── docker-compose.yml       # Docker Compose設定
│   └── mysql/
│       ├── Dockerfile           # MySQL用Dockerfile（必要に応じて）
│       └── init.sql             # データベース初期化SQL
├── migrations/                   # データベースマイグレーション
├── tests/                        # テストファイル
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_quiz.py
│   └── test_admin.py
├── .env.example                  # 環境変数サンプル
├── .gitignore
├── pyproject.toml                # Poetry設定
├── poetry.lock                   # Poetry依存関係ロック
├── README.md                     # プロジェクトREADME
└── README_APP.md                 # 本設計書
```

## 9. 実装方針

### 9.1 コーディング規約

- **コメント**: すべての関数・クラスにdocstringを記述
- **命名規則**: 
  - 関数・変数: snake_case
  - クラス: PascalCase
  - 定数: UPPER_SNAKE_CASE
- **コードフォーマット**: blackを使用
- **リンター**: flake8を使用

### 9.2 セキュリティ実装

- **パスワードハッシュ化**: Werkzeugの`generate_password_hash`を使用
- **SQLインジェクション対策**: SQLAlchemyのORMを使用（生SQLは使用しない）
- **XSS対策**: Jinja2の自動エスケープ機能を活用
- **CSRF対策**: Flask-WTFまたは手動実装
- **セッション管理**: Flaskのセッション機能を使用、セッションタイムアウトを設定

### 9.3 エラーハンドリング

- **404エラー**: カスタム404ページを用意
- **500エラー**: カスタム500ページを用意（本番環境では詳細情報を非表示）
- **バリデーションエラー**: 適切なエラーメッセージを表示
- **ログ記録**: Pythonのloggingモジュールを使用

### 9.4 パフォーマンス最適化

- **データベースクエリ**: N+1問題を避けるため、適切なJOINを使用
- **キャッシュ**: 頻繁にアクセスされるデータ（カテゴリ一覧など）はキャッシュ
- **静的ファイル**: Nginx等のリバースプロキシで配信（本番環境）

## 10. テスト方法

### 10.1 全問正解の再現手順

1. **テストデータの準備**
   - テスト用ユーザーアカウントを作成
   - 特定のカテゴリに10問のクイズを用意（正解が分かっている問題）

2. **テスト実行**
   - ログイン
   - カテゴリ選択
   - クイズ開始
   - すべての問題で正解を選択
   - 結果ページで「10/10問正解 (100%)」を確認
   - 復習リストが空であることを確認

3. **検証ポイント**
   - スコアが正確に記録されているか
   - データベースに正しい結果が保存されているか
   - 履歴ページに正しい結果が表示されているか

### 10.2 全問不正解の再現手順

1. **テストデータの準備**
   - テスト用ユーザーアカウントを作成
   - 特定のカテゴリに10問のクイズを用意

2. **テスト実行**
   - ログイン
   - カテゴリ選択
   - クイズ開始
   - すべての問題で不正解を選択（正解以外の選択肢を選択）
   - 結果ページで「0/10問正解 (0%)」を確認
   - 復習リストに10問すべてが表示されることを確認

3. **検証ポイント**
   - スコアが正確に記録されているか
   - 復習リストにすべての問題が含まれているか
   - 復習モードで正しく出題されるか

### 10.3 その他のテストケース

- **タイマー機能**: 時間切れ時の動作確認
- **効果音機能**: ON/OFF切り替えの動作確認
- **復習モード**: 間違えた問題のみが表示されるか
- **スコアコピー機能**: クリップボードへのコピーが正常に動作するか
- **アクセシビリティ**: キーボード操作、スクリーンリーダー対応の確認

## 11. 今後の拡張案

### 11.1 問題追加機能の拡張

- **CSVインポート**: 管理者がCSVファイルから一括で問題を追加
- **問題の難易度設定**: 各問題に難易度（初級・中級・上級）を設定
- **問題のタグ機能**: 複数のタグで問題を分類
- **問題の画像対応**: 問題文に画像を添付可能に

### 11.2 難易度調整機能

- **ユーザー別難易度**: ユーザーの実力に応じて問題を自動選択
- **適応的学習**: 正答率に基づいて次回の問題難易度を調整
- **難易度フィルタ**: ユーザーが難易度を指定してクイズを実施

### 11.3 検索機能

- **問題検索**: キーワードで問題を検索
- **カテゴリ検索**: カテゴリ名で検索
- **履歴検索**: 自分の履歴を日付・カテゴリ・スコアで検索
- **高度な検索**: 複数条件を組み合わせた検索

### 11.4 その他の拡張案

- **ランキング機能**: ユーザー間のスコアランキング
- **バッジシステム**: 特定の条件を満たすとバッジを獲得
- **学習統計**: 学習の進捗をグラフで可視化
- **ソーシャル機能**: 友達とスコアを共有、対戦モード
- **多言語対応**: 英語版の追加
- **モバイルアプリ**: React Native等を使用したネイティブアプリ化

## 12. 用語の参考リンク集

### 12.1 セキュリティ関連用語

- **XSS (Cross-Site Scripting)**: #
- **CSRF (Cross-Site Request Forgery)**: #
- **SQLインジェクション**: #
- **パスワードリスト攻撃**: #
- **レインボーテーブル**: #
- **ゼロトラスト**: #
- **多要素認証**: #
- **DPIA (Data Protection Impact Assessment)**: #
- **SAST/DAST**: #
- **CVE/CVSS**: #
- **フィッシング**: #
- **スミッシング**: #
- **スピアフィッシング**: #
- **ランサムウェア**: #
- **サプライチェーン攻撃**: #
- **ソーシャルエンジニアリング**: #
- **セキュアコーディング**: #
- **侵入テスト**: #
- **WAF (Web Application Firewall)**: #
- **IAM (Identity and Access Management)**: #

### 12.2 IT基礎関連用語

- **HTTP/HTTPS**: #
- **DNS**: #
- **TCP/IP**: #
- **OSI参照モデル**: #
- **クラウドコンピューティング**: #
- **仮想化**: #
- **コンテナ**: #
- **API**: #
- **RESTful**: #
- **JSON**: #
- **XML**: #
- **データベース**: #
- **リレーショナルデータベース**: #
- **NoSQL**: #
- **バックアップ**: #
- **ディザスタリカバリ**: #
- **ロードバランサー**: #
- **CDN**: #
- **DevOps**: #
- **CI/CD**: #

### 12.3 プログラミング関連用語

- **変数**: #
- **関数**: #
- **クラス**: #
- **オブジェクト指向**: #
- **継承**: #
- **ポリモーフィズム**: #
- **カプセル化**: #
- **アルゴリズム**: #
- **データ構造**: #
- **再帰**: #
- **例外処理**: #
- **デバッグ**: #
- **バージョン管理**: #
- **Git**: #
- **リファクタリング**: #
- **デザインパターン**: #
- **テスト駆動開発**: #
- **アジャイル開発**: #
- **コードレビュー**: #
- **ドキュメンテーション**: #

---

## 13. 起動方法

### 13.1 初回セットアップ

#### 13.1.1 必要な環境
- Python 3.12以上
- Poetry（パッケージ管理ツール）
- Docker および Docker Compose
- pyenv（推奨）

#### 13.1.2 環境構築手順

1. **Python環境の確認**
   ```bash
   pyenv version  # Python 3.12.2が表示されることを確認
   poetry --version  # Poetryがインストールされていることを確認
   ```

2. **依存関係のインストール**
   ```bash
   poetry install
   ```

3. **環境変数の設定**
   ```bash
   cp .env.example .env
   # .envファイルを編集して必要な環境変数を設定
   ```
   
   `.env`ファイルの主な設定項目：
   - `DATABASE_URL`: データベース接続URL（デフォルト: `mysql+pymysql://quiz_user:quiz_password@localhost:3306/quiz_db`）
   - `SECRET_KEY`: Flaskのセッション暗号化キー（本番環境では必ず変更）
   - `FLASK_ENV`: 実行環境（`development` または `production`）

### 13.2 起動方法（推奨: ラッパーシェルを使用）

#### 13.2.1 起動スクリプト（`start.sh`）の使用

最も簡単な起動方法です。以下のコマンドを実行するだけで、必要な準備からアプリケーション起動まで自動的に行われます。

```bash
./scripts/start.sh
```

**このスクリプトが実行する処理：**
1. DockerとDocker Composeの確認
2. 環境変数ファイル（`.env`）の確認と作成
3. Docker ComposeでMySQLデータベースコンテナの起動
4. データベースの起動確認と待機
5. Docker ComposeでFlaskアプリケーションコンテナの起動
6. コンテナ内でデータベースの初期化（マイグレーション実行）
7. コンテナ内で初期データの投入（カテゴリとクイズ問題）
8. アプリケーションログの表示

起動後、ブラウザで `http://localhost:5000` にアクセスしてください。

**注意**: このスクリプトはDocker Composeを使用してアプリケーションとデータベースの両方をコンテナで起動します。開発環境ではコードの変更が自動的に反映されます（ホットリロード機能付き）。

#### 13.2.2 Docker Composeを使用した手動起動

```bash
# すべてのサービス（アプリケーション + データベース）を起動
docker-compose -f docker/docker-compose.dev.yml up -d

# ログの確認
docker-compose -f docker/docker-compose.dev.yml logs -f app

# 停止
docker-compose -f docker/docker-compose.dev.yml down
```

#### 13.2.3 ローカル環境での起動（Dockerを使用しない場合）

PoetryとローカルのMySQLを使用する場合：

1. **データベースの起動**（Docker ComposeでMySQLのみ起動）
   ```bash
   docker-compose -f docker/docker-compose.dev.yml up -d mysql
   ```

2. **データベースの初期化**
   ```bash
   ./scripts/init_db.sh
   ```
   
   または手動で：
   ```bash
   poetry run flask db init  # 初回のみ
   poetry run flask db migrate -m "Initial migration"
   poetry run flask db upgrade
   poetry run python -m app.data.initial_data
   ```

3. **アプリケーションの起動**
   ```bash
   poetry run flask run
   ```
   
   または：
   ```bash
   python run.py
   ```

### 13.3 停止方法

#### 13.3.1 停止スクリプト（`stop.sh`）の使用

```bash
./scripts/stop.sh
```

このスクリプトは、アプリケーションコンテナとデータベースコンテナの両方を停止します。

#### 13.3.2 手動停止

```bash
# アプリケーションの停止（Ctrl+Cで停止）

# データベースの停止
docker-compose -f docker/docker-compose.yml stop mysql

# または、すべてのコンテナを停止・削除
docker-compose -f docker/docker-compose.yml down
```

### 13.4 ラッパーシェルスクリプトの説明

プロジェクトには、起動・停止・初期化を簡単に行うためのラッパーシェルスクリプトが用意されています。

#### 13.4.1 `scripts/start.sh` - 起動スクリプト

**機能：**
- Docker Composeを使用したアプリケーションとデータベースの起動
- 環境の自動チェックとセットアップ
- データベースの自動起動と初期化

**使用方法：**
```bash
./scripts/start.sh
```

**実行内容：**
1. DockerとDocker Composeの確認
2. `.env`ファイルの確認と自動作成（存在しない場合）
3. 既存のコンテナの停止（念のため）
4. MySQLコンテナの起動と起動確認
5. Flaskアプリケーションコンテナの起動
6. コンテナ内でデータベースマイグレーションの実行
7. コンテナ内で初期データの投入
8. アプリケーションログの表示

#### 13.4.2 `scripts/stop.sh` - 停止スクリプト

**機能：**
- Docker Composeを使用したアプリケーションとデータベースの停止
- オプションでコンテナの削除

**使用方法：**
```bash
./scripts/stop.sh
```

**実行内容：**
1. Docker Composeで全サービスの停止
2. オプションでコンテナの削除（確認付き）
   - データベースのデータは保持されます（ボリュームは削除されません）

#### 13.4.3 `scripts/init_db.sh` - データベース初期化スクリプト

**機能：**
- データベースのマイグレーション実行
- 初期データの投入

**使用方法：**
```bash
./scripts/init_db.sh
```

**実行内容：**
1. MySQLコンテナの起動確認と起動（未起動の場合）
2. データベースマイグレーションの実行
3. 初期データ（カテゴリ、クイズ、デフォルト管理者）の投入

**注意：** このスクリプトは既存のデータを上書きする可能性があります。

### 13.5 Docker Composeファイルの説明

プロジェクトには2つのDocker Composeファイルがあります：

#### 13.5.1 `docker/docker-compose.dev.yml` - 開発環境用

開発環境で使用するDocker Compose設定です。以下の特徴があります：
- コードの変更が自動的に反映される（ボリュームマウント）
- ホットリロード機能付き（`--reload`オプション）
- 開発用パッケージもインストール

**使用方法：**
```bash
# 起動
docker-compose -f docker/docker-compose.dev.yml up -d

# ログの確認
docker-compose -f docker/docker-compose.dev.yml logs -f app

# 停止
docker-compose -f docker/docker-compose.dev.yml down
```

#### 13.5.2 `docker/docker-compose.yml` - 本番環境用

本番環境で使用するDocker Compose設定です。以下の特徴があります：
- 最適化されたビルド（開発用パッケージは含まれない）
- Gunicornを使用した本番環境向けWSGIサーバー

**使用方法：**
```bash
# 起動
docker-compose -f docker/docker-compose.yml up -d

# ログの確認
docker-compose -f docker/docker-compose.yml logs -f app

# 停止
docker-compose -f docker/docker-compose.yml down
```

### 13.6 トラブルシューティング

#### データベースに接続できない場合

1. MySQLコンテナが起動しているか確認：
   ```bash
   docker ps | grep quiz_mysql
   ```

2. コンテナのログを確認：
   ```bash
   docker-compose -f docker/docker-compose.dev.yml logs mysql
   ```

3. データベースを再起動：
   ```bash
   docker-compose -f docker/docker-compose.dev.yml restart mysql
   ```

4. コンテナを再作成（データは保持されます）：
   ```bash
   docker-compose -f docker/docker-compose.dev.yml up -d --force-recreate mysql
   ```

#### マイグレーションエラーが発生した場合

1. マイグレーションをリセット（**注意：データが削除されます**）：
   ```bash
   rm -rf migrations/
   poetry run flask db init
   poetry run flask db migrate -m "Initial migration"
   poetry run flask db upgrade
   poetry run python -m app.data.initial_data
   ```

#### ポートが既に使用されている場合

Docker Composeファイルでポート番号を変更するか、既存のコンテナを停止してください。

```bash
# ポート5000を使用しているコンテナを確認
docker ps | grep 5000

# コンテナを停止
docker-compose -f docker/docker-compose.dev.yml stop

# または、ポート番号を変更（docker/docker-compose.dev.ymlを編集）
# ports:
#   - "5001:5000"  # ホストの5001ポートを使用
```

#### コンテナのログを確認する方法

```bash
# アプリケーションのログ
docker-compose -f docker/docker-compose.dev.yml logs -f app

# データベースのログ
docker-compose -f docker/docker-compose.dev.yml logs -f mysql

# すべてのサービスのログ
docker-compose -f docker/docker-compose.dev.yml logs -f
```

#### コンテナ内でコマンドを実行する方法

```bash
# アプリケーションコンテナ内でシェルを起動
docker exec -it quiz_app bash

# データベースコンテナ内でMySQLに接続
docker exec -it quiz_mysql mysql -u quiz_user -pquiz_password quiz_db
```

### 13.7 デフォルト管理者アカウント

初回起動時に以下のデフォルト管理者アカウントが作成されます：

- **ユーザーID**: `admin`
- **メールアドレス**: `admin@example.com`
- **パスワード**: `admin123`

**重要：** 本番環境では、必ずパスワードを変更してください。

---

**注意**: 本設計書は実装前の設計段階のドキュメントです。実装時に細部の調整が発生する可能性があります。


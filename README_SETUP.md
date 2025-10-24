# MBTI性格診断Webアプリケーション - セットアップガイド

## 概要

Flask + PostgreSQL + Docker ComposeによるMBTI風性格診断アプリケーションです。

## 前提条件

- Docker Desktop（Docker + Docker Compose）がインストールされていること
- ポート 5000（Web）、5432（PostgreSQL）、5050（pgAdmin）が使用可能であること

## セットアップ手順

### 1. 環境変数の設定（オプション）

`.env` ファイルをプロジェクトルートに作成します：

```bash
# Flask設定
SECRET_KEY=your-secret-key-change-in-production
FLASK_ENV=development

# データベース設定
DATABASE_URL=postgresql://mbti_user:mbti_pass@db:5432/mbti_db

# 管理者設定
ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123
```

※環境変数ファイルを作成しない場合は、デフォルト値が使用されます。

### 2. Dockerコンテナの起動

プロジェクトルートディレクトリで以下のコマンドを実行：

```bash
# コンテナをビルドして起動
docker-compose up --build

# バックグラウンドで起動する場合
docker-compose up -d --build
```

### 3. アプリケーションへのアクセス

起動完了後、以下のURLでアクセスできます：

- **Webアプリケーション**: http://localhost:5000
- **管理画面**: http://localhost:5000/admin
  - ユーザー名: `admin`
  - パスワード: `admin123`
- **pgAdmin（DB管理ツール）**: http://localhost:5050
  - メールアドレス: `admin@example.com`
  - パスワード: `admin`

## 使い方

### 診断の実行

1. トップページ（http://localhost:5000）にアクセス
2. お名前とメールアドレスを入力（任意）
3. 「診断を始める」ボタンをクリック
4. 12個の質問に回答
5. 結果ページでMBTIタイプと詳細を確認
6. 「結果を保存」ボタンで結果をDBに保存（任意）

### 管理画面の使用

1. http://localhost:5000/admin にアクセス
2. Basic認証でログイン（admin/admin123）
3. ダッシュボードで統計情報を確認
4. 診断履歴ページで過去の診断データを閲覧・削除

## Docker コマンド

```bash
# コンテナの起動
docker-compose up

# コンテナの停止
docker-compose down

# コンテナの再起動
docker-compose restart

# ログの確認
docker-compose logs -f

# 特定のサービスのログ確認
docker-compose logs -f web

# コンテナに入る
docker-compose exec web bash

# データベースをリセット（データ削除）
docker-compose down -v
docker-compose up --build
```

## データベース操作

### psqlでの接続

```bash
# Dockerコンテナ経由で接続
docker-compose exec db psql -U mbti_user -d mbti_db

# ホストから直接接続
psql -h localhost -p 5432 -U mbti_user -d mbti_db
```

### よく使うSQLコマンド

```sql
-- テーブル一覧
\dt

-- 診断データの確認
SELECT id, mbti_type, user_name, created_at FROM diagnoses ORDER BY created_at DESC LIMIT 10;

-- タイプ別集計
SELECT mbti_type, COUNT(*) as count FROM diagnoses GROUP BY mbti_type ORDER BY count DESC;

-- 全データ削除
TRUNCATE TABLE diagnoses RESTART IDENTITY;
```

## トラブルシューティング

### ポートが既に使用されている

エラー: `Bind for 0.0.0.0:5000 failed: port is already allocated`

**解決方法:**
```bash
# 使用中のプロセスを確認
lsof -i :5000

# docker-compose.ymlのポートを変更
# ports:
#   - "5001:5000"  # 左側を変更
```

### データベース接続エラー

**解決方法:**
```bash
# コンテナの状態確認
docker-compose ps

# DBコンテナのログ確認
docker-compose logs db

# すべてリセット
docker-compose down -v
docker-compose up --build
```

### コンテナが起動しない

**解決方法:**
```bash
# 古いコンテナとイメージを削除
docker-compose down
docker system prune -a

# 再ビルド
docker-compose build --no-cache
docker-compose up
```

## 開発モード（ローカル実行）

Dockerを使わずにローカルで開発する場合：

### 1. PostgreSQLのインストールと設定

```bash
# macOS (Homebrew)
brew install postgresql@15
brew services start postgresql@15

# データベース作成
createdb mbti_db
```

### 2. Python環境の構築

```bash
# 仮想環境の作成
cd app
python3 -m venv venv
source venv/bin/activate  # Windowsの場合: venv\Scripts\activate

# 依存パッケージのインストール
pip install -r requirements.txt
```

### 3. 環境変数の設定

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
export DATABASE_URL=postgresql://localhost:5432/mbti_db
export SECRET_KEY=dev-secret-key
```

### 4. アプリケーションの起動

```bash
# データベーステーブル作成
flask db init  # 初回のみ
flask db migrate
flask db upgrade

# または、Pythonスクリプトで直接作成
python app.py

# アプリケーション起動
flask run
```

## プロジェクト構造

```
traning-mbti/
├── docker-compose.yml          # Docker Compose設定
├── .gitignore                  # Git除外設定
├── DESIGN.md                   # 設計書
├── README_SETUP.md             # 本ファイル
│
├── app/                        # Flaskアプリケーション
│   ├── Dockerfile              # アプリコンテナ定義
│   ├── requirements.txt        # Python依存パッケージ
│   ├── app.py                  # エントリーポイント
│   ├── config.py               # 設定
│   │
│   ├── models/                 # データモデル
│   │   ├── __init__.py
│   │   └── diagnosis.py
│   │
│   ├── routes/                 # ルーティング
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── admin.py
│   │
│   ├── services/               # ビジネスロジック
│   │   ├── __init__.py
│   │   ├── questions.py
│   │   └── scoring.py
│   │
│   ├── static/                 # 静的ファイル
│   │   ├── css/custom.css
│   │   └── js/app.js
│   │
│   └── templates/              # HTMLテンプレート
│       ├── base.html
│       ├── index.html
│       ├── question.html
│       ├── result.html
│       └── admin/
│           ├── dashboard.html
│           └── history.html
│
└── db/                         # データベース関連
    └── init.sql                # 初期化SQL
```

## 技術スタック

- **バックエンド**: Flask 3.0.0
- **データベース**: PostgreSQL 15
- **ORM**: SQLAlchemy 3.1.1
- **フロントエンド**: Bootstrap 5.3.0
- **コンテナ化**: Docker + Docker Compose
- **言語**: Python 3.11

## ライセンス

このプロジェクトは教育・研修目的で作成されています。

## サポート

問題が発生した場合は、プロジェクトのIssueトラッカーに報告してください。


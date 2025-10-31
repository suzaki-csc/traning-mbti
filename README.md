# traning-mbti
1 day研修で使用する研修テーマ案

## 概要
このリポジトリは研修向けMBTI性格診断アプリの試作を行っています。  
段階的な機能追加を学習するため、試作はブランチごとに管理しています。

## ブランチ構成

### test/simple_mbti_app_01
**基本機能のみの実装**
- Flaskを使用したシンプルなWebアプリケーション
- セッションベースで回答を管理（データベースなし）
- MBTI診断の基本的な動作を実装

### test/simple_mbti_app_02
**データベースの追加**
- SQLAlchemy + MySQL/PostgreSQLによるデータベース連携
- 診断結果をDBに永続化（Diagnosisモデル）
- Docker ComposeによるアプリとDBのコンテナ構成

### test/simple_mbti_app_03
**管理機能とユーザー認証の追加**
- ユーザー認証機能（ログイン/新規登録）
- 個人の診断履歴表示機能
- 管理者機能（全ユーザーの履歴参照、統計ダッシュボード）

## セットアップ方法

### 必要な環境
- Docker
- Docker Compose

### 起動手順

1. リポジトリのクローン
```bash
git clone <repository-url>
cd traning-mbti
```

2. Dockerコンテナの起動
```bash
docker-compose up -d
```

3. データベースの初期化
```bash
docker-compose exec web python init_db.py
```

4. アプリケーションへアクセス
- ユーザーページ: http://localhost:5000
- 管理画面: http://localhost:5000/admin/login
  - ユーザー名: `admin`
  - パスワード: `admin123`

### 停止方法
```bash
docker-compose down
```

### データベースも含めて完全削除
```bash
docker-compose down -v
```

## アプリケーション構成

### 主要ファイル
- `app.py` - Flaskアプリケーションのメインファイル
- `config.py` - 設定ファイル
- `init_db.py` - データベース初期化スクリプト
- `docker-compose.yml` - Docker Compose設定
- `Dockerfile` - Dockerイメージ設定

### ディレクトリ構造
```
traning-mbti/
├── templates/          # HTMLテンプレート
│   ├── base.html
│   ├── index.html
│   ├── diagnosis.html
│   ├── result.html
│   └── admin/
├── static/             # 静的ファイル
│   ├── css/
│   └── js/
└── models/             # データモデル
```

## 機能一覧

### ユーザー機能
- トップページ（診断の説明）
- 診断ページ（12問の質問に回答）
- 結果表示（MBTIタイプと各軸のスコア）

### 管理者機能
- 管理者ログイン
- 診断履歴一覧表示
- 検索機能（ユーザー名、MBTIタイプ）
- 診断結果の詳細表示

## 技術スタック
- **バックエンド**: Flask (Python)
- **データベース**: MySQL 8.0
- **フロントエンド**: Bootstrap 5
- **コンテナ**: Docker, Docker Compose

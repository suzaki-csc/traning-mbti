# MBTI風性格診断Webアプリケーション

MBTI（Myers-Briggs Type Indicator）風の性格診断を行うWebアプリケーションです。
12問の質問に答えることで、4つの軸（E/I, S/N, T/F, J/P）のスコアを算出し、16タイプのいずれかを判定します。

## ⚡ クイックスタート

```bash
# 1. リポジトリをクローン
git clone <repository-url>
cd traning-mbti

# 2. 起動スクリプトを実行
./start.sh

# 3. ブラウザでアクセス
# http://localhost:5000
```

たったこれだけで起動できます！🎉

## 🎯 主要機能

- **性格診断機能**: 12問の質問で4軸を診断
- **診断結果表示**: MBTIタイプと各軸のスコアを視覚的に表示
- **診断履歴管理**: 過去の診断結果をデータベースに保存・閲覧
- **管理機能**: 診断履歴の一覧表示・検索・削除

## 🛠️ 技術スタック

- **バックエンド**: Python 3.12, Flask
- **フロントエンド**: HTML, Bootstrap 5
- **データベース**: MySQL 8.0
- **コンテナ**: Docker, Docker Compose
- **依存関係管理**: Poetry

## 📁 プロジェクト構造

```
traning-mbti/
├── docker-compose.yml          # Docker Compose設定
├── Dockerfile                  # アプリコンテナのDockerfile
├── init.sql                    # DB初期化スクリプト
├── pyproject.toml             # Poetry依存関係管理
├── poetry.lock
├── DESIGN.md                  # 設計書
├── app/
│   ├── __init__.py           # Flaskアプリ初期化
│   ├── config.py             # 設定ファイル
│   ├── models.py             # データベースモデル
│   ├── routes.py             # ルーティング定義
│   ├── quiz_data.py          # 質問データ定義
│   ├── scoring.py            # 採点ロジック
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # カスタムCSS
│   │   └── js/
│   │       └── quiz.js       # フロントエンドJS
│   └── templates/
│       ├── base.html         # ベーステンプレート
│       ├── index.html        # トップページ
│       ├── quiz.html         # 質問ページ
│       ├── result.html       # 結果ページ
│       └── admin/
│           └── history.html  # 診断履歴管理ページ
└── README.md
```

## 🚀 セットアップ手順

### 前提条件

- Docker Desktop がインストールされていること
- Poetry がインストールされていること（ローカル開発の場合）

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd traning-mbti
```

### 2. 簡単起動（推奨）

起動用のラッパーシェルスクリプトを使用すると、簡単にアプリケーションを起動できます。

```bash
# アプリケーションを起動
./start.sh
```

`start.sh` は以下の処理を自動で行います：
- `.env` ファイルの自動作成（存在しない場合）
- Docker環境のチェック
- コンテナのビルドと起動
- データベースとアプリケーションのヘルスチェック
- 起動完了メッセージとURLの表示

#### その他の便利なスクリプト

```bash
# ログをリアルタイムで確認
./logs.sh

# アプリケーションを停止
./stop.sh
```

### 3. 手動起動

手動でセットアップする場合は以下の手順に従ってください。

#### 3-1. 環境変数ファイルの作成

`.env` ファイルをプロジェクトルートに作成してください：

```env
# Flask設定
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# データベース設定
DATABASE_URL=mysql+pymysql://mbti_user:mbti_password@db:3306/mbti_db

# MySQL設定
MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=mbti_db
MYSQL_USER=mbti_user
MYSQL_PASSWORD=mbti_password
```

または `.env.example` をコピー：

```bash
cp .env.example .env
```

#### 3-2. Dockerコンテナの起動

```bash
# コンテナをビルドして起動
docker-compose up --build

# バックグラウンドで起動する場合
docker-compose up -d --build
```

#### 3-3. データベースの起動確認

```bash
# データベースが起動するまで待機（約10秒）
docker-compose exec db mysqladmin ping -h localhost -u root -proot_password
```

### 4. アプリケーションへのアクセス

ブラウザで以下のURLにアクセスしてください：

- **メインアプリ**: http://localhost:5000
- **診断履歴**: http://localhost:5000/admin/history

### 5. デフォルト管理者アカウント

アプリケーション起動時に、デフォルト管理者ユーザーが自動作成されます：

- **メールアドレス**: `admin@example.com`
- **パスワード**: `admin123`

> ⚠️ **セキュリティ警告**: 本番環境では必ずパスワードを変更してください。

## 🎮 起動スクリプトの詳細

### start.sh

アプリケーションを起動します。

**機能:**
- 環境ファイル（.env）の自動チェック・作成
- Docker/Docker Composeのインストール確認
- 既存コンテナの検出と再起動確認
- コンテナのビルドと起動
- データベースのヘルスチェック
- アプリケーションの起動確認
- アクセスURLの表示

**使い方:**
```bash
./start.sh
```

### stop.sh

アプリケーションを停止します。

**機能:**
- コンテナの状態確認
- データ削除の選択（診断履歴を保持するか削除するか）
- コンテナの停止または完全削除

**使い方:**
```bash
./stop.sh

# データも削除する場合は、プロンプトで 'yes' と入力
```

### logs.sh

アプリケーションのログをリアルタイムで表示します。

**使い方:**
```bash
./logs.sh

# 終了する場合は Ctrl+C
```

## 📝 使い方

### 診断を受ける

1. トップページで「診断を始める」ボタンをクリック
2. 12問の質問に順番に回答
3. 全問回答後、自動的に結果ページに遷移
4. MBTIタイプと各軸のスコアが表示されます

### 診断履歴を確認する

1. 「診断履歴」メニューをクリック
2. 過去の診断結果を一覧で確認
3. 「詳細」ボタンで回答内容を確認
4. 「結果」ボタンで結果ページを再表示

## 🔧 開発

### ローカル開発環境のセットアップ

```bash
# Poetryで依存関係をインストール
poetry install

# 仮想環境を有効化
poetry shell

# Flaskアプリを起動（ローカル開発）
flask run
```

### データベースマイグレーション

```bash
# マイグレーションの初期化
flask db init

# マイグレーションファイルの作成
flask db migrate -m "Initial migration"

# マイグレーションの適用
flask db upgrade
```

### コンテナ操作

```bash
# ログの確認
docker-compose logs -f app

# コンテナ内でコマンド実行
docker-compose exec app bash

# データベースのリセット
docker-compose down -v
docker-compose up -d --build
```

## 📊 データベース構造

### diagnosis_sessions テーブル
診断セッション情報を保存

| カラム名 | 型 | 説明 |
|---------|---|------|
| id | INT | セッションID（主キー） |
| session_id | VARCHAR(36) | UUID |
| mbti_type | VARCHAR(4) | 診断結果（例: INTJ） |
| scores_json | JSON | スコア詳細 |
| created_at | DATETIME | 診断実施日時 |
| ip_address | VARCHAR(45) | IPアドレス |

### diagnosis_answers テーブル
各質問の回答を保存

| カラム名 | 型 | 説明 |
|---------|---|------|
| id | INT | 回答ID（主キー） |
| session_id | INT | セッションID（外部キー） |
| question_id | INT | 質問番号 |
| axis | VARCHAR(1) | 選択された軸 |
| score | INT | スコア値 |
| answer_text | TEXT | 選択した回答テキスト |
| created_at | DATETIME | 回答日時 |

## 🔐 セキュリティについて

> ⚠️ **重要**: このプロジェクトは教育目的のデモンストレーションです。

このアプリケーションには、セキュリティ学習のために意図的に脆弱性が含まれています：

- SQLインジェクション
- XSS（クロスサイトスクリプティング）
- CSRF（クロスサイトリクエストフォージェリ）
- セッション管理の脆弱性

**本番環境では使用しないでください。**

## 📚 参考資料

- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Bootstrap公式ドキュメント](https://getbootstrap.com/)
- [SQLAlchemy公式ドキュメント](https://www.sqlalchemy.org/)
- [Docker公式ドキュメント](https://docs.docker.com/)
- [MBTI理論について](https://www.16personalities.com/)

## 📄 ライセンス

このプロジェクトは教育目的で作成されています。

## 👤 作成者

suzaki-csc

---

**作成日**: 2025年11月4日  
**バージョン**: 1.0

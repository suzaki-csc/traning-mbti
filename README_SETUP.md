# MBTI性格診断アプリ セットアップガイド

## 概要

Flask、Bootstrap、Docker、MySQL を使用した MBTI 風の性格診断 Web アプリケーションです。

## 必要な環境

- Python 3.11+
- Poetry
- Docker & Docker Compose（Docker を使用する場合）

## セットアップ手順

### 方法1: Docker を使用する場合（推奨）

1. **環境変数ファイルの作成**

```bash
# .env ファイルを作成
cat > .env << EOF
SECRET_KEY=your-secret-key-here
MYSQL_ROOT_PASSWORD=root_password
MYSQL_PASSWORD=mbti_password
EOF
```

2. **Docker コンテナの起動**

```bash
# コンテナをビルドして起動
docker-compose up -d --build

# ログを確認
docker-compose logs -f
```

3. **アプリケーションへのアクセス**

ブラウザで http://localhost:5000 にアクセスしてください。

4. **初期ログイン情報**

- 管理者アカウント
  - ユーザー名: `admin`
  - パスワード: `admin123`

- テストユーザーアカウント
  - ユーザー名: `testuser`
  - パスワード: `user123`

5. **コンテナの停止**

```bash
docker-compose down

# データベースも含めて削除する場合
docker-compose down -v
```

### 方法2: ローカル環境で実行する場合

1. **Python 環境のセットアップ**

```bash
# Poetry がインストールされていない場合
pip install poetry

# 依存関係のインストール
poetry install
```

2. **環境変数の設定**

```bash
# .env ファイルを作成
cat > .env << EOF
SECRET_KEY=your-secret-key-here
DATABASE_URL=mysql+pymysql://mbti_user:mbti_password@localhost:3306/mbti_db
FLASK_ENV=development
FLASK_APP=run.py
EOF
```

3. **MySQL データベースのセットアップ**

```bash
# MySQL にログイン
mysql -u root -p

# データベースとユーザーを作成
CREATE DATABASE mbti_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'mbti_user'@'localhost' IDENTIFIED BY 'mbti_password';
GRANT ALL PRIVILEGES ON mbti_db.* TO 'mbti_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

# 初期化スクリプトを実行
mysql -u mbti_user -p mbti_db < mysql/init.sql
```

4. **アプリケーションの起動**

```bash
# Poetry の仮想環境を有効化
poetry shell

# アプリケーションを起動
python run.py
```

5. **アプリケーションへのアクセス**

ブラウザで http://localhost:5000 にアクセスしてください。

## プロジェクト構造

```
traning-mbti/
├── app/                        # アプリケーションコード
│   ├── __init__.py            # Flask アプリの初期化
│   ├── config.py              # 設定ファイル
│   ├── models.py              # データベースモデル
│   ├── auth.py                # 認証ヘルパー
│   ├── routes/                # ルーティング
│   │   ├── main.py           # メイン機能
│   │   ├── quiz.py           # 診断機能
│   │   └── admin.py          # 管理機能
│   ├── templates/             # HTML テンプレート
│   ├── static/                # CSS、JS
│   └── utils/                 # ユーティリティ
│       ├── questions.py      # 質問データ
│       └── scoring.py        # スコアリングロジック
├── mysql/                     # MySQL 初期化スクリプト
├── docker-compose.yml         # Docker Compose 設定
├── Dockerfile                 # Docker イメージ定義
├── pyproject.toml            # Poetry 設定
└── run.py                    # アプリケーション起動スクリプト
```

## 主な機能

### ユーザー機能
- ユーザー登録・ログイン
- MBTI 診断の受診（12問）
- 診断結果の閲覧（スコア詳細、グラフ表示）
- 診断履歴の確認

### 管理者機能
- 管理ダッシュボード（統計情報）
- 全ユーザーの診断履歴閲覧
- 診断結果の削除
- MBTI タイプ別の分布確認

## トラブルシューティング

### Docker コンテナが起動しない

```bash
# ログを確認
docker-compose logs

# コンテナを再ビルド
docker-compose down -v
docker-compose up -d --build
```

### データベース接続エラー

1. MySQL コンテナが起動しているか確認
```bash
docker-compose ps
```

2. データベースの接続情報が正しいか確認
```bash
# .env ファイルの内容を確認
cat .env
```

### パッケージのインストールエラー

```bash
# Poetry のキャッシュをクリア
poetry cache clear --all pypi

# 依存関係を再インストール
poetry install --no-cache
```

## 開発

### テストの実行

```bash
# テストを実行
poetry run pytest

# カバレッジを確認
poetry run pytest --cov=app
```

### コードスタイルのチェック

```bash
# flake8 でチェック
poetry run flake8 app/

# black でフォーマット
poetry run black app/
```

## セキュリティ注意事項

本番環境で使用する場合は、以下の設定を必ず変更してください：

1. **SECRET_KEY** を強力なランダム文字列に変更
2. **データベースのパスワード** を複雑なものに変更
3. **FLASK_ENV** を `production` に変更
4. **HTTPS** を有効化
5. 初期管理者アカウントのパスワードを変更

## ライセンス

このプロジェクトは学習目的で作成されています。

## サポート

問題が発生した場合は、以下を確認してください：

1. ログファイルの内容
2. Docker コンテナの状態
3. データベースの接続情報
4. Python のバージョン

---

作成日: 2024年


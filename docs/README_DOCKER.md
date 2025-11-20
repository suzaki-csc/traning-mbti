# Docker構成について

## 概要

このプロジェクトはDocker Composeを使用してコンテナ化されています。
将来的な拡張（MySQL、Redisなどの追加）を見越した構成になっています。

## 構成

### 現在のサービス

- **web**: Flaskアプリケーション（ポート5000）

### 将来追加可能なサービス（コメントアウト済み）

- **mysql**: MySQLデータベース（ポート3306）
- **redis**: Redisキャッシュ（ポート6379）

## ファイル構成

- `Dockerfile`: Webアプリケーション用のDockerイメージ定義
- `docker-compose.yml`: サービス全体の構成定義
- `.dockerignore`: Dockerビルド時に除外するファイル

## 使用方法

### 基本的な操作

```bash
# 起動
docker compose up

# バックグラウンドで起動
docker compose up -d

# 停止
docker compose down

# ログ確認
docker compose logs -f

# 再ビルド
docker compose build --no-cache
```

### データベースの初期化

初回起動時は自動的に初期化されますが、手動で実行する場合:

```bash
docker compose exec web poetry run python data/init_questions.py
```

### コンテナ内でコマンドを実行

```bash
# Pythonシェルを起動
docker compose exec web poetry run python

# データベース操作
docker compose exec web poetry run python -c "from app import app; from models import db, Category; app.app_context().push(); print(Category.query.count())"
```

## ボリュームマウント

開発時のホットリロードのために、以下のファイル/ディレクトリがマウントされています:

- `app.py`
- `models.py`
- `config.py`
- `templates/`
- `static/`
- `quiz.db` (データベースファイル)

コードを変更すると、自動的に反映されます（Flaskのデバッグモード）。

## 環境変数

`docker-compose.yml`で設定可能な環境変数:

- `FLASK_ENV`: Flaskの環境（development/production）
- `FLASK_APP`: Flaskアプリケーションファイル
- `SECRET_KEY`: セッション用のシークレットキー

`.env`ファイルを作成して環境変数を設定することも可能です:

```bash
# .envファイルの例
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

## MySQLを使用する場合

`docker-compose.yml`のMySQLサービスを有効化:

1. MySQLサービスのコメントアウトを解除
2. `config.py`でデータベース接続をMySQLに変更
3. 環境変数を設定

```yaml
# docker-compose.yml
mysql:
  image: mysql:8.0
  # ... 設定 ...
```

```python
# config.py
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
    'mysql+pymysql://quiz_user:quiz_password@mysql:3306/quiz_db'
```

## トラブルシューティング

### ポートが使用されている

`docker-compose.yml`の`ports`セクションを変更:

```yaml
ports:
  - "5001:5000"  # ホストの5001ポートを使用
```

### コンテナが起動しない

```bash
# ログを確認
docker compose logs web

# コンテナを再ビルド
docker compose build --no-cache
docker compose up
```

### データベースをリセット

```bash
docker compose down
rm quiz.db  # または del quiz.db (Windows)
docker compose up
```

### イメージを完全に削除

```bash
docker compose down -v
docker rmi $(docker images -q quiz-app-web)
docker compose build --no-cache
```

## 本番環境へのデプロイ

本番環境では以下の点に注意してください:

1. `SECRET_KEY`を強力な値に設定
2. `FLASK_ENV=production`に設定
3. HTTPSを使用（リバースプロキシ経由）
4. データベースのバックアップを設定
5. ログの管理を設定


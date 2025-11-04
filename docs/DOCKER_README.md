# Docker環境での運用ガイド

## 概要

このアプリケーションはDockerとDocker Composeを使用して、簡単にコンテナ化された環境で実行できます。

## 構成

### サービス構成

```
┌─────────────────┐
│   app           │  Flask アプリケーション (Python 3.12)
│   Port: 5000    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐
│   db            │  MySQL 8.0 データベース
│   Port: 3306    │
└─────────────────┘

┌─────────────────┐
│  phpmyadmin     │  phpMyAdmin (開発用・オプション)
│   Port: 8080    │
└─────────────────┘
```

### コンテナ一覧

| サービス名 | イメージ | ポート | 説明 |
|-----------|---------|--------|------|
| app | カスタム (Dockerfile) | 5000 | Flaskアプリケーション |
| db | mysql:8.0 | 3306 | MySQLデータベース |
| phpmyadmin | phpmyadmin:latest | 8080 | データベース管理ツール（開発用） |

---

## 初回セットアップ

### 1. 環境変数ファイルの作成

```bash
# .env.exampleをコピーして.envを作成
cp .env.example .env

# .envファイルを編集して、必要な設定を変更
vim .env
```

**重要な設定項目:**
- `SECRET_KEY`: ランダムな文字列に変更（本番環境では必須）
- `MYSQL_ROOT_PASSWORD`: MySQLのrootパスワード
- `MYSQL_PASSWORD`: アプリケーション用DBユーザーのパスワード

### 2. Dockerイメージのビルド

```bash
# イメージをビルド
docker-compose build

# または、キャッシュを使わずに再ビルド
docker-compose build --no-cache
```

### 3. コンテナの起動

```bash
# バックグラウンドで起動
docker-compose up -d

# ログを表示しながら起動
docker-compose up
```

### 4. 起動確認

```bash
# コンテナの状態を確認
docker-compose ps

# ログを確認
docker-compose logs -f app
```

---

## 基本的な操作

### コンテナの起動・停止

```bash
# 起動
docker-compose up -d

# 停止
docker-compose down

# 停止（ボリュームも削除）
docker-compose down -v

# 再起動
docker-compose restart
```

### ログの確認

```bash
# 全サービスのログを表示
docker-compose logs -f

# 特定のサービスのログを表示
docker-compose logs -f app
docker-compose logs -f db

# 最新の50行を表示
docker-compose logs --tail=50 app
```

### コンテナ内でコマンド実行

```bash
# アプリケーションコンテナに入る
docker-compose exec app bash

# データベースコンテナに入る
docker-compose exec db bash

# MySQLに接続
docker-compose exec db mysql -u mbti_user -p mbti_db
```

---

## 開発モード

### phpMyAdminを含めて起動

```bash
# 開発プロファイルで起動
docker-compose --profile dev up -d
```

phpMyAdminへのアクセス: http://localhost:8080

### ホットリロード

`docker-compose.yml`の`app`サービスでボリュームマウントが設定されているため、ローカルのコード変更が自動的に反映されます。

```yaml
volumes:
  - .:/app
```

---

## データベース管理

### データベースのバックアップ

```bash
# バックアップを作成
docker-compose exec db mysqldump -u root -p mbti_db > backup_$(date +%Y%m%d_%H%M%S).sql

# または、圧縮して保存
docker-compose exec db mysqldump -u root -p mbti_db | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

### データベースのリストア

```bash
# バックアップからリストア
docker-compose exec -T db mysql -u root -p mbti_db < backup.sql

# 圧縮ファイルからリストア
gunzip < backup.sql.gz | docker-compose exec -T db mysql -u root -p mbti_db
```

### データベースの初期化

```bash
# コンテナとボリュームを削除
docker-compose down -v

# 再度起動（初期化スクリプトが実行される）
docker-compose up -d
```

---

## トラブルシューティング

### コンテナが起動しない

1. **ログを確認**
   ```bash
   docker-compose logs app
   docker-compose logs db
   ```

2. **ポートの競合を確認**
   ```bash
   # ポート5000が使用中か確認
   lsof -i:5000
   
   # ポート3306が使用中か確認
   lsof -i:3306
   ```

3. **コンテナを完全にクリーンアップ**
   ```bash
   docker-compose down -v --remove-orphans
   docker-compose up -d --build
   ```

### データベース接続エラー

1. **データベースの起動を待つ**
   ```bash
   docker-compose up -d db
   sleep 30
   docker-compose up -d app
   ```

2. **接続情報を確認**
   ```bash
   docker-compose exec app env | grep DATABASE
   ```

### 権限エラー

```bash
# ボリュームの権限を修正
docker-compose exec app chown -R appuser:appuser /app
```

---

## 本番環境へのデプロイ

### 1. セキュリティ設定の確認

- `.env`ファイルの`SECRET_KEY`をランダムな文字列に変更
- データベースのパスワードを強固なものに変更
- `FLASK_ENV=production`に設定
- 不要なポートの公開を停止

### 2. docker-compose.prod.ymlの使用

本番環境用の設定ファイルを作成する場合:

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d
```

### 3. リバースプロキシの設定

NginxやApacheをリバースプロキシとして配置することを推奨します。

---

## メンテナンス

### イメージの更新

```bash
# 最新のイメージを取得
docker-compose pull

# コンテナを再作成
docker-compose up -d --force-recreate
```

### 不要なリソースのクリーンアップ

```bash
# 停止中のコンテナを削除
docker container prune

# 未使用のイメージを削除
docker image prune -a

# 未使用のボリュームを削除
docker volume prune
```

---

## デフォルト認証情報

### 管理者アカウント

- **Email**: admin@example.com
- **Password**: admin123

⚠️ **警告**: 本番環境では必ずパスワードを変更してください！

### データベース

- **Root Password**: `.env`ファイルの`MYSQL_ROOT_PASSWORD`
- **Database**: mbti_db
- **User**: mbti_user
- **Password**: `.env`ファイルの`MYSQL_PASSWORD`

---

## 参考情報

- Dockerfile: アプリケーションコンテナの定義
- docker-compose.yml: サービス構成の定義
- docker/mysql/init/: データベース初期化スクリプト
- docker/mysql/conf.d/: MySQL設定ファイル

## サポート

問題が発生した場合は、以下を確認してください:

1. ログファイル (`docker-compose logs`)
2. コンテナの状態 (`docker-compose ps`)
3. ネットワーク接続 (`docker network inspect mbti_mbti-network`)


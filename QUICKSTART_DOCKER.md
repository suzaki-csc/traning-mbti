# Docker クイックスタートガイド

MBTI風性格診断アプリケーションをDockerで簡単に起動する方法

---

## 🚀 5分で起動

### 前提条件

- Docker Desktop がインストールされていること
- Docker Compose が使用可能であること

### ステップ1: 環境変数ファイルの準備

```bash
# .env.exampleをコピー
cp .env.example .env
```

**そのまま使用してもOKです！**（開発環境の場合）

本番環境では`.env`ファイルを編集して、以下を変更してください：
- `SECRET_KEY`: ランダムな文字列に変更
- `MYSQL_ROOT_PASSWORD`: 強固なパスワードに変更
- `MYSQL_PASSWORD`: 強固なパスワードに変更

### ステップ2: 起動

```bash
# イメージをビルドして起動
docker-compose up -d --build
```

初回は5〜10分程度かかります。

### ステップ3: アクセス

ブラウザで以下にアクセス：

```
http://localhost:5000
```

---

## ✅ 動作確認

### コンテナの状態を確認

```bash
docker-compose ps
```

以下のように表示されればOK：

```
NAME            STATUS          PORTS
mbti-app        Up (healthy)    0.0.0.0:5000->5000/tcp
mbti-db         Up (healthy)    0.0.0.0:3306->3306/tcp
```

### ログの確認

```bash
# アプリケーションのログ
docker-compose logs -f app

# データベースのログ
docker-compose logs -f db
```

---

## 🛠️ よく使うコマンド

```bash
# 停止
docker-compose down

# 再起動
docker-compose restart

# 完全にクリーンアップして再構築
docker-compose down -v
docker-compose up -d --build

# 開発モード（phpMyAdmin付き）で起動
docker-compose --profile dev up -d
```

---

## 🗄️ データベース管理ツール

### phpMyAdminへのアクセス（開発モード）

```bash
# phpMyAdminを含めて起動
docker-compose --profile dev up -d
```

ブラウザで以下にアクセス：
```
http://localhost:8080
```

**ログイン情報:**
- サーバー: db
- ユーザー名: mbti_user
- パスワード: mbti_password（.envで設定した値）

---

## 🔐 デフォルト認証情報

### 管理者アカウント（将来の機能拡張用）

- **Email**: admin@example.com
- **Password**: admin123

⚠️ **本番環境では必ずパスワードを変更してください！**

---

## ❓ トラブルシューティング

### ポートが既に使用されている

```bash
# 使用中のプロセスを確認
lsof -i:5000
lsof -i:3306

# docker-compose.ymlでポート番号を変更
# 例: 5000 -> 5001
ports:
  - "5001:5000"
```

### データベースに接続できない

```bash
# データベースの起動を待ってからアプリを起動
docker-compose up -d db
sleep 30
docker-compose up -d app
```

### コンテナが起動しない

```bash
# ログを確認
docker-compose logs

# 完全にクリーンアップ
docker-compose down -v --remove-orphans
docker system prune -f

# 再ビルド
docker-compose up -d --build
```

---

## 📚 詳細ドキュメント

- **詳細なDocker運用ガイド**: `DOCKER_README.md`
- **アプリケーション設計書**: `README_APP.md`
- **通常の起動方法**: `USAGE.md`

---

## 🎯 次のステップ

1. アプリケーションにアクセスして診断を試す
2. データベース設計を確認（`docker/mysql/init/01_create_tables.sql`）
3. 将来の拡張（ログイン機能、診断履歴）の準備が完了しています

楽しんでください！🎉


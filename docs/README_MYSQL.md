# MySQLデータベース設定

## 概要

このプロジェクトはMySQLデータベースを使用し、Docker Composeでアプリケーションと別々のコンテナで構築されています。

## 構成

- **web**: Flaskアプリケーションコンテナ（ポート5000）
- **mysql**: MySQLデータベースコンテナ（ポート3306）

## データベース設定

### データベース情報

- **データベース名**: `quiz_db`
- **ユーザー名**: `quiz_user`
- **パスワード**: `quiz_password`
- **ルートパスワード**: `rootpassword`

### 接続情報

アプリケーションからMySQLへの接続は、Docker Composeのネットワーク経由で行われます：

```
mysql+pymysql://quiz_user:quiz_password@mysql:3306/quiz_db
```

## 初期化

### 自動初期化

MySQLコンテナ起動時に、`docker/mysql/init.sql`が自動的に実行されます。このスクリプトは：

1. `quiz_db`データベースを作成
2. `quiz_user`ユーザーを作成
3. ユーザーに権限を付与

### 手動初期化

データベースを手動で初期化する場合：

```bash
# コンテナ内でMySQLに接続
docker compose exec mysql mysql -u root -prootpassword

# SQLを実行
CREATE DATABASE IF NOT EXISTS quiz_db;
CREATE USER IF NOT EXISTS 'quiz_user'@'%' IDENTIFIED BY 'quiz_password';
GRANT ALL PRIVILEGES ON quiz_db.* TO 'quiz_user'@'%';
FLUSH PRIVILEGES;
```

## 使用方法

### 起動

```bash
# 通常の起動
./run.sh

# または手動で
docker compose up
```

### データベース接続の確認

```bash
# MySQLコンテナに接続
docker compose exec mysql mysql -u quiz_user -pquiz_password quiz_db

# テーブル一覧を確認
SHOW TABLES;

# カテゴリを確認
SELECT * FROM category;
```

### アプリケーションから接続確認

```bash
# コンテナ内で接続テスト
docker compose exec web poetry run python -c "
from app import app
from models import db, Category
app.app_context().push()
print(f'カテゴリ数: {Category.query.count()}')
"
```

## 環境変数

`.env`ファイルを作成して、データベース設定を変更できます：

```bash
# .envファイルの例
MYSQL_ROOT_PASSWORD=your_root_password
MYSQL_DATABASE=quiz_db
MYSQL_USER=quiz_user
MYSQL_PASSWORD=your_password
DATABASE_URL=mysql+pymysql://quiz_user:your_password@mysql:3306/quiz_db
```

## トラブルシューティング

### MySQLが起動しない

```bash
# ログを確認
docker compose logs mysql

# コンテナの状態を確認
docker compose ps
```

### 接続エラー

```bash
# MySQLが起動しているか確認
docker compose exec mysql mysqladmin ping -h localhost -u root -prootpassword

# ネットワーク接続を確認
docker compose exec web ping mysql
```

### データベースをリセット

```bash
# コンテナとボリュームを削除
docker compose down -v

# 再起動（自動的に初期化されます）
docker compose up
```

### 権限エラー

```bash
# MySQLにrootで接続
docker compose exec mysql mysql -u root -prootpassword

# 権限を再付与
GRANT ALL PRIVILEGES ON quiz_db.* TO 'quiz_user'@'%';
FLUSH PRIVILEGES;
```

## データの永続化

MySQLのデータは`mysql-data`ボリュームに保存されます。このボリュームは`docker compose down -v`を実行しない限り保持されます。

## 本番環境での注意事項

1. **パスワードの変更**: デフォルトのパスワードを変更してください
2. **セキュリティ**: 本番環境では適切なファイアウォール設定を行ってください
3. **バックアップ**: 定期的なバックアップを設定してください
4. **接続プール**: 本番環境では接続プールの設定を調整してください


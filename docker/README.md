# Docker関連ファイルの説明

## ファイル構成

### Docker Composeファイル

#### `docker-compose.dev.yml` - 開発環境用
開発環境で使用するDocker Compose設定です。
- アプリケーションとデータベースを別々のコンテナで起動
- コードの変更が自動的に反映される（ボリュームマウント）
- ホットリロード機能付き

#### `docker-compose.yml` - 本番環境用
本番環境で使用するDocker Compose設定です。
- 最適化されたビルド
- Gunicornを使用した本番環境向けWSGIサーバー

### Dockerfile

#### `Dockerfile` - 本番環境用
本番環境で使用するDockerfileです。
- 開発用パッケージは含まれない
- 最適化されたビルド

#### `Dockerfile.dev` - 開発環境用
開発環境で使用するDockerfileです。
- 開発用パッケージもインストール
- ホットリロード対応

### データベース初期化

#### `mysql/init.sql` - データベース初期化SQL
MySQLコンテナの初回起動時に自動実行されます。
- データベース `quiz_db` の作成
- ユーザー `quiz_user` の作成
- 権限の付与

**注意**: `docker-compose.yml`の環境変数でもデータベースとユーザーが自動作成されますが、`init.sql`で明示的に作成することで、より確実に初期化されます。

## コンテナ構成

### MySQLコンテナ (`quiz_mysql`)
- **イメージ**: mysql:8.0
- **ポート**: 3306
- **ボリューム**: 
  - `mysql_data`: データベースの永続化
  - `./mysql/init.sql`: 初期化SQLスクリプト
- **ネットワーク**: `quiz_network`

### Flaskアプリケーションコンテナ (`quiz_app`)
- **ビルド**: Dockerfile.dev（開発環境）またはDockerfile（本番環境）
- **ポート**: 5000
- **ボリューム**: 
  - `../app`: アプリケーションコード（開発環境のみ）
  - `../migrations`: マイグレーションファイル（開発環境のみ）
- **ネットワーク**: `quiz_network`
- **依存関係**: MySQLコンテナが正常に起動してから起動

## コンテナ間通信

コンテナ間の通信は `quiz_network` というDockerネットワークを使用します。

- アプリケーションコンテナからデータベースコンテナへの接続:
  - ホスト名: `mysql`
  - ポート: `3306`
  - 接続URL: `mysql+pymysql://quiz_user:quiz_password@mysql:3306/quiz_db`

## 使用方法

### 開発環境での起動

```bash
# 起動スクリプトを使用（推奨）
./scripts/start.sh

# または直接Docker Composeを使用
docker-compose -f docker/docker-compose.dev.yml up -d
```

### 本番環境での起動

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### 停止

```bash
# 停止スクリプトを使用（推奨）
./scripts/stop.sh

# または直接Docker Composeを使用
docker-compose -f docker/docker-compose.dev.yml down
```

## データベース接続情報

- **ホスト**: `mysql` (コンテナ内から) または `localhost` (ホストマシンから)
- **ポート**: `3306`
- **データベース名**: `quiz_db`
- **ユーザー名**: `quiz_user`
- **パスワード**: `quiz_password`
- **ルートパスワード**: `root_password`

## トラブルシューティング

### データベースに接続できない場合

1. コンテナが起動しているか確認:
   ```bash
   docker ps | grep quiz_mysql
   ```

2. ログを確認:
   ```bash
   docker-compose -f docker/docker-compose.dev.yml logs mysql
   ```

3. データベースコンテナ内で直接接続を試す:
   ```bash
   docker exec -it quiz_mysql mysql -u quiz_user -pquiz_password quiz_db
   ```

### データベースを完全にリセットする場合

```bash
# コンテナとボリュームを削除
docker-compose -f docker/docker-compose.dev.yml down -v

# 再起動
./scripts/start.sh
```

**注意**: この操作により、すべてのデータが削除されます。


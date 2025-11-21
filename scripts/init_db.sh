#!/bin/bash

# データベース初期化スクリプト

set -e

echo "データベースを初期化します..."

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# Poetry環境の確認
if ! command -v poetry &> /dev/null; then
    echo "エラー: Poetryがインストールされていません"
    exit 1
fi

# docker-composeコマンドの確認
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# データベースの起動確認
if ! docker ps | grep -q quiz_mysql; then
    echo "データベースを起動しています..."
    $DOCKER_COMPOSE -f docker/docker-compose.dev.yml up -d mysql
    
    echo "データベースの起動を待機しています..."
    # MySQLが完全に起動するまで待機（最大30秒）
    max_attempts=30
    attempt=0
    while [ $attempt -lt $max_attempts ]; do
        if docker exec quiz_mysql mysqladmin ping -h localhost --silent 2>/dev/null; then
            echo "データベースが起動しました"
            break
        fi
        attempt=$((attempt + 1))
        echo "データベースの起動を待機中... ($attempt/$max_attempts)"
        sleep 1
    done
    
    if [ $attempt -eq $max_attempts ]; then
        echo "警告: データベースの起動確認に失敗しましたが、続行します..."
    fi
    
    # 追加の待機時間（ユーザー作成のため）
    sleep 3
fi

# データベース接続を確認
max_retries=5
retry=0
while [ $retry -lt $max_retries ]; do
    if poetry run python -c "
from app import create_app
app = create_app()
with app.app_context():
    from app import db
    try:
        db.engine.connect()
        print('データベース接続成功')
        exit(0)
    except Exception as e:
        print(f'データベース接続失敗: {e}')
        exit(1)
" 2>/dev/null; then
        echo "データベース接続を確認しました"
        break
    fi
    retry=$((retry + 1))
    echo "データベース接続を再試行中... ($retry/$max_retries)"
    sleep 2
done

if [ $retry -eq $max_retries ]; then
    echo "エラー: データベースに接続できませんでした"
    echo "以下のコマンドでデータベースの状態を確認してください:"
    echo "  $DOCKER_COMPOSE -f docker/docker-compose.dev.yml logs mysql"
    exit 1
fi

# データベースの初期化
echo "マイグレーションを実行しています..."
poetry run flask db init || true
poetry run flask db migrate -m "Initial migration" || true
poetry run flask db upgrade

# 初期データの投入
echo "初期データを投入しています..."
poetry run python -m app.data.initial_data

echo "データベースの初期化が完了しました。"


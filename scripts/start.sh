#!/bin/bash

# クイズアプリケーション起動スクリプト
# Docker Composeを使用してアプリケーションとデータベースを起動します

set -e

echo "クイズアプリケーションを起動します..."

# プロジェクトルートに移動
cd "$(dirname "$0")/.."

# Dockerの確認
if ! command -v docker &> /dev/null; then
    echo "エラー: Dockerがインストールされていません"
    exit 1
fi

if ! command -v docker-compose &> /dev/null && ! command -v docker compose &> /dev/null; then
    echo "エラー: Docker Composeがインストールされていません"
    exit 1
fi

# docker-composeコマンドの確認（docker compose または docker-compose）
if command -v docker compose &> /dev/null; then
    DOCKER_COMPOSE="docker compose"
else
    DOCKER_COMPOSE="docker-compose"
fi

# 環境変数ファイルの確認
if [ ! -f ".env" ]; then
    echo "警告: .envファイルが見つかりません。.env.exampleをコピーして設定してください。"
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo ".envファイルを作成しました。必要に応じて編集してください。"
    fi
fi

# 既存のコンテナを停止（念のため）
echo "既存のコンテナを確認しています..."
$DOCKER_COMPOSE -f docker/docker-compose.dev.yml down 2>/dev/null || true

# Docker Composeでサービスを起動
echo "Docker Composeでサービスを起動しています..."
$DOCKER_COMPOSE -f docker/docker-compose.dev.yml up -d mysql

# データベースの起動を待機
echo "データベースの起動を待機しています..."
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

# アプリケーションコンテナを起動
echo "アプリケーションコンテナを起動しています..."
$DOCKER_COMPOSE -f docker/docker-compose.dev.yml up -d app

# ログを表示
echo ""
echo "=========================================="
echo "アプリケーションが起動しました！"
echo "ブラウザで http://localhost:5000 にアクセスしてください"
echo ""
echo "ログを表示するには:"
echo "  $DOCKER_COMPOSE -f docker/docker-compose.dev.yml logs -f app"
echo ""
echo "停止するには:"
echo "  ./scripts/stop.sh"
echo "=========================================="
echo ""

# ログをフォロー表示
$DOCKER_COMPOSE -f docker/docker-compose.dev.yml logs -f app


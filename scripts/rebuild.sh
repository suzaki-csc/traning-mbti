#!/bin/bash
# Dockerコンテナを完全に再ビルドするスクリプト

set -e

# スクリプトのディレクトリからプロジェクトルートに移動
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

# Docker Composeコマンドの確認
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo "Dockerコンテナを完全に再ビルドします..."

# コンテナを停止して削除
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml down -v

# イメージを削除
docker rmi quiz-app-web 2>/dev/null || true
docker rmi mysql:8.0 2>/dev/null || true

# 再ビルド
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml build --no-cache

echo "再ビルドが完了しました。起動します..."
echo "MySQLの初期化には30秒程度かかります。しばらくお待ちください..."
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml up


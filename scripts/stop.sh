#!/bin/bash
# クイズアプリ停止スクリプト（Docker Compose使用）

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

echo "クイズアプリを停止します..."

# コンテナを停止
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml down

echo "クイズアプリが停止しました。"


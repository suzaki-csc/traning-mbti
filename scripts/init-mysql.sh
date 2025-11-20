#!/bin/bash
# MySQLデータベースを初期化するスクリプト

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

echo "MySQLデータベースを初期化します..."
echo "コンテナが起動していることを確認してください..."

# MySQLが起動するまで待機
echo "MySQLの起動を待機しています..."
sleep 10

# データベースを初期化
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web poetry run python -m app.data.init_questions

echo "初期化が完了しました。"


#!/bin/bash
# Dockerコンテナ内の状態を確認するスクリプト

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

echo "=== Dockerコンテナ内の状態を確認します ==="
echo ""

# コンテナが起動しているか確認
if ! $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml ps | grep -q "quiz-app-web"; then
    echo "エラー: コンテナが起動していません。"
    echo "先に './scripts/run.sh' を実行してください。"
    exit 1
fi

echo "1. コンテナ内のディレクトリ構造:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web ls -la /app/ | head -20
echo ""

echo "2. app.pyの存在確認:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web test -f /app/app/app.py && echo "✓ /app/app/app.py が存在します" || echo "✗ /app/app/app.py が存在しません"
echo ""

echo "3. app/app/routes/main.pyの存在確認:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web test -f /app/app/routes/main.py && echo "⚠ /app/app/routes/main.py が存在します（これは問題です）" || echo "✓ /app/app/routes/main.py は存在しません（正常）"
echo ""

echo "4. 実行されているapp.pyの最初の20行:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web head -20 /app/app/app.py
echo ""

echo "5. データベースの状態:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web poetry run python -c "
from app.app import app
from app.models import db, Category
app.app_context().push()
try:
    count = Category.query.count()
    print(f'✓ カテゴリ数: {count}')
except Exception as e:
    print(f'✗ エラー: {e}')
"
echo ""

echo "6. データベースファイルの存在:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web test -f /app/quiz.db && echo "✓ /app/quiz.db が存在します" || echo "✗ /app/quiz.db が存在しません"
echo ""

echo "確認完了"


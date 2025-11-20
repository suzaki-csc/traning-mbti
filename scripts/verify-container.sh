#!/bin/bash
# コンテナ内の状態を詳細に確認するスクリプト

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

echo "=========================================="
echo "コンテナ内の状態を確認します"
echo "=========================================="
echo ""

# コンテナが起動しているか確認
if ! $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml ps | grep -q "quiz-app-web"; then
    echo "エラー: コンテナが起動していません。"
    echo "先に './scripts/run.sh' を実行してください。"
    exit 1
fi

echo "1. /appディレクトリの内容:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web ls -la /app/
echo ""

echo "2. /app/appディレクトリの存在確認:"
echo "-----------------------------------"
if $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web test -d /app/app; then
    echo "⚠ /app/app ディレクトリが存在します！"
    echo "内容:"
    $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web ls -la /app/app/ 2>/dev/null || echo "  アクセスできません"
else
    echo "✓ /app/app ディレクトリは存在しません（正常）"
fi
echo ""

echo "3. /app/app/routes/main.pyの存在確認:"
echo "-----------------------------------"
if $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web test -f /app/app/routes/main.py; then
    echo "⚠ /app/app/routes/main.py が存在します！"
    echo "最初の20行:"
    $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web head -20 /app/app/routes/main.py
else
    echo "✓ /app/app/routes/main.py は存在しません（正常）"
fi
echo ""

echo "4. 実行されているapp.pyの確認:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web head -30 /app/app/app.py
echo ""

echo "5. Pythonのモジュール検索パス:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web poetry run python -c "import sys; print('\n'.join(sys.path))"
echo ""

echo "6. データベース接続テスト:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec web poetry run python -c "
from app.app import app
from app.models import db, Category
app.app_context().push()
try:
    db.session.execute(db.text('SELECT 1'))
    print('✓ データベース接続成功')
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print(f'テーブル一覧: {tables}')
    count = Category.query.count()
    print(f'カテゴリ数: {count}')
except Exception as e:
    print(f'✗ エラー: {e}')
"
echo ""

echo "確認完了"


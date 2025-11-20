#!/bin/bash
# データベースの状態を確認するスクリプト

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
echo "データベース状態確認"
echo "=========================================="
echo ""

# MySQLコンテナが起動しているか確認
if ! $DOCKER_COMPOSE_CMD -f docker/docker-compose.yml ps | grep -q "quiz-app-mysql"; then
    echo "エラー: MySQLコンテナが起動していません。"
    echo "先に './scripts/run.sh' を実行してください。"
    exit 1
fi

echo "1. テーブル一覧:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "SHOW TABLES;" 2>/dev/null | grep -v "Warning" || echo "エラー: テーブル一覧の取得に失敗しました"

echo ""
echo "2. カテゴリ数:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "SELECT COUNT(*) as count FROM category;" 2>/dev/null | grep -v "Warning" || echo "エラー: カテゴリ数の取得に失敗しました"

echo ""
echo "3. 問題数:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "SELECT COUNT(*) as count FROM question;" 2>/dev/null | grep -v "Warning" || echo "エラー: 問題数の取得に失敗しました"

echo ""
echo "4. カテゴリ一覧:"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "SELECT id, name FROM category;" 2>/dev/null | grep -v "Warning" || echo "エラー: カテゴリ一覧の取得に失敗しました"

echo ""
echo "5. テーブル構造確認 (category):"
echo "-----------------------------------"
$DOCKER_COMPOSE_CMD -f docker/docker-compose.yml exec mysql mysql -uquiz_user -pquiz_password quiz_db -e "DESCRIBE category;" 2>/dev/null | grep -v "Warning" || echo "エラー: テーブル構造の取得に失敗しました"

echo ""
echo "=========================================="
echo "確認完了"
echo "=========================================="


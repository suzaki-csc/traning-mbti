#!/bin/bash

# MBTI性格診断アプリ - 停止スクリプト

set -e

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "================================================"
echo "   MBTI性格診断アプリケーション"
echo "   停止スクリプト"
echo "================================================"
echo -e "${NC}"

# コンテナの状態確認
if ! docker ps | grep -q mbti_app; then
    echo -e "${YELLOW}⚠️  コンテナは起動していません${NC}"
    exit 0
fi

# データ削除の確認
echo -e "${YELLOW}データベースのデータも削除しますか？${NC}"
echo "  (診断履歴が全て削除されます)"
read -p "データを削除する場合は 'yes' と入力してください: " -r
echo

if [[ $REPLY == "yes" ]]; then
    echo -e "${RED}🗑️  データを含めて完全に削除します...${NC}"
    docker-compose down -v
    echo -e "${GREEN}✓ データベースを含めて削除しました${NC}"
else
    echo -e "${BLUE}⏸️  コンテナを停止します...${NC}"
    docker-compose down
    echo -e "${GREEN}✓ コンテナを停止しました（データは保持されています）${NC}"
fi

echo ""
echo -e "${GREEN}停止完了${NC}"


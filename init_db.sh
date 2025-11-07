#!/bin/bash

# 色付けのための変数
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  データベース初期化スクリプト (JSON版)${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# 確認メッセージ
echo -e "${RED}⚠️  警告: この操作は既存のデータベースを完全に削除します！${NC}"
echo -e "${YELLOW}以下のデータが失われます:${NC}"
echo -e "  - 全ユーザーアカウント（管理者を含む）"
echo -e "  - 全クイズ履歴"
echo -e "  - 全問題データ"
echo ""
echo -e "${YELLOW}この操作を実行しますか？ (yes/no): ${NC}"
read -r response

if [[ "$response" != "yes" ]]; then
    echo -e "${RED}操作をキャンセルしました。${NC}"
    exit 0
fi

echo ""
echo -e "${BLUE}================================================${NC}"
echo -e "${BLUE}  データベースの初期化を開始します${NC}"
echo -e "${BLUE}================================================${NC}"
echo ""

# MySQLのdataディレクトリを削除
echo -e "${YELLOW}Step 1: MySQLデータボリュームを削除中...${NC}"
docker-compose down
docker volume rm traning-mbti_mysql_data 2>/dev/null || echo "ボリュームが存在しませんでした"
echo -e "${GREEN}✓ データボリュームを削除しました${NC}"
echo ""

# Docker Composeでサービスを起動
echo -e "${YELLOW}Step 2: Dockerサービスを起動中...${NC}"
docker-compose up -d
echo ""

# データベースの準備ができるまで待機
echo -e "${YELLOW}Step 3: データベースの起動を待機中...${NC}"
echo -e "${BLUE}（最大60秒）${NC}"
for i in {1..60}; do
    if docker-compose exec -T db mysqladmin ping -h localhost --silent 2>/dev/null; then
        echo -e "${GREEN}✓ データベースが起動しました${NC}"
        break
    fi
    echo -n "."
    sleep 1
done
echo ""
echo ""

# 初期データを投入
echo -e "${YELLOW}Step 4: 初期データを投入中...${NC}"
docker-compose exec -T web python migrations/seeds/init_data.py

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${BLUE}================================================${NC}"
    echo -e "${GREEN}✓ データベースの初期化が完了しました！${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo ""
    echo -e "${GREEN}デフォルト管理者アカウント:${NC}"
    echo -e "  Email: ${BLUE}admin@example.com${NC}"
    echo -e "  Password: ${BLUE}admin123${NC}"
    echo ""
    echo -e "${GREEN}データソース:${NC}"
    echo -e "  📁 data/categories.json"
    echo -e "  📁 data/questions/*.json"
    echo -e "  📁 data/terms/*.json"
    echo ""
    echo -e "${GREEN}ブラウザで以下のURLにアクセスしてください:${NC}"
    echo -e "  ${BLUE}http://localhost:5000${NC}"
    echo ""
else
    echo -e "${RED}エラー: 初期データの投入に失敗しました${NC}"
    echo -e "${YELLOW}ログを確認してください: docker-compose logs web${NC}"
    exit 1
fi

#!/bin/bash

# MBTI性格診断アプリ - 起動スクリプト

set -e

# 色の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# ロゴ表示
echo -e "${BLUE}"
echo "================================================"
echo "   MBTI性格診断アプリケーション"
echo "   起動スクリプト"
echo "================================================"
echo -e "${NC}"

# .envファイルの確認
if [ ! -f .env ]; then
    echo -e "${YELLOW}⚠️  .envファイルが見つかりません${NC}"
    echo "   .env.exampleから.envを作成します..."
    
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}✓ .envファイルを作成しました${NC}"
    else
        echo -e "${RED}✗ .env.exampleファイルが見つかりません${NC}"
        echo "  手動で.envファイルを作成してください"
        exit 1
    fi
fi

# Dockerの確認
if ! command -v docker &> /dev/null; then
    echo -e "${RED}✗ Dockerがインストールされていません${NC}"
    echo "  Docker Desktopをインストールしてください"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}✗ Docker Composeがインストールされていません${NC}"
    echo "  Docker Composeをインストールしてください"
    exit 1
fi

echo -e "${GREEN}✓ Dockerの確認完了${NC}"

# コンテナが既に起動しているか確認
if docker ps | grep -q mbti_app; then
    echo -e "${YELLOW}⚠️  コンテナが既に起動しています${NC}"
    read -p "再起動しますか？ (y/N): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "コンテナを停止します..."
        docker-compose down
    else
        echo "終了します"
        exit 0
    fi
fi

# コンテナのビルドと起動
echo -e "${BLUE}📦 Dockerコンテナをビルドして起動します...${NC}"
docker-compose up --build -d

# 起動待機
echo -e "${YELLOW}⏳ データベースの起動を待機中...${NC}"
sleep 10

# ヘルスチェック
MAX_RETRY=30
RETRY=0
while [ $RETRY -lt $MAX_RETRY ]; do
    if docker-compose exec -T db mysqladmin ping -h localhost -u root -proot_password &> /dev/null; then
        echo -e "${GREEN}✓ データベースが起動しました${NC}"
        break
    fi
    RETRY=$((RETRY+1))
    echo -n "."
    sleep 2
done

if [ $RETRY -eq $MAX_RETRY ]; then
    echo -e "${RED}✗ データベースの起動に失敗しました${NC}"
    echo "  ログを確認してください: docker-compose logs db"
    exit 1
fi

# アプリケーションの起動確認
echo -e "${YELLOW}⏳ アプリケーションの起動を待機中...${NC}"
sleep 5

if curl -s http://localhost:5000 > /dev/null; then
    echo -e "${GREEN}✓ アプリケーションが起動しました${NC}"
else
    echo -e "${YELLOW}⚠️  アプリケーションの起動確認に失敗しました${NC}"
    echo "  ログを確認してください: docker-compose logs app"
fi

# 完了メッセージ
echo -e "${GREEN}"
echo "================================================"
echo "   🎉 起動完了！"
echo "================================================"
echo -e "${NC}"
echo ""
echo -e "アプリケーションURL:"
echo -e "  ${BLUE}メインページ:${NC}    http://localhost:5000"
echo -e "  ${BLUE}診断履歴:${NC}        http://localhost:5000/admin/history"
echo ""
echo -e "コマンド:"
echo -e "  ${YELLOW}ログ確認:${NC}        docker-compose logs -f app"
echo -e "  ${YELLOW}停止:${NC}            docker-compose down"
echo -e "  ${YELLOW}完全削除:${NC}        docker-compose down -v"
echo ""


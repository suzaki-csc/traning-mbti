#!/bin/bash

# MBTI性格診断アプリ - ログ確認スクリプト

set -e

# 色の定義
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "================================================"
echo "   ログを表示します (Ctrl+C で終了)"
echo "================================================"
echo -e "${NC}"

# ログの表示
docker-compose logs -f --tail=100 app


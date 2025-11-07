#!/bin/bash

###############################################################################
# パスワード強度チェッカー - 起動スクリプト（Docker Compose版）
#
# このスクリプトは、Docker Composeを使用してパスワード強度チェッカーを起動します。
# Docker環境のチェック、イメージのビルド、コンテナの起動を自動で行います。
###############################################################################

# 色付き出力用の定義
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# スクリプトのディレクトリを取得
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# 使用方法を表示
show_usage() {
    echo "使用方法: $0 [オプション]"
    echo ""
    echo "オプション:"
    echo "  start       アプリケーションを起動（デフォルト）"
    echo "  stop        アプリケーションを停止"
    echo "  restart     アプリケーションを再起動"
    echo "  logs        ログを表示"
    echo "  status      コンテナの状態を確認"
    echo "  build       イメージを再ビルド"
    echo "  clean       コンテナとイメージを削除"
    echo "  help        このヘルプを表示"
    echo ""
}

# ヘッダー表示
show_header() {
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${BLUE}  パスワード強度チェッカー - Docker Compose版${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
}

# Dockerがインストールされているかチェック
check_docker() {
    echo -e "${YELLOW}[1/3] Docker環境をチェック中...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}エラー: Dockerがインストールされていません${NC}"
        echo -e "${YELLOW}以下のURLからDockerをインストールしてください:${NC}"
        echo "https://docs.docker.com/get-docker/"
        exit 1
    fi
    
    if ! docker info &> /dev/null; then
        echo -e "${RED}エラー: Dockerデーモンが起動していません${NC}"
        echo -e "${YELLOW}Docker Desktopを起動してください${NC}"
        exit 1
    fi
    
    echo -e "${GREEN}✓ Docker: $(docker --version)${NC}"
    
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        echo -e "${RED}エラー: Docker Composeがインストールされていません${NC}"
        exit 1
    fi
    
    # Docker Compose v2 (docker compose) または v1 (docker-compose) を判定
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
        echo -e "${GREEN}✓ Docker Compose: $(docker compose version)${NC}"
    else
        DOCKER_COMPOSE="docker-compose"
        echo -e "${GREEN}✓ Docker Compose: $(docker-compose --version)${NC}"
    fi
    echo ""
}

# 必要なファイルが存在するかチェック
check_files() {
    echo -e "${YELLOW}[2/3] 必要なファイルをチェック中...${NC}"
    
    REQUIRED_FILES=(
        "Dockerfile"
        "docker-compose.yml"
        "password_checker_app.py"
        "templates/password_checker.html"
        "static/css/password_style.css"
        "static/js/password_checker.js"
    )
    
    ALL_FILES_EXIST=true
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$file" ]; then
            echo -e "${GREEN}  ✓ $file${NC}"
        else
            echo -e "${RED}  ✗ $file が見つかりません${NC}"
            ALL_FILES_EXIST=false
        fi
    done
    echo ""
    
    if [ "$ALL_FILES_EXIST" = false ]; then
        echo -e "${RED}エラー: 必要なファイルが不足しています${NC}"
        exit 1
    fi
}

# アプリケーションを起動
start_app() {
    show_header
    check_docker
    check_files
    
    echo -e "${YELLOW}[3/3] アプリケーションを起動中...${NC}"
    echo ""
    
    # ポート5000が使用中かチェック
    if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
        echo -e "${YELLOW}⚠ ポート5000は既に使用されています${NC}"
        PID=$(lsof -ti:5000)
        PROCESS=$(ps -p $PID -o comm=)
        echo -e "${YELLOW}  プロセス: $PROCESS (PID: $PID)${NC}"
        
        # Dockerコンテナかどうかチェック
        if docker ps --format '{{.Names}}' | grep -q "password_checker_app"; then
            echo -e "${CYAN}既存のコンテナを停止します...${NC}"
            $DOCKER_COMPOSE down
            sleep 2
        else
            echo -e "${YELLOW}  既存のプロセスを終了しますか？ (y/n)${NC}"
            read -r response
            if [[ "$response" =~ ^[Yy]$ ]]; then
                kill -9 $PID 2>/dev/null
                echo -e "${GREEN}✓ プロセスを終了しました${NC}"
                sleep 1
            else
                echo -e "${RED}起動を中止しました${NC}"
                exit 1
            fi
        fi
    fi
    
    # Docker Composeでビルドして起動
    echo -e "${CYAN}Dockerイメージをビルド中...${NC}"
    $DOCKER_COMPOSE build
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}エラー: イメージのビルドに失敗しました${NC}"
        exit 1
    fi
    
    echo ""
    echo -e "${CYAN}コンテナを起動中...${NC}"
    $DOCKER_COMPOSE up -d
    
    if [ $? -ne 0 ]; then
        echo -e "${RED}エラー: コンテナの起動に失敗しました${NC}"
        exit 1
    fi
    
    # 起動待機
    echo ""
    echo -e "${CYAN}アプリケーションの起動を待機中...${NC}"
    sleep 3
    
    # ヘルスチェック
    for i in {1..10}; do
        if curl -s http://localhost:5000/health > /dev/null 2>&1; then
            echo -e "${GREEN}✓ アプリケーションが正常に起動しました${NC}"
            break
        fi
        if [ $i -eq 10 ]; then
            echo -e "${RED}⚠ アプリケーションの起動確認がタイムアウトしました${NC}"
            echo -e "${YELLOW}ログを確認してください: ./start_password_checker.sh logs${NC}"
        fi
        sleep 1
    done
    
    echo ""
    echo -e "${BLUE}================================================================${NC}"
    echo -e "${GREEN}パスワード強度チェッカーが起動しました${NC}"
    echo -e "${BLUE}================================================================${NC}"
    echo ""
    echo -e "${GREEN}アクセスURL: ${CYAN}http://localhost:5000${NC}"
    echo ""
    echo -e "${YELLOW}コマンド:${NC}"
    echo -e "  ${CYAN}./start_password_checker.sh stop${NC}     - アプリケーションを停止"
    echo -e "  ${CYAN}./start_password_checker.sh logs${NC}     - ログを表示"
    echo -e "  ${CYAN}./start_password_checker.sh status${NC}   - 状態を確認"
    echo ""
    echo -e "${BLUE}================================================================${NC}"
}

# アプリケーションを停止
stop_app() {
    show_header
    echo -e "${YELLOW}アプリケーションを停止中...${NC}"
    
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}エラー: Dockerがインストールされていません${NC}"
        exit 1
    fi
    
    # Docker Compose コマンドを判定
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
    fi
    
    $DOCKER_COMPOSE down
    
    echo ""
    echo -e "${GREEN}✓ アプリケーションを停止しました${NC}"
    echo ""
}

# アプリケーションを再起動
restart_app() {
    show_header
    echo -e "${YELLOW}アプリケーションを再起動中...${NC}"
    stop_app
    sleep 2
    start_app
}

# ログを表示
show_logs() {
    show_header
    echo -e "${YELLOW}ログを表示します (Ctrl+C で終了)${NC}"
    echo ""
    
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
    fi
    
    $DOCKER_COMPOSE logs -f
}

# コンテナの状態を確認
show_status() {
    show_header
    echo -e "${YELLOW}コンテナの状態:${NC}"
    echo ""
    
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
    fi
    
    $DOCKER_COMPOSE ps
    echo ""
    
    # ヘルスチェック
    if curl -s http://localhost:5000/health > /dev/null 2>&1; then
        echo -e "${GREEN}✓ アプリケーションは正常に動作しています${NC}"
        echo -e "${GREEN}  URL: http://localhost:5000${NC}"
    else
        echo -e "${RED}✗ アプリケーションにアクセスできません${NC}"
    fi
    echo ""
}

# イメージを再ビルド
rebuild_app() {
    show_header
    echo -e "${YELLOW}イメージを再ビルド中...${NC}"
    
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
    fi
    
    $DOCKER_COMPOSE build --no-cache
    
    echo ""
    echo -e "${GREEN}✓ イメージを再ビルドしました${NC}"
    echo -e "${YELLOW}変更を反映するには restart を実行してください${NC}"
    echo ""
}

# コンテナとイメージを削除
clean_app() {
    show_header
    echo -e "${RED}コンテナとイメージを削除します${NC}"
    echo -e "${YELLOW}この操作は元に戻せません。続行しますか？ (y/n)${NC}"
    read -r response
    
    if [[ ! "$response" =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}キャンセルしました${NC}"
        exit 0
    fi
    
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE="docker compose"
    else
        DOCKER_COMPOSE="docker-compose"
    fi
    
    echo ""
    echo -e "${YELLOW}コンテナを停止中...${NC}"
    $DOCKER_COMPOSE down
    
    echo -e "${YELLOW}イメージを削除中...${NC}"
    docker rmi traning-mbti-password-checker 2>/dev/null || true
    
    echo ""
    echo -e "${GREEN}✓ クリーンアップが完了しました${NC}"
    echo ""
}

# メイン処理
case "${1:-start}" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    restart)
        restart_app
        ;;
    logs)
        show_logs
        ;;
    status)
        show_status
        ;;
    build)
        rebuild_app
        ;;
    clean)
        clean_app
        ;;
    help|--help|-h)
        show_header
        show_usage
        ;;
    *)
        echo -e "${RED}エラー: 不明なオプション '$1'${NC}"
        echo ""
        show_usage
        exit 1
        ;;
esac

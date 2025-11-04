#!/bin/bash

# MBTI風性格診断アプリケーション 管理スクリプト

# 設定
APP_NAME="MBTI風性格診断"
PID_FILE="app.pid"
LOG_FILE="app.log"
APP_SCRIPT="app/main.py"
PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# プロジェクトのルートディレクトリに移動
cd "$PROJECT_ROOT"

# カラー定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 実行モード（docker or native）
EXEC_MODE=""

# ヘッダー表示
print_header() {
    echo "=========================================="
    echo "  ${APP_NAME}"
    echo "=========================================="
    echo ""
}

# 使用方法を表示
show_usage() {
    print_header
    echo "使用方法: $0 [--docker|--native] {start|stop|restart|status}"
    echo ""
    echo "オプション:"
    echo "  --docker  - Docker環境で実行"
    echo "  --native  - ネイティブPython環境で実行"
    echo "  (指定なし) - 自動検出"
    echo ""
    echo "コマンド:"
    echo "  start   - アプリケーションを起動します"
    echo "  stop    - アプリケーションを停止します"
    echo "  restart - アプリケーションを再起動します"
    echo "  status  - アプリケーションの状態を確認します"
    echo ""
    echo "例:"
    echo "  $0 start              # 自動検出して起動"
    echo "  $0 --docker start     # Docker環境で起動"
    echo "  $0 --native start     # ネイティブ環境で起動"
    echo ""
    exit 1
}

# 実行モードを検出
detect_mode() {
    if [ -n "$EXEC_MODE" ]; then
        return
    fi
    
    # docker-compose.ymlの存在とDockerの利用可能性をチェック
    if [ -f "docker/docker-compose.yml" ] && command -v docker-compose &> /dev/null; then
        EXEC_MODE="docker"
    else
        EXEC_MODE="native"
    fi
}

# ========================================
# Docker環境用の関数
# ========================================

# Docker環境でアプリケーションを起動
docker_start() {
    print_header
    echo -e "${BLUE}[Docker環境]${NC}"
    echo ""
    
    # 既に起動しているかチェック
    if docker-compose -f docker/docker-compose.yml ps | grep -q "mbti-app.*Up"; then
        echo -e "${YELLOW}⚠ Docker環境は既に起動しています${NC}"
        docker-compose -f docker/docker-compose.yml ps
        return 0
    fi
    
    # .envファイルの存在確認
    if [ ! -f ".env" ]; then
        echo -e "${YELLOW}⚠ .envファイルが見つかりません${NC}"
        echo -e "${GREEN}✓${NC} .env.exampleから.envを作成します..."
        cp .env.example .env
        echo -e "${GREEN}✓${NC} .envファイルを作成しました"
        echo ""
    fi
    
    echo -e "${GREEN}✓${NC} Dockerコンテナを起動しています..."
    echo ""
    
    # docker-compose up
    docker-compose -f docker/docker-compose.yml up -d --build
    
    if [ $? -eq 0 ]; then
        echo ""
        echo -e "${GREEN}✓ Docker環境が起動しました！${NC}"
        echo ""
        echo -e "${BLUE}ブラウザで以下のURLにアクセスしてください：${NC}"
        echo -e "  ${BLUE}→ http://localhost:5000${NC}"
        echo ""
        echo "コンテナ状態:"
        docker-compose -f docker/docker-compose.yml ps
        echo "=========================================="
    else
        echo -e "${RED}✗ Docker環境の起動に失敗しました${NC}"
        echo -e "ログを確認してください: docker-compose -f docker/docker-compose.yml logs"
        exit 1
    fi
}

# Docker環境でアプリケーションを停止
docker_stop() {
    print_header
    echo -e "${BLUE}[Docker環境]${NC}"
    echo ""
    
    # 起動しているかチェック
    if ! docker-compose -f docker/docker-compose.yml ps | grep -q "mbti-app"; then
        echo -e "${YELLOW}⚠ Docker環境は起動していません${NC}"
        return 0
    fi
    
    echo -e "${GREEN}✓${NC} Dockerコンテナを停止しています..."
    
    docker-compose -f docker/docker-compose.yml down
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Docker環境を停止しました${NC}"
        echo "=========================================="
    else
        echo -e "${RED}✗ Docker環境の停止に失敗しました${NC}"
        exit 1
    fi
}

# Docker環境でアプリケーションを再起動
docker_restart() {
    print_header
    echo -e "${BLUE}[Docker環境]${NC}"
    echo "アプリケーションを再起動します..."
    echo ""
    
    docker_stop
    echo ""
    sleep 2
    docker_start
}

# Docker環境の状態確認
docker_status() {
    print_header
    echo -e "${BLUE}[Docker環境]${NC}"
    echo ""
    
    if docker-compose -f docker/docker-compose.yml ps | grep -q "mbti-app.*Up"; then
        echo -e "${GREEN}✓ Docker環境は実行中です${NC}"
        echo ""
        echo -e "  URL: ${BLUE}http://localhost:5000${NC}"
        echo ""
        echo "コンテナ状態:"
        docker-compose -f docker/docker-compose.yml ps
        echo ""
        echo "リソース使用状況:"
        docker stats --no-stream --format "table {{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}" $(docker-compose -f docker/docker-compose.yml ps -q 2>/dev/null) 2>/dev/null || echo "  (情報取得不可)"
    else
        echo -e "${YELLOW}⚠ Docker環境は起動していません${NC}"
        echo ""
        echo "利用可能なコンテナ:"
        docker-compose -f docker/docker-compose.yml ps -a
    fi
    
    echo "=========================================="
}

# ========================================
# ネイティブ環境用の関数
# ========================================

# アプリケーションが実行中かチェック（ネイティブ環境）
is_running() {
    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        if ps -p "$PID" > /dev/null 2>&1; then
            return 0
        else
            # PIDファイルは存在するがプロセスが存在しない
            rm -f "$PID_FILE"
            return 1
        fi
    fi
    return 1
}

# アプリケーションを起動（ネイティブ環境）
start_app() {
    print_header
    echo -e "${BLUE}[ネイティブ環境]${NC}"
    echo ""
    
    if is_running; then
        echo -e "${YELLOW}⚠ アプリケーションは既に起動しています${NC}"
        PID=$(cat "$PID_FILE")
        echo -e "  PID: ${PID}"
        echo -e "  URL: http://localhost:5000"
        exit 1
    fi
    
    # Poetryの環境があるかチェック
    if [ -f "pyproject.toml" ] && command -v poetry &> /dev/null; then
        echo -e "${GREEN}✓${NC} Poetry環境を検出しました"
        echo -e "${GREEN}✓${NC} 依存パッケージを確認中..."
        poetry install --no-interaction --quiet
        
        echo -e "${GREEN}✓${NC} アプリケーションを起動しています..."
        
        # バックグラウンドで起動
        nohup poetry run python "$APP_SCRIPT" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
    else
        echo -e "${GREEN}✓${NC} 標準Python環境で起動します"
        
        # Flaskがインストールされているかチェック
        if ! python -c "import flask" 2>/dev/null; then
            echo -e "${YELLOW}⚠${NC} Flaskがインストールされていません"
            echo -e "${GREEN}✓${NC} Flaskをインストール中..."
            pip install flask
        fi
        
        echo -e "${GREEN}✓${NC} アプリケーションを起動しています..."
        
        # バックグラウンドで起動
        nohup python "$APP_SCRIPT" > "$LOG_FILE" 2>&1 &
        echo $! > "$PID_FILE"
    fi
    
    # 起動を確認
    sleep 2
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo ""
        echo -e "${GREEN}✓ アプリケーションが起動しました！${NC}"
        echo ""
        echo -e "${BLUE}ブラウザで以下のURLにアクセスしてください：${NC}"
        echo -e "  ${BLUE}→ http://localhost:5000${NC}"
        echo ""
        echo -e "PID: ${PID}"
        echo -e "ログファイル: ${LOG_FILE}"
        echo "=========================================="
    else
        echo -e "${RED}✗ アプリケーションの起動に失敗しました${NC}"
        echo -e "ログファイル（${LOG_FILE}）を確認してください"
        exit 1
    fi
}

# アプリケーションを停止（ネイティブ環境）
stop_app() {
    print_header
    echo -e "${BLUE}[ネイティブ環境]${NC}"
    echo ""
    
    if ! is_running; then
        echo -e "${YELLOW}⚠ アプリケーションは起動していません${NC}"
        exit 1
    fi
    
    PID=$(cat "$PID_FILE")
    echo -e "${GREEN}✓${NC} アプリケーションを停止しています... (PID: ${PID})"
    
    # プロセスを終了
    kill "$PID" 2>/dev/null
    
    # 終了を待つ（最大10秒）
    for i in {1..10}; do
        if ! ps -p "$PID" > /dev/null 2>&1; then
            break
        fi
        sleep 1
    done
    
    # まだ実行中の場合は強制終了
    if ps -p "$PID" > /dev/null 2>&1; then
        echo -e "${YELLOW}⚠${NC} 強制終了を実行します..."
        kill -9 "$PID" 2>/dev/null
    fi
    
    rm -f "$PID_FILE"
    echo -e "${GREEN}✓ アプリケーションを停止しました${NC}"
    echo "=========================================="
}

# アプリケーションを再起動（ネイティブ環境）
restart_app() {
    print_header
    echo -e "${BLUE}[ネイティブ環境]${NC}"
    echo "アプリケーションを再起動します..."
    echo ""
    
    if is_running; then
        stop_app
        echo ""
        sleep 2
    fi
    
    start_app
}

# アプリケーションの状態を確認（ネイティブ環境）
status_app() {
    print_header
    echo -e "${BLUE}[ネイティブ環境]${NC}"
    echo ""
    
    if is_running; then
        PID=$(cat "$PID_FILE")
        echo -e "${GREEN}✓ アプリケーションは実行中です${NC}"
        echo ""
        echo -e "  PID: ${PID}"
        echo -e "  URL: ${BLUE}http://localhost:5000${NC}"
        echo -e "  ログ: ${LOG_FILE}"
        echo ""
        
        # プロセス情報を表示
        if command -v ps &> /dev/null; then
            echo "プロセス情報:"
            ps -p "$PID" -o pid,ppid,user,%cpu,%mem,etime,command 2>/dev/null | tail -n +1
        fi
    else
        echo -e "${YELLOW}⚠ アプリケーションは起動していません${NC}"
    fi
    
    echo "=========================================="
}

# ========================================
# メイン処理
# ========================================

# コマンドライン引数の解析
while [[ $# -gt 0 ]]; do
    case $1 in
        --docker)
            EXEC_MODE="docker"
            shift
            ;;
        --native)
            EXEC_MODE="native"
            shift
            ;;
        start|stop|restart|status)
            COMMAND=$1
            shift
            ;;
        *)
            show_usage
            ;;
    esac
done

# コマンドが指定されていない場合はusageを表示
if [ -z "${COMMAND:-}" ]; then
    show_usage
fi

# 実行モードを検出
detect_mode

# 実行モードに応じて適切な関数を呼び出す
case "$EXEC_MODE" in
    docker)
        case "$COMMAND" in
            start)
                docker_start
                ;;
            stop)
                docker_stop
                ;;
            restart)
                docker_restart
                ;;
            status)
                docker_status
                ;;
        esac
        ;;
    native)
        case "$COMMAND" in
            start)
                start_app
                ;;
            stop)
                stop_app
                ;;
            restart)
                restart_app
                ;;
            status)
                status_app
                ;;
        esac
        ;;
    *)
        echo -e "${RED}✗ 実行モードの検出に失敗しました${NC}"
        exit 1
        ;;
esac

exit 0

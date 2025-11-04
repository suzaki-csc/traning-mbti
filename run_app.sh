#!/bin/bash

# MBTI風性格診断アプリケーション 管理スクリプト

# 設定
APP_NAME="MBTI風性格診断"
PID_FILE="app.pid"
LOG_FILE="app.log"
APP_SCRIPT="app.py"

# スクリプトのディレクトリに移動
cd "$(dirname "$0")"

# カラー定義
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

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
    echo "使用方法: $0 {start|stop|restart|status}"
    echo ""
    echo "コマンド:"
    echo "  start   - アプリケーションを起動します"
    echo "  stop    - アプリケーションを停止します"
    echo "  restart - アプリケーションを再起動します"
    echo "  status  - アプリケーションの状態を確認します"
    echo ""
    exit 1
}

# アプリケーションが実行中かチェック
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

# アプリケーションを起動
start_app() {
    print_header
    
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

# アプリケーションを停止
stop_app() {
    print_header
    
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

# アプリケーションを再起動
restart_app() {
    print_header
    echo "アプリケーションを再起動します..."
    echo ""
    
    if is_running; then
        stop_app
        echo ""
        sleep 2
    fi
    
    start_app
}

# アプリケーションの状態を確認
status_app() {
    print_header
    
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

# メイン処理
case "${1:-}" in
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
    *)
        show_usage
        ;;
esac

exit 0

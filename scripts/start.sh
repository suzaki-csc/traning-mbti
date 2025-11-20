#!/bin/bash
# クイズアプリケーション起動用ラッパーシェル
#
# このスクリプトは、クイズアプリケーションを起動するためのラッパーです。
# Docker Composeを使用する場合とローカル環境で起動する場合の両方に対応しています。
#
# 使用方法:
#   ./scripts/start.sh
#
# 環境変数:
#   USE_DOCKER: true/false (デフォルト: true)
#                falseに設定するとローカル環境で起動します

set -e

# プロジェクトルートディレクトリに移動
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================="
echo "クイズアプリケーション 起動スクリプト"
echo "=========================================="
echo ""

# 環境変数ファイルの確認
if [ ! -f .env ]; then
    echo "⚠️  警告: .envファイルが見つかりません。"
    if [ -f .env.example ]; then
        echo ""
        echo ".env.exampleを.envにコピーしますか？ (y/n)"
        read -r response
        if [ "$response" = "y" ] || [ "$response" = "Y" ]; then
            cp .env.example .env
            echo "✅ .envファイルを作成しました。"
            echo "   必要に応じて .env ファイルを編集してください。"
            echo ""
        else
            echo "❌ .envファイルが必要です。.env.exampleをコピーして作成してください。"
            exit 1
        fi
    else
        echo "❌ エラー: .env.exampleファイルも見つかりません。"
        exit 1
    fi
fi

# 環境変数を読み込み（.envファイルから）
if [ -f .env ]; then
    export $(grep -v '^#' .env | xargs)
fi

# Docker Composeを使用するかどうか
USE_DOCKER=${USE_DOCKER:-true}

if [ "$USE_DOCKER" = "true" ]; then
    echo "🐳 Docker Composeを使用してアプリケーションを起動します..."
    echo ""
    
    # Dockerの確認
    if ! command -v docker &> /dev/null; then
        echo "❌ エラー: Dockerがインストールされていません。"
        echo "   Dockerをインストールするか、USE_DOCKER=falseでローカル環境で起動してください。"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ エラー: Docker Composeがインストールされていません。"
        echo "   Docker Composeをインストールするか、USE_DOCKER=falseでローカル環境で起動してください。"
        exit 1
    fi
    
    cd docker
    echo "📦 コンテナをビルドして起動します..."
    echo "   初回起動時は時間がかかる場合があります。"
    echo ""
    docker-compose up --build
else
    echo "💻 ローカル環境でアプリケーションを起動します..."
    echo ""
    
    # Poetry環境の確認
    if ! command -v poetry &> /dev/null; then
        echo "❌ エラー: Poetryがインストールされていません。"
        echo ""
        echo "Poetryのインストール方法:"
        echo "  curl -sSL https://install.python-poetry.org | python3 -"
        echo "  または"
        echo "  pip install poetry"
        exit 1
    fi
    
    echo "📚 依存関係をインストールします..."
    poetry install
    echo ""
    
    echo "🗄️  データベースを初期化します..."
    poetry run python scripts/init_db.py
    echo ""
    
    echo "🚀 アプリケーションを起動します..."
    echo "   ブラウザで http://localhost:5000 にアクセスしてください。"
    echo ""
    poetry run python wsgi.py
fi


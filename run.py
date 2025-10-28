"""
アプリケーション起動スクリプト
"""
from app import create_app
import os

# アプリケーションの作成
app = create_app()

if __name__ == '__main__':
    # 開発サーバーの起動
    debug_mode = os.getenv('FLASK_ENV', 'development') == 'development'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug_mode
    )


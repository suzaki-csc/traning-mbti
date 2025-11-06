"""
アプリケーション起動スクリプト

開発サーバーを起動します。
"""
import os
from app import create_app

# 環境変数から環境を取得（デフォルトは development）
env = os.environ.get('FLASK_ENV', 'development')
app = create_app(env)

if __name__ == '__main__':
    # 開発サーバーを起動
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config['DEBUG']
    )


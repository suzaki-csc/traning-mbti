"""
Flaskアプリケーションの初期化
"""
from flask import Flask
from config import config


def create_app(config_name='default'):
    """
    Flaskアプリケーションファクトリ

    Args:
        config_name: 設定名（development, production, testing）

    Returns:
        Flask: 初期化されたFlaskアプリケーション
    """
    app = Flask(__name__)

    # 設定の読み込み
    app.config.from_object(config[config_name])

    # ブループリントの登録
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app

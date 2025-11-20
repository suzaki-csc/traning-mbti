"""
Flaskアプリケーション初期化モジュール

このモジュールはFlaskアプリケーションの初期化を行います。
データベース接続、設定の読み込み、ブループリントの登録などを担当します。
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# SQLAlchemyとMigrateのインスタンスを作成
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """
    Flaskアプリケーションのファクトリ関数
    
    Args:
        config_name: 設定名（未使用、将来の拡張用）
    
    Returns:
        Flask: 初期化されたFlaskアプリケーションインスタンス
    """
    app = Flask(__name__)
    
    # 設定の読み込み
    # データベース接続情報を環境変数から取得
    db_user = os.getenv('DB_USER', 'quiz_user')
    db_password = os.getenv('DB_PASSWORD', 'quiz_password')
    db_host = os.getenv('DB_HOST', 'localhost')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'quiz_db')
    
    # SQLAlchemyの設定
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f'mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # SQLAlchemyとMigrateの初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
    # ブループリントの登録
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app


"""
Flaskアプリケーションの初期化モジュール
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

# 環境変数の読み込み
load_dotenv()

# データベースとマイグレーションのインスタンス作成
db = SQLAlchemy()
migrate = Migrate()


def create_app(config_name=None):
    """
    Flaskアプリケーションのファクトリ関数
    
    Args:
        config_name: 設定名（未使用、将来の拡張用）
    
    Returns:
        Flask: 設定済みのFlaskアプリケーションインスタンス
    """
    app = Flask(__name__)
    
    # 設定の読み込み
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL',
        'mysql+pymysql://quiz_user:quiz_password@localhost:3306/quiz_db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # データベースとマイグレーションの初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
    # ルーティングの登録
    from app.routes import auth, quiz, history, review, admin
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(quiz.bp)
    app.register_blueprint(history.bp)
    app.register_blueprint(review.bp)
    app.register_blueprint(admin.bp)
    
    # トップページのルーティング
    @app.route('/')
    def index():
        """トップページ"""
        from flask import render_template
        return render_template('index.html')
    
    return app


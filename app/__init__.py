"""
Flaskアプリケーションファクトリ

アプリケーションの初期化と設定を行います。
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import config

# 拡張機能のインスタンス化（アプリケーションにはまだバインドしない）
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_name='default'):
    """
    Flaskアプリケーションを作成するファクトリ関数
    
    Args:
        config_name: 設定名（development, production, testing）
    
    Returns:
        Flaskアプリケーションインスタンス
    """
    app = Flask(__name__)
    
    # 設定の読み込み
    app.config.from_object(config[config_name])
    
    # 拡張機能の初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Flask-Login設定
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'このページにアクセスするにはログインが必要です。'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        """Flask-Login用のユーザーローダー"""
        from app.models import User
        return User.query.get(int(user_id))
    
    # ブループリントの登録
    from app.routes import main, quiz, api, auth, admin
    app.register_blueprint(main.main_bp)
    app.register_blueprint(quiz.quiz_bp)
    app.register_blueprint(api.api_bp, url_prefix='/api')
    app.register_blueprint(auth.auth_bp)
    app.register_blueprint(admin.admin_bp)
    
    # データベースモデルのインポート（マイグレーション用）
    from app import models
    
    # コンテキストプロセッサ（全テンプレートで使用可能な変数）
    @app.context_processor
    def inject_globals():
        """テンプレートにグローバル変数を注入"""
        return {
            'app_name': 'ITクイズアプリ',
            'app_description': 'IT用語を楽しく学べる4択クイズ'
        }
    
    # エラーハンドラ
    @app.errorhandler(404)
    def not_found_error(error):
        """404エラーハンドラ"""
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        """500エラーハンドラ"""
        from flask import render_template
        db.session.rollback()  # データベースのロールバック
        return render_template('errors/500.html'), 500
    
    return app


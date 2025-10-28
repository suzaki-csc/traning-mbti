"""
Flaskアプリケーションファクトリ
"""
from flask import Flask
from flask_login import LoginManager
from app.models import db, User
from app.config import config_dict
import os


login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    """ユーザーローダー"""
    return User.query.get(int(user_id))


def create_app(config_name=None):
    """
    Flaskアプリケーションを作成
    
    Args:
        config_name: 設定名（development, production, testing）
    
    Returns:
        Flask: Flaskアプリケーション
    """
    app = Flask(__name__)
    
    # 設定の読み込み
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app.config.from_object(config_dict.get(config_name, config_dict['default']))
    
    # データベースの初期化
    db.init_app(app)
    
    # ログインマネージャーの初期化
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'
    login_manager.login_message = 'このページにアクセスするにはログインが必要です。'
    login_manager.login_message_category = 'warning'
    
    # Blueprintの登録
    from app.routes.main import main as main_blueprint
    from app.routes.quiz import quiz as quiz_blueprint
    from app.routes.admin import admin as admin_blueprint
    
    app.register_blueprint(main_blueprint)
    app.register_blueprint(quiz_blueprint)
    app.register_blueprint(admin_blueprint)
    
    # データベーステーブルの作成
    with app.app_context():
        db.create_all()
        
        # 初期管理者ユーザーの作成（存在しない場合）
        if not User.query.filter_by(username='admin').first():
            admin_user = User(
                username='admin',
                email='admin@example.com',
                role='admin'
            )
            admin_user.set_password('admin123')
            db.session.add(admin_user)
            db.session.commit()
            print('初期管理者ユーザーを作成しました: admin / admin123')
    
    # エラーハンドラー
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        db.session.rollback()
        return render_template('errors/500.html'), 500
    
    # コンテキストプロセッサー
    @app.context_processor
    def utility_processor():
        """テンプレートで使用できるユーティリティ関数"""
        from app.auth import get_mbti_name, get_mbti_description
        return {
            'get_mbti_name': get_mbti_name,
            'get_mbti_description': get_mbti_description
        }
    
    return app


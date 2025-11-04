from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # 拡張機能の初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
    # Flask-Loginの初期化
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'このページにアクセスするにはログインが必要です。'
    login_manager.login_message_category = 'warning'
    
    @login_manager.user_loader
    def load_user(user_id):
        from app.models import User
        return User.query.get(int(user_id))

    # ブループリントの登録
    from app.routes import main_bp, admin_bp, auth_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(auth_bp, url_prefix='/auth')

    # アプリケーションコンテキスト内でテーブルを作成
    with app.app_context():
        from app import models
        db.create_all()
        
        # デフォルト管理者ユーザーの作成
        create_default_admin()

    return app


def create_default_admin():
    """デフォルト管理者ユーザーを作成（存在しない場合のみ）"""
    from app.models import User
    
    # 管理者ユーザーが既に存在するかチェック
    admin_user = User.query.filter_by(email='admin@example.com').first()
    
    if not admin_user:
        # デフォルト管理者を作成
        admin = User(
            email='admin@example.com',
            username='admin',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        
        db.session.add(admin)
        db.session.commit()
        
        print('✓ デフォルト管理者ユーザーを作成しました')
        print('  Email: admin@example.com')
        print('  Password: admin123')
    else:
        print('✓ 管理者ユーザーは既に存在します')


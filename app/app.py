"""Flaskアプリケーションエントリーポイント"""
from flask import Flask
from flask_migrate import Migrate
from config import Config
from models import db

# Migrateインスタンス
migrate = Migrate()


def create_app(config_class=Config):
    """アプリケーションファクトリ"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # データベース初期化
    db.init_app(app)
    migrate.init_app(app, db)
    
    # ブループリント登録
    from routes.main import main_bp
    from routes.admin import admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp)
    
    # データベーステーブル作成
    with app.app_context():
        db.create_all()
    
    return app


# アプリケーションインスタンス作成
app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


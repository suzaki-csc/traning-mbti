"""
カスタムデコレーター

ロールベースのアクセス制御などのデコレーターを定義します。
"""
from functools import wraps
from flask import abort, flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """
    管理者権限が必要なルートに適用するデコレーター
    
    Usage:
        @app.route('/admin')
        @login_required
        @admin_required
        def admin_page():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('このページにアクセスするにはログインが必要です。', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            flash('このページにアクセスする権限がありません。', 'danger')
            abort(403)
        
        return f(*args, **kwargs)
    return decorated_function


def active_user_required(f):
    """
    アクティブなユーザーのみアクセス可能にするデコレーター
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('このページにアクセスするにはログインが必要です。', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_active:
            flash('アカウントが無効化されています。管理者にお問い合わせください。', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function


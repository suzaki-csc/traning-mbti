"""アクセス制御デコレータ"""
from functools import wraps
from flask import flash, redirect, url_for
from flask_login import current_user


def admin_required(f):
    """管理者権限が必要なルートに適用するデコレータ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('このページにアクセスするには管理者としてログインが必要です。', 'danger')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin():
            flash('このページにアクセスする権限がありません。', 'danger')
            return redirect(url_for('main.index'))
        
        return f(*args, **kwargs)
    return decorated_function


def user_required(f):
    """ログイン済みユーザーが必要なルートに適用するデコレータ"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('このページにアクセスするにはログインが必要です。', 'warning')
            return redirect(url_for('auth.login'))
        
        return f(*args, **kwargs)
    return decorated_function


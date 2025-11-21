"""
認証関連のユーティリティ関数
"""
from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(f):
    """
    ログイン必須デコレータ
    
    Args:
        f: デコレートする関数
    
    Returns:
        デコレートされた関数
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('ログインが必要です', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """
    管理者権限必須デコレータ
    
    Args:
        f: デコレートする関数
    
    Returns:
        デコレートされた関数
    """
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin', False):
            flash('管理者権限が必要です', 'danger')
            return redirect(url_for('quiz.select'))
        return f(*args, **kwargs)
    return decorated_function


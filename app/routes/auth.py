"""
認証関連のルート

ログイン、ログアウト、ユーザー登録などの認証機能を提供します。
"""
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ログイン画面"""
    # 既にログイン済みの場合はホームにリダイレクト
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        remember = request.form.get('remember', False) == 'on'
        
        # バリデーション
        if not email or not password:
            flash('メールアドレスとパスワードを入力してください。', 'danger')
            return render_template('auth/login.html')
        
        # ユーザー検索
        user = User.query.filter_by(email=email).first()
        
        # 認証チェック
        if user is None or not user.check_password(password):
            flash('メールアドレスまたはパスワードが正しくありません。', 'danger')
            return render_template('auth/login.html')
        
        # アカウントが無効化されているかチェック
        if not user.is_active:
            flash('このアカウントは無効化されています。管理者にお問い合わせください。', 'danger')
            return render_template('auth/login.html')
        
        # ログイン成功
        login_user(user, remember=remember)
        user.last_login_at = datetime.utcnow()
        db.session.commit()
        
        flash(f'ようこそ、{user.email}さん！', 'success')
        
        # next パラメータがあればそこにリダイレクト、なければホームへ
        next_page = request.args.get('next')
        if next_page and next_page.startswith('/'):
            return redirect(next_page)
        return redirect(url_for('main.index'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """ログアウト"""
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """ユーザー登録画面"""
    # 既にログイン済みの場合はホームにリダイレクト
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # バリデーション
        if not email or not password or not password_confirm:
            flash('すべての項目を入力してください。', 'danger')
            return render_template('auth/register.html')
        
        # メールアドレスの形式チェック（簡易版）
        if '@' not in email or '.' not in email:
            flash('有効なメールアドレスを入力してください。', 'danger')
            return render_template('auth/register.html')
        
        # パスワードの長さチェック
        if len(password) < 6:
            flash('パスワードは6文字以上で設定してください。', 'danger')
            return render_template('auth/register.html')
        
        # パスワード確認
        if password != password_confirm:
            flash('パスワードが一致しません。', 'danger')
            return render_template('auth/register.html')
        
        # メールアドレスの重複チェック
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('このメールアドレスは既に登録されています。', 'danger')
            return render_template('auth/register.html')
        
        # ユーザーを作成
        user = User(email=email, role='user')
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            flash('アカウントを作成しました。ログインしてください。', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('アカウントの作成に失敗しました。もう一度お試しください。', 'danger')
            return render_template('auth/register.html')
    
    return render_template('auth/register.html')


@auth_bp.route('/profile')
@login_required
def profile():
    """ユーザープロフィール画面"""
    # ユーザーのクイズ履歴を取得
    quiz_sessions = current_user.quiz_sessions.filter_by(
        is_review_mode=False
    ).order_by(db.desc('started_at')).limit(10).all()
    
    # 統計情報を計算
    total_quizzes = current_user.quiz_sessions.filter_by(is_review_mode=False).count()
    completed_quizzes = current_user.quiz_sessions.filter(
        db.and_(
            db.Column('is_review_mode') == False,
            db.Column('completed_at').isnot(None)
        )
    ).count()
    
    total_correct = 0
    total_questions = 0
    for session in current_user.quiz_sessions.filter_by(is_review_mode=False).all():
        if session.completed_at:
            total_correct += session.correct_count
            total_questions += session.total_questions
    
    avg_accuracy = (total_correct / total_questions * 100) if total_questions > 0 else 0
    
    return render_template('auth/profile.html',
                         quiz_sessions=quiz_sessions,
                         total_quizzes=total_quizzes,
                         completed_quizzes=completed_quizzes,
                         avg_accuracy=avg_accuracy)

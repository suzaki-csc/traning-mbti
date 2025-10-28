"""
メインルーティング（認証、トップページなど）
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app.models import db, User, TestResult

# Blueprintの作成
main = Blueprint('main', __name__)


@main.route('/')
def index():
    """トップページ"""
    if not current_user.is_authenticated:
        return redirect(url_for('main.login'))
    
    # 最新の診断結果を取得
    latest_results = TestResult.query.filter_by(user_id=current_user.id)\
        .order_by(TestResult.taken_at.desc())\
        .limit(5).all()
    
    return render_template('index.html', latest_results=latest_results)


@main.route('/login', methods=['GET', 'POST'])
def login():
    """ログインページ"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not username or not password:
            flash('ユーザー名とパスワードを入力してください。', 'danger')
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            flash(f'ようこそ、{user.username}さん！', 'success')
            return redirect(url_for('main.index'))
        else:
            flash('ユーザー名またはパスワードが正しくありません。', 'danger')
    
    return render_template('login.html')


@main.route('/register', methods=['GET', 'POST'])
def register():
    """新規登録ページ"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # バリデーション
        if not all([username, email, password, password_confirm]):
            flash('すべての項目を入力してください。', 'danger')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('パスワードが一致しません。', 'danger')
            return render_template('register.html')
        
        if len(password) < 6:
            flash('パスワードは6文字以上にしてください。', 'danger')
            return render_template('register.html')
        
        # ユーザー名とメールの重複チェック
        if User.query.filter_by(username=username).first():
            flash('このユーザー名は既に使用されています。', 'danger')
            return render_template('register.html')
        
        if User.query.filter_by(email=email).first():
            flash('このメールアドレスは既に使用されています。', 'danger')
            return render_template('register.html')
        
        # 新規ユーザー作成
        user = User(username=username, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('登録が完了しました。ログインしてください。', 'success')
            return redirect(url_for('main.login'))
        except Exception as e:
            db.session.rollback()
            flash('登録中にエラーが発生しました。', 'danger')
            return render_template('register.html')
    
    return render_template('register.html')


@main.route('/logout')
@login_required
def logout():
    """ログアウト"""
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('main.login'))


@main.route('/history')
@login_required
def history():
    """診断履歴ページ"""
    page = request.args.get('page', 1, type=int)
    per_page = 10
    
    pagination = TestResult.query.filter_by(user_id=current_user.id)\
        .order_by(TestResult.taken_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    results = pagination.items
    
    return render_template('history.html', 
                         results=results, 
                         pagination=pagination)


"""
認証関連のルーティング
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User
from app.utils.auth import login_required
import pymysql

bp = Blueprint('auth', __name__, url_prefix='')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    """ログインページ"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        password = request.form.get('password', '').strip()
        
        if not user_id or not password:
            flash('ユーザーIDとパスワードを入力してください', 'danger')
            return render_template('auth/login.html')
        
        # SQLインジェクション脆弱性: 文字列連結でSQLクエリを構築
        try:
            # データベース接続情報を取得
            from flask import current_app
            db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
            
            # URIから接続情報を抽出
            # mysql+pymysql://user:password@host:port/database
            import re
            match = re.match(r'mysql\+pymysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_uri)
            if match:
                db_user, db_password, db_host, db_port, db_name = match.groups()
                
                # データベースに接続
                connection = pymysql.connect(
                    host=db_host,
                    port=int(db_port),
                    user=db_user,
                    password=db_password,
                    database=db_name,
                    cursorclass=pymysql.cursors.DictCursor
                )
                
                # 脆弱なSQLクエリ: 文字列連結を使用
                query = f"SELECT * FROM users WHERE user_id = '{user_id}' AND password_hash = '{password}'"
                cursor = connection.cursor()
                cursor.execute(query)
                user_data = cursor.fetchone()
                cursor.close()
                connection.close()
                
                if user_data:
                    # ログイン成功
                    session['user_id'] = user_data['id']
                    session['user_name'] = user_data['user_id']
                    session['is_admin'] = (user_data['role'] == 'admin')
                    flash('ログインに成功しました', 'success')
                    return redirect(url_for('quiz.select'))
                else:
                    # 通常の認証方法も試行（既存ユーザーのため）
                    user = User.query.filter_by(user_id=user_id).first()
                    if user and user.check_password(password):
                        session['user_id'] = user.id
                        session['user_name'] = user.user_id
                        session['is_admin'] = user.is_admin()
                        flash('ログインに成功しました', 'success')
                        return redirect(url_for('quiz.select'))
                    else:
                        flash('ユーザーIDまたはパスワードが正しくありません', 'danger')
            else:
                # 通常の認証方法
                user = User.query.filter_by(user_id=user_id).first()
                if user and user.check_password(password):
                    session['user_id'] = user.id
                    session['user_name'] = user.user_id
                    session['is_admin'] = user.is_admin()
                    flash('ログインに成功しました', 'success')
                    return redirect(url_for('quiz.select'))
                else:
                    flash('ユーザーIDまたはパスワードが正しくありません', 'danger')
        except Exception as e:
            # エラーが発生した場合は通常の認証方法を試行
            user = User.query.filter_by(user_id=user_id).first()
            if user and user.check_password(password):
                session['user_id'] = user.id
                session['user_name'] = user.user_id
                session['is_admin'] = user.is_admin()
                flash('ログインに成功しました', 'success')
                return redirect(url_for('quiz.select'))
            else:
                flash('ユーザーIDまたはパスワードが正しくありません', 'danger')
    
    return render_template('auth/login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    """新規登録ページ"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        password_confirm = request.form.get('password_confirm', '').strip()
        
        # バリデーション
        if not user_id or not email or not password:
            flash('すべての項目を入力してください', 'danger')
            return render_template('auth/register.html')
        
        if password != password_confirm:
            flash('パスワードが一致しません', 'danger')
            return render_template('auth/register.html')
        
        if len(password) < 6:
            flash('パスワードは6文字以上で入力してください', 'danger')
            return render_template('auth/register.html')
        
        # ユーザーIDとメールアドレスの重複チェック
        if User.query.filter_by(user_id=user_id).first():
            flash('このユーザーIDは既に使用されています', 'danger')
            return render_template('auth/register.html')
        
        if User.query.filter_by(email=email).first():
            flash('このメールアドレスは既に使用されています', 'danger')
            return render_template('auth/register.html')
        
        # 新規ユーザー作成
        user = User(user_id=user_id, email=email)
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            flash('登録が完了しました。ログインしてください', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            db.session.rollback()
            flash('登録に失敗しました', 'danger')
    
    return render_template('auth/register.html')


@bp.route('/logout')
@login_required
def logout():
    """ログアウト"""
    session.clear()
    flash('ログアウトしました', 'info')
    return redirect(url_for('index'))


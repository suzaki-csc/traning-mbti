"""
パスワード強度チェッカー - Flaskアプリケーション

このアプリケーションは、ユーザーが入力したパスワードの強度を
リアルタイムで評価し、セキュリティ向上のためのアドバイスを提供します。

データベース機能:
- パスワードチェック結果の保存（ハッシュ値とマスク表示）
- チェック履歴の表示
- ユーザー認証とロール管理
"""

import os
from datetime import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, PasswordCheck, User

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# SECRET_KEY設定（本番環境では環境変数から読み込む）
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# データベース設定
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'password_checker')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'apppassword')

# SQLAlchemy設定
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True,
}

# データベース初期化
db.init_app(app)

# Flask-Login設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'このページにアクセスするにはログインが必要です。'


@login_manager.user_loader
def load_user(user_id):
    """
    Flask-Login用のユーザーローダー
    """
    return User.query.get(int(user_id))


def admin_required(f):
    """
    管理者権限が必要なルートのためのデコレーター
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return redirect(url_for('login'))
        if not current_user.is_admin():
            flash('このページにアクセスする権限がありません。', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/')
def index():
    """
    メインページを表示するルート
    
    ルートURL（/）にアクセスされた場合、
    パスワード強度チェッカーのHTMLページを返します。
    """
    return render_template('password_checker.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    ログインページ
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        if not email or not password:
            flash('メールアドレスとパスワードを入力してください。', 'warning')
            return render_template('login.html')
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('このアカウントは無効化されています。', 'danger')
                return render_template('login.html')
            
            # ログイン成功
            login_user(user, remember=remember)
            
            # 最終ログイン時刻を更新
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            flash(f'ようこそ、{user.email}さん！', 'success')
            
            # リダイレクト先を取得
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            # 管理者は管理画面へ、一般ユーザーはトップページへ
            if user.is_admin():
                return redirect(url_for('admin_dashboard'))
            return redirect(url_for('index'))
        else:
            flash('メールアドレスまたはパスワードが正しくありません。', 'danger')
    
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """
    ログアウト
    """
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """
    ユーザー登録ページ
    """
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        username = request.form.get('username')
        
        # バリデーション
        if not email or not password:
            flash('メールアドレスとパスワードは必須です。', 'warning')
            return render_template('register.html')
        
        if password != password_confirm:
            flash('パスワードが一致しません。', 'warning')
            return render_template('register.html')
        
        if len(password) < 8:
            flash('パスワードは8文字以上で設定してください。', 'warning')
            return render_template('register.html')
        
        # 既存ユーザーチェック
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('このメールアドレスは既に登録されています。', 'danger')
            return render_template('register.html')
        
        # 新規ユーザー作成
        user = User(
            email=email,
            username=username or email.split('@')[0],
            role='user'
        )
        user.set_password(password)
        
        try:
            db.session.add(user)
            db.session.commit()
            
            flash('アカウントを作成しました。ログインしてください。', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'User registration error: {str(e)}')
            flash('アカウントの作成に失敗しました。', 'danger')
    
    return render_template('register.html')


@app.route('/health')
def health():
    """
    ヘルスチェック用のエンドポイント
    
    アプリケーションとデータベースが正常に動作しているか確認するためのAPI
    """
    try:
        # データベース接続確認
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'ok',
            'message': 'Password Checker App is running',
            'database': 'connected'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Database connection failed',
            'error': str(e)
        }), 500


@app.route('/api/save-check', methods=['POST'])
def save_check():
    """
    パスワードチェック結果を保存するAPI
    
    Request Body (JSON):
    {
        "password": "元のパスワード",
        "score": 75,
        "strength_level": "strong",
        "entropy": 52.4,
        "crack_time": "約1,425年",
        "has_lowercase": true,
        "has_uppercase": true,
        "has_digit": true,
        "has_symbol": true,
        "has_common_word": false,
        "has_repeating": false,
        "has_sequential": false,
        "has_keyboard_pattern": false
    }
    
    Returns:
        JSON: 保存結果
    """
    try:
        data = request.get_json()
        
        # 必須パラメータの確認
        if not data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'パスワードが指定されていません'
            }), 400
        
        password = data['password']
        
        # パスワードチェック結果をデータベースに保存
        # ログインユーザーがいる場合はuser_idを設定
        check = PasswordCheck(
            user_id=current_user.id if current_user.is_authenticated else None,
            password_hash=PasswordCheck.hash_password(password),
            password_masked=PasswordCheck.mask_password(password),
            score=data.get('score', 0),
            strength_level=data.get('strength_level', 'unknown'),
            entropy=data.get('entropy', 0.0),
            crack_time=data.get('crack_time', '不明'),
            has_lowercase=data.get('has_lowercase', False),
            has_uppercase=data.get('has_uppercase', False),
            has_digit=data.get('has_digit', False),
            has_symbol=data.get('has_symbol', False),
            has_common_word=data.get('has_common_word', False),
            has_repeating=data.get('has_repeating', False),
            has_sequential=data.get('has_sequential', False),
            has_keyboard_pattern=data.get('has_keyboard_pattern', False),
            password_length=len(password)
        )
        
        db.session.add(check)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'チェック結果を保存しました',
            'id': check.id,
            'password_masked': check.password_masked
        })
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error saving check result: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'チェック結果の保存に失敗しました',
            'error': str(e)
        }), 500


@app.route('/api/history')
def get_history():
    """
    パスワードチェック履歴を取得するAPI
    
    Query Parameters:
        limit (int): 取得件数（デフォルト: 10、最大: 100）
        offset (int): オフセット（デフォルト: 0）
    
    Returns:
        JSON: チェック履歴のリスト
    """
    try:
        # クエリパラメータの取得
        limit = min(int(request.args.get('limit', 10)), 100)
        offset = int(request.args.get('offset', 0))
        
        # データベースから履歴を取得（新しい順）
        checks = PasswordCheck.query.order_by(
            PasswordCheck.created_at.desc()
        ).limit(limit).offset(offset).all()
        
        # 総件数を取得
        total = PasswordCheck.query.count()
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': [check.to_dict() for check in checks]
        })
        
    except Exception as e:
        app.logger.error(f'Error getting history: {str(e)}')
        return jsonify({
            'success': False,
            'message': '履歴の取得に失敗しました',
            'error': str(e)
        }), 500


@app.route('/api/stats')
def get_stats():
    """
    パスワードチェック統計情報を取得するAPI
    
    Returns:
        JSON: 統計情報
    """
    try:
        # 総チェック数
        total_checks = PasswordCheck.query.count()
        
        # 強度レベル別の集計
        from sqlalchemy import func
        strength_stats = db.session.query(
            PasswordCheck.strength_level,
            func.count(PasswordCheck.id).label('count')
        ).group_by(PasswordCheck.strength_level).all()
        
        # 平均スコア
        avg_score = db.session.query(
            func.avg(PasswordCheck.score)
        ).scalar() or 0
        
        # 平均パスワード長
        avg_length = db.session.query(
            func.avg(PasswordCheck.password_length)
        ).scalar() or 0
        
        # パターン検出統計
        pattern_stats = {
            'common_word': PasswordCheck.query.filter_by(has_common_word=True).count(),
            'repeating': PasswordCheck.query.filter_by(has_repeating=True).count(),
            'sequential': PasswordCheck.query.filter_by(has_sequential=True).count(),
            'keyboard_pattern': PasswordCheck.query.filter_by(has_keyboard_pattern=True).count(),
        }
        
        return jsonify({
            'success': True,
            'total_checks': total_checks,
            'avg_score': round(avg_score, 2),
            'avg_length': round(avg_length, 2),
            'strength_distribution': {level: count for level, count in strength_stats},
            'pattern_stats': pattern_stats
        })
        
    except Exception as e:
        app.logger.error(f'Error getting stats: {str(e)}')
        return jsonify({
            'success': False,
            'message': '統計情報の取得に失敗しました',
            'error': str(e)
        }), 500


@app.route('/admin')
@admin_required
def admin_dashboard():
    """
    管理者ダッシュボード
    """
    # 統計情報を取得
    total_users = User.query.count()
    total_checks = PasswordCheck.query.count()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_checks=total_checks,
                         recent_users=recent_users)


@app.route('/admin/users')
@admin_required
def admin_users():
    """
    ユーザー一覧
    """
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/users/<int:user_id>')
@admin_required
def admin_user_detail(user_id):
    """
    ユーザー詳細
    """
    user = User.query.get_or_404(user_id)
    checks = user.password_checks.order_by(PasswordCheck.created_at.desc()).limit(20).all()
    return render_template('admin/user_detail.html', user=user, checks=checks)


@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_user_edit(user_id):
    """
    ユーザー情報編集
    """
    user = User.query.get_or_404(user_id)
    
    # 自分自身の管理者権限は剥奪できないようにする
    if user.id == current_user.id and request.method == 'POST':
        role = request.form.get('role')
        if role != 'admin':
            flash('自分自身の管理者権限は変更できません。', 'danger')
            return redirect(url_for('admin_user_edit', user_id=user_id))
    
    if request.method == 'POST':
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        user.role = request.form.get('role', user.role)
        user.is_active = request.form.get('is_active') == 'on'
        
        # パスワード変更（入力された場合のみ）
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        try:
            db.session.commit()
            flash('ユーザー情報を更新しました。', 'success')
            return redirect(url_for('admin_user_detail', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'User update error: {str(e)}')
            flash('ユーザー情報の更新に失敗しました。', 'danger')
    
    return render_template('admin/user_edit.html', user=user)


@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_user_delete(user_id):
    """
    ユーザー削除
    """
    user = User.query.get_or_404(user_id)
    
    # 自分自身は削除できない
    if user.id == current_user.id:
        flash('自分自身は削除できません。', 'danger')
        return redirect(url_for('admin_users'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'ユーザー {user.email} を削除しました。', 'success')
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'User deletion error: {str(e)}')
        flash('ユーザーの削除に失敗しました。', 'danger')
    
    return redirect(url_for('admin_users'))


@app.route('/profile')
@login_required
def profile():
    """
    ユーザープロフィールページ（自分の履歴確認）
    """
    checks = current_user.password_checks.order_by(PasswordCheck.created_at.desc()).limit(20).all()
    return render_template('profile.html', user=current_user, checks=checks)


@app.cli.command('init-db')
def init_db():
    """
    データベースを初期化するコマンド
    
    使用方法:
        flask init-db
    """
    db.create_all()
    print('データベースを初期化しました')


@app.cli.command('drop-db')
def drop_db():
    """
    データベースを削除するコマンド
    
    使用方法:
        flask drop-db
    """
    db.drop_all()
    print('データベースを削除しました')


@app.cli.command('create-admin')
def create_admin():
    """
    デフォルト管理者を作成するコマンド
    
    使用方法:
        flask create-admin
    """
    # 既存の管理者をチェック
    existing_admin = User.query.filter_by(email='admin@example.com').first()
    if existing_admin:
        print('管理者アカウント admin@example.com は既に存在します')
        return
    
    # 管理者を作成
    admin = User(
        email='admin@example.com',
        username='Administrator',
        role='admin',
        is_active=True
    )
    admin.set_password('admin123')
    
    try:
        db.session.add(admin)
        db.session.commit()
        print('デフォルト管理者を作成しました:')
        print('  Email: admin@example.com')
        print('  Password: admin123')
        print('⚠️ 本番環境では必ずパスワードを変更してください！')
    except Exception as e:
        db.session.rollback()
        print(f'管理者の作成に失敗しました: {str(e)}')


if __name__ == '__main__':
    """
    アプリケーションのエントリーポイント
    
    このスクリプトを直接実行した場合、開発用サーバーを起動します。
    debug=True: コード変更時に自動リロード、詳細なエラー表示
    host='0.0.0.0': すべてのネットワークインターフェースでリッスン
    port=5000: ポート5000で起動
    """
    with app.app_context():
        # データベーステーブルを自動作成
        db.create_all()
        print("データベーステーブルを作成/確認しました")
        
        # デフォルト管理者が存在しない場合は作成
        existing_admin = User.query.filter_by(email='admin@example.com').first()
        if not existing_admin:
            admin = User(
                email='admin@example.com',
                username='Administrator',
                role='admin',
                is_active=True
            )
            admin.set_password('admin123')
            
            try:
                db.session.add(admin)
                db.session.commit()
                print("")
                print("=" * 60)
                print("デフォルト管理者を作成しました:")
                print("  Email: admin@example.com")
                print("  Password: admin123")
                print("⚠️ 本番環境では必ずパスワードを変更してください！")
                print("=" * 60)
                print("")
            except Exception as e:
                db.session.rollback()
                print(f"管理者の作成に失敗しました: {str(e)}")
    
    print("=" * 60)
    print("パスワード強度チェッカーを起動中...")
    print("アクセスURL: http://localhost:5000")
    print("ログイン: http://localhost:5000/login")
    print("管理画面: http://localhost:5000/admin")
    print("停止: Ctrl+C")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

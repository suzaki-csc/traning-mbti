"""
MBTI風性格診断Webアプリケーション（ログイン機能付き）
"""

import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime
from app.database import db, User, DiagnosisResult
from app.mbti import (
    QUESTIONS, ANSWER_OPTIONS, get_question_by_id, get_total_questions,
    calculate_scores, determine_mbti_type, get_axis_percentages, get_mbti_info
)

app = Flask(__name__)

# 設定
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mbti-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mbti.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# 拡張機能の初期化
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message = 'ログインが必要です'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# ==================== 診断機能 ====================

@app.route('/')
def index():
    """トップページ"""
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    """診断開始"""
    session.clear()
    session['answers'] = {}
    return redirect(url_for('question', q_num=1))


@app.route('/question/<int:q_num>')
def question(q_num):
    """質問ページ"""
    total = get_total_questions()
    if q_num < 1 or q_num > total or 'answers' not in session:
        return redirect(url_for('index'))
    
    current_question = get_question_by_id(q_num)
    if not current_question:
        return redirect(url_for('index'))
    
    current_answer = session['answers'].get(str(q_num))
    
    return render_template(
        'question.html',
        question=current_question,
        q_num=q_num,
        total=total,
        answer_options=ANSWER_OPTIONS,
        current_answer=current_answer
    )


@app.route('/answer/<int:q_num>', methods=['POST'])
def answer(q_num):
    """回答受付"""
    if 'answers' not in session:
        return redirect(url_for('index'))
    
    answer_value = request.form.get('answer')
    if not answer_value:
        return redirect(url_for('question', q_num=q_num))
    
    session['answers'][str(q_num)] = int(answer_value)
    session.modified = True
    
    total = get_total_questions()
    next_q_num = q_num + 1
    
    if next_q_num > total:
        return redirect(url_for('result'))
    else:
        return redirect(url_for('question', q_num=next_q_num))


@app.route('/back/<int:q_num>', methods=['POST'])
def back(q_num):
    """前の質問に戻る"""
    if q_num <= 1:
        return redirect(url_for('index'))
    return redirect(url_for('question', q_num=q_num - 1))


@app.route('/result')
def result():
    """結果ページ"""
    if 'answers' not in session:
        return redirect(url_for('index'))
    
    answers = session['answers']
    total = get_total_questions()
    
    # 未回答チェック
    if len(answers) < total:
        for i in range(1, total + 1):
            if str(i) not in answers:
                return redirect(url_for('question', q_num=i))
    
    # スコア計算
    scores = calculate_scores(answers)
    mbti_type = determine_mbti_type(scores)
    mbti_info = get_mbti_info(mbti_type)
    percentages = get_axis_percentages(scores)
    
    # ログインしている場合はデータベースに保存
    if current_user.is_authenticated:
        try:
            result = DiagnosisResult(
                user_id=current_user.id,
                mbti_type=mbti_type,
                score_ei=scores['EI'],
                score_sn=scores['SN'],
                score_tf=scores['TF'],
                score_jp=scores['JP'],
                answers=answers
            )
            db.session.add(result)
            db.session.commit()
            flash('診断結果を保存しました', 'success')
        except Exception as e:
            db.session.rollback()
            app.logger.error(f'保存エラー: {e}')
    
    return render_template(
        'result.html',
        mbti_type=mbti_type,
        mbti_info=mbti_info,
        scores=scores,
        percentages=percentages
    )


@app.route('/restart')
def restart():
    """診断をやり直す"""
    session.clear()
    return redirect(url_for('index'))


# ==================== 認証機能 ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ログイン"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password) and user.is_active:
            login_user(user)
            user.last_login = datetime.utcnow()
            db.session.commit()
            flash(f'ようこそ、{user.username}さん！', 'success')
            return redirect(url_for('index'))
        else:
            flash('メールアドレスまたはパスワードが正しくありません', 'danger')
    
    return render_template('auth/login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """新規登録"""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(email=email).first():
            flash('このメールアドレスは既に登録されています', 'danger')
        else:
            user = User(email=email, username=username, role='user')
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash('登録完了しました。ログインしてください', 'success')
            return redirect(url_for('login'))
    
    return render_template('auth/register.html')


@app.route('/logout')
@login_required
def logout():
    """ログアウト"""
    logout_user()
    flash('ログアウトしました', 'info')
    return redirect(url_for('index'))


# ==================== 診断履歴 ====================

@app.route('/history')
@login_required
def history():
    """診断履歴"""
    results = DiagnosisResult.query.filter_by(user_id=current_user.id)\
        .order_by(DiagnosisResult.created_at.desc()).all()
    return render_template('diagnosis/history.html', results=results)


# ==================== 管理画面 ====================

def admin_required(f):
    """管理者権限チェックデコレータ"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            flash('管理者権限が必要です', 'danger')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated_function


@app.route('/admin')
@admin_required
def admin_dashboard():
    """管理ダッシュボード"""
    total_users = User.query.count()
    total_results = DiagnosisResult.query.count()
    return render_template('admin/dashboard.html', 
                         total_users=total_users, 
                         total_results=total_results)


@app.route('/admin/users')
@admin_required
def admin_users():
    """ユーザー一覧"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/users/<int:user_id>')
@admin_required
def admin_user_detail(user_id):
    """ユーザー詳細"""
    user = User.query.get_or_404(user_id)
    results = DiagnosisResult.query.filter_by(user_id=user_id)\
        .order_by(DiagnosisResult.created_at.desc()).all()
    return render_template('admin/user_detail.html', user=user, results=results)


@app.route('/admin/users/<int:user_id>/edit', methods=['POST'])
@admin_required
def admin_user_edit(user_id):
    """ユーザー情報編集"""
    user = User.query.get_or_404(user_id)
    
    # 自分自身の管理者権限は削除できない
    if user.id == current_user.id and request.form.get('role') != 'admin':
        flash('自分自身の管理者権限は削除できません', 'danger')
        return redirect(url_for('admin_user_detail', user_id=user_id))
    
    try:
        user.username = request.form.get('username', user.username)
        user.email = request.form.get('email', user.email)
        user.role = request.form.get('role', user.role)
        user.is_active = request.form.get('is_active') == 'on'
        
        # パスワード変更（入力された場合のみ）
        new_password = request.form.get('new_password')
        if new_password:
            user.set_password(new_password)
        
        db.session.commit()
        flash(f'ユーザー「{user.username}」の情報を更新しました', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'エラーが発生しました: {str(e)}', 'danger')
    
    return redirect(url_for('admin_user_detail', user_id=user_id))


@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_user_delete(user_id):
    """ユーザー削除"""
    user = User.query.get_or_404(user_id)
    
    # 自分自身は削除できない
    if user.id == current_user.id:
        flash('自分自身のアカウントは削除できません', 'danger')
        return redirect(url_for('admin_users'))
    
    try:
        username = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f'ユーザー「{username}」を削除しました', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'エラーが発生しました: {str(e)}', 'danger')
    
    return redirect(url_for('admin_users'))


# ==================== 初期化 ====================

def init_database():
    """データベースとデフォルトユーザーの初期化"""
    with app.app_context():
        # テーブル作成
        db.create_all()
        
        # デフォルト管理者の確認と作成
        try:
            admin = User.query.filter_by(email='admin@example.com').first()
            if not admin:
                admin = User(
                    email='admin@example.com',
                    username='管理者',
                    role='admin',
                    is_active=True
                )
                admin.set_password('admin123')
                db.session.add(admin)
                db.session.commit()
                print('✓ デフォルト管理者を作成: admin@example.com / admin123')
            else:
                print('✓ デフォルト管理者は既に存在します')
        except Exception as e:
            print(f'⚠ 管理者作成エラー: {e}')
            db.session.rollback()

# アプリケーション起動時に初期化
init_database()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


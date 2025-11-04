"""ルーティング定義"""
import uuid
from datetime import datetime
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import db
from app.models import DiagnosisSession, DiagnosisAnswer, User
from app.quiz_data import QUESTIONS, get_question_by_id, get_total_questions, get_mbti_info
from app.scoring import calculate_scores, determine_type, get_score_percentages, get_axis_descriptions
from app.decorators import admin_required, user_required

# ブループリント定義
main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__)
auth_bp = Blueprint('auth', __name__)


# ========== メインルート ==========

@main_bp.route('/')
def index():
    """トップページ"""
    return render_template('index.html')


@main_bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """診断ページ"""
    
    if request.method == 'GET':
        # 新規診断開始
        session.clear()
        session['quiz_session_id'] = str(uuid.uuid4())
        session['answers'] = []
        session['current_question'] = 1
        
        question = get_question_by_id(1)
        return render_template(
            'quiz.html',
            question=question,
            current=1,
            total=get_total_questions()
        )
    
    # POST: 回答を処理
    current_question_id = session.get('current_question', 1)
    answers = session.get('answers', [])
    
    # 回答を取得（脆弱性: 入力検証なし）
    option_index = request.form.get('option')
    
    if option_index is not None:
        option_index = int(option_index)
        question = get_question_by_id(current_question_id)
        
        if question and 0 <= option_index < len(question['options']):
            selected_option = question['options'][option_index]
            
            # 回答を保存
            answer = {
                'question_id': current_question_id,
                'axis': selected_option['axis'],
                'score': selected_option['score'],
                'answer_text': selected_option['text']
            }
            answers.append(answer)
            session['answers'] = answers
    
    # 次の質問へ
    next_question_id = current_question_id + 1
    
    if next_question_id > get_total_questions():
        # 全質問完了 → 結果を計算してDBに保存
        return redirect(url_for('main.calculate_result'))
    
    # 次の質問を表示
    session['current_question'] = next_question_id
    next_question = get_question_by_id(next_question_id)
    
    return render_template(
        'quiz.html',
        question=next_question,
        current=next_question_id,
        total=get_total_questions()
    )


@main_bp.route('/calculate_result')
def calculate_result():
    """結果を計算してDBに保存"""
    answers = session.get('answers', [])
    quiz_session_id = session.get('quiz_session_id')
    
    if not answers or not quiz_session_id:
        return redirect(url_for('main.index'))
    
    # スコア計算
    scores = calculate_scores(answers)
    mbti_type = determine_type(scores)
    
    # IPアドレス取得（脆弱性: X-Forwarded-Forを信頼）
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # DBに保存
    diagnosis_session = DiagnosisSession(
        session_id=quiz_session_id,
        user_id=current_user.id if current_user.is_authenticated else None,  # ログイン済みユーザーの場合はuser_idを保存
        mbti_type=mbti_type,
        scores_json=scores,
        ip_address=ip_address
    )
    db.session.add(diagnosis_session)
    db.session.commit()
    
    # 各回答を保存
    for answer in answers:
        diagnosis_answer = DiagnosisAnswer(
            session_id=diagnosis_session.id,
            question_id=answer['question_id'],
            axis=answer['axis'],
            score=answer['score'],
            answer_text=answer['answer_text']
        )
        db.session.add(diagnosis_answer)
    
    db.session.commit()
    
    # セッションクリア
    session.clear()
    
    return redirect(url_for('main.result', session_id=quiz_session_id))


@main_bp.route('/result/<session_id>')
def result(session_id):
    """診断結果ページ"""
    
    # DBから結果を取得（脆弱性: SQLインジェクション対策なしのクエリ例）
    diagnosis = DiagnosisSession.query.filter_by(session_id=session_id).first()
    
    if not diagnosis:
        return redirect(url_for('main.index'))
    
    # MBTIタイプ情報を取得
    mbti_info = get_mbti_info(diagnosis.mbti_type)
    
    # スコアのパーセンテージを計算
    percentages = get_score_percentages(diagnosis.scores_json)
    
    # 軸の説明を取得
    axis_descriptions = get_axis_descriptions()
    
    return render_template(
        'result.html',
        mbti_type=diagnosis.mbti_type,
        mbti_info=mbti_info,
        scores=diagnosis.scores_json,
        percentages=percentages,
        axis_descriptions=axis_descriptions,
        created_at=diagnosis.created_at
    )


# ========== 管理者ルート ==========

@admin_bp.route('/')
def index():
    """管理トップページ"""
    return redirect(url_for('admin.history'))


@admin_bp.route('/history')
@admin_required
def history():
    """診断履歴一覧（管理者のみ）"""
    
    # ページネーション
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 検索フィルター（脆弱性: SQLインジェクション）
    search_type = request.args.get('type', '')
    
    query = DiagnosisSession.query
    
    if search_type:
        # 脆弱性: 直接SQL文字列を構築
        query = query.filter(DiagnosisSession.mbti_type == search_type)
    
    # 新しい順に並べ替え
    diagnoses = query.order_by(DiagnosisSession.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    # MBTIタイプの一覧（フィルター用）
    mbti_types = db.session.query(DiagnosisSession.mbti_type).distinct().all()
    mbti_types = [t[0] for t in mbti_types]
    
    return render_template(
        'admin/history.html',
        diagnoses=diagnoses,
        mbti_types=mbti_types,
        search_type=search_type
    )


@admin_bp.route('/history/<int:id>')
def history_detail(id):
    """診断履歴詳細（JSON）"""
    
    diagnosis = DiagnosisSession.query.get_or_404(id)
    
    return jsonify(diagnosis.to_dict())


@admin_bp.route('/history/<int:id>', methods=['DELETE'])
def history_delete(id):
    """診断履歴削除"""
    
    diagnosis = DiagnosisSession.query.get_or_404(id)
    
    db.session.delete(diagnosis)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '診断履歴を削除しました'
    })


@admin_bp.route('/stats')
@admin_required
def stats():
    """統計情報（API）"""
    
    # タイプ別の診断数
    type_counts = db.session.query(
        DiagnosisSession.mbti_type,
        db.func.count(DiagnosisSession.id)
    ).group_by(DiagnosisSession.mbti_type).all()
    
    # 総診断数
    total_diagnoses = DiagnosisSession.query.count()
    
    return jsonify({
        'total_diagnoses': total_diagnoses,
        'type_distribution': {t: c for t, c in type_counts}
    })


# ========== 認証ルート ==========

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """ユーザー登録"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # 脆弱性: 入力検証が不十分
        if not email or not username or not password:
            flash('全ての項目を入力してください。', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != password_confirm:
            flash('パスワードが一致しません。', 'danger')
            return redirect(url_for('auth.register'))
        
        # ユーザーが既に存在するかチェック
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('このメールアドレスは既に登録されています。', 'danger')
            return redirect(url_for('auth.register'))
        
        # 新規ユーザー作成
        user = User(
            email=email,
            username=username,
            role='user'  # デフォルトは一般ユーザー
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('ユーザー登録が完了しました。ログインしてください。', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """ログイン"""
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        # 脆弱性: 入力検証が不十分
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            if not user.is_active:
                flash('このアカウントは無効化されています。', 'danger')
                return redirect(url_for('auth.login'))
            
            # ログイン成功
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            login_user(user, remember=remember)
            
            flash(f'ようこそ、{user.username}さん！', 'success')
            
            # next パラメータがあればそこにリダイレクト（脆弱性: オープンリダイレクト）
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            
            return redirect(url_for('main.index'))
        
        flash('メールアドレスまたはパスワードが正しくありません。', 'danger')
        return redirect(url_for('auth.login'))
    
    return render_template('auth/login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    """ログアウト"""
    logout_user()
    flash('ログアウトしました。', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/profile')
@login_required
def profile():
    """プロフィールページ"""
    # ユーザーの診断履歴を取得
    diagnoses = DiagnosisSession.query.filter_by(
        user_id=current_user.id
    ).order_by(DiagnosisSession.created_at.desc()).limit(10).all()
    
    return render_template('auth/profile.html', diagnoses=diagnoses)


# ========== ユーザー管理ルート（管理者のみ） ==========

@admin_bp.route('/users')
@admin_required
def user_list():
    """ユーザー一覧"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    users = User.query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return render_template('admin/users.html', users=users)


@admin_bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    """ユーザー詳細（JSON）"""
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


@admin_bp.route('/users/<int:user_id>/toggle-active', methods=['POST'])
@admin_required
def user_toggle_active(user_id):
    """ユーザーのアクティブ状態を切り替え"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({
            'success': False,
            'message': '自分自身のアカウントは無効化できません'
        }), 400
    
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'ユーザーを{"有効化" if user.is_active else "無効化"}しました',
        'is_active': user.is_active
    })


@admin_bp.route('/users/<int:user_id>/change-role', methods=['POST'])
@admin_required
def user_change_role(user_id):
    """ユーザーのロールを変更"""
    user = User.query.get_or_404(user_id)
    new_role = request.form.get('role')
    
    if new_role not in ['user', 'admin']:
        return jsonify({
            'success': False,
            'message': '無効なロールです'
        }), 400
    
    if user.id == current_user.id:
        return jsonify({
            'success': False,
            'message': '自分自身のロールは変更できません'
        }), 400
    
    user.role = new_role
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': f'ユーザーのロールを{new_role}に変更しました',
        'role': user.role
    })


@admin_bp.route('/users/<int:user_id>/delete', methods=['DELETE'])
@admin_required
def user_delete(user_id):
    """ユーザーを削除"""
    user = User.query.get_or_404(user_id)
    
    if user.id == current_user.id:
        return jsonify({
            'success': False,
            'message': '自分自身のアカウントは削除できません'
        }), 400
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'ユーザーを削除しました'
    })


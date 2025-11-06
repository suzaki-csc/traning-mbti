"""
管理者用ルート

ユーザー管理、カテゴリ管理、クイズ管理などの管理機能を提供します。
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import User, Category, Question, Choice, QuizSession, TermReference
from app.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('/')
@login_required
@admin_required
def dashboard():
    """管理者ダッシュボード"""
    # 統計情報を取得
    total_users = User.query.count()
    total_categories = Category.query.count()
    total_questions = Question.query.count()
    total_quiz_sessions = QuizSession.query.filter_by(is_review_mode=False).count()
    
    # 最近のクイズセッション
    recent_sessions = QuizSession.query.filter_by(
        is_review_mode=False
    ).order_by(db.desc('started_at')).limit(10).all()
    
    # 最近登録されたユーザー
    recent_users = User.query.order_by(db.desc('created_at')).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_categories=total_categories,
                         total_questions=total_questions,
                         total_quiz_sessions=total_quiz_sessions,
                         recent_sessions=recent_sessions,
                         recent_users=recent_users)


# ======================
# ユーザー管理
# ======================

@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """ユーザー一覧"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # ページネーション
    pagination = User.query.order_by(db.desc('created_at')).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    return render_template('admin/users/list.html',
                         users=pagination.items,
                         pagination=pagination)


@admin_bp.route('/users/<int:user_id>')
@login_required
@admin_required
def user_detail(user_id):
    """ユーザー詳細"""
    user = User.query.get_or_404(user_id)
    
    # ユーザーのクイズ履歴
    quiz_sessions = user.quiz_sessions.filter_by(
        is_review_mode=False
    ).order_by(db.desc('started_at')).limit(20).all()
    
    return render_template('admin/users/detail.html',
                         user=user,
                         quiz_sessions=quiz_sessions)


@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    """ユーザー編集"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'user')
        is_active = request.form.get('is_active', 'false') == 'true'
        new_password = request.form.get('new_password', '').strip()
        
        # バリデーション
        if not email:
            flash('メールアドレスを入力してください。', 'danger')
            return render_template('admin/users/edit.html', user=user)
        
        # メールアドレスの重複チェック（自分以外）
        existing_user = User.query.filter(
            db.and_(User.email == email, User.id != user_id)
        ).first()
        if existing_user:
            flash('このメールアドレスは既に使用されています。', 'danger')
            return render_template('admin/users/edit.html', user=user)
        
        # ロールのバリデーション
        if role not in ['user', 'admin']:
            flash('無効なロールが指定されました。', 'danger')
            return render_template('admin/users/edit.html', user=user)
        
        # 自分自身の管理者権限を削除しようとしている場合は警告
        if user.id == current_user.id and role != 'admin' and current_user.is_admin():
            flash('自分自身の管理者権限を削除することはできません。', 'danger')
            return render_template('admin/users/edit.html', user=user)
        
        # 更新
        user.email = email
        user.role = role
        user.is_active = is_active
        
        # パスワードが入力されていれば更新
        if new_password:
            if len(new_password) < 6:
                flash('パスワードは6文字以上で設定してください。', 'danger')
                return render_template('admin/users/edit.html', user=user)
            user.set_password(new_password)
        
        try:
            db.session.commit()
            flash('ユーザー情報を更新しました。', 'success')
            return redirect(url_for('admin.user_detail', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            flash('ユーザー情報の更新に失敗しました。', 'danger')
    
    return render_template('admin/users/edit.html', user=user)


@admin_bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def user_delete(user_id):
    """ユーザー削除"""
    user = User.query.get_or_404(user_id)
    
    # 自分自身を削除しようとしている場合は拒否
    if user.id == current_user.id:
        flash('自分自身を削除することはできません。', 'danger')
        return redirect(url_for('admin.users'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash(f'ユーザー「{user.email}」を削除しました。', 'success')
    except Exception as e:
        db.session.rollback()
        flash('ユーザーの削除に失敗しました。', 'danger')
    
    return redirect(url_for('admin.users'))


# ======================
# カテゴリ管理
# ======================

@admin_bp.route('/categories')
@login_required
@admin_required
def categories():
    """カテゴリ一覧"""
    categories = Category.query.order_by('display_order', 'name').all()
    return render_template('admin/categories/list.html', categories=categories)


@admin_bp.route('/categories/create', methods=['GET', 'POST'])
@login_required
@admin_required
def category_create():
    """カテゴリ作成"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        display_order = request.form.get('display_order', 0, type=int)
        is_active = request.form.get('is_active', 'true') == 'true'
        
        # バリデーション
        if not name:
            flash('カテゴリ名を入力してください。', 'danger')
            return render_template('admin/categories/create.html')
        
        # 重複チェック
        existing_category = Category.query.filter_by(name=name).first()
        if existing_category:
            flash('このカテゴリ名は既に使用されています。', 'danger')
            return render_template('admin/categories/create.html')
        
        # 作成
        category = Category(
            name=name,
            description=description,
            display_order=display_order,
            is_active=is_active
        )
        
        try:
            db.session.add(category)
            db.session.commit()
            flash(f'カテゴリ「{name}」を作成しました。', 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            db.session.rollback()
            flash('カテゴリの作成に失敗しました。', 'danger')
    
    return render_template('admin/categories/create.html')


@admin_bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def category_edit(category_id):
    """カテゴリ編集"""
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        display_order = request.form.get('display_order', 0, type=int)
        is_active = request.form.get('is_active', 'true') == 'true'
        
        # バリデーション
        if not name:
            flash('カテゴリ名を入力してください。', 'danger')
            return render_template('admin/categories/edit.html', category=category)
        
        # 重複チェック（自分以外）
        existing_category = Category.query.filter(
            db.and_(Category.name == name, Category.id != category_id)
        ).first()
        if existing_category:
            flash('このカテゴリ名は既に使用されています。', 'danger')
            return render_template('admin/categories/edit.html', category=category)
        
        # 更新
        category.name = name
        category.description = description
        category.display_order = display_order
        category.is_active = is_active
        
        try:
            db.session.commit()
            flash(f'カテゴリ「{name}」を更新しました。', 'success')
            return redirect(url_for('admin.categories'))
        except Exception as e:
            db.session.rollback()
            flash('カテゴリの更新に失敗しました。', 'danger')
    
    return render_template('admin/categories/edit.html', category=category)


@admin_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def category_delete(category_id):
    """カテゴリ削除"""
    category = Category.query.get_or_404(category_id)
    
    # 問題が関連付けられている場合は警告
    if category.questions.count() > 0:
        flash(f'カテゴリ「{category.name}」には{category.questions.count()}個の問題が関連付けられています。削除すると問題も削除されます。', 'warning')
    
    try:
        db.session.delete(category)
        db.session.commit()
        flash(f'カテゴリ「{category.name}」を削除しました。', 'success')
    except Exception as e:
        db.session.rollback()
        flash('カテゴリの削除に失敗しました。', 'danger')
    
    return redirect(url_for('admin.categories'))


# ======================
# クイズ管理
# ======================

@admin_bp.route('/questions')
@login_required
@admin_required
def questions():
    """問題一覧"""
    category_id = request.args.get('category_id', type=int)
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # カテゴリでフィルタリング
    query = Question.query
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # ページネーション
    pagination = query.order_by(db.desc('created_at')).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    categories = Category.query.order_by('display_order').all()
    
    return render_template('admin/questions/list.html',
                         questions=pagination.items,
                         pagination=pagination,
                         categories=categories,
                         selected_category_id=category_id)


@admin_bp.route('/questions/create', methods=['GET', 'POST'])
@login_required
@admin_required
def question_create():
    """問題作成"""
    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        question_text = request.form.get('question_text', '').strip()
        explanation = request.form.get('explanation', '').strip()
        difficulty = request.form.get('difficulty', 1, type=int)
        is_active = request.form.get('is_active', 'true') == 'true'
        
        # 選択肢（4つ）
        choices_data = []
        for i in range(1, 5):
            choice_text = request.form.get(f'choice_{i}', '').strip()
            is_correct = request.form.get('correct_choice') == str(i)
            if choice_text:
                choices_data.append({
                    'choice_text': choice_text,
                    'is_correct': is_correct,
                    'display_order': i
                })
        
        # バリデーション
        if not category_id:
            flash('カテゴリを選択してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/create.html', categories=categories)
        
        if not question_text:
            flash('問題文を入力してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/create.html', categories=categories)
        
        if not explanation:
            flash('解説を入力してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/create.html', categories=categories)
        
        if len(choices_data) < 4:
            flash('4つの選択肢を入力してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/create.html', categories=categories)
        
        if not any(choice['is_correct'] for choice in choices_data):
            flash('正解の選択肢を1つ選択してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/create.html', categories=categories)
        
        # 問題を作成
        question = Question(
            category_id=category_id,
            question_text=question_text,
            explanation=explanation,
            difficulty=difficulty,
            is_active=is_active
        )
        
        try:
            db.session.add(question)
            db.session.flush()  # questionのIDを取得するため
            
            # 選択肢を作成
            for choice_data in choices_data:
                choice = Choice(
                    question_id=question.id,
                    choice_text=choice_data['choice_text'],
                    is_correct=choice_data['is_correct'],
                    display_order=choice_data['display_order']
                )
                db.session.add(choice)
            
            db.session.commit()
            flash('問題を作成しました。', 'success')
            return redirect(url_for('admin.questions'))
        except Exception as e:
            db.session.rollback()
            flash('問題の作成に失敗しました。', 'danger')
    
    categories = Category.query.order_by('display_order').all()
    return render_template('admin/questions/create.html', categories=categories)


@admin_bp.route('/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def question_edit(question_id):
    """問題編集"""
    question = Question.query.get_or_404(question_id)
    
    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        question_text = request.form.get('question_text', '').strip()
        explanation = request.form.get('explanation', '').strip()
        difficulty = request.form.get('difficulty', 1, type=int)
        is_active = request.form.get('is_active', 'true') == 'true'
        
        # 選択肢（4つ）
        choices_data = []
        for i in range(1, 5):
            choice_id = request.form.get(f'choice_id_{i}', type=int)
            choice_text = request.form.get(f'choice_{i}', '').strip()
            is_correct = request.form.get('correct_choice') == str(i)
            if choice_text:
                choices_data.append({
                    'id': choice_id,
                    'choice_text': choice_text,
                    'is_correct': is_correct,
                    'display_order': i
                })
        
        # バリデーション
        if not category_id:
            flash('カテゴリを選択してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/edit.html', question=question, categories=categories)
        
        if not question_text:
            flash('問題文を入力してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/edit.html', question=question, categories=categories)
        
        if len(choices_data) < 4:
            flash('4つの選択肢を入力してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/edit.html', question=question, categories=categories)
        
        if not any(choice['is_correct'] for choice in choices_data):
            flash('正解の選択肢を1つ選択してください。', 'danger')
            categories = Category.query.order_by('display_order').all()
            return render_template('admin/questions/edit.html', question=question, categories=categories)
        
        # 問題を更新
        question.category_id = category_id
        question.question_text = question_text
        question.explanation = explanation
        question.difficulty = difficulty
        question.is_active = is_active
        
        try:
            # 既存の選択肢を更新
            for choice_data in choices_data:
                if choice_data['id']:
                    choice = Choice.query.get(choice_data['id'])
                    if choice:
                        choice.choice_text = choice_data['choice_text']
                        choice.is_correct = choice_data['is_correct']
                        choice.display_order = choice_data['display_order']
            
            db.session.commit()
            flash('問題を更新しました。', 'success')
            return redirect(url_for('admin.questions'))
        except Exception as e:
            db.session.rollback()
            flash('問題の更新に失敗しました。', 'danger')
    
    categories = Category.query.order_by('display_order').all()
    return render_template('admin/questions/edit.html', question=question, categories=categories)


@admin_bp.route('/questions/<int:question_id>/delete', methods=['POST'])
@login_required
@admin_required
def question_delete(question_id):
    """問題削除"""
    question = Question.query.get_or_404(question_id)
    
    try:
        db.session.delete(question)
        db.session.commit()
        flash('問題を削除しました。', 'success')
    except Exception as e:
        db.session.rollback()
        flash('問題の削除に失敗しました。', 'danger')
    
    return redirect(url_for('admin.questions'))


# ======================
# クイズ履歴管理
# ======================

@admin_bp.route('/quiz-history')
@login_required
@admin_required
def quiz_history():
    """全ユーザーのクイズ履歴"""
    page = request.args.get('page', 1, type=int)
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    per_page = 20
    
    # フィルタリング
    query = QuizSession.query.filter_by(is_review_mode=False)
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # ページネーション
    pagination = query.order_by(db.desc('started_at')).paginate(
        page=page, per_page=per_page, error_out=False
    )
    
    users = User.query.order_by('email').all()
    categories = Category.query.order_by('display_order').all()
    
    return render_template('admin/quiz_history.html',
                         sessions=pagination.items,
                         pagination=pagination,
                         users=users,
                         categories=categories,
                         selected_user_id=user_id,
                         selected_category_id=category_id)


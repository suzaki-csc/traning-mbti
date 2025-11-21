"""
管理機能関連のルーティング
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import User, Category, Quiz, QuizResult, Review
from app.utils.auth import admin_required
import pymysql

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/')
@admin_required
def dashboard():
    """管理ダッシュボード"""
    # 統計情報を取得
    total_users = User.query.count()
    total_categories = Category.query.count()
    total_quizzes = Quiz.query.count()
    total_results = QuizResult.query.count()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_categories=total_categories,
                         total_quizzes=total_quizzes,
                         total_results=total_results)


@bp.route('/users')
@admin_required
def users():
    """ユーザー管理ページ"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@bp.route('/users/<int:user_id>')
@admin_required
def user_detail(user_id):
    """ユーザー詳細ページ"""
    user = User.query.get_or_404(user_id)
    return render_template('admin/user_detail.html', user=user)


@bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def user_edit(user_id):
    """ユーザー編集ページ"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user_id_form = request.form.get('user_id', '').strip()
        email = request.form.get('email', '').strip()
        role = request.form.get('role', 'user')
        
        # バリデーション
        if not user_id_form or not email:
            flash('すべての項目を入力してください', 'danger')
            return render_template('admin/user_edit.html', user=user)
        
        # ユーザーIDとメールアドレスの重複チェック（自分以外）
        other_user = User.query.filter(
            (User.user_id == user_id_form) | (User.email == email)
        ).filter(User.id != user_id).first()
        
        if other_user:
            flash('このユーザーIDまたはメールアドレスは既に使用されています', 'danger')
            return render_template('admin/user_edit.html', user=user)
        
        # 更新
        user.user_id = user_id_form
        user.email = email
        user.role = role
        
        # パスワードが入力されている場合は更新
        password = request.form.get('password', '').strip()
        if password:
            if len(password) < 6:
                flash('パスワードは6文字以上で入力してください', 'danger')
                return render_template('admin/user_edit.html', user=user)
            user.set_password(password)
        
        try:
            db.session.commit()
            flash('ユーザー情報を更新しました', 'success')
            return redirect(url_for('admin.user_detail', user_id=user_id))
        except Exception as e:
            db.session.rollback()
            flash('ユーザー情報の更新に失敗しました', 'danger')
    
    return render_template('admin/user_edit.html', user=user)


@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def user_delete(user_id):
    """ユーザー削除"""
    user = User.query.get_or_404(user_id)
    
    # 自分は削除できない
    if user.id == session['user_id']:
        flash('自分自身を削除することはできません', 'danger')
        return redirect(url_for('admin.users'))
    
    try:
        db.session.delete(user)
        db.session.commit()
        flash('ユーザーを削除しました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('ユーザーの削除に失敗しました', 'danger')
    
    return redirect(url_for('admin.users'))


@bp.route('/quizzes')
@admin_required
def quizzes():
    """クイズ管理ページ"""
    # カテゴリフィルタ
    category_id = request.args.get('category_id', type=int)
    
    if category_id:
        category = Category.query.get_or_404(category_id)
        quizzes = Quiz.query.filter_by(category_id=category_id).order_by(Quiz.created_at.desc()).all()
    else:
        category = None
        quizzes = Quiz.query.order_by(Quiz.created_at.desc()).all()
    
    categories = Category.query.all()
    
    return render_template('admin/quizzes.html',
                         quizzes=quizzes,
                         categories=categories,
                         selected_category=category)


@bp.route('/categories/new', methods=['GET', 'POST'])
@admin_required
def category_new():
    """カテゴリ作成ページ"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('カテゴリ名を入力してください', 'danger')
            return render_template('admin/category_edit.html')
        
        # 重複チェック
        if Category.query.filter_by(name=name).first():
            flash('このカテゴリ名は既に使用されています', 'danger')
            return render_template('admin/category_edit.html')
        
        category = Category(name=name, description=description)
        
        try:
            db.session.add(category)
            db.session.commit()
            flash('カテゴリを作成しました', 'success')
            return redirect(url_for('admin.quizzes'))
        except Exception as e:
            db.session.rollback()
            flash('カテゴリの作成に失敗しました', 'danger')
    
    return render_template('admin/category_edit.html')


@bp.route('/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@admin_required
def category_edit(category_id):
    """カテゴリ編集ページ"""
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            flash('カテゴリ名を入力してください', 'danger')
            return render_template('admin/category_edit.html', category=category)
        
        # 重複チェック（自分以外）
        other_category = Category.query.filter_by(name=name).filter(Category.id != category_id).first()
        if other_category:
            flash('このカテゴリ名は既に使用されています', 'danger')
            return render_template('admin/category_edit.html', category=category)
        
        category.name = name
        category.description = description
        
        try:
            db.session.commit()
            flash('カテゴリを更新しました', 'success')
            return redirect(url_for('admin.quizzes'))
        except Exception as e:
            db.session.rollback()
            flash('カテゴリの更新に失敗しました', 'danger')
    
    return render_template('admin/category_edit.html', category=category)


@bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@admin_required
def category_delete(category_id):
    """カテゴリ削除"""
    category = Category.query.get_or_404(category_id)
    
    # 関連するクイズがある場合は削除できない
    if Quiz.query.filter_by(category_id=category_id).first():
        flash('このカテゴリに問題が含まれているため削除できません', 'danger')
        return redirect(url_for('admin.quizzes'))
    
    try:
        db.session.delete(category)
        db.session.commit()
        flash('カテゴリを削除しました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('カテゴリの削除に失敗しました', 'danger')
    
    return redirect(url_for('admin.quizzes'))


@bp.route('/quizzes/new', methods=['GET', 'POST'])
@admin_required
def quiz_new():
    """クイズ作成ページ"""
    categories = Category.query.all()
    
    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        question = request.form.get('question', '').strip()
        option1 = request.form.get('option1', '').strip()
        option2 = request.form.get('option2', '').strip()
        option3 = request.form.get('option3', '').strip()
        option4 = request.form.get('option4', '').strip()
        correct_answer = request.form.get('correct_answer', type=int)
        explanation = request.form.get('explanation', '').strip()
        
        # バリデーション
        if not all([category_id, question, option1, option2, option3, option4, explanation]):
            flash('すべての項目を入力してください', 'danger')
            return render_template('admin/quiz_edit.html', categories=categories)
        
        if correct_answer not in [1, 2, 3, 4]:
            flash('正解は1から4の間で選択してください', 'danger')
            return render_template('admin/quiz_edit.html', categories=categories)
        
        quiz = Quiz(
            category_id=category_id,
            question=question,
            option1=option1,
            option2=option2,
            option3=option3,
            option4=option4,
            correct_answer=correct_answer,
            explanation=explanation
        )
        
        try:
            db.session.add(quiz)
            db.session.commit()
            flash('クイズを作成しました', 'success')
            return redirect(url_for('admin.quizzes', category_id=category_id))
        except Exception as e:
            db.session.rollback()
            flash('クイズの作成に失敗しました', 'danger')
    
    return render_template('admin/quiz_edit.html', categories=categories)


@bp.route('/quizzes/<int:quiz_id>/edit', methods=['GET', 'POST'])
@admin_required
def quiz_edit(quiz_id):
    """クイズ編集ページ"""
    quiz = Quiz.query.get_or_404(quiz_id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        question = request.form.get('question', '').strip()
        option1 = request.form.get('option1', '').strip()
        option2 = request.form.get('option2', '').strip()
        option3 = request.form.get('option3', '').strip()
        option4 = request.form.get('option4', '').strip()
        correct_answer = request.form.get('correct_answer', type=int)
        explanation = request.form.get('explanation', '').strip()
        
        # バリデーション
        if not all([category_id, question, option1, option2, option3, option4, explanation]):
            flash('すべての項目を入力してください', 'danger')
            return render_template('admin/quiz_edit.html', quiz=quiz, categories=categories)
        
        if correct_answer not in [1, 2, 3, 4]:
            flash('正解は1から4の間で選択してください', 'danger')
            return render_template('admin/quiz_edit.html', quiz=quiz, categories=categories)
        
        quiz.category_id = category_id
        quiz.question = question
        quiz.option1 = option1
        quiz.option2 = option2
        quiz.option3 = option3
        quiz.option4 = option4
        quiz.correct_answer = correct_answer
        quiz.explanation = explanation
        
        try:
            db.session.commit()
            flash('クイズを更新しました', 'success')
            return redirect(url_for('admin.quizzes', category_id=category_id))
        except Exception as e:
            db.session.rollback()
            flash('クイズの更新に失敗しました', 'danger')
    
    return render_template('admin/quiz_edit.html', quiz=quiz, categories=categories)


@bp.route('/quizzes/<int:quiz_id>/delete', methods=['POST'])
@admin_required
def quiz_delete(quiz_id):
    """クイズ削除"""
    quiz = Quiz.query.get_or_404(quiz_id)
    category_id = quiz.category_id
    
    try:
        db.session.delete(quiz)
        db.session.commit()
        flash('クイズを削除しました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('クイズの削除に失敗しました', 'danger')
    
    return redirect(url_for('admin.quizzes', category_id=category_id))


@bp.route('/reviews')
@admin_required
def reviews():
    """レビュー管理ページ"""
    # SQLインジェクション脆弱性: レビュー検索機能
    search = request.args.get('search', '').strip()
    
    if search:
        # 脆弱なSQLクエリ: 文字列連結を使用
        try:
            from flask import current_app
            db_uri = current_app.config['SQLALCHEMY_DATABASE_URI']
            
            import re
            match = re.match(r'mysql\+pymysql://([^:]+):([^@]+)@([^:]+):(\d+)/(.+)', db_uri)
            if match:
                db_user, db_password, db_host, db_port, db_name = match.groups()
                
                connection = pymysql.connect(
                    host=db_host,
                    port=int(db_port),
                    user=db_user,
                    password=db_password,
                    database=db_name,
                    cursorclass=pymysql.cursors.DictCursor
                )
                
                # 脆弱なSQLクエリ
                query = f"SELECT * FROM reviews WHERE title LIKE '%{search}%' OR content LIKE '%{search}%'"
                cursor = connection.cursor()
                cursor.execute(query)
                review_data = cursor.fetchall()
                cursor.close()
                connection.close()
                
                # データをReviewオブジェクトに変換
                reviews = []
                for data in review_data:
                    review = Review.query.get(data['id'])
                    if review:
                        reviews.append(review)
            else:
                # 通常の検索方法
                reviews = Review.query.filter(
                    (Review.title.contains(search)) | (Review.content.contains(search))
                ).order_by(Review.created_at.desc()).all()
        except Exception as e:
            # エラーが発生した場合は通常の検索方法
            reviews = Review.query.filter(
                (Review.title.contains(search)) | (Review.content.contains(search))
            ).order_by(Review.created_at.desc()).all()
    else:
        reviews = Review.query.order_by(Review.created_at.desc()).all()
    
    return render_template('admin/reviews.html', reviews=reviews, search=search)


@bp.route('/reviews/<int:review_id>/delete', methods=['POST'])
@admin_required
def review_delete(review_id):
    """レビュー削除"""
    review = Review.query.get_or_404(review_id)
    
    try:
        db.session.delete(review)
        db.session.commit()
        flash('レビューを削除しました', 'success')
    except Exception as e:
        db.session.rollback()
        flash('レビューの削除に失敗しました', 'danger')
    
    return redirect(url_for('admin.reviews'))


@bp.route('/history')
@admin_required
def history():
    """全ユーザー履歴ページ"""
    # フィルタ
    user_id = request.args.get('user_id', type=int)
    category_id = request.args.get('category_id', type=int)
    
    # クエリを構築
    query = QuizResult.query.filter_by(is_review_mode=False)
    
    if user_id:
        query = query.filter_by(user_id=user_id)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 日付順（新しい順）でソート
    results = query.order_by(QuizResult.completed_at.desc()).all()
    
    # フィルタ用のデータ
    users = User.query.all()
    categories = Category.query.all()
    
    return render_template('admin/history.html',
                         results=results,
                         users=users,
                         categories=categories,
                         selected_user_id=user_id,
                         selected_category_id=category_id)


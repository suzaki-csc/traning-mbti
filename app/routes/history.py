"""
履歴関連のルーティング
"""
from flask import Blueprint, render_template, request, session
from app.models import QuizResult, Category
from app.utils.auth import login_required

bp = Blueprint('history', __name__, url_prefix='/history')


@bp.route('/')
@login_required
def list():
    """履歴一覧ページ"""
    user_id = session['user_id']
    
    # カテゴリフィルタ
    category_id = request.args.get('category_id', type=int)
    
    # クエリを構築
    query = QuizResult.query.filter_by(user_id=user_id, is_review_mode=False)
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    # 日付順（新しい順）でソート
    results = query.order_by(QuizResult.completed_at.desc()).all()
    
    # カテゴリ一覧を取得（フィルタ用）
    categories = Category.query.all()
    
    return render_template('history/list.html', 
                         results=results, 
                         categories=categories,
                         selected_category_id=category_id)


@bp.route('/<int:result_id>')
@login_required
def detail(result_id):
    """履歴詳細ページ"""
    result = QuizResult.query.get_or_404(result_id)
    
    # 自分の履歴か確認
    if result.user_id != session['user_id']:
        from flask import flash, redirect, url_for
        flash('アクセス権限がありません', 'danger')
        return redirect(url_for('history.list'))
    
    # 回答詳細を取得
    from app.models import QuizAnswer, Quiz
    answers = QuizAnswer.query.filter_by(quiz_result_id=result_id).all()
    
    # 問題情報も取得
    quiz_data = []
    for answer in answers:
        quiz = Quiz.query.get(answer.quiz_id)
        quiz_data.append({
            'quiz': quiz,
            'answer': answer
        })
    
    return render_template('history/detail.html', 
                         result=result, 
                         quiz_data=quiz_data)


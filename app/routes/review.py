"""
レビュー関連のルーティング
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from app import db
from app.models import Review
from app.utils.auth import login_required

bp = Blueprint('review', __name__, url_prefix='/reviews')


@bp.route('/')
def list():
    """レビュー一覧ページ"""
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('review/list.html', reviews=reviews)


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def new():
    """レビュー投稿ページ"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        rating = request.form.get('rating', type=int)
        
        # バリデーション
        if not title or not content:
            flash('タイトルと内容を入力してください', 'danger')
            return render_template('review/new.html')
        
        if rating and (rating < 1 or rating > 5):
            flash('評価は1から5の間で入力してください', 'danger')
            return render_template('review/new.html')
        
        # レビューを作成（XSS脆弱性: エスケープなしで保存）
        review = Review(
            user_id=session['user_id'],
            title=title,
            content=content,  # XSS脆弱性: エスケープなし
            rating=rating
        )
        
        try:
            db.session.add(review)
            db.session.commit()
            flash('レビューを投稿しました', 'success')
            return redirect(url_for('review.list'))
        except Exception as e:
            db.session.rollback()
            flash('レビューの投稿に失敗しました', 'danger')
    
    return render_template('review/new.html')


@bp.route('/<int:review_id>')
def detail(review_id):
    """レビュー詳細ページ"""
    review = Review.query.get_or_404(review_id)
    return render_template('review/detail.html', review=review)


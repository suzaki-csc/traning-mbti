"""
メインページのルーティング

トップページ、カテゴリ選択、用語参考リンク集など
"""
from flask import Blueprint, render_template
from app.models import Category, TermReference
from sqlalchemy import func

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """トップページ"""
    return render_template('index.html')


@main_bp.route('/category')
def category():
    """カテゴリ選択ページ"""
    # 有効なカテゴリを表示順で取得
    categories = Category.query.filter_by(
        is_active=True
    ).order_by(Category.display_order).all()
    
    return render_template('category.html', categories=categories)


@main_bp.route('/reference')
def reference():
    """用語参考リンク集ページ"""
    # すべてのカテゴリを取得
    categories = Category.query.filter_by(
        is_active=True
    ).order_by(Category.display_order).all()
    
    # カテゴリごとの用語を取得
    terms_by_category = {}
    for category in categories:
        terms = TermReference.query.filter_by(
            category_id=category.id
        ).order_by(TermReference.display_order).all()
        
        if terms:
            terms_by_category[category.name] = terms
    
    return render_template('reference.html', 
                         categories=categories,
                         terms_by_category=terms_by_category)


"""
管理者機能のルーティング
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required
from sqlalchemy import func
from app.models import db, User, TestResult
from app.auth import admin_required

# Blueprintの作成
admin = Blueprint('admin', __name__, url_prefix='/admin')


@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """管理ダッシュボード"""
    # 統計情報を取得
    total_users = User.query.count()
    total_tests = TestResult.query.count()
    
    # MBTIタイプ別の分布
    type_distribution = db.session.query(
        TestResult.mbti_type,
        func.count(TestResult.id).label('count')
    ).group_by(TestResult.mbti_type).all()
    
    # 最近の診断結果
    recent_results = TestResult.query\
        .order_by(TestResult.taken_at.desc())\
        .limit(10).all()
    
    return render_template('admin/dashboard.html',
                         total_users=total_users,
                         total_tests=total_tests,
                         type_distribution=type_distribution,
                         recent_results=recent_results)


@admin.route('/history')
@login_required
@admin_required
def history():
    """全ユーザーの診断履歴"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # ユーザー名でフィルタ
    username_filter = request.args.get('username', '')
    
    query = TestResult.query.join(User)
    
    if username_filter:
        query = query.filter(User.username.like(f'%{username_filter}%'))
    
    pagination = query.order_by(TestResult.taken_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    results = pagination.items
    
    return render_template('admin/all_history.html',
                         results=results,
                         pagination=pagination,
                         username_filter=username_filter)


@admin.route('/result/<int:result_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_result(result_id):
    """診断結果削除"""
    test_result = TestResult.query.get_or_404(result_id)
    
    try:
        db.session.delete(test_result)
        db.session.commit()
        flash('診断結果を削除しました。', 'success')
    except Exception as e:
        db.session.rollback()
        flash('削除中にエラーが発生しました。', 'danger')
    
    # リファラーに戻る（なければ履歴ページへ）
    return redirect(request.referrer or url_for('admin.history'))


@admin.route('/users')
@login_required
@admin_required
def users():
    """ユーザー一覧"""
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    pagination = User.query.order_by(User.created_at.desc())\
        .paginate(page=page, per_page=per_page, error_out=False)
    
    users_list = pagination.items
    
    return render_template('admin/users.html',
                         users=users_list,
                         pagination=pagination)


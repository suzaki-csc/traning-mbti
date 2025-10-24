"""管理画面のルーティング"""
from functools import wraps
from flask import Blueprint, render_template, request, jsonify, session as flask_session
from sqlalchemy import func, desc
from models import db, Diagnosis
from config import Config
from datetime import datetime, timedelta

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


def check_admin_auth():
    """管理者認証チェック"""
    auth = request.authorization
    if not auth:
        return False
    return (auth.username == Config.ADMIN_USERNAME and 
            auth.password == Config.ADMIN_PASSWORD)


def requires_admin_auth(f):
    """管理者認証デコレータ"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not check_admin_auth():
            return ('認証が必要です', 401, {
                'WWW-Authenticate': 'Basic realm="Admin Area"'
            })
        return f(*args, **kwargs)
    return decorated


@admin_bp.route('/')
@requires_admin_auth
def dashboard():
    """管理ダッシュボード"""
    # 統計情報を取得
    total_diagnoses = Diagnosis.query.count()
    
    # 直近7日間の診断数
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_diagnoses = Diagnosis.query.filter(
        Diagnosis.created_at >= seven_days_ago
    ).count()
    
    # タイプ別分布
    type_distribution = db.session.query(
        Diagnosis.mbti_type,
        func.count(Diagnosis.id).label('count')
    ).group_by(Diagnosis.mbti_type).order_by(desc('count')).all()
    
    type_dist_dict = {item[0]: item[1] for item in type_distribution}
    most_common_type = type_distribution[0][0] if type_distribution else 'N/A'
    
    # 最新の診断一覧（5件）
    recent_list = Diagnosis.query.order_by(
        desc(Diagnosis.created_at)
    ).limit(5).all()
    
    return render_template(
        'admin/dashboard.html',
        total_diagnoses=total_diagnoses,
        recent_diagnoses=recent_diagnoses,
        most_common_type=most_common_type,
        type_distribution=type_dist_dict,
        recent_list=recent_list
    )


@admin_bp.route('/history')
@requires_admin_auth
def history():
    """診断履歴一覧"""
    # ページネーション
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # フィルター
    mbti_type_filter = request.args.get('type', '')
    
    # クエリ構築
    query = Diagnosis.query
    
    if mbti_type_filter:
        query = query.filter(Diagnosis.mbti_type == mbti_type_filter)
    
    # ページネーション実行
    pagination = query.order_by(desc(Diagnosis.created_at)).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    return render_template(
        'admin/history.html',
        diagnoses=pagination.items,
        pagination=pagination,
        current_filter=mbti_type_filter
    )


@admin_bp.route('/stats')
@requires_admin_auth
def stats():
    """統計情報API"""
    total_diagnoses = Diagnosis.query.count()
    
    # 直近7日間
    seven_days_ago = datetime.utcnow() - timedelta(days=7)
    recent_7days = Diagnosis.query.filter(
        Diagnosis.created_at >= seven_days_ago
    ).count()
    
    # タイプ別分布
    type_distribution = db.session.query(
        Diagnosis.mbti_type,
        func.count(Diagnosis.id).label('count')
    ).group_by(Diagnosis.mbti_type).all()
    
    type_dist_dict = {item[0]: item[1] for item in type_distribution}
    
    return jsonify({
        'total_diagnoses': total_diagnoses,
        'recent_7days': recent_7days,
        'type_distribution': type_dist_dict
    })


@admin_bp.route('/history/<int:id>', methods=['DELETE'])
@requires_admin_auth
def delete_diagnosis(id):
    """診断削除"""
    diagnosis = Diagnosis.query.get_or_404(id)
    
    try:
        db.session.delete(diagnosis)
        db.session.commit()
        return jsonify({'success': True, 'message': '削除しました'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 500


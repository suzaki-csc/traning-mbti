"""
クイズ実行のルーティング

クイズ実行、結果表示、復習モードなど
"""
from flask import Blueprint, render_template, session, redirect, url_for, request
from app.services import quiz_service, result_service

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('/quiz/<session_key>')
def quiz(session_key):
    """クイズ実行画面"""
    # セッション情報を取得
    quiz_session = quiz_service.get_session_by_key(session_key)
    
    if not quiz_session:
        return redirect(url_for('main.index'))
    
    # セッションが完了している場合は結果画面へ
    if quiz_session.is_completed():
        return redirect(url_for('quiz.result', session_key=session_key))
    
    # セッションストレージに問題IDリストを保存
    # （実際にはRedisやデータベースを使用することを推奨）
    if f'question_ids_{session_key}' not in session:
        # 新規セッションの場合はエラー
        return redirect(url_for('main.category'))
    
    question_ids = session.get(f'question_ids_{session_key}', [])
    
    return render_template('quiz.html',
                         session_key=session_key,
                         quiz_session=quiz_session,
                         total_questions=quiz_session.total_questions,
                         is_review_mode=quiz_session.is_review_mode)


@quiz_bp.route('/result/<session_key>')
def result(session_key):
    """結果表示画面"""
    # セッション情報を取得
    quiz_session = quiz_service.get_session_by_key(session_key)
    
    if not quiz_session:
        return redirect(url_for('main.index'))
    
    # 結果データを取得
    result_data = result_service.get_session_result(session_key)
    
    if not result_data:
        return redirect(url_for('main.index'))
    
    # 評価メッセージを取得
    evaluation_message = result_service.get_evaluation_message(
        result_data['accuracy_rate']
    )
    
    return render_template('result.html',
                         result=result_data,
                         evaluation_message=evaluation_message,
                         quiz_session=quiz_session)


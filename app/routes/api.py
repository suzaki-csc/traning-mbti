"""
APIエンドポイント

クイズ操作用のREST API
"""
from flask import Blueprint, jsonify, request, session
from flask_login import current_user
from app.services import quiz_service, result_service
from app.models import Category

api_bp = Blueprint('api', __name__)


@api_bp.route('/quiz/start', methods=['POST'])
def start_quiz():
    """クイズ開始API"""
    data = request.get_json()
    
    category_id = data.get('category_id')
    timer_seconds = data.get('timer_seconds', 30)
    sound_enabled = data.get('sound_enabled', True)
    is_review_mode = data.get('is_review_mode', False)
    parent_session_key = data.get('parent_session_key')
    
    # カテゴリの存在確認
    category = Category.query.get(category_id)
    if not category:
        return jsonify({'error': 'カテゴリが見つかりません'}), 404
    
    # ログインユーザーのIDを取得（ログインしていない場合はNone）
    user_id = current_user.id if current_user.is_authenticated else None
    
    # セッションを作成
    quiz_session, question_ids = quiz_service.create_quiz_session(
        category_id=category_id,
        timer_seconds=timer_seconds,
        sound_enabled=sound_enabled,
        is_review_mode=is_review_mode,
        parent_session_key=parent_session_key,
        user_id=user_id
    )
    
    # 問題IDをセッションに保存
    session[f'question_ids_{quiz_session.session_key}'] = question_ids
    
    # 問題情報のリストを作成
    questions_info = [
        {
            'question_id': qid,
            'question_number': idx + 1
        }
        for idx, qid in enumerate(question_ids)
    ]
    
    return jsonify({
        'session_key': quiz_session.session_key,
        'total_questions': quiz_session.total_questions,
        'questions': questions_info,
        'timer_seconds': timer_seconds,
        'sound_enabled': sound_enabled
    })


@api_bp.route('/quiz/<session_key>/question/<int:question_number>', methods=['GET'])
def get_question(session_key, question_number):
    """問題取得API"""
    # セッション確認
    quiz_session = quiz_service.get_session_by_key(session_key)
    if not quiz_session:
        return jsonify({'error': 'セッションが見つかりません'}), 404
    
    # 問題IDリストを取得
    question_ids = session.get(f'question_ids_{session_key}', [])
    
    if not question_ids:
        return jsonify({'error': '問題データが見つかりません'}), 404
    
    # 問題と選択肢を取得
    question, choices = quiz_service.get_question_for_session(
        session_key, question_number, question_ids
    )
    
    if not question:
        return jsonify({'error': '問題が見つかりません'}), 404
    
    # レスポンスデータを作成
    response = {
        'question_id': question.id,
        'question_number': question_number,
        'total_questions': len(question_ids),
        'question_text': question.question_text,
        'choices': [
            {
                'choice_id': choice.id,
                'choice_text': choice.choice_text
            }
            for choice in choices
        ]
    }
    
    return jsonify(response)


@api_bp.route('/quiz/<session_key>/answer', methods=['POST'])
def submit_answer(session_key):
    """回答送信API"""
    data = request.get_json()
    
    question_id = data.get('question_id')
    choice_id = data.get('choice_id')  # タイムアウトの場合はNone
    time_spent_seconds = data.get('time_spent_seconds', 0)
    
    # セッション確認
    quiz_session = quiz_service.get_session_by_key(session_key)
    if not quiz_session:
        return jsonify({'error': 'セッションが見つかりません'}), 404
    
    # 回答を送信して採点
    is_correct, explanation, correct_choice_id = quiz_service.submit_answer(
        session_key, question_id, choice_id, time_spent_seconds
    )
    
    if is_correct is None:
        return jsonify({'error': '回答の処理に失敗しました'}), 500
    
    return jsonify({
        'is_correct': is_correct,
        'correct_choice_id': correct_choice_id,
        'explanation': explanation
    })


@api_bp.route('/quiz/<session_key>/complete', methods=['POST'])
def complete_quiz(session_key):
    """クイズ完了API"""
    # セッションを完了状態にする
    quiz_session = quiz_service.complete_session(session_key)
    
    if not quiz_session:
        return jsonify({'error': 'セッションが見つかりません'}), 404
    
    return jsonify({
        'session_key': session_key,
        'completed': True,
        'result_url': f'/result/{session_key}'
    })


@api_bp.route('/quiz/<session_key>/result', methods=['GET'])
def get_result(session_key):
    """結果取得API"""
    result_data = result_service.get_session_result(session_key)
    
    if not result_data:
        return jsonify({'error': '結果が見つかりません'}), 404
    
    return jsonify(result_data)


@api_bp.route('/settings', methods=['POST'])
def save_settings():
    """設定保存API"""
    data = request.get_json()
    
    # セッションに設定を保存
    session['timer_seconds'] = data.get('timer_seconds', 30)
    session['sound_enabled'] = data.get('sound_enabled', True)
    
    return jsonify({
        'message': '設定を保存しました'
    })


@api_bp.route('/settings', methods=['GET'])
def get_settings():
    """設定取得API"""
    return jsonify({
        'timer_seconds': session.get('timer_seconds', 30),
        'sound_enabled': session.get('sound_enabled', True)
    })


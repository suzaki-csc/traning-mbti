"""
ルーティング定義
"""
from flask import (
    Blueprint, render_template, request, session, redirect, url_for
)
from app.questions import get_question, get_total_questions
from app.mbti_logic import (
    calculate_mbti_type, get_type_description, get_axis_percentages
)
import uuid

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    トップページ
    """
    # セッションをクリア（新しい診断を開始）
    session.clear()
    return render_template('index.html')


@main_bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """
    質問ページ
    GET: 質問を表示
    POST: 回答を受け取り、次の質問へ進む
    """
    # セッションの初期化
    if 'current_question' not in session:
        session['current_question'] = 1
        session['answers'] = []
        session['session_id'] = str(uuid.uuid4())

    if request.method == 'POST':
        # 回答を取得
        selected_option = request.form.get('option')

        if selected_option is not None:
            try:
                option_index = int(selected_option)
                current_q = get_question(session['current_question'])

                if current_q and 0 <= option_index < len(
                        current_q['options']):
                    # 回答を保存
                    option_data = current_q['options'][option_index]
                    session['answers'].append({
                        'question_id': current_q['id'],
                        'axis': option_data['axis'],
                        'score': option_data['score']
                    })

                    # 次の質問へ
                    session['current_question'] += 1
                    session.modified = True

                    # 全質問終了したら結果ページへ
                    if session['current_question'] > get_total_questions():
                        return redirect(url_for('main.result'))
            except (ValueError, TypeError):
                pass

    # 現在の質問を取得
    current_question_id = session.get('current_question', 1)
    question = get_question(current_question_id)

    # 質問が存在しない場合はトップページへ
    if not question:
        return redirect(url_for('main.index'))

    # 進捗情報
    progress = {
        'current': current_question_id,
        'total': get_total_questions(),
        'percentage': round(
            (current_question_id / get_total_questions()) * 100)
    }

    return render_template(
        'quiz.html', question=question, progress=progress)


@main_bp.route('/result')
def result():
    """
    結果表示ページ
    """
    # 回答がない場合はトップページへ
    if 'answers' not in session or len(session['answers']) == 0:
        return redirect(url_for('main.index'))

    # MBTIタイプを計算
    mbti_result = calculate_mbti_type(session['answers'])
    mbti_type = mbti_result['type']
    scores = mbti_result['scores']

    # タイプの説明を取得
    type_info = get_type_description(mbti_type)

    # パーセンテージを計算
    percentages = get_axis_percentages(scores)

    return render_template(
        'result.html',
        mbti_type=mbti_type,
        type_name=type_info['name'],
        description=type_info['description'],
        scores=scores,
        percentages=percentages
    )


@main_bp.route('/restart')
def restart():
    """
    診断をリスタート
    """
    session.clear()
    return redirect(url_for('main.index'))

"""
MBTI風性格診断Webアプリケーション
Flaskメインアプリケーション
"""

from flask import Flask, render_template, request, redirect, url_for, session
from questions import QUESTIONS, ANSWER_OPTIONS, get_question_by_id, get_total_questions
from mbti_logic import calculate_scores, determine_mbti_type, get_axis_percentages
from mbti_descriptions import get_mbti_info
import os

app = Flask(__name__)
# セッション用のシークレットキー（本番環境では環境変数から取得すること）
app.secret_key = os.environ.get('SECRET_KEY', 'mbti-test-secret-key-change-in-production')


@app.route('/')
def index():
    """トップページ"""
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    """診断開始"""
    # セッションを初期化
    session.clear()
    session['answers'] = {}
    # 最初の質問ページへリダイレクト
    return redirect(url_for('question', q_num=1))


@app.route('/question/<int:q_num>')
def question(q_num):
    """質問ページ"""
    # 質問番号の妥当性チェック
    total = get_total_questions()
    if q_num < 1 or q_num > total:
        return redirect(url_for('index'))
    
    # セッションが初期化されていない場合はトップページへ
    if 'answers' not in session:
        return redirect(url_for('index'))
    
    # 質問データを取得
    current_question = get_question_by_id(q_num)
    if not current_question:
        return redirect(url_for('index'))
    
    # 既に回答済みの場合、その回答を取得
    current_answer = session['answers'].get(str(q_num))
    
    return render_template(
        'question.html',
        question=current_question,
        q_num=q_num,
        total=total,
        answer_options=ANSWER_OPTIONS,
        current_answer=current_answer
    )


@app.route('/answer/<int:q_num>', methods=['POST'])
def answer(q_num):
    """回答を受け付けて次の質問へ"""
    # セッションチェック
    if 'answers' not in session:
        return redirect(url_for('index'))
    
    # 回答を取得
    answer_value = request.form.get('answer')
    if not answer_value:
        # 回答が選択されていない場合は同じ質問に戻る
        return redirect(url_for('question', q_num=q_num))
    
    # 回答を保存（キーは文字列型に統一）
    session['answers'][str(q_num)] = int(answer_value)
    session.modified = True
    
    # 次の質問番号を計算
    total = get_total_questions()
    next_q_num = q_num + 1
    
    if next_q_num > total:
        # 全ての質問に回答済みの場合は結果ページへ
        return redirect(url_for('result'))
    else:
        # 次の質問へ
        return redirect(url_for('question', q_num=next_q_num))


@app.route('/back/<int:q_num>', methods=['POST'])
def back(q_num):
    """前の質問に戻る"""
    if q_num <= 1:
        return redirect(url_for('index'))
    
    prev_q_num = q_num - 1
    return redirect(url_for('question', q_num=prev_q_num))


@app.route('/result')
def result():
    """結果ページ"""
    # セッションチェック
    if 'answers' not in session:
        return redirect(url_for('index'))
    
    answers = session['answers']
    
    # 全ての質問に回答しているかチェック
    total = get_total_questions()
    if len(answers) < total:
        # 未回答の質問がある場合は最初の未回答質問へ
        for i in range(1, total + 1):
            if str(i) not in answers:
                return redirect(url_for('question', q_num=i))
    
    # スコアを計算
    scores = calculate_scores(answers)
    
    # MBTIタイプを判定
    mbti_type = determine_mbti_type(scores)
    
    # タイプ情報を取得
    mbti_info = get_mbti_info(mbti_type)
    
    # パーセンテージを計算
    percentages = get_axis_percentages(scores)
    
    return render_template(
        'result.html',
        mbti_type=mbti_type,
        mbti_info=mbti_info,
        scores=scores,
        percentages=percentages
    )


@app.route('/restart')
def restart():
    """診断をやり直す"""
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


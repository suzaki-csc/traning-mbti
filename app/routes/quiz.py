"""
診断機能のルーティング
"""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app.models import db, TestResult
from app.utils import get_questions, calculate_mbti_type
from app.auth import get_mbti_description, get_mbti_name

# Blueprintの作成
quiz = Blueprint('quiz', __name__, url_prefix='/quiz')


@quiz.route('/')
@login_required
def start():
    """診断開始"""
    # セッションをクリア
    session.pop('quiz_answers', None)
    session.pop('current_question', None)
    
    # 最初の質問へリダイレクト
    return redirect(url_for('quiz.question', question_id=1))


@quiz.route('/question/<int:question_id>', methods=['GET', 'POST'])
@login_required
def question(question_id):
    """質問ページ"""
    questions = get_questions()
    
    # 質問IDの範囲チェック
    if question_id < 1 or question_id > len(questions):
        flash('無効な質問IDです。', 'danger')
        return redirect(url_for('quiz.start'))
    
    current_question = questions[question_id - 1]
    
    # セッションから回答を取得
    answers = session.get('quiz_answers', {})
    
    if request.method == 'POST':
        # 回答を取得
        selected_option = request.form.get('option')
        
        if not selected_option:
            flash('選択肢を選んでください。', 'warning')
            return render_template('quiz.html',
                                 question=current_question,
                                 question_id=question_id,
                                 total_questions=len(questions),
                                 selected=answers.get(str(question_id)))
        
        try:
            option_index = int(selected_option)
            selected = current_question['options'][option_index]
            
            # 回答を保存
            answers[str(question_id)] = {
                'question_id': question_id,
                'axis': selected['axis'],
                'score': selected['score']
            }
            session['quiz_answers'] = answers
            
            # 次の質問へ or 結果ページへ
            if question_id < len(questions):
                return redirect(url_for('quiz.question', question_id=question_id + 1))
            else:
                return redirect(url_for('quiz.submit'))
                
        except (ValueError, IndexError):
            flash('無効な選択肢です。', 'danger')
    
    return render_template('quiz.html',
                         question=current_question,
                         question_id=question_id,
                         total_questions=len(questions),
                         selected=answers.get(str(question_id)))


@quiz.route('/submit', methods=['GET', 'POST'])
@login_required
def submit():
    """診断結果送信・保存"""
    answers = session.get('quiz_answers', {})
    questions = get_questions()
    
    # すべての質問に回答しているかチェック
    if len(answers) != len(questions):
        flash('すべての質問に回答してください。', 'warning')
        return redirect(url_for('quiz.start'))
    
    # 回答リストを作成
    answer_list = [answers[str(i)] for i in range(1, len(questions) + 1)]
    
    # MBTIタイプを計算
    result = calculate_mbti_type(answer_list)
    mbti_type = result['mbti_type']
    scores = result['scores']
    
    # データベースに保存
    test_result = TestResult(
        user_id=current_user.id,
        mbti_type=mbti_type,
        e_score=scores['E'],
        i_score=scores['I'],
        s_score=scores['S'],
        n_score=scores['N'],
        t_score=scores['T'],
        f_score=scores['F'],
        j_score=scores['J'],
        p_score=scores['P']
    )
    test_result.set_answers(answer_list)
    
    try:
        db.session.add(test_result)
        db.session.commit()
        
        # セッションをクリア
        session.pop('quiz_answers', None)
        
        # 結果ページへリダイレクト
        return redirect(url_for('quiz.result', result_id=test_result.id))
        
    except Exception as e:
        db.session.rollback()
        flash('結果の保存中にエラーが発生しました。', 'danger')
        return redirect(url_for('main.index'))


@quiz.route('/result/<int:result_id>')
@login_required
def result(result_id):
    """診断結果表示"""
    test_result = TestResult.query.get_or_404(result_id)
    
    # 自分の結果または管理者のみアクセス可能
    if test_result.user_id != current_user.id and not current_user.is_admin():
        flash('この結果を表示する権限がありません。', 'danger')
        return redirect(url_for('main.index'))
    
    # スコア情報
    scores = test_result.get_scores_dict()
    
    # パーセンテージ計算
    from app.utils.scoring import get_axis_percentages
    percentages = get_axis_percentages(scores)
    
    # タイプ情報
    mbti_type = test_result.mbti_type
    mbti_name = get_mbti_name(mbti_type)
    mbti_description = get_mbti_description(mbti_type)
    
    return render_template('result.html',
                         result=test_result,
                         scores=scores,
                         percentages=percentages,
                         mbti_type=mbti_type,
                         mbti_name=mbti_name,
                         mbti_description=mbti_description)


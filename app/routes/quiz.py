"""
クイズ関連のルーティング
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from app import db
from app.models import Category, Quiz, QuizResult, QuizAnswer
from app.utils.auth import login_required
from app.utils.quiz import select_quiz_questions
import json

bp = Blueprint('quiz', __name__, url_prefix='/quiz')


@bp.route('/select')
@login_required
def select():
    """カテゴリ選択ページ"""
    categories = Category.query.all()
    return render_template('quiz/select.html', categories=categories)


@bp.route('/<int:category_id>')
@login_required
def start(category_id):
    """クイズ開始"""
    category = Category.query.get_or_404(category_id)
    
    # 問題を選択（10問）
    questions = select_quiz_questions(category_id, 10)
    
    if not questions:
        flash('このカテゴリには問題がありません', 'warning')
        return redirect(url_for('quiz.select'))
    
    # セッションに問題IDを保存
    session['quiz_questions'] = [q.id for q in questions]
    session['quiz_category_id'] = category_id
    session['quiz_current'] = 0
    session['quiz_answers'] = []
    
    # 最初の問題へリダイレクト
    return redirect(url_for('quiz.question', category_id=category_id, question_num=0))


@bp.route('/<int:category_id>/question/<int:question_num>')
@login_required
def question(category_id, question_num):
    """問題表示ページ"""
    # セッションから問題情報を取得
    question_ids = session.get('quiz_questions', [])
    current_category_id = session.get('quiz_category_id')
    
    if not question_ids or current_category_id != category_id:
        flash('クイズが開始されていません', 'warning')
        return redirect(url_for('quiz.select'))
    
    if question_num < 0 or question_num >= len(question_ids):
        flash('無効な問題番号です', 'danger')
        return redirect(url_for('quiz.select'))
    
    # 問題を取得
    quiz = Quiz.query.get_or_404(question_ids[question_num])
    category = Category.query.get_or_404(category_id)
    
    # 進捗情報
    progress = {
        'current': question_num + 1,
        'total': len(question_ids),
        'answered': len(session.get('quiz_answers', []))
    }
    
    return render_template('quiz/question.html', 
                         quiz=quiz, 
                         category=category,
                         question_num=question_num,
                         progress=progress)


@bp.route('/<int:category_id>/answer', methods=['POST'])
@login_required
def answer(category_id):
    """回答送信"""
    data = request.get_json()
    question_num = data.get('question_num', 0)
    user_answer = data.get('answer', 0)
    
    # セッションから問題情報を取得
    question_ids = session.get('quiz_questions', [])
    current_category_id = session.get('quiz_category_id')
    
    if not question_ids or current_category_id != category_id:
        return jsonify({'error': 'クイズが開始されていません'}), 400
    
    if question_num < 0 or question_num >= len(question_ids):
        return jsonify({'error': '無効な問題番号です'}), 400
    
    # 問題を取得
    quiz = Quiz.query.get_or_404(question_ids[question_num])
    
    # 正解かどうかを判定
    is_correct = (user_answer == quiz.correct_answer)
    
    # セッションに回答を保存
    answers = session.get('quiz_answers', [])
    answers.append({
        'quiz_id': quiz.id,
        'user_answer': user_answer,
        'is_correct': is_correct
    })
    session['quiz_answers'] = answers
    session['quiz_current'] = question_num + 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': quiz.correct_answer,
        'explanation': quiz.explanation
    })


@bp.route('/<int:category_id>/explanation/<int:question_num>')
@login_required
def explanation(category_id, question_num):
    """解説ページ"""
    # セッションから問題情報を取得
    question_ids = session.get('quiz_questions', [])
    answers = session.get('quiz_answers', [])
    current_category_id = session.get('quiz_category_id')
    
    if not question_ids or current_category_id != category_id:
        flash('クイズが開始されていません', 'warning')
        return redirect(url_for('quiz.select'))
    
    if question_num < 0 or question_num >= len(question_ids):
        flash('無効な問題番号です', 'danger')
        return redirect(url_for('quiz.select'))
    
    # 問題を取得
    quiz = Quiz.query.get_or_404(question_ids[question_num])
    category = Category.query.get_or_404(category_id)
    
    # 回答情報を取得
    answer_data = answers[question_num] if question_num < len(answers) else None
    
    if not answer_data:
        flash('回答が見つかりません', 'warning')
        return redirect(url_for('quiz.question', category_id=category_id, question_num=question_num))
    
    # 次の問題があるかチェック
    has_next = (question_num + 1) < len(question_ids)
    
    return render_template('quiz/explanation.html',
                         quiz=quiz,
                         category=category,
                         question_num=question_num,
                         answer_data=answer_data,
                         has_next=has_next)


@bp.route('/<int:category_id>/result')
@login_required
def result(category_id):
    """結果ページ"""
    # セッションから問題情報を取得
    question_ids = session.get('quiz_questions', [])
    answers = session.get('quiz_answers', [])
    current_category_id = session.get('quiz_category_id')
    
    if not question_ids or current_category_id != category_id:
        flash('クイズが開始されていません', 'warning')
        return redirect(url_for('quiz.select'))
    
    if len(answers) != len(question_ids):
        flash('すべての問題に回答してください', 'warning')
        return redirect(url_for('quiz.select'))
    
    # スコアを計算
    score = sum(1 for a in answers if a['is_correct'])
    total = len(question_ids)
    
    # データベースに結果を保存
    quiz_result = QuizResult(
        user_id=session['user_id'],
        category_id=category_id,
        score=score,
        total_questions=total,
        is_review_mode=False
    )
    db.session.add(quiz_result)
    db.session.flush()  # IDを取得するためにflush
    
    # 回答詳細を保存
    for answer_data in answers:
        quiz_answer = QuizAnswer(
            quiz_result_id=quiz_result.id,
            quiz_id=answer_data['quiz_id'],
            user_answer=answer_data['user_answer'],
            is_correct=answer_data['is_correct']
        )
        db.session.add(quiz_answer)
    
    db.session.commit()
    
    # 間違えた問題のリストを作成
    wrong_quiz_ids = [a['quiz_id'] for a in answers if not a['is_correct']]
    wrong_quizzes = Quiz.query.filter(Quiz.id.in_(wrong_quiz_ids)).all() if wrong_quiz_ids else []
    
    # カテゴリ情報を取得
    category = Category.query.get_or_404(category_id)
    
    # セッションをクリア
    session.pop('quiz_questions', None)
    session.pop('quiz_category_id', None)
    session.pop('quiz_current', None)
    session.pop('quiz_answers', None)
    
    return render_template('quiz/result.html',
                         category=category,
                         score=score,
                         total=total,
                         wrong_quizzes=wrong_quizzes,
                         quiz_result_id=quiz_result.id)


@bp.route('/<int:category_id>/review/<int:quiz_result_id>')
@login_required
def review_mode(category_id, quiz_result_id):
    """復習モード開始"""
    # クイズ結果を取得
    quiz_result = QuizResult.query.get_or_404(quiz_result_id)
    
    # 自分の結果か確認
    if quiz_result.user_id != session['user_id']:
        flash('アクセス権限がありません', 'danger')
        return redirect(url_for('history.list'))
    
    # 間違えた問題を取得
    wrong_answers = QuizAnswer.query.filter_by(
        quiz_result_id=quiz_result_id,
        is_correct=False
    ).all()
    
    if not wrong_answers:
        flash('復習する問題がありません', 'info')
        return redirect(url_for('history.list'))
    
    # セッションに問題IDを保存
    session['review_questions'] = [a.quiz_id for a in wrong_answers]
    session['review_category_id'] = category_id
    session['review_current'] = 0
    session['review_answers'] = []
    session['review_result_id'] = quiz_result_id
    
    # 最初の問題へリダイレクト
    return redirect(url_for('quiz.review_question', category_id=category_id, question_num=0))


@bp.route('/<int:category_id>/review/question/<int:question_num>')
@login_required
def review_question(category_id, question_num):
    """復習モード問題表示"""
    # セッションから問題情報を取得
    question_ids = session.get('review_questions', [])
    current_category_id = session.get('review_category_id')
    
    if not question_ids or current_category_id != category_id:
        flash('復習モードが開始されていません', 'warning')
        return redirect(url_for('history.list'))
    
    if question_num < 0 or question_num >= len(question_ids):
        flash('無効な問題番号です', 'danger')
        return redirect(url_for('history.list'))
    
    # 問題を取得
    quiz = Quiz.query.get_or_404(question_ids[question_num])
    category = Category.query.get_or_404(category_id)
    
    # 進捗情報
    progress = {
        'current': question_num + 1,
        'total': len(question_ids)
    }
    
    return render_template('quiz/review_question.html',
                         quiz=quiz,
                         category=category,
                         question_num=question_num,
                         progress=progress)


@bp.route('/<int:category_id>/review/result')
@login_required
def review_result(category_id):
    """復習モード結果"""
    # セッションから問題情報を取得
    question_ids = session.get('review_questions', [])
    answers = session.get('review_answers', [])
    quiz_result_id = session.get('review_result_id')
    
    if not question_ids:
        flash('復習モードが開始されていません', 'warning')
        return redirect(url_for('history.list'))
    
    if len(answers) != len(question_ids):
        flash('すべての問題に回答してください', 'warning')
        return redirect(url_for('history.list'))
    
    # スコアを計算
    score = sum(1 for a in answers if a['is_correct'])
    total = len(question_ids)
    
    # データベースに結果を保存（復習モード）
    quiz_result = QuizResult(
        user_id=session['user_id'],
        category_id=category_id,
        score=score,
        total_questions=total,
        is_review_mode=True
    )
    db.session.add(quiz_result)
    db.session.flush()
    
    # 回答詳細を保存
    for answer_data in answers:
        quiz_answer = QuizAnswer(
            quiz_result_id=quiz_result.id,
            quiz_id=answer_data['quiz_id'],
            user_answer=answer_data['user_answer'],
            is_correct=answer_data['is_correct']
        )
        db.session.add(quiz_answer)
    
    db.session.commit()
    
    # カテゴリ情報を取得
    category = Category.query.get_or_404(category_id)
    
    # セッションをクリア
    session.pop('review_questions', None)
    session.pop('review_category_id', None)
    session.pop('review_current', None)
    session.pop('review_answers', None)
    session.pop('review_result_id', None)
    
    return render_template('quiz/review_result.html',
                         category=category,
                         score=score,
                         total=total)


@bp.route('/<int:category_id>/review/answer', methods=['POST'])
@login_required
def review_answer(category_id):
    """復習モード回答送信"""
    data = request.get_json()
    question_num = data.get('question_num', 0)
    user_answer = data.get('answer', 0)
    
    # セッションから問題情報を取得
    question_ids = session.get('review_questions', [])
    current_category_id = session.get('review_category_id')
    
    if not question_ids or current_category_id != category_id:
        return jsonify({'error': '復習モードが開始されていません'}), 400
    
    if question_num < 0 or question_num >= len(question_ids):
        return jsonify({'error': '無効な問題番号です'}), 400
    
    # 問題を取得
    quiz = Quiz.query.get_or_404(question_ids[question_num])
    
    # 正解かどうかを判定
    is_correct = (user_answer == quiz.correct_answer)
    
    # セッションに回答を保存
    answers = session.get('review_answers', [])
    answers.append({
        'quiz_id': quiz.id,
        'user_answer': user_answer,
        'is_correct': is_correct
    })
    session['review_answers'] = answers
    session['review_current'] = question_num + 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': quiz.correct_answer,
        'explanation': quiz.explanation
    })


@bp.route('/<int:category_id>/review/explanation/<int:question_num>')
@login_required
def review_explanation(category_id, question_num):
    """復習モード解説ページ"""
    # セッションから問題情報を取得
    question_ids = session.get('review_questions', [])
    answers = session.get('review_answers', [])
    current_category_id = session.get('review_category_id')
    
    if not question_ids or current_category_id != category_id:
        flash('復習モードが開始されていません', 'warning')
        return redirect(url_for('history.list'))
    
    if question_num < 0 or question_num >= len(question_ids):
        flash('無効な問題番号です', 'danger')
        return redirect(url_for('history.list'))
    
    # 問題を取得
    quiz = Quiz.query.get_or_404(question_ids[question_num])
    category = Category.query.get_or_404(category_id)
    
    # 回答情報を取得
    answer_data = answers[question_num] if question_num < len(answers) else None
    
    if not answer_data:
        flash('回答が見つかりません', 'warning')
        return redirect(url_for('quiz.review_question', category_id=category_id, question_num=question_num))
    
    # 次の問題があるかチェック
    has_next = (question_num + 1) < len(question_ids)
    
    return render_template('quiz/review_explanation.html',
                         quiz=quiz,
                         category=category,
                         question_num=question_num,
                         answer_data=answer_data,
                         has_next=has_next)


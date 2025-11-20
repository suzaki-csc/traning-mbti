"""
ルーティング定義モジュール

Flaskアプリケーションのルーティングを定義します。
クイズアプリケーションの各画面へのルートとAPIエンドポイントを提供します。
"""

from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from app import db
from app.models import Category, Question, QuizResult, AnswerDetail
from app.utils import select_questions, calculate_score, format_score_string
from datetime import datetime
import json

# ブループリントの作成
main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """
    トップページ（カテゴリ選択画面）
    
    利用可能なカテゴリの一覧を表示します。
    """
    categories = Category.query.all()
    return render_template('index.html', categories=categories)


@main_bp.route('/quiz/<int:category_id>')
def start_quiz(category_id):
    """
    クイズ開始
    
    指定されたカテゴリのクイズを開始します。
    問題をランダムに選択してセッションに保存し、最初の問題を表示します。
    
    Args:
        category_id: カテゴリID
    """
    # カテゴリの存在確認
    category = Category.query.get_or_404(category_id)
    
    # カテゴリに紐づく問題を取得
    questions = Question.query.filter_by(category_id=category_id).all()
    
    if not questions:
        # 問題が存在しない場合
        return render_template('error.html', message='このカテゴリには問題がありません。'), 404
    
    # 問題IDリストを取得
    question_ids = [q.id for q in questions]
    
    # 最大10問をランダムに選択（重複ありの場合は自動処理）
    selected_question_ids = select_questions(question_ids, max_questions=10)
    
    # セッションにクイズ情報を保存
    session['quiz'] = {
        'category_id': category_id,
        'category_name': category.name,
        'question_ids': selected_question_ids,
        'current_index': 0,
        'answers': {},
        'start_time': datetime.utcnow().isoformat(),
        'timer_duration': 30  # デフォルト30秒
    }
    
    # 最初の問題を取得
    first_question_id = selected_question_ids[0]
    first_question = Question.query.get(first_question_id)
    
    return render_template('quiz.html', 
                         question=first_question,
                         question_number=1,
                         total_questions=len(selected_question_ids),
                         category_name=category.name)


@main_bp.route('/quiz/answer', methods=['POST'])
def submit_answer():
    """
    回答送信（AJAXエンドポイント）
    
    ユーザーの回答を受け取り、正誤判定を行います。
    
    Returns:
        JSON: 正誤判定結果と解説を含むJSONレスポンス
    """
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('answer')  # 'A', 'B', 'C', 'D'のいずれか
    time_taken = data.get('time_taken', 0)  # 回答にかかった時間（秒）
    
    # セッションからクイズ情報を取得
    quiz_session = session.get('quiz')
    if not quiz_session:
        return jsonify({'error': 'クイズセッションが見つかりません'}), 400
    
    # 問題を取得
    question = Question.query.get_or_404(question_id)
    
    # 正誤判定
    is_correct = question.check_answer(user_answer)
    
    # セッションに回答を保存
    quiz_session['answers'][question_id] = {
        'user_answer': user_answer,
        'is_correct': is_correct,
        'time_taken': time_taken
    }
    session['quiz'] = quiz_session
    
    # レスポンスを返す
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation
    })


@main_bp.route('/quiz/next', methods=['GET'])
def next_question():
    """
    次の問題へ進む（AJAXエンドポイント）
    
    現在の問題の次の問題を取得します。
    すべての問題に回答済みの場合は、クイズ終了処理を行います。
    
    Returns:
        JSON: 次の問題情報またはクイズ終了フラグを含むJSONレスポンス
    """
    # セッションからクイズ情報を取得
    quiz_session = session.get('quiz')
    if not quiz_session:
        return jsonify({'error': 'クイズセッションが見つかりません'}), 400
    
    current_index = quiz_session['current_index']
    question_ids = quiz_session['question_ids']
    
    # 次の問題のインデックス
    next_index = current_index + 1
    
    # すべての問題に回答済みかチェック
    if next_index >= len(question_ids):
        # クイズ終了処理
        return finish_quiz(quiz_session)
    
    # 次の問題を取得
    next_question_id = question_ids[next_index]
    next_question = Question.query.get(next_question_id)
    
    # セッションを更新
    quiz_session['current_index'] = next_index
    session['quiz'] = quiz_session
    
    return jsonify({
        'question': next_question.to_dict(),
        'question_number': next_index + 1,
        'total_questions': len(question_ids),
        'finished': False
    })


def finish_quiz(quiz_session):
    """
    クイズ終了処理
    
    セッションから回答履歴を取得し、スコアを計算してデータベースに保存します。
    
    Args:
        quiz_session: セッションに保存されたクイズ情報
    
    Returns:
        JSON: クイズ結果IDを含むJSONレスポンス
    """
    # スコアを計算
    score_info = calculate_score(quiz_session['answers'])
    
    # かかった時間を計算
    start_time = datetime.fromisoformat(quiz_session['start_time'])
    end_time = datetime.utcnow()
    time_taken = int((end_time - start_time).total_seconds())
    
    # クイズ結果をデータベースに保存
    quiz_result = QuizResult(
        category_id=quiz_session['category_id'],
        total_questions=score_info['total_questions'],
        correct_answers=score_info['correct_answers'],
        score_percentage=score_info['score_percentage'],
        time_taken=time_taken
    )
    db.session.add(quiz_result)
    db.session.flush()  # IDを取得するためにflush
    
    # 回答詳細をデータベースに保存
    for question_id, answer_data in quiz_session['answers'].items():
        answer_detail = AnswerDetail(
            quiz_result_id=quiz_result.id,
            question_id=question_id,
            user_answer=answer_data['user_answer'],
            is_correct=answer_data['is_correct'],
            time_taken=answer_data.get('time_taken', 0)
        )
        db.session.add(answer_detail)
    
    db.session.commit()
    
    # セッションをクリア
    session.pop('quiz', None)
    
    return jsonify({
        'finished': True,
        'quiz_result_id': quiz_result.id,
        'redirect_url': url_for('main.show_result', quiz_result_id=quiz_result.id)
    })


@main_bp.route('/result/<int:quiz_result_id>')
def show_result(quiz_result_id):
    """
    結果表示画面
    
    クイズの結果を表示します。スコア、復習リストなどを表示します。
    
    Args:
        quiz_result_id: クイズ結果ID
    """
    quiz_result = QuizResult.query.get_or_404(quiz_result_id)
    category = Category.query.get(quiz_result.category_id)
    
    # 回答詳細を取得（間違えた問題を含む）
    answer_details = AnswerDetail.query.filter_by(quiz_result_id=quiz_result_id).all()
    
    # 間違えた問題の詳細を取得
    incorrect_questions = []
    for detail in answer_details:
        if not detail.is_correct:
            question = Question.query.get(detail.question_id)
            incorrect_questions.append({
                'question': question.to_dict(),
                'user_answer': detail.user_answer,
                'correct_answer': question.correct_answer,
                'explanation': question.explanation
            })
    
    # スコア文字列を生成
    score_string = format_score_string(
        category.name,
        quiz_result.correct_answers,
        quiz_result.total_questions,
        float(quiz_result.score_percentage)
    )
    
    return render_template('result.html',
                         quiz_result=quiz_result,
                         category=category,
                         incorrect_questions=incorrect_questions,
                         score_string=score_string)


@main_bp.route('/review/<int:quiz_result_id>')
def review_quiz(quiz_result_id):
    """
    復習モード開始
    
    間違えた問題のみを再度出題します。
    
    Args:
        quiz_result_id: クイズ結果ID
    """
    quiz_result = QuizResult.query.get_or_404(quiz_result_id)
    category = Category.query.get(quiz_result.category_id)
    
    # 間違えた問題のIDリストを取得
    incorrect_question_ids = quiz_result.get_incorrect_questions()
    
    if not incorrect_question_ids:
        # 間違えた問題がない場合
        return redirect(url_for('main.show_result', quiz_result_id=quiz_result_id))
    
    # 問題IDリストをシャッフル
    from app.utils import shuffle_list
    shuffled_ids = shuffle_list(incorrect_question_ids)
    
    # セッションに復習モードの情報を保存
    session['review'] = {
        'quiz_result_id': quiz_result_id,
        'category_id': quiz_result.category_id,
        'category_name': category.name,
        'question_ids': shuffled_ids,
        'current_index': 0,
        'answers': {},
        'start_time': datetime.utcnow().isoformat(),
        'timer_duration': 30
    }
    
    # 最初の問題を取得
    first_question_id = shuffled_ids[0]
    first_question = Question.query.get(first_question_id)
    
    return render_template('review.html',
                         question=first_question,
                         question_number=1,
                         total_questions=len(shuffled_ids),
                         category_name=category.name)


@main_bp.route('/review/answer', methods=['POST'])
def submit_review_answer():
    """
    復習モードでの回答送信（AJAXエンドポイント）
    
    Returns:
        JSON: 正誤判定結果と解説を含むJSONレスポンス
    """
    data = request.get_json()
    question_id = data.get('question_id')
    user_answer = data.get('answer')
    time_taken = data.get('time_taken', 0)
    
    # セッションから復習モード情報を取得
    review_session = session.get('review')
    if not review_session:
        return jsonify({'error': '復習セッションが見つかりません'}), 400
    
    # 問題を取得
    question = Question.query.get_or_404(question_id)
    
    # 正誤判定
    is_correct = question.check_answer(user_answer)
    
    # セッションに回答を保存
    review_session['answers'][question_id] = {
        'user_answer': user_answer,
        'is_correct': is_correct,
        'time_taken': time_taken
    }
    session['review'] = review_session
    
    # レスポンスを返す
    return jsonify({
        'is_correct': is_correct,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation
    })


@main_bp.route('/review/next', methods=['GET'])
def next_review_question():
    """
    復習モードでの次の問題へ進む（AJAXエンドポイント）
    
    Returns:
        JSON: 次の問題情報または復習終了フラグを含むJSONレスポンス
    """
    # セッションから復習モード情報を取得
    review_session = session.get('review')
    if not review_session:
        return jsonify({'error': '復習セッションが見つかりません'}), 400
    
    current_index = review_session['current_index']
    question_ids = review_session['question_ids']
    
    # 次の問題のインデックス
    next_index = current_index + 1
    
    # すべての問題に回答済みかチェック
    if next_index >= len(question_ids):
        # 復習終了
        session.pop('review', None)
        return jsonify({
            'finished': True,
            'redirect_url': url_for('main.index')
        })
    
    # 次の問題を取得
    next_question_id = question_ids[next_index]
    next_question = Question.query.get(next_question_id)
    
    # セッションを更新
    review_session['current_index'] = next_index
    session['review'] = review_session
    
    return jsonify({
        'question': next_question.to_dict(),
        'question_number': next_index + 1,
        'total_questions': len(question_ids),
        'finished': False
    })


@main_bp.route('/api/copy-score', methods=['POST'])
def copy_score():
    """
    スコア文字列をコピー用に返す（AJAXエンドポイント）
    
    Returns:
        JSON: スコア文字列を含むJSONレスポンス
    """
    data = request.get_json()
    quiz_result_id = data.get('quiz_result_id')
    
    quiz_result = QuizResult.query.get_or_404(quiz_result_id)
    category = Category.query.get(quiz_result.category_id)
    
    score_string = format_score_string(
        category.name,
        quiz_result.correct_answers,
        quiz_result.total_questions,
        float(quiz_result.score_percentage)
    )
    
    return jsonify({'score_string': score_string})


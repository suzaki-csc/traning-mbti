"""メイン診断フローのルーティング"""
import uuid
from flask import Blueprint, render_template, request, redirect, url_for, session
from models import db, Diagnosis
from services.questions import QUESTIONS, MBTI_TYPES, get_question_by_id, get_total_questions
from services.scoring import calculate_mbti_type, get_axis_percentages

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """トップページ"""
    return render_template('index.html')


@main_bp.route('/start', methods=['POST'])
def start():
    """診断開始"""
    # セッションをクリア
    session.clear()
    
    # 新しいセッションIDを生成
    session['session_id'] = str(uuid.uuid4())
    session['user_name'] = request.form.get('user_name', '')
    session['user_email'] = request.form.get('user_email', '')
    session['current_question'] = 1
    session['answers'] = {}
    session['scores'] = {
        'E': 0, 'I': 0,
        'S': 0, 'N': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }
    
    return redirect(url_for('main.question', q_id=1))


@main_bp.route('/question/<int:q_id>', methods=['GET', 'POST'])
def question(q_id):
    """質問ページ"""
    total_questions = get_total_questions()
    
    # セッションチェック
    if 'session_id' not in session:
        return redirect(url_for('main.index'))
    
    # 質問範囲チェック
    if q_id < 1 or q_id > total_questions:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        # 回答を保存
        answer = request.form.get('answer')
        if answer:
            current_question = get_question_by_id(q_id)
            if current_question:
                # 選択された選択肢を探す
                selected_option = None
                for option in current_question['options']:
                    if option['value'] == answer:
                        selected_option = option
                        break
                
                if selected_option:
                    # 回答を保存
                    session['answers'][str(q_id)] = {
                        'selected': answer,
                        'axis': selected_option['axis'],
                        'score': selected_option['score']
                    }
                    
                    # スコアを更新
                    axis = selected_option['axis']
                    session['scores'][axis] = session['scores'].get(axis, 0) + selected_option['score']
                    
                    # セッションを明示的に保存
                    session.modified = True
        
        # 次の質問または結果ページへ
        if q_id < total_questions:
            return redirect(url_for('main.question', q_id=q_id + 1))
        else:
            return redirect(url_for('main.result'))
    
    # GET: 質問を表示
    current_question = get_question_by_id(q_id)
    if not current_question:
        return redirect(url_for('main.index'))
    
    # 既に回答済みの場合、その回答を取得
    saved_answer = session.get('answers', {}).get(str(q_id), {}).get('selected')
    
    return render_template(
        'question.html',
        question=current_question,
        question_number=q_id,
        total_questions=total_questions,
        saved_answer=saved_answer
    )


@main_bp.route('/result')
def result():
    """結果ページ"""
    # セッションチェック
    if 'session_id' not in session or 'scores' not in session:
        return redirect(url_for('main.index'))
    
    # MBTIタイプを判定
    scores = session['scores']
    mbti_type = calculate_mbti_type(scores)
    
    # タイプ情報を取得
    type_info = MBTI_TYPES.get(mbti_type, {})
    
    # 百分率を計算
    percentages = get_axis_percentages(scores)
    
    # セッションに結果を保存
    session['mbti_type'] = mbti_type
    
    return render_template(
        'result.html',
        mbti_type=mbti_type,
        type_info=type_info,
        scores=scores,
        percentages=percentages
    )


@main_bp.route('/result/save', methods=['POST'])
def save_result():
    """結果をデータベースに保存"""
    # セッションチェック
    if 'session_id' not in session or 'mbti_type' not in session:
        return redirect(url_for('main.index'))
    
    try:
        # 診断結果をDBに保存
        diagnosis = Diagnosis(
            session_id=session['session_id'],
            user_name=session.get('user_name'),
            user_email=session.get('user_email'),
            e_score=session['scores'].get('E', 0),
            i_score=session['scores'].get('I', 0),
            s_score=session['scores'].get('S', 0),
            n_score=session['scores'].get('N', 0),
            t_score=session['scores'].get('T', 0),
            f_score=session['scores'].get('F', 0),
            j_score=session['scores'].get('J', 0),
            p_score=session['scores'].get('P', 0),
            mbti_type=session['mbti_type'],
            answers=session.get('answers')
        )
        
        db.session.add(diagnosis)
        db.session.commit()
        
    except Exception as e:
        print(f"Error saving diagnosis: {e}")
        db.session.rollback()
    
    return redirect(url_for('main.index'))


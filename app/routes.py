"""ルーティング定義"""
import uuid
from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app import db
from app.models import DiagnosisSession, DiagnosisAnswer
from app.quiz_data import QUESTIONS, get_question_by_id, get_total_questions, get_mbti_info
from app.scoring import calculate_scores, determine_type, get_score_percentages, get_axis_descriptions

# ブループリント定義
main_bp = Blueprint('main', __name__)
admin_bp = Blueprint('admin', __name__)


# ========== メインルート ==========

@main_bp.route('/')
def index():
    """トップページ"""
    return render_template('index.html')


@main_bp.route('/quiz', methods=['GET', 'POST'])
def quiz():
    """診断ページ"""
    
    if request.method == 'GET':
        # 新規診断開始
        session.clear()
        session['quiz_session_id'] = str(uuid.uuid4())
        session['answers'] = []
        session['current_question'] = 1
        
        question = get_question_by_id(1)
        return render_template(
            'quiz.html',
            question=question,
            current=1,
            total=get_total_questions()
        )
    
    # POST: 回答を処理
    current_question_id = session.get('current_question', 1)
    answers = session.get('answers', [])
    
    # 回答を取得（脆弱性: 入力検証なし）
    option_index = request.form.get('option')
    
    if option_index is not None:
        option_index = int(option_index)
        question = get_question_by_id(current_question_id)
        
        if question and 0 <= option_index < len(question['options']):
            selected_option = question['options'][option_index]
            
            # 回答を保存
            answer = {
                'question_id': current_question_id,
                'axis': selected_option['axis'],
                'score': selected_option['score'],
                'answer_text': selected_option['text']
            }
            answers.append(answer)
            session['answers'] = answers
    
    # 次の質問へ
    next_question_id = current_question_id + 1
    
    if next_question_id > get_total_questions():
        # 全質問完了 → 結果を計算してDBに保存
        return redirect(url_for('main.calculate_result'))
    
    # 次の質問を表示
    session['current_question'] = next_question_id
    next_question = get_question_by_id(next_question_id)
    
    return render_template(
        'quiz.html',
        question=next_question,
        current=next_question_id,
        total=get_total_questions()
    )


@main_bp.route('/calculate_result')
def calculate_result():
    """結果を計算してDBに保存"""
    answers = session.get('answers', [])
    quiz_session_id = session.get('quiz_session_id')
    
    if not answers or not quiz_session_id:
        return redirect(url_for('main.index'))
    
    # スコア計算
    scores = calculate_scores(answers)
    mbti_type = determine_type(scores)
    
    # IPアドレス取得（脆弱性: X-Forwarded-Forを信頼）
    ip_address = request.headers.get('X-Forwarded-For', request.remote_addr)
    
    # DBに保存
    diagnosis_session = DiagnosisSession(
        session_id=quiz_session_id,
        mbti_type=mbti_type,
        scores_json=scores,
        ip_address=ip_address
    )
    db.session.add(diagnosis_session)
    db.session.commit()
    
    # 各回答を保存
    for answer in answers:
        diagnosis_answer = DiagnosisAnswer(
            session_id=diagnosis_session.id,
            question_id=answer['question_id'],
            axis=answer['axis'],
            score=answer['score'],
            answer_text=answer['answer_text']
        )
        db.session.add(diagnosis_answer)
    
    db.session.commit()
    
    # セッションクリア
    session.clear()
    
    return redirect(url_for('main.result', session_id=quiz_session_id))


@main_bp.route('/result/<session_id>')
def result(session_id):
    """診断結果ページ"""
    
    # DBから結果を取得（脆弱性: SQLインジェクション対策なしのクエリ例）
    diagnosis = DiagnosisSession.query.filter_by(session_id=session_id).first()
    
    if not diagnosis:
        return redirect(url_for('main.index'))
    
    # MBTIタイプ情報を取得
    mbti_info = get_mbti_info(diagnosis.mbti_type)
    
    # スコアのパーセンテージを計算
    percentages = get_score_percentages(diagnosis.scores_json)
    
    # 軸の説明を取得
    axis_descriptions = get_axis_descriptions()
    
    return render_template(
        'result.html',
        mbti_type=diagnosis.mbti_type,
        mbti_info=mbti_info,
        scores=diagnosis.scores_json,
        percentages=percentages,
        axis_descriptions=axis_descriptions,
        created_at=diagnosis.created_at
    )


# ========== 管理者ルート ==========

@admin_bp.route('/')
def index():
    """管理トップページ"""
    return redirect(url_for('admin.history'))


@admin_bp.route('/history')
def history():
    """診断履歴一覧"""
    
    # ページネーション
    page = request.args.get('page', 1, type=int)
    per_page = 20
    
    # 検索フィルター（脆弱性: SQLインジェクション）
    search_type = request.args.get('type', '')
    
    query = DiagnosisSession.query
    
    if search_type:
        # 脆弱性: 直接SQL文字列を構築
        query = query.filter(DiagnosisSession.mbti_type == search_type)
    
    # 新しい順に並べ替え
    diagnoses = query.order_by(DiagnosisSession.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    # MBTIタイプの一覧（フィルター用）
    mbti_types = db.session.query(DiagnosisSession.mbti_type).distinct().all()
    mbti_types = [t[0] for t in mbti_types]
    
    return render_template(
        'admin/history.html',
        diagnoses=diagnoses,
        mbti_types=mbti_types,
        search_type=search_type
    )


@admin_bp.route('/history/<int:id>')
def history_detail(id):
    """診断履歴詳細（JSON）"""
    
    diagnosis = DiagnosisSession.query.get_or_404(id)
    
    return jsonify(diagnosis.to_dict())


@admin_bp.route('/history/<int:id>', methods=['DELETE'])
def history_delete(id):
    """診断履歴削除"""
    
    diagnosis = DiagnosisSession.query.get_or_404(id)
    
    db.session.delete(diagnosis)
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': '診断履歴を削除しました'
    })


@admin_bp.route('/stats')
def stats():
    """統計情報（API）"""
    
    # タイプ別の診断数
    type_counts = db.session.query(
        DiagnosisSession.mbti_type,
        db.func.count(DiagnosisSession.id)
    ).group_by(DiagnosisSession.mbti_type).all()
    
    # 総診断数
    total_diagnoses = DiagnosisSession.query.count()
    
    return jsonify({
        'total_diagnoses': total_diagnoses,
        'type_distribution': {t: c for t, c in type_counts}
    })


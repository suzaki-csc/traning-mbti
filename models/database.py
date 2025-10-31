# このファイルは後方互換性のために残していますが、
# 現在はmodels.pyでFlask-SQLAlchemyを使用しています
from models.models import db, DiagnosisResult, Answer, Question

def get_all_results():
    """全ての診断結果を取得"""
    return DiagnosisResult.query.order_by(DiagnosisResult.diagnosed_at.desc()).all()

def get_result_by_id(result_id):
    """IDで診断結果を取得"""
    return DiagnosisResult.query.get(result_id)

def save_diagnosis_result(user_name, mbti_type, scores, user_ip):
    """診断結果を保存"""
    diagnosis = DiagnosisResult(
        user_name=user_name,
        mbti_type=mbti_type,
        e_score=scores['E'],
        i_score=scores['I'],
        s_score=scores['S'],
        n_score=scores['N'],
        t_score=scores['T'],
        f_score=scores['F'],
        j_score=scores['J'],
        p_score=scores['P'],
        user_ip=user_ip
    )
    db.session.add(diagnosis)
    db.session.commit()
    return diagnosis.id

def save_answers(result_id, answers):
    """回答を保存"""
    for question_id, answer_value in answers.items():
        if question_id.isdigit():
            answer = Answer(
                result_id=result_id,
                question_id=int(question_id),
                answer_value=int(answer_value)
            )
            db.session.add(answer)
    db.session.commit()


from flask_mysqldb import MySQL

mysql = MySQL()

def init_db(app):
    """データベースの初期化"""
    mysql.init_app(app)
    return mysql

def get_all_results():
    """全ての診断結果を取得"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, user_name, mbti_type, diagnosed_at FROM diagnosis_results ORDER BY diagnosed_at DESC")
    results = cur.fetchall()
    cur.close()
    return results

def get_result_by_id(result_id):
    """IDで診断結果を取得"""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM diagnosis_results WHERE id = %s", (result_id,))
    result = cur.fetchone()
    cur.close()
    return result

def save_diagnosis_result(user_name, mbti_type, scores, user_ip):
    """診断結果を保存"""
    cur = mysql.connection.cursor()
    cur.execute(
        """INSERT INTO diagnosis_results 
        (user_name, mbti_type, e_score, i_score, s_score, n_score, t_score, f_score, j_score, p_score, user_ip) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        (user_name, mbti_type, scores['E'], scores['I'], scores['S'], scores['N'], 
         scores['T'], scores['F'], scores['J'], scores['P'], user_ip)
    )
    result_id = cur.lastrowid
    mysql.connection.commit()
    cur.close()
    return result_id

def save_answers(result_id, answers):
    """回答を保存"""
    cur = mysql.connection.cursor()
    for question_id, answer_value in answers.items():
        if question_id.isdigit():
            cur.execute(
                "INSERT INTO answers (result_id, question_id, answer_value) VALUES (%s, %s, %s)",
                (result_id, question_id, answer_value)
            )
    mysql.connection.commit()
    cur.close()


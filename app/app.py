"""
MBTI風性格診断Webアプリケーション

警告: このアプリケーションは学習目的で意図的に脆弱性を含んでいます。
本番環境では使用しないでください。
"""

from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
import time
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# MBTIタイプの説明
MBTI_DESCRIPTIONS = {
    'INTJ': '建築家 - 戦略的思考と完璧主義者',
    'INTP': '論理学者 - 革新的な発明家',
    'ENTJ': '指揮官 - 大胆で想像力豊かなリーダー',
    'ENTP': '討論者 - 知的好奇心旺盛な思考家',
    'INFJ': '提唱者 - 理想主義的で思いやりのある人',
    'INFP': '仲介者 - 詩的で親切で利他的な人',
    'ENFJ': '主人公 - カリスマ性のあるインスピレーションを与えるリーダー',
    'ENFP': '運動家 - 熱心で創造的で社交的な人',
    'ISTJ': '管理者 - 実用的で事実に基づいた人',
    'ISFJ': '擁護者 - 献身的で温かい保護者',
    'ESTJ': '幹部 - 優れた管理者',
    'ESFJ': '領事官 - 非常に思いやりがあり社交的で人気者',
    'ISTP': '巨匠 - 大胆で実践的な実験者',
    'ISFP': '冒険家 - 柔軟で魅力的な芸術家',
    'ESTP': '起業家 - 賢くエネルギッシュで知覚的',
    'ESFP': 'エンターテイナー - 自発的でエネルギッシュで熱心'
}


def get_db_connection():
    """データベース接続を取得"""
    max_retries = 5
    retry_delay = 2
    
    for attempt in range(max_retries):
        try:
            connection = pymysql.connect(
                host=app.config['DB_HOST'],
                user=app.config['DB_USER'],
                password=app.config['DB_PASSWORD'],
                database=app.config['DB_NAME'],
                port=app.config['DB_PORT'],
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except pymysql.err.OperationalError as e:
            if attempt < max_retries - 1:
                print(f"データベース接続失敗 (試行 {attempt + 1}/{max_retries}): {e}")
                time.sleep(retry_delay)
            else:
                raise


def calculate_mbti_type(answers, questions):
    """
    回答からMBTIタイプを判定
    
    Args:
        answers: {question_id: answer_value} の辞書
        questions: 質問のリスト
    
    Returns:
        dict: {'mbti_type': str, 'scores': dict}
    """
    scores = {
        'E': 0, 'I': 0,
        'S': 0, 'N': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }
    
    # 各回答を集計
    for question in questions:
        question_id = question['id']
        if question_id in answers:
            axis = question['axis']
            value = int(answers[question_id])
            
            # directionに応じてスコアを加算
            if question['direction'] == 'positive':
                scores[axis] += value
            else:
                scores[axis] += (6 - value)
    
    # MBTIタイプ判定
    mbti_type = ''
    mbti_type += 'E' if scores['E'] > scores['I'] else 'I'
    mbti_type += 'S' if scores['S'] > scores['N'] else 'N'
    mbti_type += 'T' if scores['T'] > scores['F'] else 'F'
    mbti_type += 'J' if scores['J'] > scores['P'] else 'P'
    
    return {
        'mbti_type': mbti_type,
        'scores': scores
    }


@app.route('/')
def index():
    """トップページ"""
    return render_template('index.html')


@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    """診断ページ（質問表示と回答処理）"""
    
    if request.method == 'GET':
        # 質問を取得して表示
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM questions ORDER BY order_num")
                questions = cursor.fetchall()
            return render_template('diagnosis.html', questions=questions)
        finally:
            connection.close()
    
    else:  # POST
        # 回答を処理
        user_name = request.form.get('user_name', '匿名')
        
        # 全ての質問を取得
        connection = get_db_connection()
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM questions ORDER BY order_num")
                questions = cursor.fetchall()
            
            # 回答を収集
            answers = {}
            for question in questions:
                answer_value = request.form.get(f'q_{question["id"]}')
                if answer_value:
                    answers[question['id']] = int(answer_value)
            
            # MBTIタイプを計算
            result = calculate_mbti_type(answers, questions)
            mbti_type = result['mbti_type']
            scores = result['scores']
            
            # 結果をデータベースに保存
            with connection.cursor() as cursor:
                # 脆弱性: SQLインジェクション対策なし（学習目的）
                # 本来はプレースホルダーを使用すべき
                query = f"""
                    INSERT INTO diagnosis_results 
                    (user_name, mbti_type, e_score, i_score, s_score, n_score, t_score, f_score, j_score, p_score)
                    VALUES ('{user_name}', '{mbti_type}', {scores['E']}, {scores['I']}, 
                            {scores['S']}, {scores['N']}, {scores['T']}, {scores['F']}, 
                            {scores['J']}, {scores['P']})
                """
                cursor.execute(query)
                result_id = cursor.lastrowid
                
                # 回答を保存
                for question_id, answer_value in answers.items():
                    cursor.execute(
                        "INSERT INTO answers (result_id, question_id, answer_value) VALUES (%s, %s, %s)",
                        (result_id, question_id, answer_value)
                    )
                
                connection.commit()
            
            return redirect(url_for('result', result_id=result_id))
        
        finally:
            connection.close()


@app.route('/result/<int:result_id>')
def result(result_id):
    """診断結果表示"""
    
    # 脆弱性: SQLインジェクション対策なし（学習目的）
    # result_idを直接SQLに埋め込んでいる
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            query = f"SELECT * FROM diagnosis_results WHERE id = {result_id}"
            cursor.execute(query)
            diagnosis = cursor.fetchone()
            
            if not diagnosis:
                flash('診断結果が見つかりません', 'error')
                return redirect(url_for('index'))
            
            # MBTIタイプの説明を取得
            description = MBTI_DESCRIPTIONS.get(diagnosis['mbti_type'], '説明なし')
            
            return render_template('result.html', 
                                   diagnosis=diagnosis, 
                                   description=description)
    finally:
        connection.close()


@app.route('/admin')
def admin():
    """管理画面（診断履歴一覧）"""
    
    search_name = request.args.get('name', '')
    search_type = request.args.get('type', '')
    
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # 脆弱性: SQLインジェクション対策なし（学習目的）
            # ユーザー入力を直接SQLに埋め込んでいる
            if search_name or search_type:
                conditions = []
                if search_name:
                    conditions.append(f"user_name LIKE '%{search_name}%'")
                if search_type:
                    conditions.append(f"mbti_type = '{search_type}'")
                
                where_clause = " AND ".join(conditions)
                query = f"SELECT * FROM diagnosis_results WHERE {where_clause} ORDER BY created_at DESC"
            else:
                query = "SELECT * FROM diagnosis_results ORDER BY created_at DESC"
            
            cursor.execute(query)
            results = cursor.fetchall()
            
            # MBTIタイプのリストを取得（検索用）
            cursor.execute("SELECT DISTINCT mbti_type FROM diagnosis_results ORDER BY mbti_type")
            mbti_types = [row['mbti_type'] for row in cursor.fetchall()]
            
            return render_template('admin.html', 
                                   results=results,
                                   mbti_types=mbti_types,
                                   search_name=search_name,
                                   search_type=search_type)
    finally:
        connection.close()


@app.errorhandler(404)
def not_found(error):
    """404エラーハンドラー"""
    return render_template('index.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドラー"""
    return "Internal Server Error", 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


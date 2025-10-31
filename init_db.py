import MySQLdb
import time
import os

def wait_for_db():
    """データベースの起動を待機"""
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            conn = MySQLdb.connect(
                host=os.environ.get('DB_HOST', 'localhost'),
                user=os.environ.get('DB_USER', 'mbti_user'),
                password=os.environ.get('DB_PASSWORD', 'mbti_password'),
                database=os.environ.get('DB_NAME', 'mbti_db')
            )
            conn.close()
            print("データベース接続成功")
            return True
        except MySQLdb.Error as e:
            retry_count += 1
            print(f"データベース接続待機中... ({retry_count}/{max_retries})")
            time.sleep(2)
    
    return False

def init_database():
    """データベースの初期化"""
    try:
        conn = MySQLdb.connect(
            host=os.environ.get('DB_HOST', 'localhost'),
            user=os.environ.get('DB_USER', 'mbti_user'),
            password=os.environ.get('DB_PASSWORD', 'mbti_password'),
            database=os.environ.get('DB_NAME', 'mbti_db')
        )
        
        cursor = conn.cursor()
        
        # 既存のテーブルを削除
        cursor.execute("DROP TABLE IF EXISTS answers")
        cursor.execute("DROP TABLE IF EXISTS diagnosis_results")
        cursor.execute("DROP TABLE IF EXISTS questions")
        
        # questionsテーブル作成
        cursor.execute("""
            CREATE TABLE questions (
                id INT AUTO_INCREMENT PRIMARY KEY,
                question_text TEXT NOT NULL,
                axis VARCHAR(10) NOT NULL,
                weight INT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # diagnosis_resultsテーブル作成
        cursor.execute("""
            CREATE TABLE diagnosis_results (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_name VARCHAR(100),
                mbti_type VARCHAR(4) NOT NULL,
                e_score INT NOT NULL,
                i_score INT NOT NULL,
                s_score INT NOT NULL,
                n_score INT NOT NULL,
                t_score INT NOT NULL,
                f_score INT NOT NULL,
                j_score INT NOT NULL,
                p_score INT NOT NULL,
                diagnosed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_ip VARCHAR(45)
            )
        """)
        
        # answersテーブル作成
        cursor.execute("""
            CREATE TABLE answers (
                id INT AUTO_INCREMENT PRIMARY KEY,
                result_id INT NOT NULL,
                question_id INT NOT NULL,
                answer_value INT NOT NULL,
                FOREIGN KEY (result_id) REFERENCES diagnosis_results(id),
                FOREIGN KEY (question_id) REFERENCES questions(id)
            )
        """)
        
        # サンプル質問データを投入
        questions_data = [
            ('人と会うことでエネルギーが湧いてくる', 'EI', 1),
            ('一人でじっくり考える時間が必要だ', 'EI', -1),
            ('初対面の人とも気軽に話せる', 'EI', 1),
            ('現実的で具体的な情報を重視する', 'SN', 1),
            ('抽象的な概念やアイデアに興味がある', 'SN', -1),
            ('細かいディテールに気づきやすい', 'SN', 1),
            ('論理的な分析を重視して判断する', 'TF', 1),
            ('人の気持ちを考えて行動する', 'TF', -1),
            ('客観的な事実を感情より優先する', 'TF', 1),
            ('計画を立てて物事を進めるのが好きだ', 'JP', 1),
            ('柔軟に対応できる自由さが重要だ', 'JP', -1),
            ('締め切りを守ることを優先する', 'JP', 1)
        ]
        
        for question in questions_data:
            cursor.execute(
                "INSERT INTO questions (question_text, axis, weight) VALUES (%s, %s, %s)",
                question
            )
        
        conn.commit()
        print("データベースの初期化が完了しました")
        print(f"- questionsテーブル: {len(questions_data)}件のデータを投入")
        print("- diagnosis_resultsテーブル作成完了")
        print("- answersテーブル作成完了")
        
        cursor.close()
        conn.close()
        
    except MySQLdb.Error as e:
        print(f"エラーが発生しました: {e}")
        return False
    
    return True

if __name__ == '__main__':
    print("データベース初期化スクリプトを開始します...")
    
    if wait_for_db():
        init_database()
    else:
        print("データベースへの接続に失敗しました")


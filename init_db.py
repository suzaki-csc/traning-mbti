from app import app, db, QUESTIONS
from models.models import Question
import time

def wait_for_db(max_retries=30):
    """データベースの起動を待機"""
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            with app.app_context():
                db.engine.connect()
            print("データベース接続成功")
            return True
        except Exception as e:
            retry_count += 1
            print(f"データベース接続待機中... ({retry_count}/{max_retries}): {e}")
            time.sleep(2)
    
    return False

def init_database():
    """データベースの初期化"""
    try:
        with app.app_context():
            # テーブルを作成（既存の場合は削除して再作成）
            db.drop_all()
            db.create_all()
            
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
            
            for question_text, axis, weight in questions_data:
                question = Question(
                    question_text=question_text,
                    axis=axis,
                    weight=weight
                )
                db.session.add(question)
            
            db.session.commit()
            
            print("データベースの初期化が完了しました")
            print(f"- questionsテーブル: {len(questions_data)}件のデータを投入")
            print("- diagnosis_resultsテーブル作成完了")
            print("- answersテーブル作成完了")
            
            return True
            
    except Exception as e:
        print(f"エラーが発生しました: {e}")
        return False

if __name__ == '__main__':
    print("データベース初期化スクリプトを開始します...")
    
    if wait_for_db():
        init_database()
    else:
        print("データベースへの接続に失敗しました")

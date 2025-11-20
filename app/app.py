"""
クイズアプリケーション メインファイル
FlaskアプリケーションのルーティングとAPIエンドポイントを定義
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
import random
import os
import sys
from pathlib import Path

# appディレクトリをパスに追加
app_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(app_dir))

from config import config
from models import db, Category, Question

# Flaskアプリケーションの初期化
# テンプレートと静的ファイルのパスを設定
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')

# 環境に応じた設定を読み込み
env = os.environ.get('FLASK_ENV', 'development')
app.config.from_object(config[env])

# データベースの初期化
db.init_app(app)

# アプリケーションコンテキスト内でデータベーステーブルを作成
def init_database():
    """データベースを初期化する関数"""
    import time
    max_retries = 30
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            with app.app_context():
                # データベース接続をテスト
                db.session.execute(db.text("SELECT 1"))
                print("データベース接続に成功しました。")
                
                # テーブルが存在しない場合は作成
                db.create_all()
                print("データベーステーブルを作成しました。")
                
                # 作成されたテーブルを確認
                from sqlalchemy import inspect
                inspector = inspect(db.engine)
                tables = inspector.get_table_names()
                print(f"作成されたテーブル: {tables}")
                
                # カテゴリが存在しない場合は初期データを登録
                if Category.query.count() == 0:
                    try:
                        # app.app_context()内で実行されるため、dbとCategory, Questionを渡す
                        from app.data.init_questions import init_security_questions, init_it_basics_questions, init_programming_questions
                        print("初期データを登録します...")
                        # 明示的にdb, Category, Questionを渡す
                        init_security_questions(db, Category, Question)
                        init_it_basics_questions(db, Category, Question)
                        init_programming_questions(db, Category, Question)
                        print("初期データの登録が完了しました。")
                    except Exception as e:
                        print(f"初期データの登録中にエラーが発生しました: {e}")
                        import traceback
                        traceback.print_exc()
                else:
                    print(f"既存のデータベースを使用します（カテゴリ数: {Category.query.count()}）")
                return  # 成功したらループを抜ける
        except Exception as e:
            retry_count += 1
            if retry_count < max_retries:
                print(f"データベース接続に失敗しました（{retry_count}/{max_retries}）。5秒後に再試行します...")
                print(f"エラー: {e}")
                time.sleep(5)
            else:
                print(f"データベース接続に失敗しました（最大試行回数に達しました）: {e}")
                import traceback
                traceback.print_exc()
                raise

# アプリケーション起動時にデータベースを初期化
init_database()

# ============================================================================
# ルーティング: ページ表示
# ============================================================================

@app.route('/')
def index():
    """
    トップページを表示
    利用可能なカテゴリ一覧を取得して表示
    """
    categories = Category.query.all()
    return render_template('index.html', categories=categories)

@app.route('/category/<int:category_id>')
def select_category(category_id):
    """
    選択されたカテゴリのクイズを開始
    
    Args:
        category_id: カテゴリID
    
    Returns:
        クイズ画面またはエラーページ
    """
    category = Category.query.get_or_404(category_id)
    
    # カテゴリに属する全問題を取得
    all_questions = Question.query.filter_by(category_id=category_id).all()
    
    # 問題数の確認
    if len(all_questions) == 0:
        return render_template('error.html', 
                             message='この問題カテゴリには問題が登録されていません。')
    
    # ランダムに10問選択（重複を許可）
    if len(all_questions) <= 10:
        # 10問以下の場合は重複を許可して10問にする
        selected_questions = random.choices(all_questions, k=10)
    else:
        # 10問以上の場合は重複なしで10問選択
        selected_questions = random.sample(all_questions, 10)
    
    # 順番をシャッフル
    random.shuffle(selected_questions)
    
    # セッションに問題IDリストを保存
    session['question_ids'] = [q.id for q in selected_questions]
    session['current_index'] = 0
    session['score'] = 0
    session['wrong_questions'] = []
    session['category_id'] = category_id
    
    return render_template('quiz.html', 
                         category=category,
                         total_questions=len(selected_questions))

@app.route('/result')
def show_result():
    """
    クイズ終了後の結果を表示
    スコアと間違えた問題の一覧を表示
    """
    score = session.get('score', 0)
    question_ids = session.get('question_ids', [])
    wrong_question_ids = session.get('wrong_questions', [])
    category_id = session.get('category_id')
    
    if not category_id:
        return redirect(url_for('index'))
    
    category = Category.query.get(category_id)
    if not category:
        return redirect(url_for('index'))
    
    total = len(question_ids)
    percentage = int((score / total) * 100) if total > 0 else 0
    
    # 間違えた問題の詳細を取得
    wrong_questions = Question.query.filter(
        Question.id.in_(wrong_question_ids)
    ).all() if wrong_question_ids else []
    
    # スコア共有用テキスト生成
    share_text = f"クイズ「{category.name}」の結果: {score}/{total}問正解 ({percentage}%) #クイズアプリ"
    
    return render_template('result.html',
                         category=category,
                         score=score,
                         total=total,
                         percentage=percentage,
                         wrong_questions=wrong_questions,
                         share_text=share_text)

@app.route('/review')
def review_mode():
    """
    間違えた問題のみを復習するモード
    """
    wrong_question_ids = session.get('wrong_questions', [])
    
    if not wrong_question_ids:
        return render_template('error.html', 
                             message='復習する問題がありません。')
    
    # 復習用セッションを設定
    random.shuffle(wrong_question_ids)
    session['question_ids'] = wrong_question_ids
    session['current_index'] = 0
    session['score'] = 0
    session['is_review_mode'] = True
    
    category_id = session.get('category_id')
    category = Category.query.get(category_id)
    
    return render_template('quiz.html',
                         category=category,
                         total_questions=len(wrong_question_ids),
                         is_review=True)

# ============================================================================
# APIエンドポイント
# ============================================================================

@app.route('/api/question/current')
def get_current_question():
    """
    現在の問題を取得するAPI
    
    Returns:
        JSON: 問題データ（問題文、選択肢）
    """
    question_ids = session.get('question_ids', [])
    current_index = session.get('current_index', 0)
    
    if current_index >= len(question_ids):
        return jsonify({'finished': True})
    
    question_id = question_ids[current_index]
    question = Question.query.get(question_id)
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    return jsonify({
        'finished': False,
        'question_number': current_index + 1,
        'total': len(question_ids),
        'question_text': question.question_text,
        'options': {
            'A': question.option_a,
            'B': question.option_b,
            'C': question.option_c,
            'D': question.option_d
        }
    })

@app.route('/api/question/answer', methods=['POST'])
def submit_answer():
    """
    ユーザーの回答を受け取り、正誤判定を行う
    
    Request Body:
        answer: 選択された回答（A, B, C, D）
    
    Returns:
        JSON: 正誤結果と解説
    """
    data = request.get_json()
    user_answer = data.get('answer', '').upper()
    
    question_ids = session.get('question_ids', [])
    current_index = session.get('current_index', 0)
    
    if current_index >= len(question_ids):
        return jsonify({'error': 'Invalid question index'}), 400
    
    question_id = question_ids[current_index]
    question = Question.query.get(question_id)
    
    if not question:
        return jsonify({'error': 'Question not found'}), 404
    
    # 正誤判定
    is_correct = (user_answer == question.correct_answer)
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    else:
        # 間違えた問題を記録
        wrong_questions = session.get('wrong_questions', [])
        if question_id not in wrong_questions:
            wrong_questions.append(question_id)
        session['wrong_questions'] = wrong_questions
    
    # 次の問題へ
    session['current_index'] = current_index + 1
    
    return jsonify({
        'correct': is_correct,
        'correct_answer': question.correct_answer,
        'explanation': question.explanation,
        'score': session.get('score', 0)
    })

# ============================================================================
# エラーハンドリング
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """404エラーハンドラー"""
    return render_template('error.html', message='ページが見つかりません。'), 404

@app.errorhandler(500)
def internal_error(error):
    """500エラーハンドラー"""
    db.session.rollback()
    return render_template('error.html', message='サーバーエラーが発生しました。'), 500

# ============================================================================
# アプリケーション起動
# ============================================================================

if __name__ == '__main__':
    # 開発環境でのみ直接実行可能
    app.run(debug=True, host='0.0.0.0', port=5000)


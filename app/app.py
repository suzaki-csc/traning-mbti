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
from models import db, Category, Question, User, QuizSession

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
                
                # デフォルト管理者が存在しない場合は作成
                if User.query.filter_by(user_id='admin@example.com').first() is None:
                    admin_user = User(
                        user_id='admin@example.com',
                        email='admin@example.com',
                        role='admin'
                    )
                    admin_user.set_password('admin123')
                    db.session.add(admin_user)
                    db.session.commit()
                    print("デフォルト管理者を作成しました（ID: admin@example.com, password: admin123）")
                else:
                    print("デフォルト管理者は既に存在します")
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
# 認証・認可ヘルパー関数
# ============================================================================

def login_required(f):
    """ログイン必須デコレータ"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    """管理者必須デコレータ"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        user = User.query.filter_by(user_id=session['user_id']).first()
        if not user or not user.is_admin():
            return render_template('error.html', message='管理者権限が必要です。'), 403
        return f(*args, **kwargs)
    return decorated_function

# ============================================================================
# ルーティング: 認証関連
# ============================================================================

@app.route('/login', methods=['GET', 'POST'])
def login():
    """ログインページ"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        password = request.form.get('password', '')
        
        if not user_id or not password:
            return render_template('login.html', 
                                 error='ユーザIDとパスワードを入力してください。')
        
        user = User.query.filter_by(user_id=user_id).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.user_id
            session['user_role'] = user.role
            session['user_email'] = user.email
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            return render_template('login.html', 
                                 error='ユーザIDまたはパスワードが正しくありません。')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """ログアウト"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    """ユーザ登録ページ"""
    if request.method == 'POST':
        user_id = request.form.get('user_id', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '')
        password_confirm = request.form.get('password_confirm', '')
        
        # バリデーション
        if not user_id or not email or not password:
            return render_template('register.html', 
                                 error='すべての項目を入力してください。')
        
        if password != password_confirm:
            return render_template('register.html', 
                                 error='パスワードが一致しません。')
        
        if len(password) < 6:
            return render_template('register.html', 
                                 error='パスワードは6文字以上で入力してください。')
        
        # 既存ユーザのチェック
        if User.query.filter_by(user_id=user_id).first():
            return render_template('register.html', 
                                 error='このユーザIDは既に使用されています。')
        
        if User.query.filter_by(email=email).first():
            return render_template('register.html', 
                                 error='このメールアドレスは既に使用されています。')
        
        # ユーザ作成
        try:
            new_user = User(
                user_id=user_id,
                email=email,
                role='user'
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            
            # 自動ログイン
            session['user_id'] = new_user.user_id
            session['user_role'] = new_user.role
            session['user_email'] = new_user.email
            
            return redirect(url_for('index'))
        except Exception as e:
            db.session.rollback()
            return render_template('register.html', 
                                 error=f'ユーザ登録に失敗しました: {str(e)}')
    
    return render_template('register.html')

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
    
    # ログインしている場合はクイズセッションを保存
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter_by(user_id=user_id).first()
        if user:
            quiz_session = QuizSession(
                user_id=user.id,
                category_id=category_id,
                score=score,
                total_questions=total
            )
            db.session.add(quiz_session)
            db.session.commit()
    
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
# ルーティング: ユーザー機能
# ============================================================================

@app.route('/my/history')
@login_required
def my_history():
    """自分の診断履歴を表示"""
    user_id = session.get('user_id')
    user = User.query.filter_by(user_id=user_id).first()
    
    if not user:
        return redirect(url_for('login'))
    
    # 自分のクイズセッション履歴を取得
    quiz_sessions = QuizSession.query.filter_by(user_id=user.id).order_by(QuizSession.completed_at.desc()).all()
    
    return render_template('my_history.html', quiz_sessions=quiz_sessions, user=user)

# ============================================================================
# ルーティング: 管理者機能
# ============================================================================

@app.route('/admin')
@admin_required
def admin_index():
    """管理者トップページ"""
    return render_template('admin/index.html')

@app.route('/admin/users')
@admin_required
def admin_users():
    """ユーザ一覧"""
    users = User.query.order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/users/<int:user_id>')
@admin_required
def admin_user_detail(user_id):
    """ユーザ詳細"""
    user = User.query.get_or_404(user_id)
    quiz_sessions = QuizSession.query.filter_by(user_id=user_id).order_by(QuizSession.completed_at.desc()).all()
    return render_template('admin/user_detail.html', user=user, quiz_sessions=quiz_sessions)

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_user_edit(user_id):
    """ユーザ情報・ロールの変更"""
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.user_id = request.form.get('user_id', user.user_id).strip()
        user.email = request.form.get('email', user.email).strip()
        user.role = request.form.get('role', user.role)
        
        # パスワードが入力されている場合は変更
        new_password = request.form.get('password', '').strip()
        if new_password:
            if len(new_password) < 6:
                return render_template('admin/user_edit.html', 
                                     user=user,
                                     error='パスワードは6文字以上で入力してください。')
            user.set_password(new_password)
        
        try:
            db.session.commit()
            return redirect(url_for('admin_user_detail', user_id=user.id))
        except Exception as e:
            db.session.rollback()
            return render_template('admin/user_edit.html', 
                                 user=user,
                                 error=f'更新に失敗しました: {str(e)}')
    
    return render_template('admin/user_edit.html', user=user)

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_user_delete(user_id):
    """ユーザ削除"""
    user = User.query.get_or_404(user_id)
    
    # 自分自身は削除できない
    if user.user_id == session.get('user_id'):
        return render_template('error.html', message='自分自身を削除することはできません。'), 400
    
    try:
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('admin_users'))
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=f'削除に失敗しました: {str(e)}'), 500

@app.route('/admin/history')
@admin_required
def admin_history():
    """全ユーザの診断履歴"""
    quiz_sessions = QuizSession.query.order_by(QuizSession.completed_at.desc()).all()
    return render_template('admin/history.html', quiz_sessions=quiz_sessions)

@app.route('/admin/categories')
@admin_required
def admin_categories():
    """カテゴリ管理"""
    categories = Category.query.order_by(Category.created_at.desc()).all()
    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/categories/new', methods=['GET', 'POST'])
@admin_required
def admin_category_new():
    """カテゴリ作成"""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        description = request.form.get('description', '').strip()
        
        if not name:
            return render_template('admin/category_edit.html', 
                                 error='カテゴリ名を入力してください。')
        
        try:
            category = Category(name=name, description=description)
            db.session.add(category)
            db.session.commit()
            return redirect(url_for('admin_categories'))
        except Exception as e:
            db.session.rollback()
            return render_template('admin/category_edit.html', 
                                 error=f'作成に失敗しました: {str(e)}')
    
    return render_template('admin/category_edit.html')

@app.route('/admin/categories/<int:category_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_category_edit(category_id):
    """カテゴリ修正"""
    category = Category.query.get_or_404(category_id)
    
    if request.method == 'POST':
        category.name = request.form.get('name', category.name).strip()
        category.description = request.form.get('description', category.description).strip()
        
        if not category.name:
            return render_template('admin/category_edit.html', 
                                 category=category,
                                 error='カテゴリ名を入力してください。')
        
        try:
            db.session.commit()
            return redirect(url_for('admin_categories'))
        except Exception as e:
            db.session.rollback()
            return render_template('admin/category_edit.html', 
                                 category=category,
                                 error=f'更新に失敗しました: {str(e)}')
    
    return render_template('admin/category_edit.html', category=category)

@app.route('/admin/categories/<int:category_id>/delete', methods=['POST'])
@admin_required
def admin_category_delete(category_id):
    """カテゴリ削除"""
    category = Category.query.get_or_404(category_id)
    
    try:
        db.session.delete(category)
        db.session.commit()
        return redirect(url_for('admin_categories'))
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=f'削除に失敗しました: {str(e)}'), 500

@app.route('/admin/questions')
@admin_required
def admin_questions():
    """クイズ管理"""
    category_id = request.args.get('category_id', type=int)
    if category_id:
        questions = Question.query.filter_by(category_id=category_id).order_by(Question.created_at.desc()).all()
    else:
        questions = Question.query.order_by(Question.created_at.desc()).all()
    
    categories = Category.query.all()
    return render_template('admin/questions.html', 
                         questions=questions, 
                         categories=categories,
                         selected_category_id=category_id)

@app.route('/admin/questions/new', methods=['GET', 'POST'])
@admin_required
def admin_question_new():
    """クイズ作成"""
    categories = Category.query.all()
    
    if request.method == 'POST':
        category_id = request.form.get('category_id', type=int)
        question_text = request.form.get('question_text', '').strip()
        option_a = request.form.get('option_a', '').strip()
        option_b = request.form.get('option_b', '').strip()
        option_c = request.form.get('option_c', '').strip()
        option_d = request.form.get('option_d', '').strip()
        correct_answer = request.form.get('correct_answer', '').upper()
        explanation = request.form.get('explanation', '').strip()
        
        if not all([category_id, question_text, option_a, option_b, option_c, option_d, correct_answer, explanation]):
            return render_template('admin/question_edit.html', 
                                 categories=categories,
                                 error='すべての項目を入力してください。')
        
        if correct_answer not in ['A', 'B', 'C', 'D']:
            return render_template('admin/question_edit.html', 
                                 categories=categories,
                                 error='正解はA, B, C, Dのいずれかを選択してください。')
        
        try:
            question = Question(
                category_id=category_id,
                question_text=question_text,
                option_a=option_a,
                option_b=option_b,
                option_c=option_c,
                option_d=option_d,
                correct_answer=correct_answer,
                explanation=explanation
            )
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('admin_questions'))
        except Exception as e:
            db.session.rollback()
            return render_template('admin/question_edit.html', 
                                 categories=categories,
                                 error=f'作成に失敗しました: {str(e)}')
    
    return render_template('admin/question_edit.html', categories=categories)

@app.route('/admin/questions/<int:question_id>/edit', methods=['GET', 'POST'])
@admin_required
def admin_question_edit(question_id):
    """クイズ修正"""
    question = Question.query.get_or_404(question_id)
    categories = Category.query.all()
    
    if request.method == 'POST':
        question.category_id = request.form.get('category_id', type=int) or question.category_id
        question.question_text = request.form.get('question_text', question.question_text).strip()
        question.option_a = request.form.get('option_a', question.option_a).strip()
        question.option_b = request.form.get('option_b', question.option_b).strip()
        question.option_c = request.form.get('option_c', question.option_c).strip()
        question.option_d = request.form.get('option_d', question.option_d).strip()
        question.correct_answer = request.form.get('correct_answer', question.correct_answer).upper()
        question.explanation = request.form.get('explanation', question.explanation).strip()
        
        if not all([question.category_id, question.question_text, question.option_a, 
                   question.option_b, question.option_c, question.option_d, 
                   question.correct_answer, question.explanation]):
            return render_template('admin/question_edit.html', 
                                 question=question,
                                 categories=categories,
                                 error='すべての項目を入力してください。')
        
        if question.correct_answer not in ['A', 'B', 'C', 'D']:
            return render_template('admin/question_edit.html', 
                                 question=question,
                                 categories=categories,
                                 error='正解はA, B, C, Dのいずれかを選択してください。')
        
        try:
            db.session.commit()
            return redirect(url_for('admin_questions'))
        except Exception as e:
            db.session.rollback()
            return render_template('admin/question_edit.html', 
                                 question=question,
                                 categories=categories,
                                 error=f'更新に失敗しました: {str(e)}')
    
    return render_template('admin/question_edit.html', question=question, categories=categories)

@app.route('/admin/questions/<int:question_id>/delete', methods=['POST'])
@admin_required
def admin_question_delete(question_id):
    """クイズ削除"""
    question = Question.query.get_or_404(question_id)
    
    try:
        db.session.delete(question)
        db.session.commit()
        return redirect(url_for('admin_questions'))
    except Exception as e:
        db.session.rollback()
        return render_template('error.html', message=f'削除に失敗しました: {str(e)}'), 500

# ============================================================================
# アプリケーション起動
# ============================================================================

if __name__ == '__main__':
    # 開発環境でのみ直接実行可能
    app.run(debug=True, host='0.0.0.0', port=5000)


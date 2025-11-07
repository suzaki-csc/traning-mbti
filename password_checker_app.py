"""
パスワード強度チェッカー - Flaskアプリケーション

このアプリケーションは、ユーザーが入力したパスワードの強度を
リアルタイムで評価し、セキュリティ向上のためのアドバイスを提供します。

データベース機能:
- パスワードチェック結果の保存（ハッシュ値とマスク表示）
- チェック履歴の表示
"""

import os
from flask import Flask, render_template, request, jsonify
from models import db, PasswordCheck

# Flaskアプリケーションのインスタンスを作成
app = Flask(__name__)

# データベース設定
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'password_checker')
DB_USER = os.getenv('DB_USER', 'appuser')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'apppassword')

# SQLAlchemy設定
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': 280,
    'pool_pre_ping': True,
}

# データベース初期化
db.init_app(app)


@app.route('/')
def index():
    """
    メインページを表示するルート
    
    ルートURL（/）にアクセスされた場合、
    パスワード強度チェッカーのHTMLページを返します。
    """
    return render_template('password_checker.html')


@app.route('/health')
def health():
    """
    ヘルスチェック用のエンドポイント
    
    アプリケーションとデータベースが正常に動作しているか確認するためのAPI
    """
    try:
        # データベース接続確認
        db.session.execute(db.text('SELECT 1'))
        return jsonify({
            'status': 'ok',
            'message': 'Password Checker App is running',
            'database': 'connected'
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': 'Database connection failed',
            'error': str(e)
        }), 500


@app.route('/api/save-check', methods=['POST'])
def save_check():
    """
    パスワードチェック結果を保存するAPI
    
    Request Body (JSON):
    {
        "password": "元のパスワード",
        "score": 75,
        "strength_level": "strong",
        "entropy": 52.4,
        "crack_time": "約1,425年",
        "has_lowercase": true,
        "has_uppercase": true,
        "has_digit": true,
        "has_symbol": true,
        "has_common_word": false,
        "has_repeating": false,
        "has_sequential": false,
        "has_keyboard_pattern": false
    }
    
    Returns:
        JSON: 保存結果
    """
    try:
        data = request.get_json()
        
        # 必須パラメータの確認
        if not data or 'password' not in data:
            return jsonify({
                'success': False,
                'message': 'パスワードが指定されていません'
            }), 400
        
        password = data['password']
        
        # パスワードチェック結果をデータベースに保存
        check = PasswordCheck(
            password_hash=PasswordCheck.hash_password(password),
            password_masked=PasswordCheck.mask_password(password),
            score=data.get('score', 0),
            strength_level=data.get('strength_level', 'unknown'),
            entropy=data.get('entropy', 0.0),
            crack_time=data.get('crack_time', '不明'),
            has_lowercase=data.get('has_lowercase', False),
            has_uppercase=data.get('has_uppercase', False),
            has_digit=data.get('has_digit', False),
            has_symbol=data.get('has_symbol', False),
            has_common_word=data.get('has_common_word', False),
            has_repeating=data.get('has_repeating', False),
            has_sequential=data.get('has_sequential', False),
            has_keyboard_pattern=data.get('has_keyboard_pattern', False),
            password_length=len(password)
        )
        
        db.session.add(check)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'チェック結果を保存しました',
            'id': check.id,
            'password_masked': check.password_masked
        })
        
    except Exception as e:
        db.session.rollback()
        app.logger.error(f'Error saving check result: {str(e)}')
        return jsonify({
            'success': False,
            'message': 'チェック結果の保存に失敗しました',
            'error': str(e)
        }), 500


@app.route('/api/history')
def get_history():
    """
    パスワードチェック履歴を取得するAPI
    
    Query Parameters:
        limit (int): 取得件数（デフォルト: 10、最大: 100）
        offset (int): オフセット（デフォルト: 0）
    
    Returns:
        JSON: チェック履歴のリスト
    """
    try:
        # クエリパラメータの取得
        limit = min(int(request.args.get('limit', 10)), 100)
        offset = int(request.args.get('offset', 0))
        
        # データベースから履歴を取得（新しい順）
        checks = PasswordCheck.query.order_by(
            PasswordCheck.created_at.desc()
        ).limit(limit).offset(offset).all()
        
        # 総件数を取得
        total = PasswordCheck.query.count()
        
        return jsonify({
            'success': True,
            'total': total,
            'limit': limit,
            'offset': offset,
            'data': [check.to_dict() for check in checks]
        })
        
    except Exception as e:
        app.logger.error(f'Error getting history: {str(e)}')
        return jsonify({
            'success': False,
            'message': '履歴の取得に失敗しました',
            'error': str(e)
        }), 500


@app.route('/api/stats')
def get_stats():
    """
    パスワードチェック統計情報を取得するAPI
    
    Returns:
        JSON: 統計情報
    """
    try:
        # 総チェック数
        total_checks = PasswordCheck.query.count()
        
        # 強度レベル別の集計
        from sqlalchemy import func
        strength_stats = db.session.query(
            PasswordCheck.strength_level,
            func.count(PasswordCheck.id).label('count')
        ).group_by(PasswordCheck.strength_level).all()
        
        # 平均スコア
        avg_score = db.session.query(
            func.avg(PasswordCheck.score)
        ).scalar() or 0
        
        # 平均パスワード長
        avg_length = db.session.query(
            func.avg(PasswordCheck.password_length)
        ).scalar() or 0
        
        # パターン検出統計
        pattern_stats = {
            'common_word': PasswordCheck.query.filter_by(has_common_word=True).count(),
            'repeating': PasswordCheck.query.filter_by(has_repeating=True).count(),
            'sequential': PasswordCheck.query.filter_by(has_sequential=True).count(),
            'keyboard_pattern': PasswordCheck.query.filter_by(has_keyboard_pattern=True).count(),
        }
        
        return jsonify({
            'success': True,
            'total_checks': total_checks,
            'avg_score': round(avg_score, 2),
            'avg_length': round(avg_length, 2),
            'strength_distribution': {level: count for level, count in strength_stats},
            'pattern_stats': pattern_stats
        })
        
    except Exception as e:
        app.logger.error(f'Error getting stats: {str(e)}')
        return jsonify({
            'success': False,
            'message': '統計情報の取得に失敗しました',
            'error': str(e)
        }), 500


@app.cli.command('init-db')
def init_db():
    """
    データベースを初期化するコマンド
    
    使用方法:
        flask init-db
    """
    db.create_all()
    print('データベースを初期化しました')


@app.cli.command('drop-db')
def drop_db():
    """
    データベースを削除するコマンド
    
    使用方法:
        flask drop-db
    """
    db.drop_all()
    print('データベースを削除しました')


if __name__ == '__main__':
    """
    アプリケーションのエントリーポイント
    
    このスクリプトを直接実行した場合、開発用サーバーを起動します。
    debug=True: コード変更時に自動リロード、詳細なエラー表示
    host='0.0.0.0': すべてのネットワークインターフェースでリッスン
    port=5000: ポート5000で起動
    """
    with app.app_context():
        # データベーステーブルを自動作成
        db.create_all()
        print("データベーステーブルを作成/確認しました")
    
    print("=" * 60)
    print("パスワード強度チェッカーを起動中...")
    print("アクセスURL: http://localhost:5000")
    print("停止: Ctrl+C")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

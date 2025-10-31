# MBTI風性格診断Webアプリ 設計書

## 1. プロジェクト概要

### 目的
学習目的のMBTI風性格診断Webアプリケーション（脆弱性を含む実装）

### 技術スタック
- **バックエンド**: Python 3.11+、Flask 2.3+
- **データベース**: MySQL 8.0
- **フロントエンド**: Bootstrap 5.3、Jinja2テンプレート
- **インフラ**: Docker、Docker Compose

---

## 2. システム構成

### 2.1 コンテナ構成

```
traning-mbti/
├── app/                    # Flaskアプリケーション
│   ├── app.py             # メインアプリケーション
│   ├── models.py          # データモデル
│   ├── config.py          # 設定ファイル
│   ├── requirements.txt   # Python依存関係
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   └── js/
│   │       └── app.js
│   └── templates/
│       ├── base.html      # ベーステンプレート
│       ├── index.html     # トップページ
│       ├── diagnosis.html # 診断ページ
│       ├── result.html    # 結果ページ
│       └── admin.html     # 管理画面
├── db/
│   └── init.sql           # DB初期化スクリプト
├── Dockerfile             # アプリ用Dockerfile
├── docker-compose.yml     # Docker Compose設定
└── README.md
```

### 2.2 Docker Compose構成

```yaml
version: '3.8'

services:
  app:
    build: .
    container_name: mbti_app
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=development
      - DB_HOST=db
      - DB_USER=mbti_user
      - DB_PASSWORD=mbti_pass
      - DB_NAME=mbti_db
    depends_on:
      - db
    volumes:
      - ./app:/app
    command: python app.py

  db:
    image: mysql:8.0
    container_name: mbti_db
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=mbti_db
      - MYSQL_USER=mbti_user
      - MYSQL_PASSWORD=mbti_pass
    ports:
      - "3306:3306"
    volumes:
      - ./db:/docker-entrypoint-initdb.d
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

---

## 3. データベース設計

### 3.1 テーブル構成

#### questions テーブル
質問データを格納

| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT PRIMARY KEY AUTO_INCREMENT | 質問ID |
| question_text | TEXT | 質問文 |
| axis | VARCHAR(10) | 診断軸 (E/I, S/N, T/F, J/P) |
| direction | VARCHAR(10) | スコア方向 (positive/negative) |
| order_num | INT | 表示順序 |

#### diagnosis_results テーブル
診断結果を保存

| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT PRIMARY KEY AUTO_INCREMENT | 結果ID |
| user_name | VARCHAR(255) | ユーザー名 |
| mbti_type | VARCHAR(4) | MBTIタイプ (例: ENFP) |
| e_score | INT | E軸スコア |
| i_score | INT | I軸スコア |
| s_score | INT | S軸スコア |
| n_score | INT | N軸スコア |
| t_score | INT | T軸スコア |
| f_score | INT | F軸スコア |
| j_score | INT | J軸スコア |
| p_score | INT | P軸スコア |
| created_at | DATETIME | 診断日時 |

#### answers テーブル
回答履歴を保存

| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT PRIMARY KEY AUTO_INCREMENT | 回答ID |
| result_id | INT FOREIGN KEY | 診断結果ID |
| question_id | INT FOREIGN KEY | 質問ID |
| answer_value | INT | 回答値 (1-5) |

### 3.2 初期データ（質問セット）

```sql
-- 12問の質問例（各軸3問ずつ）

-- E/I軸の質問
INSERT INTO questions (question_text, axis, direction, order_num) VALUES
('パーティーや集まりでエネルギーを得ますか？', 'E', 'positive', 1),
('一人で過ごす時間が必要ですか？', 'I', 'positive', 2),
('初対面の人とすぐに打ち解けられますか？', 'E', 'positive', 3),

-- S/N軸の質問
('具体的な事実やデータを重視しますか？', 'S', 'positive', 4),
('可能性や未来のビジョンに興味がありますか？', 'N', 'positive', 5),
('実践的で現実的な解決策を好みますか？', 'S', 'positive', 6),

-- T/F軸の質問
('論理的な分析を重視しますか？', 'T', 'positive', 7),
('他者の感情を考慮して判断しますか？', 'F', 'positive', 8),
('客観的な基準で物事を判断しますか？', 'T', 'positive', 9),

-- J/P軸の質問
('計画的に物事を進めますか？', 'J', 'positive', 10),
('柔軟に対応することを好みますか？', 'P', 'positive', 11),
('締め切り前にタスクを完了させますか？', 'J', 'positive', 12);
```

---

## 4. アプリケーション設計

### 4.1 ルーティング構成

| パス | メソッド | 説明 | 脆弱性 |
|------|---------|------|--------|
| `/` | GET | トップページ | - |
| `/diagnosis` | GET | 診断開始ページ（質問表示） | - |
| `/diagnosis` | POST | 回答送信・結果表示 | XSS（ユーザー名） |
| `/result/<result_id>` | GET | 過去の診断結果表示 | SQL Injection |
| `/admin` | GET | 管理画面（診断履歴一覧） | SQL Injection |
| `/admin/search` | GET | 診断履歴検索 | SQL Injection |

### 4.2 データ構造

#### 質問データ構造（Python）

```python
# 質問オブジェクト
Question = {
    'id': int,
    'question_text': str,
    'axis': str,  # 'E', 'I', 'S', 'N', 'T', 'F', 'J', 'P'
    'direction': str,  # 'positive', 'negative'
    'order_num': int
}

# 回答データ構造
Answer = {
    'question_id': int,
    'answer_value': int  # 1-5のスケール
}

# 診断結果データ構造
DiagnosisResult = {
    'id': int,
    'user_name': str,
    'mbti_type': str,  # 'ENFP', 'ISTJ'など
    'scores': {
        'E': int, 'I': int,
        'S': int, 'N': int,
        'T': int, 'F': int,
        'J': int, 'P': int
    },
    'created_at': datetime
}
```

---

## 5. 採点ロジック

### 5.1 スコア計算方式

```
1. 各質問の回答値（1-5）を収集
   - 1: 全くそう思わない
   - 2: あまりそう思わない
   - 3: どちらでもない
   - 4: ややそう思う
   - 5: とてもそう思う

2. 各軸ごとにスコアを集計
   - 質問のaxis（E/I/S/N/T/F/J/P）に基づいて分類
   - directionが'positive'の場合: スコア = answer_value
   - directionが'negative'の場合: スコア = 6 - answer_value

3. 各軸ペアでの判定
   - E vs I: E_score > I_score → 'E', それ以外 → 'I'
   - S vs N: S_score > N_score → 'S', それ以外 → 'N'
   - T vs F: T_score > F_score → 'T', それ以外 → 'F'
   - J vs P: J_score > P_score → 'J', それ以外 → 'P'

4. 4文字のMBTIタイプを生成
   例: E + N + F + P = "ENFP"
```

### 5.2 採点ロジック実装例（疑似コード）

```python
def calculate_mbti_type(answers):
    """
    回答からMBTIタイプを判定
    
    Args:
        answers: [{'question_id': int, 'answer_value': int}, ...]
    
    Returns:
        dict: {
            'mbti_type': str,
            'scores': dict
        }
    """
    scores = {
        'E': 0, 'I': 0,
        'S': 0, 'N': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }
    
    # 各回答を集計
    for answer in answers:
        question = get_question_by_id(answer['question_id'])
        axis = question['axis']
        value = answer['answer_value']
        
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
```

---

## 6. UI設計（Bootstrap）

### 6.1 画面構成

#### トップページ（index.html）
- ヒーローセクション（診断の説明）
- 「診断を始める」ボタン
- 過去の診断結果へのリンク

#### 診断ページ（diagnosis.html）
- 質問表示エリア
  - 質問番号（1/12、2/12...）
  - 質問文
  - 5段階ラジオボタン
- 「次へ」/「結果を見る」ボタン
- プログレスバー

#### 結果ページ（result.html）
- MBTIタイプ表示（大きく）
- 各軸のスコアグラフ（Bootstrap Progress）
- タイプの説明文
- 「もう一度診断する」ボタン

#### 管理画面（admin.html）
- 診断履歴テーブル
  - ID、ユーザー名、MBTIタイプ、診断日時
- 検索フォーム（ユーザー名、MBTIタイプ）
- ページネーション

### 6.2 レスポンシブ対応
- モバイル（< 768px）: 1カラム
- タブレット（768px - 992px）: 1カラム
- デスクトップ（> 992px）: センタリング、最大幅800px

---

## 7. 脆弱性の実装（学習目的）

### 7.1 XSS（Cross-Site Scripting）

**診断結果ページでのユーザー名表示**

```python
# app.py - 脆弱な実装例
@app.route('/diagnosis', methods=['POST'])
def submit_diagnosis():
    user_name = request.form.get('user_name')
    # エスケープせずにそのまま表示（脆弱）
    return render_template('result.html', user_name=user_name)
```

```html
<!-- result.html - 脆弱な実装例 -->
<h2>{{ user_name | safe }}さんの診断結果</h2>
<!-- {{ user_name }}のみでもautoescapeがfalseの場合脆弱 -->
```

**攻撃例**: `<script>alert('XSS')</script>` をユーザー名に入力

### 7.2 SQL Injection

**管理画面での検索機能**

```python
# app.py - 脆弱な実装例
@app.route('/admin/search')
def search_results():
    search_name = request.args.get('name', '')
    
    # SQLインジェクション脆弱性
    query = f"SELECT * FROM diagnosis_results WHERE user_name LIKE '%{search_name}%'"
    cursor.execute(query)
    results = cursor.fetchall()
    
    return render_template('admin.html', results=results)
```

**攻撃例**: `' OR '1'='1` を検索欄に入力してすべてのデータを取得

**結果IDでの個別表示**

```python
# app.py - 脆弱な実装例
@app.route('/result/<result_id>')
def show_result(result_id):
    query = f"SELECT * FROM diagnosis_results WHERE id = {result_id}"
    cursor.execute(query)
    result = cursor.fetchone()
    
    return render_template('result.html', result=result)
```

**攻撃例**: `/result/1 OR 1=1` でクエリを操作

---

## 8. 実装の手順

### Step 1: Dockerコンテナのセットアップ
1. Dockerfileの作成
2. docker-compose.ymlの作成
3. `docker-compose up -d` で起動確認

### Step 2: データベースの初期化
1. init.sqlの作成（テーブル作成SQL）
2. 質問データの投入
3. DB接続確認

### Step 3: Flaskアプリケーションの実装
1. 基本的なFlaskアプリの構築
2. データベース接続（mysqlclient or PyMySQL）
3. ルーティングの実装

### Step 4: フロントエンドの実装
1. Bootstrapテンプレートの作成
2. 質問表示UIの実装
3. 結果表示UIの実装
4. 管理画面UIの実装

### Step 5: 脆弱性の実装
1. XSSの実装（エスケープ処理の除去）
2. SQLインジェクションの実装（プレースホルダーの不使用）

### Step 6: テストと検証
1. 正常系の動作確認
2. 脆弱性の検証
3. 学習教材としての説明資料作成

---

## 9. セキュリティ対策（学習後の修正案）

### 9.1 XSS対策

```python
# 修正例
from markupsafe import escape

@app.route('/diagnosis', methods=['POST'])
def submit_diagnosis():
    user_name = escape(request.form.get('user_name'))
    return render_template('result.html', user_name=user_name)
```

```html
<!-- Jinja2デフォルトのautoescapeを有効化 -->
<h2>{{ user_name }}さんの診断結果</h2>
```

### 9.2 SQL Injection対策

```python
# 修正例（プレースホルダー使用）
@app.route('/admin/search')
def search_results():
    search_name = request.args.get('name', '')
    
    query = "SELECT * FROM diagnosis_results WHERE user_name LIKE %s"
    cursor.execute(query, (f'%{search_name}%',))
    results = cursor.fetchall()
    
    return render_template('admin.html', results=results)
```

---

## 10. 拡張機能の提案

### 10.1 追加機能案
- ユーザー認証機能
- SNSシェア機能
- 診断結果のPDF出力
- MBTIタイプごとの統計データ表示
- 相性診断機能

### 10.2 性能改善案
- キャッシュの導入（Redis）
- セッション管理の改善
- データベースインデックスの最適化

---

## 11. 参考資料

### 11.1 技術ドキュメント
- Flask公式ドキュメント: https://flask.palletsprojects.com/
- Bootstrap公式ドキュメント: https://getbootstrap.com/
- MySQL公式ドキュメント: https://dev.mysql.com/doc/

### 11.2 セキュリティ学習資料
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- SQLインジェクション解説
- XSS（Cross-Site Scripting）解説

---

## 付録A: コードスニペット集

### A.1 Flask設定ファイル（config.py）

```python
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    
    # データベース設定
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_USER = os.environ.get('DB_USER', 'mbti_user')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'mbti_pass')
    DB_NAME = os.environ.get('DB_NAME', 'mbti_db')
    
    # その他設定
    DEBUG = True
```

### A.2 MBTIタイプ説明辞書

```python
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
```

---

以上


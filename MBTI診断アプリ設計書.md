# MBTI風性格診断Webアプリ設計書

## 1. システム概要

FlaskとMySQLを使用したMBTI風性格診断Webアプリケーション。  
Dockerコンテナ構成で、診断機能と管理機能を提供します。

## 2. ファイル構成

```
traning-mbti/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── app.py
├── config.py
├── init_db.py
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── diagnosis.html
│   ├── result.html
│   └── admin/
│       ├── login.html
│       └── dashboard.html
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
└── models/
    ├── __init__.py
    └── database.py
```

## 3. Docker構成

### 3.1 docker-compose.yml

```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=development
      - DB_HOST=db
      - DB_PORT=3306
      - DB_USER=mbti_user
      - DB_PASSWORD=mbti_password
      - DB_NAME=mbti_db
    depends_on:
      - db
    volumes:
      - .:/app
    command: python app.py

  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=mbti_db
      - MYSQL_USER=mbti_user
      - MYSQL_PASSWORD=mbti_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

### 3.2 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["python", "app.py"]
```

### 3.3 requirements.txt

```
Flask==3.0.0
Flask-MySQLdb==2.0.0
mysqlclient==2.2.0
python-dotenv==1.0.0
```

## 4. データベース設計

### 4.1 テーブル構成

#### questionsテーブル
診断質問を管理

```sql
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    axis VARCHAR(10) NOT NULL,
    weight INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT | 質問ID（主キー） |
| question_text | TEXT | 質問文 |
| axis | VARCHAR(10) | 診断軸（E/I、S/N、T/F、J/P） |
| weight | INT | 重み（正の値: 前者寄り、負の値: 後者寄り） |
| created_at | TIMESTAMP | 作成日時 |

#### diagnosis_resultsテーブル
診断結果を記録

```sql
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
);
```

| カラム名 | 型 | 説明 |
|---------|-----|------|
| id | INT | 診断ID（主キー） |
| user_name | VARCHAR(100) | ユーザー名（任意） |
| mbti_type | VARCHAR(4) | 診断結果タイプ（例：INTJ） |
| e_score ~ p_score | INT | 各軸のスコア |
| diagnosed_at | TIMESTAMP | 診断日時 |
| user_ip | VARCHAR(45) | ユーザーIP |

#### answersテーブル
回答履歴を保存

```sql
CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    result_id INT NOT NULL,
    question_id INT NOT NULL,
    answer_value INT NOT NULL,
    FOREIGN KEY (result_id) REFERENCES diagnosis_results(id),
    FOREIGN KEY (question_id) REFERENCES questions(id)
);
```

## 5. 質問データ構造

### 5.1 質問配列の例（12問）

```python
QUESTIONS = [
    # E/I軸（外向-内向）
    {
        'id': 1,
        'text': '人と会うことでエネルギーが湧いてくる',
        'axis': 'EI',
        'options': [
            {'value': 5, 'label': 'とてもそう思う'},
            {'value': 3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': -3, 'label': 'あまりそう思わない'},
            {'value': -5, 'label': '全くそう思わない'}
        ]
    },
    {
        'id': 2,
        'text': '一人でじっくり考える時間が必要だ',
        'axis': 'EI',
        'options': [
            {'value': -5, 'label': 'とてもそう思う'},
            {'value': -3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': 3, 'label': 'あまりそう思わない'},
            {'value': 5, 'label': '全くそう思わない'}
        ]
    },
    {
        'id': 3,
        'text': '初対面の人とも気軽に話せる',
        'axis': 'EI',
        'options': [
            {'value': 5, 'label': 'とてもそう思う'},
            {'value': 3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': -3, 'label': 'あまりそう思わない'},
            {'value': -5, 'label': '全くそう思わない'}
        ]
    },
    
    # S/N軸（感覚-直感）
    {
        'id': 4,
        'text': '現実的で具体的な情報を重視する',
        'axis': 'SN',
        'options': [
            {'value': 5, 'label': 'とてもそう思う'},
            {'value': 3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': -3, 'label': 'あまりそう思わない'},
            {'value': -5, 'label': '全くそう思わない'}
        ]
    },
    {
        'id': 5,
        'text': '抽象的な概念やアイデアに興味がある',
        'axis': 'SN',
        'options': [
            {'value': -5, 'label': 'とてもそう思う'},
            {'value': -3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': 3, 'label': 'あまりそう思わない'},
            {'value': 5, 'label': '全くそう思わない'}
        ]
    },
    {
        'id': 6,
        'text': '細かいディテールに気づきやすい',
        'axis': 'SN',
        'options': [
            {'value': 5, 'label': 'とてもそう思う'},
            {'value': 3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': -3, 'label': 'あまりそう思わない'},
            {'value': -5, 'label': '全くそう思わない'}
        ]
    },
    
    # T/F軸（思考-感情）
    {
        'id': 7,
        'text': '論理的な分析を重視して判断する',
        'axis': 'TF',
        'options': [
            {'value': 5, 'label': 'とてもそう思う'},
            {'value': 3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': -3, 'label': 'あまりそう思わない'},
            {'value': -5, 'label': '全くそう思わない'}
        ]
    },
    {
        'id': 8,
        'text': '人の気持ちを考えて行動する',
        'axis': 'TF',
        'options': [
            {'value': -5, 'label': 'とてもそう思う'},
            {'value': -3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': 3, 'label': 'あまりそう思わない'},
            {'value': 5, 'label': '全くそう思わない'}
        ]
    },
    {
        'id': 9,
        'text': '客観的な事実を感情より優先する',
        'axis': 'TF',
        'options': [
            {'value': 5, 'label': 'とてもそう思う'},
            {'value': 3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': -3, 'label': 'あまりそう思わない'},
            {'value': -5, 'label': '全くそう思わない'}
        ]
    },
    
    # J/P軸（判断-知覚）
    {
        'id': 10,
        'text': '計画を立てて物事を進めるのが好きだ',
        'axis': 'JP',
        'options': [
            {'value': 5, 'label': 'とてもそう思う'},
            {'value': 3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': -3, 'label': 'あまりそう思わない'},
            {'value': -5, 'label': '全くそう思わない'}
        ]
    },
    {
        'id': 11,
        'text': '柔軟に対応できる自由さが重要だ',
        'axis': 'JP',
        'options': [
            {'value': -5, 'label': 'とてもそう思う'},
            {'value': -3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': 3, 'label': 'あまりそう思わない'},
            {'value': 5, 'label': '全くそう思わない'}
        ]
    },
    {
        'id': 12,
        'text': '締め切りを守ることを優先する',
        'axis': 'JP',
        'options': [
            {'value': 5, 'label': 'とてもそう思う'},
            {'value': 3, 'label': 'ややそう思う'},
            {'value': 1, 'label': 'どちらでもない'},
            {'value': -3, 'label': 'あまりそう思わない'},
            {'value': -5, 'label': '全くそう思わない'}
        ]
    }
]
```

### 5.2 軸マッピング

```python
AXIS_MAPPING = {
    'EI': ['E', 'I'],  # 外向-内向
    'SN': ['S', 'N'],  # 感覚-直感
    'TF': ['T', 'F'],  # 思考-感情
    'JP': ['J', 'P']   # 判断-知覚
}
```

## 6. ルーティング設計

### 6.1 ユーザー向け機能

| URL | メソッド | 説明 | テンプレート |
|-----|---------|------|-------------|
| `/` | GET | トップページ | index.html |
| `/diagnosis` | GET | 診断ページ | diagnosis.html |
| `/submit` | POST | 回答送信・採点処理 | - |
| `/result/<int:id>` | GET | 結果表示 | result.html |

### 6.2 管理機能

| URL | メソッド | 説明 | テンプレート |
|-----|---------|------|-------------|
| `/admin/login` | GET/POST | 管理者ログイン | admin/login.html |
| `/admin/dashboard` | GET | 診断履歴一覧 | admin/dashboard.html |
| `/admin/result/<int:id>` | GET | 個別診断詳細 | admin/detail.html |
| `/admin/export` | GET | CSV出力 | - |
| `/admin/logout` | GET | ログアウト | - |

## 7. 採点ロジック

### 7.1 スコア計算アルゴリズム

```python
def calculate_mbti_type(answers):
    """
    回答から MBTI タイプを判定
    
    Args:
        answers: dict - {question_id: answer_value} の形式
    
    Returns:
        dict - {
            'type': 'INTJ',
            'scores': {'E': 10, 'I': 20, 'S': 15, 'N': 15, ...}
        }
    """
    # 各軸のスコアを初期化
    scores = {
        'E': 0, 'I': 0,
        'S': 0, 'N': 0,
        'T': 0, 'F': 0,
        'J': 0, 'P': 0
    }
    
    # 質問ごとに回答値を集計
    for question in QUESTIONS:
        question_id = question['id']
        axis = question['axis']
        answer_value = answers.get(question_id, 0)
        
        # 正の値: 軸の前者にポイント、負の値: 軸の後者にポイント
        if answer_value > 0:
            scores[axis[0]] += answer_value
        elif answer_value < 0:
            scores[axis[1]] += abs(answer_value)
    
    # 各軸で優勢な方を選択
    mbti_type = ''
    mbti_type += 'E' if scores['E'] >= scores['I'] else 'I'
    mbti_type += 'S' if scores['S'] >= scores['N'] else 'N'
    mbti_type += 'T' if scores['T'] >= scores['F'] else 'F'
    mbti_type += 'J' if scores['J'] >= scores['P'] else 'P'
    
    return {
        'type': mbti_type,
        'scores': scores
    }
```

### 7.2 判定例

#### 回答例
```python
answers = {
    1: 5,   # E+5
    2: -3,  # I+3
    3: 3,   # E+3
    4: 5,   # S+5
    5: -5,  # N+5
    6: 1,   # S+1
    7: 5,   # T+5
    8: -1,  # F+1
    9: 3,   # T+3
    10: 5,  # J+5
    11: -3, # P+3
    12: 3   # J+3
}
```

#### スコア計算結果
```
E: 8点 vs I: 3点 → E判定
S: 6点 vs N: 5点 → S判定
T: 8点 vs F: 1点 → T判定
J: 8点 vs P: 3点 → J判定

結果: ESTJ
```

## 8. UI設計（Bootstrap使用）

### 8.1 カラースキーム

```css
:root {
    --primary-color: #4A90E2;
    --secondary-color: #7B68EE;
    --success-color: #50C878;
    --background-color: #F8F9FA;
    --text-color: #333333;
}
```

### 8.2 レイアウト構成

#### トップページ（index.html）
- ヘッダー: タイトルとナビゲーション
- メインセクション: 診断の説明
- CTAボタン: 「診断を始める」

#### 診断ページ（diagnosis.html）
- プログレスバー: 進捗表示
- 質問カード: 1問ずつ表示または全問表示
- 選択肢: ラジオボタンまたはスライダー
- ナビゲーションボタン: 「次へ」「戻る」「送信」

#### 結果ページ（result.html）
- MBTIタイプ表示（大きく）
- 各軸のスコアグラフ
- タイプの説明
- SNS共有ボタン

#### 管理画面（admin/dashboard.html）
- 検索・フィルター機能
- 診断履歴テーブル
  - 診断日時
  - ユーザー名
  - MBTIタイプ
  - 詳細リンク
- ページネーション
- CSV出力ボタン

## 9. セキュリティ考慮事項

### 9.1 入力検証
- 回答値のバリデーション
- SQLインジェクション対策
- XSS対策

### 9.2 管理画面
- セッション管理
- ログイン認証
- CSRF対策

### 9.3 データベース
- プリペアドステートメント使用
- パスワードハッシュ化

## 10. 実装手順

### Step 1: 環境構築
1. Docker環境の準備
2. docker-compose.yml作成
3. Dockerfile作成
4. requirements.txt作成

### Step 2: データベース設計
1. テーブル定義
2. init_db.pyスクリプト作成
3. サンプルデータ投入

### Step 3: Flaskアプリケーション実装
1. app.py（メインアプリケーション）
2. config.py（設定管理）
3. models/database.py（DB操作）

### Step 4: テンプレート作成
1. base.html（共通レイアウト）
2. ユーザー向けページ
3. 管理画面

### Step 5: スタイリング
1. Bootstrap統合
2. カスタムCSS作成
3. レスポンシブ対応

### Step 6: 動作確認
1. 診断フロー確認
2. 採点ロジック検証
3. 管理画面動作確認

### Step 7: デプロイ準備
1. Docker コンテナビルド
2. docker-compose起動確認
3. データ永続化確認

## 11. 機能拡張案

- チャート形式での結果表示（Chart.js使用）
- 過去の診断結果比較機能
- 診断結果のPDF出力
- 複数言語対応
- APIエンドポイント提供
- ソーシャルログイン
- 質問のランダム化
- 診断結果の統計情報表示

## 12. パフォーマンス最適化

- データベースインデックス作成
- クエリキャッシング
- 静的ファイルの圧縮
- CDN使用（Bootstrap等）
- コネクションプーリング

## 13. まとめ

本設計書では、FlaskとMySQLを使用したMBTI風性格診断Webアプリの全体像を示しました。
Docker Composeによるコンテナ構成で、開発環境の構築が容易になっています。
BootstrapによるシンプルなUIと、管理機能による診断履歴の確認が可能な設計となっています。


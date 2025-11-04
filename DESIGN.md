# MBTI風性格診断Webアプリケーション 設計書

## 1. システム概要

MBTI（Myers-Briggs Type Indicator）風の性格診断を行うWebアプリケーションです。
10〜12問の質問に回答することで、4つの軸（E/I, S/N, T/F, J/P）のスコアを算出し、16タイプのいずれかを判定します。

### 主要機能
- 性格診断機能（質問表示 → 回答 → 結果表示）
- 診断履歴の保存
- 管理機能（診断履歴の確認）

## 2. 技術スタック

- **バックエンド**: Python 3.11+, Flask
- **フロントエンド**: HTML, Bootstrap 5
- **データベース**: MySQL 8.0
- **コンテナ**: Docker, Docker Compose
- **依存関係管理**: Poetry

## 3. ファイル構成

```
traning-mbti/
├── docker-compose.yml          # Docker Compose設定
├── Dockerfile                  # アプリコンテナのDockerfile
├── pyproject.toml             # Poetry依存関係管理
├── poetry.lock
├── .env                       # 環境変数（DB接続情報など）
├── app/
│   ├── __init__.py           # Flaskアプリ初期化
│   ├── config.py             # 設定ファイル
│   ├── models.py             # データベースモデル
│   ├── routes.py             # ルーティング定義
│   ├── quiz_data.py          # 質問データ定義
│   ├── scoring.py            # 採点ロジック
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css     # カスタムCSS
│   │   └── js/
│   │       └── quiz.js       # フロントエンドJS
│   └── templates/
│       ├── base.html         # ベーステンプレート
│       ├── index.html        # トップページ
│       ├── quiz.html         # 質問ページ
│       ├── result.html       # 結果ページ
│       └── admin/
│           └── history.html  # 診断履歴管理ページ
├── migrations/               # DBマイグレーション（Flask-Migrate）
├── tests/                    # テストコード
└── README.md
```

## 4. ルーティング設計

### 4.1 ユーザー向けルート

| メソッド | パス | 説明 | レスポンス |
|---------|------|------|-----------|
| GET | `/` | トップページ | HTML |
| GET | `/quiz` | 診断開始ページ | HTML（質問1） |
| POST | `/quiz` | 回答送信・次の質問表示 | HTML（次の質問 or 結果） |
| GET | `/result/<session_id>` | 診断結果表示 | HTML |

### 4.2 管理者向けルート

| メソッド | パス | 説明 | レスポンス |
|---------|------|------|-----------|
| GET | `/admin` | 管理トップページ | HTML |
| GET | `/admin/history` | 診断履歴一覧 | HTML |
| GET | `/admin/history/<id>` | 診断履歴詳細 | JSON |
| DELETE | `/admin/history/<id>` | 診断履歴削除 | JSON |

## 5. データ構造

### 5.1 質問データ（quiz_data.py）

```python
QUESTIONS = [
    {
        "id": 1,
        "text": "パーティーや集まりで、あなたはどちらのタイプですか？",
        "options": [
            {"text": "多くの人と話すのが楽しい", "axis": "E", "score": 2},
            {"text": "少数の人と深く話すのが好き", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 2,
        "text": "新しい情報を得るとき、何を重視しますか？",
        "options": [
            {"text": "具体的な事実やデータ", "axis": "S", "score": 2},
            {"text": "全体的なパターンや可能性", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 3,
        "text": "決断をするとき、何を優先しますか？",
        "options": [
            {"text": "論理的な分析と客観性", "axis": "T", "score": 2},
            {"text": "人々への影響と調和", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 4,
        "text": "日常生活で、どちらの方が心地よいですか？",
        "options": [
            {"text": "計画を立てて実行する", "axis": "J", "score": 2},
            {"text": "柔軟に対応する", "axis": "P", "score": 2}
        ]
    },
    {
        "id": 5,
        "text": "週末の過ごし方として、どちらが魅力的ですか？",
        "options": [
            {"text": "友人と外出してアクティブに過ごす", "axis": "E", "score": 2},
            {"text": "家でゆっくりと趣味に没頭する", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 6,
        "text": "仕事や勉強で、どちらのアプローチが得意ですか？",
        "options": [
            {"text": "細部に注目して正確に進める", "axis": "S", "score": 2},
            {"text": "全体像を把握して創造的に進める", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 7,
        "text": "対立や問題が起きたとき、どう対処しますか？",
        "options": [
            {"text": "事実を基に論理的に解決する", "axis": "T", "score": 2},
            {"text": "感情を考慮して調和を図る", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 8,
        "text": "旅行の計画について、どちらのスタイルですか？",
        "options": [
            {"text": "事前に詳細に計画を立てる", "axis": "J", "score": 2},
            {"text": "その場の状況に応じて決める", "axis": "P", "score": 2}
        ]
    },
    {
        "id": 9,
        "text": "エネルギーを充電するには？",
        "options": [
            {"text": "人と話したり、外に出たりする", "axis": "E", "score": 2},
            {"text": "一人の時間を持つ", "axis": "I", "score": 2}
        ]
    },
    {
        "id": 10,
        "text": "新しいスキルを学ぶとき、どちらが好きですか？",
        "options": [
            {"text": "実践的な手順を学ぶ", "axis": "S", "score": 2},
            {"text": "理論や概念を理解する", "axis": "N", "score": 2}
        ]
    },
    {
        "id": 11,
        "text": "他人を評価するとき、何を重視しますか？",
        "options": [
            {"text": "能力と成果", "axis": "T", "score": 2},
            {"text": "人柄と誠実さ", "axis": "F", "score": 2}
        ]
    },
    {
        "id": 12,
        "text": "プロジェクトに取り組むとき、どちらが好きですか？",
        "options": [
            {"text": "締め切りを設定して計画的に進める", "axis": "J", "score": 2},
            {"text": "柔軟に方向性を変えながら進める", "axis": "P", "score": 2}
        ]
    }
]

# MBTIタイプの説明
MBTI_TYPES = {
    "INTJ": {
        "name": "建築家",
        "description": "戦略的な思考力を持ち、独立心が強く、完璧主義的な傾向があります。長期的なビジョンを持ち、それを実現するために計画的に行動します。"
    },
    "INTP": {
        "name": "論理学者",
        "description": "分析的で創造的な思考を持ち、理論や抽象的な概念に興味を示します。独立心が強く、自分のペースで物事を進めることを好みます。"
    },
    "ENTJ": {
        "name": "指揮官",
        "description": "リーダーシップに優れ、目標志向で決断力があります。効率性を重視し、組織やプロジェクトを成功に導く能力を持っています。"
    },
    "ENTP": {
        "name": "討論者",
        "description": "知的好奇心が旺盛で、議論や討論を楽しみます。創造的で柔軟な思考を持ち、新しいアイデアを生み出すことが得意です。"
    },
    "INFJ": {
        "name": "提唱者",
        "description": "理想主義的で、深い洞察力を持ちます。人々を助けることに情熱を持ち、長期的なビジョンに基づいて行動します。"
    },
    "INFP": {
        "name": "仲介者",
        "description": "理想主義的で創造的、価値観を大切にします。調和を重視し、自分の信念に基づいて行動することを好みます。"
    },
    "ENFJ": {
        "name": "主人公",
        "description": "カリスマ性があり、人々を鼓舞し導く能力を持ちます。共感力が高く、他者の成長を支援することに喜びを感じます。"
    },
    "ENFP": {
        "name": "広報運動家",
        "description": "熱意があり、創造的で社交的です。新しい可能性を探求することを楽しみ、人々を励まし、つなげることが得意です。"
    },
    "ISTJ": {
        "name": "管理者",
        "description": "責任感が強く、信頼性があります。伝統や規則を尊重し、実用的で組織的なアプローチを好みます。"
    },
    "ISFJ": {
        "name": "擁護者",
        "description": "思いやりがあり、献身的です。他者のニーズに敏感で、安定した環境を作ることを大切にします。"
    },
    "ESTJ": {
        "name": "幹部",
        "description": "組織的で決断力があり、リーダーシップを発揮します。伝統や秩序を重視し、効率的に物事を管理する能力があります。"
    },
    "ESFJ": {
        "name": "領事官",
        "description": "社交的で協調性があり、他者を支援することに喜びを感じます。調和を重視し、コミュニティの一員として貢献します。"
    },
    "ISTP": {
        "name": "巨匠",
        "description": "実用的で論理的、問題解決能力に優れています。手を動かして学ぶことを好み、柔軟に対応する能力があります。"
    },
    "ISFP": {
        "name": "冒険家",
        "description": "芸術的で柔軟、現在を楽しむことを大切にします。調和を重視し、自分の価値観に従って生きることを好みます。"
    },
    "ESTP": {
        "name": "起業家",
        "description": "エネルギッシュで行動的、リスクを恐れません。現実的で柔軟性があり、即座に問題を解決する能力があります。"
    },
    "ESFP": {
        "name": "エンターテイナー",
        "description": "社交的で楽観的、人々を楽しませることが得意です。現在を楽しみ、周囲の人々に喜びをもたらします。"
    }
}
```

### 5.2 軸とスコアリング

4つの軸（ディメンション）:
- **E/I**: 外向型（Extraversion）/ 内向型（Introversion）
- **S/N**: 感覚型（Sensing）/ 直観型（iNtuition）
- **T/F**: 思考型（Thinking）/ 感情型（Feeling）
- **J/P**: 判断型（Judging）/ 知覚型（Perceiving）

各質問の選択肢には、該当する軸とスコア（通常は2点）が設定されています。

## 6. 採点ロジック（scoring.py）

### 6.1 スコア計算アルゴリズム

```python
def calculate_scores(answers):
    """
    回答からMBTIスコアを計算
    
    Args:
        answers: list of dict
            [{"question_id": 1, "axis": "E", "score": 2}, ...]
    
    Returns:
        dict: {"E": 6, "I": 0, "S": 4, "N": 2, ...}
    """
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    for answer in answers:
        axis = answer["axis"]
        score = answer["score"]
        scores[axis] += score
    
    return scores

def determine_type(scores):
    """
    スコアからMBTIタイプを判定
    
    Args:
        scores: dict {"E": 6, "I": 0, ...}
    
    Returns:
        str: MBTIタイプ（例: "INTJ"）
    """
    mbti_type = ""
    
    # E vs I
    mbti_type += "E" if scores["E"] >= scores["I"] else "I"
    
    # S vs N
    mbti_type += "S" if scores["S"] >= scores["N"] else "N"
    
    # T vs F
    mbti_type += "T" if scores["T"] >= scores["F"] else "T"
    
    # J vs P
    mbti_type += "J" if scores["J"] >= scores["P"] else "P"
    
    return mbti_type

def get_score_percentages(scores):
    """
    各軸のスコアをパーセンテージに変換
    
    Returns:
        dict: {"E/I": {"E": 75, "I": 25}, ...}
    """
    percentages = {}
    
    axes = [("E", "I"), ("S", "N"), ("T", "F"), ("J", "P")]
    
    for axis1, axis2 in axes:
        total = scores[axis1] + scores[axis2]
        if total > 0:
            percentages[f"{axis1}/{axis2}"] = {
                axis1: round((scores[axis1] / total) * 100),
                axis2: round((scores[axis2] / total) * 100)
            }
        else:
            percentages[f"{axis1}/{axis2}"] = {axis1: 50, axis2: 50}
    
    return percentages
```

### 6.2 判定ロジック

1. 各質問の回答から、対応する軸にスコアを加算
2. 4つの軸それぞれで、高いスコアの文字を採用
3. 4文字を組み合わせてMBTIタイプを決定（例: INTJ）
4. スコア同点の場合は、最初の文字を採用（E, S, T, J）

## 7. データベース設計

### 7.1 テーブル定義

#### diagnosis_sessions テーブル
診断セッション情報を保存

| カラム名 | 型 | 制約 | 説明 |
|---------|---|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | セッションID |
| session_id | VARCHAR(36) | UNIQUE, NOT NULL | UUID |
| mbti_type | VARCHAR(4) | NOT NULL | 診断結果（例: INTJ） |
| scores_json | JSON | NOT NULL | スコア詳細（JSON） |
| created_at | DATETIME | NOT NULL | 診断実施日時 |
| ip_address | VARCHAR(45) | NULL | IPアドレス（任意） |

#### diagnosis_answers テーブル
各質問の回答を保存

| カラム名 | 型 | 制約 | 説明 |
|---------|---|------|------|
| id | INT | PRIMARY KEY, AUTO_INCREMENT | 回答ID |
| session_id | INT | FOREIGN KEY | セッションID |
| question_id | INT | NOT NULL | 質問番号 |
| axis | VARCHAR(1) | NOT NULL | 選択された軸（E, I, S...） |
| score | INT | NOT NULL | スコア値 |
| answer_text | TEXT | NOT NULL | 選択した回答テキスト |
| created_at | DATETIME | NOT NULL | 回答日時 |

### 7.2 ER図

```
diagnosis_sessions (1) ----< (N) diagnosis_answers
```

### 7.3 SQLAlchemyモデル（models.py）

```python
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class DiagnosisSession(db.Model):
    __tablename__ = 'diagnosis_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), unique=True, nullable=False)
    mbti_type = db.Column(db.String(4), nullable=False)
    scores_json = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    ip_address = db.Column(db.String(45), nullable=True)
    
    # リレーション
    answers = db.relationship('DiagnosisAnswer', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'session_id': self.session_id,
            'mbti_type': self.mbti_type,
            'scores': self.scores_json,
            'created_at': self.created_at.isoformat(),
            'ip_address': self.ip_address
        }

class DiagnosisAnswer(db.Model):
    __tablename__ = 'diagnosis_answers'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('diagnosis_sessions.id'), nullable=False)
    question_id = db.Column(db.Integer, nullable=False)
    axis = db.Column(db.String(1), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    answer_text = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'axis': self.axis,
            'score': self.score,
            'answer_text': self.answer_text,
            'created_at': self.created_at.isoformat()
        }
```

## 8. Docker構成

### 8.1 docker-compose.yml

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: mbti_app
    ports:
      - "5000:5000"
    environment:
      - FLASK_APP=app
      - FLASK_ENV=development
      - DATABASE_URL=mysql+pymysql://mbti_user:mbti_password@db:3306/mbti_db
    depends_on:
      - db
    volumes:
      - .:/app
    networks:
      - mbti_network
    command: flask run --host=0.0.0.0

  db:
    image: mysql:8.0
    container_name: mbti_db
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=mbti_db
      - MYSQL_USER=mbti_user
      - MYSQL_PASSWORD=mbti_password
    ports:
      - "3306:3306"
    volumes:
      - mysql_data:/var/lib/mysql
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    networks:
      - mbti_network

networks:
  mbti_network:
    driver: bridge

volumes:
  mysql_data:
```

### 8.2 Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Poetryのインストール
RUN pip install poetry

# 依存関係ファイルのコピー
COPY pyproject.toml poetry.lock ./

# 依存関係のインストール（仮想環境を作らない）
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

# アプリケーションコードのコピー
COPY . .

# ポート公開
EXPOSE 5000

# 起動コマンド
CMD ["flask", "run", "--host=0.0.0.0"]
```

### 8.3 .env（環境変数）

```env
# Flask設定
FLASK_APP=app
FLASK_ENV=development
SECRET_KEY=your-secret-key-here-change-in-production

# データベース設定
DATABASE_URL=mysql+pymysql://mbti_user:mbti_password@db:3306/mbti_db

# MySQL設定
MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=mbti_db
MYSQL_USER=mbti_user
MYSQL_PASSWORD=mbti_password
```

### 8.4 init.sql（DB初期化スクリプト）

```sql
-- 文字コード設定
ALTER DATABASE mbti_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- テーブルが存在する場合は削除
DROP TABLE IF EXISTS diagnosis_answers;
DROP TABLE IF EXISTS diagnosis_sessions;

-- diagnosis_sessionsテーブル作成
CREATE TABLE diagnosis_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) UNIQUE NOT NULL,
    mbti_type VARCHAR(4) NOT NULL,
    scores_json JSON NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL,
    INDEX idx_created_at (created_at),
    INDEX idx_mbti_type (mbti_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- diagnosis_answersテーブル作成
CREATE TABLE diagnosis_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    question_id INT NOT NULL,
    axis VARCHAR(1) NOT NULL,
    score INT NOT NULL,
    answer_text TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES diagnosis_sessions(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_question_id (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

## 9. UI設計（Bootstrap）

### 9.1 レイアウト構成

全ページ共通のベーステンプレート（base.html）を使用し、Bootstrapのコンポーネントを活用します。

#### 共通要素
- ナビゲーションバー（トップ固定）
- フッター
- レスポンシブデザイン（モバイル対応）

### 9.2 各ページの構成

#### トップページ（index.html）
- タイトル: "MBTI性格診断"
- 説明文: 診断の概要
- "診断を始める"ボタン（大きく目立つ）
- Bootstrap Card コンポーネント使用

#### 質問ページ（quiz.html）
- 進捗バー（Bootstrap Progress Bar）
  - 例: "質問 3 / 12"
- 質問テキスト（大きく見やすく）
- 選択肢（Bootstrap Button Group または Card）
- "次へ"ボタン
- シンプルで直感的なデザイン

#### 結果ページ（result.html）
- MBTIタイプ表示（大きく）
- タイプ名と説明（100字程度）
- 各軸のスコア表示（Bootstrap Progress Bar）
  - E/I: 75% / 25%
  - S/N: 40% / 60%
  - T/F: 60% / 40%
  - J/P: 80% / 20%
- "もう一度診断する"ボタン
- "結果をシェア"機能（オプション）

#### 管理ページ（admin/history.html）
- 診断履歴一覧（Bootstrap Table）
  - カラム: ID, 診断日時, MBTIタイプ, IPアドレス, 操作
- ページネーション
- 検索・フィルター機能
- 詳細表示モーダル（Bootstrap Modal）

### 9.3 カラースキーム

```css
:root {
    --primary-color: #4a90e2;
    --secondary-color: #f39c12;
    --success-color: #27ae60;
    --danger-color: #e74c3c;
    --light-bg: #f8f9fa;
    --dark-text: #2c3e50;
}
```

## 10. セッション管理

### 10.1 診断セッションフロー

1. ユーザーが診断開始
2. UUIDでセッションIDを生成
3. セッションにFlaskセッション or クッキーで保存
4. 各回答をセッションに保存
5. 全質問完了後、DBに保存してセッションクリア

### 10.2 Flask Session設定

```python
# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'  # またはRedis
    PERMANENT_SESSION_LIFETIME = 1800  # 30分
```

## 11. 依存パッケージ（pyproject.toml）

```toml
[tool.poetry]
name = "traning-mbti"
version = "0.1.0"
description = "MBTI personality test web application"
authors = ["Your Name <you@example.com>"]

[tool.poetry.dependencies]
python = "^3.11"
flask = "^3.0.0"
flask-sqlalchemy = "^3.1.1"
pymysql = "^1.1.0"
cryptography = "^41.0.7"
python-dotenv = "^1.0.0"
flask-migrate = "^4.0.5"

[tool.poetry.dev-dependencies]
pytest = "^7.4.3"
pytest-flask = "^1.3.0"
black = "^23.12.1"
flake8 = "^7.0.0"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## 12. セキュリティ考慮事項（教育目的）

> **注意**: このプロジェクトは教育目的です。以下のセキュリティ脆弱性が意図的に含まれる可能性があります。

### 12.1 想定される脆弱性

- SQLインジェクション
- XSS（クロスサイトスクリプティング）
- CSRF（クロスサイトリクエストフォージェリ）
- セッション管理の脆弱性

### 12.2 本番環境での対策（参考）

実際のサービスでは以下の対策が必要です：
- ORM（SQLAlchemy）の適切な使用
- テンプレートエンジンの自動エスケープ
- CSRF保護（Flask-WTF）
- セキュアなセッション管理
- HTTPS通信
- 入力バリデーション

## 13. 開発・起動手順

### 13.1 環境構築

```bash
# リポジトリクローン
git clone <repository-url>
cd traning-mbti

# Poetry環境構築
poetry install

# 環境変数設定
cp .env.example .env
# .envファイルを編集

# Docker起動
docker-compose up -d

# データベースマイグレーション
docker-compose exec app flask db upgrade
```

### 13.2 アプリケーション起動

```bash
# Dockerで起動
docker-compose up

# ブラウザでアクセス
# http://localhost:5000
```

### 13.3 開発時

```bash
# ログ確認
docker-compose logs -f app

# コンテナ内でコマンド実行
docker-compose exec app bash

# データベースリセット
docker-compose down -v
docker-compose up -d
```

## 14. テスト計画

### 14.1 単体テスト
- 採点ロジックのテスト
- MBTIタイプ判定のテスト
- データベースモデルのテスト

### 14.2 統合テスト
- ルーティングのテスト
- セッション管理のテスト
- データベース連携のテスト

### 14.3 E2Eテスト
- 診断フロー全体のテスト
- 管理機能のテスト

## 15. 今後の拡張案

### 15.1 機能拡張
- ユーザー登録・ログイン機能
- 診断結果の保存・比較機能
- 詳細な性格分析レポート
- SNSシェア機能
- 多言語対応

### 15.2 技術的改善
- Redis導入（セッション管理、キャッシング）
- REST API化
- フロントエンドフレームワーク導入（React/Vue.js）
- テストカバレッジ向上
- CI/CDパイプライン構築

## 16. 参考資料

- Flask公式ドキュメント: https://flask.palletsprojects.com/
- Bootstrap公式ドキュメント: https://getbootstrap.com/
- SQLAlchemy公式ドキュメント: https://www.sqlalchemy.org/
- Docker公式ドキュメント: https://docs.docker.com/
- MBTI理論について: https://www.16personalities.com/

---

**作成日**: 2025年11月4日  
**バージョン**: 1.0  
**ステータス**: 設計完了


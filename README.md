# MBTI性格診断Webアプリケーション

Flask、Bootstrap、Docker、MySQLを使用したMBTI風の性格診断Webアプリケーションです。

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Flask](https://img.shields.io/badge/flask-3.0+-green.svg)
![Docker](https://img.shields.io/badge/docker-compose-blue.svg)
![MySQL](https://img.shields.io/badge/mysql-8.0-orange.svg)

## 主な機能

### ユーザー機能
- 🔐 ユーザー登録・ログイン（セキュアな認証）
- 📝 MBTI診断の受診（12問の質問）
- 📊 診断結果の詳細表示（スコア、グラフ）
- 📅 診断履歴の確認

### 管理者機能
- 📈 管理ダッシュボード（統計情報）
- 👥 全ユーザーの診断履歴閲覧
- 🗑️ 診断結果の削除
- 📊 MBTIタイプ別の分布確認

## 技術スタック

- **バックエンド**: Flask 3.0+
- **フロントエンド**: Bootstrap 5.3、JavaScript
- **データベース**: MySQL 8.0
- **ORM**: SQLAlchemy
- **認証**: Flask-Login
- **コンテナ**: Docker、Docker Compose
- **パッケージ管理**: Poetry

## クイックスタート

### 前提条件

- Docker と Docker Compose がインストールされていること
- または Python 3.11+ と Poetry がインストールされていること

### Dockerを使用する場合（推奨）

```bash
# リポジトリをクローン
git clone <repository-url>
cd traning-mbti

# 環境変数ファイルを作成
cat > .env << EOF
SECRET_KEY=change-this-to-random-secret-key
MYSQL_ROOT_PASSWORD=root_password
MYSQL_PASSWORD=mbti_password
EOF

# Dockerコンテナをビルド・起動
docker-compose up -d --build

# ログを確認
docker-compose logs -f web
```

アプリケーションは http://localhost:5000 で利用可能になります。

### ローカル環境で実行する場合

詳細は [README_SETUP.md](./README_SETUP.md) を参照してください。

## 初期ログイン情報

### 管理者アカウント
- **ユーザー名**: `admin`
- **パスワード**: `admin123`

### テストユーザーアカウント
- **ユーザー名**: `testuser`
- **パスワード**: `user123`

> ⚠️ 本番環境では必ずパスワードを変更してください。

## プロジェクト構造

```
traning-mbti/
├── app/                        # アプリケーションコード
│   ├── __init__.py            # Flaskアプリの初期化
│   ├── config.py              # 設定ファイル
│   ├── models.py              # データベースモデル
│   ├── auth.py                # 認証ヘルパー
│   ├── routes/                # ルーティング
│   │   ├── main.py           # メイン機能（ログイン、トップページ等）
│   │   ├── quiz.py           # 診断機能
│   │   └── admin.py          # 管理機能
│   ├── templates/             # HTMLテンプレート（Jinja2）
│   │   ├── base.html         # ベーステンプレート
│   │   ├── login.html        # ログインページ
│   │   ├── register.html     # 登録ページ
│   │   ├── index.html        # トップページ
│   │   ├── quiz.html         # 診断ページ
│   │   ├── result.html       # 結果ページ
│   │   ├── history.html      # 履歴ページ
│   │   ├── admin/            # 管理者ページ
│   │   └── errors/           # エラーページ
│   ├── static/                # 静的ファイル
│   │   ├── css/style.css     # カスタムCSS
│   │   └── js/quiz.js        # カスタムJS
│   └── utils/                 # ユーティリティ
│       ├── questions.py      # 質問データ（12問）
│       └── scoring.py        # スコアリングロジック
├── mysql/                     # MySQL初期化スクリプト
│   └── init.sql              # データベース初期化SQL
├── docker-compose.yml         # Docker Compose設定
├── Dockerfile                 # Dockerイメージ定義
├── pyproject.toml            # Poetry依存関係管理
├── run.py                    # アプリケーション起動スクリプト
└── README.md                 # このファイル
```

## 使用方法

### 1. ユーザー登録
1. トップページの「新規登録」をクリック
2. ユーザー名、メールアドレス、パスワードを入力
3. 登録ボタンをクリック

### 2. 診断を受ける
1. ログイン後、「診断を開始する」ボタンをクリック
2. 12問の質問に回答
3. 結果ページで自分のMBTIタイプを確認

### 3. 診断履歴を見る
1. ナビゲーションバーの「履歴」をクリック
2. 過去の診断結果一覧を表示
3. 詳細を見たい結果をクリック

### 4. 管理機能（管理者のみ）
1. 管理者アカウントでログイン
2. ナビゲーションバーの「管理」メニューから各機能にアクセス
   - ダッシュボード: 統計情報とMBTIタイプ分布
   - 全履歴: すべてのユーザーの診断履歴

## MBTI 4軸の説明

診断では以下の4軸でスコアを計算します：

| 軸 | 説明 |
|---|------|
| **E/I** | 外向性（Extraversion）/ 内向性（Introversion）<br>エネルギーの方向性 |
| **S/N** | 感覚（Sensing）/ 直観（Intuition）<br>情報の受け取り方 |
| **T/F** | 思考（Thinking）/ 感情（Feeling）<br>意思決定の基準 |
| **J/P** | 判断（Judging）/ 知覚（Perceiving）<br>外界への接し方 |

## 16のMBTIタイプ

- **INTJ** - 建築家
- **INTP** - 論理学者
- **ENTJ** - 指揮官
- **ENTP** - 討論者
- **INFJ** - 提唱者
- **INFP** - 仲介者
- **ENFJ** - 主人公
- **ENFP** - 広報運動家
- **ISTJ** - 管理者
- **ISFJ** - 擁護者
- **ESTJ** - 幹部
- **ESFJ** - 領事官
- **ISTP** - 巨匠
- **ISFP** - 冒険家
- **ESTP** - 起業家
- **ESFP** - エンターテイナー

## データベース設計

### usersテーブル
- ユーザー情報（ID、ユーザー名、メール、パスワードハッシュ、権限）
- 認証に使用

### test_resultsテーブル
- 診断結果（ID、ユーザーID、MBTIタイプ、各軸のスコア、回答データ）
- 診断履歴の保存に使用

## 開発

### テストの実行

```bash
poetry run pytest
```

### コードスタイルチェック

```bash
poetry run flake8 app/
poetry run black app/
```

### データベースマイグレーション

```bash
# Flaskシェルを起動
poetry run flask shell

# テーブルの作成
>>> from app import create_app, db
>>> app = create_app()
>>> with app.app_context():
...     db.create_all()
```

## トラブルシューティング

### Dockerコンテナが起動しない

```bash
# ログを確認
docker-compose logs

# コンテナを再ビルド
docker-compose down -v
docker-compose up -d --build
```

### データベース接続エラー

1. MySQLコンテナが起動しているか確認
```bash
docker-compose ps
```

2. 環境変数を確認
```bash
cat .env
```

### ポート5000が既に使用されている

```bash
# docker-compose.ymlのポート番号を変更
ports:
  - "8000:5000"  # 5000 -> 8000に変更
```

## セキュリティ

本番環境で使用する場合は、以下を必ず実施してください：

- [ ] `SECRET_KEY` を強力なランダム文字列に変更
- [ ] データベースパスワードを複雑なものに変更
- [ ] `FLASK_ENV` を `production` に設定
- [ ] HTTPS を有効化
- [ ] 初期管理者アカウントのパスワードを変更
- [ ] CSRF保護が有効になっていることを確認
- [ ] SQLインジェクション対策が適用されていることを確認

## ライセンス

このプロジェクトは教育目的で作成されています。

## 貢献

バグ報告や機能要望は Issue で受け付けています。

## 作成者

- 作成日: 2024年
- Python + Flask + Docker を使用した MBTI 風性格診断アプリ

## 参考資料

- [Flask公式ドキュメント](https://flask.palletsprojects.com/)
- [Bootstrap公式ドキュメント](https://getbootstrap.com/)
- [Docker公式ドキュメント](https://docs.docker.com/)
- [MBTI について](https://www.16personalities.com/ja)

---

**注意**: このアプリケーションは教育目的で作成されており、公式なMBTI診断ではありません。

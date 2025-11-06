# ITクイズアプリ

大学3年生向けのIT・セキュリティ用語学習Webアプリケーション。4択クイズ形式で、カテゴリ別に用語を学習できます。

## 特徴

- 📚 **多彩なカテゴリ**: セキュリティ、IT基礎、プログラミング
- ⏱️ **タイマー機能**: 制限時間内に回答してスキルアップ
- 🔄 **復習モード**: 間違えた問題だけを集中的に復習
- 🎵 **効果音**: 正誤で異なる効果音で楽しく学習
- ♿ **アクセシビリティ**: キーボード操作、スクリーンリーダー対応
- 📱 **レスポンシブ**: PC、タブレット、スマートフォンに対応

## 技術スタック

- **バックエンド**: Python 3.12 + Flask 3.1.2
- **フロントエンド**: Bootstrap 5 + Vanilla JavaScript
- **データベース**: SQLite（開発）/ MySQL 8.0（本番）
- **ORM**: SQLAlchemy + Flask-SQLAlchemy
- **環境管理**: Poetry + pyenv

## セットアップ

### 前提条件

- Python 3.12以上
- Poetry
- pyenv（推奨）

### インストール手順

1. **リポジトリのクローン**

```bash
cd /path/to/traning-mbti
```

2. **Python環境の確認**

```bash
python --version  # Python 3.12.2
poetry --version  # Poetry 1.8.2
```

3. **依存関係のインストール**

```bash
poetry install
```

4. **データベースの初期化と初期データ投入**

```bash
poetry run python migrations/seeds/init_data.py
```

5. **アプリケーションの起動**

```bash
poetry run python run.py
```

6. **ブラウザでアクセス**

```
http://localhost:5000
```

## Docker を使用する場合（推奨）

### 前提条件

- Docker Desktop がインストールされていること
- Docker Desktop が起動していること
- ポート5000と3306が使用可能であること

### クイックスタート（シェルスクリプト使用）

プロジェクトには便利な起動スクリプトが用意されています：

```bash
# アプリケーションを起動
./start.sh

# 初回のみ：データベースを初期化
./init_db.sh

# アプリケーションを停止
./stop.sh

# アプリケーションを再起動
./restart.sh

# ログをリアルタイムで表示
./logs.sh
```

`./start.sh` を実行すると、自動的に以下が実行されます：
1. Dockerの起動確認
2. コンテナのビルドと起動
3. アクセス情報の表示
4. ブラウザで開くか確認（macOSのみ）

### Docker Composeを直接使用

シェルスクリプトを使わない場合は、以下のコマンドで起動できます：

```bash
# コンテナをビルドして起動（初回）
docker-compose up --build -d

# 2回目以降
docker-compose up -d

# データベースの初期化（初回のみ）
# データベースの起動を待つ（10秒程度）
sleep 10
docker-compose exec web python migrations/seeds/init_data.py

# ログを確認
docker-compose logs -f
```

**注意**: 初回起動時、データベースの準備に1-2分かかる場合があります。

### アクセス

起動後、以下のURLでアクセスできます：

```
http://localhost:5000
```

### 停止

```bash
# シェルスクリプトを使用
./stop.sh

# または Docker Compose コマンド
docker-compose down

# データベースも含めて削除
docker-compose down -v
```

### トラブルシューティング

#### ポートが使用中の場合

```bash
# ポート5000を使用しているプロセスを確認
lsof -i :5000

# ポート3306を使用しているプロセスを確認
lsof -i :3306
```

#### コンテナが起動しない場合

```bash
# ログを確認
./logs.sh
# または
docker-compose logs web

# コンテナを完全にクリーンアップして再起動
docker-compose down -v
docker-compose up -d --build
./init_db.sh
```

## 使い方

1. **トップページ**: アプリケーションの説明を確認
2. **カテゴリ選択**: 学習したいカテゴリを選択
3. **クイズ実行**: 10問の4択クイズに挑戦
4. **結果確認**: スコアと解説を確認
5. **復習モード**: 間違えた問題のみを再挑戦

### 設定

カテゴリ選択画面で以下の設定が可能です：

- **タイマー**: ON/OFF、制限時間（15-60秒）
- **効果音**: ON/OFF

## プロジェクト構造

```
.
├── app/
│   ├── __init__.py          # Flaskアプリ初期化
│   ├── models.py            # データモデル
│   ├── routes/              # ルーティング
│   │   ├── main.py          # メインページ
│   │   ├── quiz.py          # クイズ実行
│   │   └── api.py           # REST API
│   ├── services/            # ビジネスロジック
│   │   ├── quiz_service.py
│   │   └── result_service.py
│   ├── templates/           # HTMLテンプレート
│   └── static/              # 静的ファイル
│       ├── css/
│       ├── js/
│       └── sounds/
├── migrations/              # データベースマイグレーション
│   └── seeds/               # 初期データ
├── tests/                   # テストコード
├── config.py                # 設定ファイル
├── run.py                   # 起動スクリプト
├── Dockerfile
├── docker-compose.yml
└── README_QUIZ.md
```

## 開発

### テストの実行

```bash
poetry run pytest
```

### コードフォーマット

```bash
poetry run black app/
```

### リンターの実行

```bash
poetry run flake8 app/
```

### マイグレーションの作成

```bash
poetry run flask db init
poetry run flask db migrate -m "Initial migration"
poetry run flask db upgrade
```

## API エンドポイント

### クイズ開始
```
POST /api/quiz/start
```

### 問題取得
```
GET /api/quiz/<session_key>/question/<question_number>
```

### 回答送信
```
POST /api/quiz/<session_key>/answer
```

### 結果取得
```
GET /api/quiz/<session_key>/result
```

### 設定保存
```
POST /api/settings
```

詳細は [README_APP.md](README_APP.md) を参照してください。

## アクセシビリティ

このアプリケーションは WCAG 2.1 Level AA を目指して設計されています：

- **キーボードナビゲーション**: すべての機能にキーボードでアクセス可能
- **スクリーンリーダー対応**: ARIA属性を適切に使用
- **フォーカス管理**: 明確なフォーカスインジケーター
- **色だけに依存しない表示**: アイコンとテキストで情報を伝達

### キーボードショートカット

- `Tab` / `Shift+Tab`: 要素間の移動
- `矢印キー`: 選択肢の移動
- `Enter` / `Space`: 選択・決定
- `Esc`: モーダルを閉じる

## トラブルシューティング

### データベース接続エラー

```bash
# SQLiteの場合、ファイルを削除して再作成
rm quiz_app.db
poetry run python migrations/seeds/init_data.py
```

### ポートがすでに使用されている

```bash
# 別のポートで起動
PORT=5001 poetry run python run.py
```

### 依存関係のエラー

```bash
# キャッシュをクリアして再インストール
poetry cache clear pypi --all
poetry install
```

## ライセンス

このプロジェクトは教育目的で作成されています。

## 貢献

バグ報告や機能提案は Issue でお願いします。

## 作成者

- 作成日: 2025年11月6日
- バージョン: 1.0

---

**注意**: このプロジェクトは教育目的で作成されており、意図的にセキュリティの脆弱性が含まれる可能性があります。本番環境での使用は推奨されません。


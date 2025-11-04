# ディレクトリ構成

## 概要

このプロジェクトは、保守性と拡張性を考慮して、以下のように整理されています：

```
traning-mbti/
├── app/                      # アプリケーションディレクトリ
│   ├── __init__.py          # パッケージ初期化
│   ├── main.py              # メインアプリケーション
│   ├── database.py          # データベースモデル
│   ├── mbti/                # MBTI診断ロジック
│   │   ├── __init__.py
│   │   ├── questions.py     # 質問データ
│   │   ├── logic.py         # 採点・判定ロジック
│   │   └── descriptions.py  # タイプ説明
│   ├── static/              # 静的ファイル
│   │   ├── css/
│   │   └── js/
│   └── templates/           # Jinjaテンプレート
│       ├── base.html
│       ├── index.html
│       ├── question.html
│       ├── result.html
│       ├── auth/            # 認証関連テンプレート
│       ├── diagnosis/       # 診断関連テンプレート
│       └── admin/           # 管理画面テンプレート
│
├── scripts/                 # スクリプトディレクトリ
│   └── run_app.sh          # アプリケーション管理スクリプト
│
├── docker/                  # Docker関連ファイル
│   ├── Dockerfile          # Flaskアプリ用Dockerfile
│   ├── docker-compose.yml  # Docker Compose設定
│   └── mysql/              # MySQL設定
│       ├── conf.d/         # MySQL設定ファイル
│       └── init/           # 初期化SQLスクリプト
│
├── docs/                    # ドキュメントディレクトリ
│   ├── README_APP.md       # アプリケーション設計書
│   ├── LOGIN_SETUP.md      # ログイン機能ガイド
│   ├── USER_MANAGEMENT.md  # ユーザー管理ガイド
│   ├── DOCKER_README.md    # Docker運用ガイド
│   ├── QUICKSTART_DOCKER.md # Docker クイックスタート
│   ├── USAGE.md            # 使用方法
│   └── RUN_APP_EXAMPLES.md # 起動スクリプト例
│
├── instance/                # インスタンス固有ファイル
│   └── mbti.db             # SQLiteデータベース（開発用）
│
├── pyproject.toml          # Poetry依存関係定義
├── poetry.lock             # Poetry依存関係ロック
├── .env                    # 環境変数（ローカル設定）
├── .env.example            # 環境変数テンプレート
├── .dockerignore           # Docker除外ファイル
├── .gitignore              # Git除外ファイル
├── .python-version         # Python バージョン指定
└── README.md               # プロジェクトREADME
```

## 各ディレクトリの役割

### 📁 `app/` - アプリケーションディレクトリ

アプリケーションのコアロジックとUIを含む。

#### `app/main.py`
- Flaskアプリケーションのエントリーポイント
- ルート定義、認証、管理機能を統合
- データベース初期化とデフォルトユーザー作成

#### `app/database.py`
- SQLAlchemyモデル定義
  - `User`: ユーザーモデル
  - `DiagnosisResult`: 診断結果モデル

#### `app/mbti/`
- MBTI診断ロジックをモジュール化
- `questions.py`: 12問の質問データと選択肢
- `logic.py`: スコア計算とMBTIタイプ判定
- `descriptions.py`: 16タイプの説明文

#### `app/static/`
- CSSファイル、JavaScriptファイル、画像など

#### `app/templates/`
- Jinjaテンプレート
- サブディレクトリで機能ごとに分類
  - `auth/`: ログイン・登録
  - `diagnosis/`: 診断履歴
  - `admin/`: 管理画面

### 📁 `scripts/` - スクリプトディレクトリ

運用スクリプトを配置。

#### `scripts/run_app.sh`
- アプリケーション管理スクリプト
- Docker環境とネイティブ環境の両方に対応
- 起動、停止、再起動、状態確認機能

**使用例:**
```bash
./scripts/run_app.sh start      # 起動
./scripts/run_app.sh stop       # 停止
./scripts/run_app.sh restart    # 再起動
./scripts/run_app.sh status     # 状態確認
```

### 📁 `docker/` - Docker関連ファイル

コンテナ化に必要なファイルを集約。

#### `docker/Dockerfile`
- Flaskアプリケーション用のDockerイメージ定義
- Python 3.12-slimベース
- Poetryで依存関係管理

#### `docker/docker-compose.yml`
- マルチコンテナ構成定義
  - `app`: Flaskアプリケーション
  - `db`: MySQL 8.0データベース
  - `phpmyadmin`: データベース管理UI（オプション）

#### `docker/mysql/`
- MySQL固有の設定と初期化スクリプト
- `conf.d/`: MySQL設定ファイル
- `init/`: データベース初期化SQL

### 📁 `docs/` - ドキュメントディレクトリ

プロジェクトのドキュメントを集約。

- **README_APP.md**: アプリケーション全体の設計書
- **LOGIN_SETUP.md**: ログイン機能の詳細ガイド
- **USER_MANAGEMENT.md**: ユーザー管理機能の使用方法
- **DOCKER_README.md**: Docker環境の詳細ガイド
- **QUICKSTART_DOCKER.md**: Dockerクイックスタート
- **USAGE.md**: 基本的な使用方法
- **RUN_APP_EXAMPLES.md**: 起動スクリプトの例

### 📁 `instance/` - インスタンス固有ファイル

実行時に生成されるファイル。

- SQLiteデータベース（開発環境）
- ログファイル
- **Git管理外**（`.gitignore`で除外）

## 環境ファイル

### `.env`
ローカル環境変数設定。

```bash
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///mbti.db  # または MySQL接続文字列
MYSQL_ROOT_PASSWORD=root_password
MYSQL_DATABASE=mbti_db
MYSQL_USER=mbti_user
MYSQL_PASSWORD=mbti_password
```

### `.env.example`
環境変数のテンプレート。新規セットアップ時にコピーして使用。

## 起動方法

### Docker環境（推奨）

```bash
# 起動
./scripts/run_app.sh start

# または明示的にDockerを指定
./scripts/run_app.sh --docker start
```

### ネイティブ環境

```bash
# 起動
./scripts/run_app.sh --native start

# または直接実行
poetry run python app/main.py
```

## パス設定

### スクリプトから見たパス

`scripts/run_app.sh`は自動的にプロジェクトルートに移動するため、すべてのパスはプロジェクトルートからの相対パスで指定。

```bash
APP_SCRIPT="app/main.py"
DOCKER_COMPOSE_FILE="docker/docker-compose.yml"
```

### Docker から見たパス

Dockerコンテナ内では`/app`がワーキングディレクトリ。

```dockerfile
WORKDIR /app
CMD ["python", "-m", "app.main"]
```

### Python から見たパス

Pythonモジュールとしてインポート。

```python
from app.mbti import QUESTIONS, calculate_scores
from app.database import db, User
```

## ディレクトリ構成の利点

### 1. **分離と整理**
- アプリケーションコード（`app/`）
- 運用スクリプト（`scripts/`）
- コンテナ設定（`docker/`）
- ドキュメント（`docs/`）

### 2. **モジュール化**
- `app/mbti/`で診断ロジックをモジュール化
- 機能ごとにテンプレートを分類
- 拡張や保守が容易

### 3. **スケーラビリティ**
- 新機能追加時の影響範囲が明確
- 複数の開発者が同時作業可能
- CI/CDパイプラインとの統合が容易

### 4. **開発環境と本番環境の分離**
- Docker（本番想定）とネイティブ（開発）を両サポート
- 環境変数で設定を切り替え
- インスタンスファイルは`.gitignore`で除外

## 新機能追加のガイドライン

### 新しいルートを追加する場合
1. `app/main.py`にルート定義を追加
2. 必要に応じて`app/templates/`にテンプレート追加

### 新しいロジックを追加する場合
1. `app/`直下または適切なサブディレクトリに新規モジュール作成
2. `app/__init__.py`でエクスポート（必要に応じて）

### 新しいドキュメントを追加する場合
1. `docs/`ディレクトリに`.md`ファイル作成
2. `docs/README.md`（存在する場合）に目次として追加

### 新しいスクリプトを追加する場合
1. `scripts/`ディレクトリに追加
2. 実行権限を付与: `chmod +x scripts/your_script.sh`

## トラブルシューティング

### インポートエラー
```
ModuleNotFoundError: No module named 'xxx'
```

**原因**: 相対インポートが適切でない

**解決策**:
- `app/`内のモジュールは`from app.xxx import yyy`
- 同一パッケージ内は`from .xxx import yyy`

### パス not found エラー
```
FileNotFoundError: [Errno 2] No such file or directory
```

**原因**: 作業ディレクトリが想定と異なる

**解決策**:
- スクリプトはプロジェクトルートから実行
- パスはプロジェクトルート基準で指定

### Docker ビルドエラー
```
ERROR [internal] load metadata for...
```

**原因**: Dockerfile または docker-compose.ymlのパス設定が不正

**解決策**:
- `docker/docker-compose.yml`から見た相対パス確認
- `context: ..`（親ディレクトリ）が正しく設定されているか確認

## まとめ

この整理されたディレクトリ構成により、以下が実現されています：

✅ 明確な責任分離
✅ 保守性の向上
✅ 拡張性の確保
✅ チーム開発の容易化
✅ CI/CD対応

---

**注意**: このアプリケーションは教育目的で開発されており、本番環境での使用は推奨されません。


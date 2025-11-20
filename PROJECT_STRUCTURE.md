# プロジェクト構造

## ディレクトリ構成

```
traning-mbti/
├── app/                    # アプリケーションコード
│   ├── __init__.py        # パッケージ初期化
│   ├── app.py             # メインアプリケーション
│   ├── models.py          # データベースモデル
│   ├── config.py          # 設定ファイル
│   ├── data/              # データ初期化スクリプト
│   │   └── init_questions.py
│   ├── templates/         # HTMLテンプレート
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── quiz.html
│   │   ├── result.html
│   │   └── error.html
│   └── static/            # 静的ファイル
│       ├── css/
│       │   └── style.css
│       ├── js/
│       │   └── quiz.js
│       └── sounds/
│           └── README.md
├── docker/                 # Docker関連ファイル
│   ├── Dockerfile         # Dockerイメージ定義
│   ├── docker-compose.yml # Docker Compose設定
│   ├── .dockerignore      # Docker除外ファイル
│   └── mysql/             # MySQL初期化スクリプト
│       └── init.sql
├── docs/                   # ドキュメント
│   ├── README_APP.md      # アプリケーション設計書
│   ├── README_QUIZ.md     # クイズアプリ起動ガイド
│   ├── README_MYSQL.md    # MySQL設定ガイド
│   ├── README_DOCKER.md   # Docker構成ガイド
│   └── TROUBLESHOOTING.md # トラブルシューティング
├── scripts/                # スクリプト
│   ├── run.sh             # 起動スクリプト（macOS/Linux）
│   ├── stop.sh            # 停止スクリプト（macOS/Linux）
│   ├── run.bat            # 起動スクリプト（Windows）
│   ├── stop.bat           # 停止スクリプト（Windows）
│   ├── rebuild.sh          # 再ビルドスクリプト
│   ├── clean-rebuild.sh   # 完全再ビルドスクリプト
│   ├── init-mysql.sh      # MySQL初期化スクリプト
│   ├── verify-container.sh # コンテナ確認スクリプト
│   └── check-container.sh  # コンテナ状態確認スクリプト
├── pyproject.toml          # Poetry設定
├── poetry.lock             # Poetry依存関係ロック
├── README.md               # プロジェクト概要
└── PROJECT_STRUCTURE.md    # このファイル
```

## ディレクトリの説明

### `app/`
アプリケーションのメインコードが格納されています。
- `app.py`: FlaskアプリケーションのルーティングとAPI
- `models.py`: データベースモデル定義
- `config.py`: アプリケーション設定
- `data/`: 初期データ登録スクリプト
- `templates/`: Jinja2テンプレート
- `static/`: CSS、JavaScript、画像などの静的ファイル

### `docker/`
Docker関連の設定ファイルが格納されています。
- `Dockerfile`: Webアプリケーション用のDockerイメージ定義
- `docker-compose.yml`: サービス全体の構成（web、mysql）
- `.dockerignore`: Dockerビルド時に除外するファイル
- `mysql/init.sql`: MySQL初期化スクリプト

### `docs/`
プロジェクトのドキュメントが格納されています。
- 設計書、起動ガイド、トラブルシューティングなど

### `scripts/`
各種スクリプトが格納されています。
- 起動・停止スクリプト
- ビルドスクリプト
- 初期化スクリプト
- 確認スクリプト

## 使用方法

### 起動

```bash
# macOS/Linux
./scripts/run.sh

# Windows
scripts\run.bat
```

### 停止

```bash
# macOS/Linux
./scripts/stop.sh

# Windows
scripts\stop.bat
```

### 再ビルド

```bash
# macOS/Linux
./scripts/clean-rebuild.sh

# Windows
# PowerShellまたはコマンドプロンプトから
cd docker
docker compose build --no-cache
docker compose up
```

## ファイルパスの変更

ファイルを移動したため、以下のパスが変更されています：

- `app.py` → `app/app.py`
- `models.py` → `app/models.py`
- `config.py` → `app/config.py`
- `Dockerfile` → `docker/Dockerfile`
- `docker-compose.yml` → `docker/docker-compose.yml`
- スクリプト → `scripts/`

すべてのスクリプトとDocker設定は新しいパスに対応済みです。


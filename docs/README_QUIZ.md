# クイズアプリ 起動ガイド

## 概要

セキュリティ、IT基礎、プログラミングの技術用語を学習できる4択クイズアプリケーションです。

## 必要な環境

- Python 3.12+
- Poetry（パッケージ管理）

## セットアップ手順

### 1. 依存関係のインストール

```bash
poetry install
```

### 2. 仮想環境の有効化

```bash
poetry shell
```

### 3. データベースの初期化と初期データの登録

```bash
poetry run python data/init_questions.py
```

これにより、以下のカテゴリと問題が登録されます：
- **セキュリティ**: 20問
- **IT基礎**: カテゴリのみ（問題は後で追加可能）
- **プログラミング**: カテゴリのみ（問題は後で追加可能）

### 4. アプリケーションの起動

```bash
poetry run python app.py
```

または

```bash
flask run
```

アプリケーションは `http://localhost:5000` で起動します。

## 効果音ファイルについて

効果音ファイル（`static/sounds/correct.mp3` と `static/sounds/incorrect.mp3`）は、プロジェクトには含まれていません。

必要に応じて、以下の方法で追加してください：

1. 適切な効果音ファイルを用意
2. `static/sounds/` ディレクトリに配置
3. ファイル名を `correct.mp3` と `incorrect.mp3` にリネーム

効果音がなくてもアプリケーションは正常に動作します（音が鳴らないだけです）。

## 使い方

1. ブラウザで `http://localhost:5000` にアクセス
2. カテゴリを選択（セキュリティ、IT基礎、プログラミング）
3. クイズを開始
4. 各問題は30秒以内に回答
5. 正解後は解説が表示されます
6. 結果画面でスコアと間違えた問題を確認
7. 復習モードで間違えた問題のみ再挑戦可能

## キーボードショートカット

- **1-4キー**: 選択肢を選択（A, B, C, D）
- **Enterキー**: 解説表示中に次の問題へ進む
- **Tabキー**: 要素間を移動

## トラブルシューティング

### データベースエラーが発生する場合

```bash
# データベースファイルを削除して再初期化
rm quiz.db
poetry run python data/init_questions.py
```

### ポートが既に使用されている場合

`app.py` の最後の行を編集して、別のポートを指定：

```python
app.run(debug=True, host='0.0.0.0', port=5001)
```

## 開発者向け情報

### プロジェクト構造

```
traning-mbti/
├── app.py                  # メインアプリケーション
├── models.py               # データベースモデル
├── config.py               # 設定ファイル
├── data/
│   └── init_questions.py   # 初期データスクリプト
├── templates/              # HTMLテンプレート
│   ├── base.html
│   ├── index.html
│   ├── quiz.html
│   ├── result.html
│   └── error.html
├── static/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   └── quiz.js
│   └── sounds/
│       ├── correct.mp3
│       └── incorrect.mp3
└── quiz.db                 # SQLiteデータベース（自動生成）
```

### データベースの操作

Pythonインタラクティブシェルでデータベースを操作：

```bash
poetry run python
```

```python
from app import app, db
from models import Category, Question

with app.app_context():
    # カテゴリ一覧を取得
    categories = Category.query.all()
    for cat in categories:
        print(f"{cat.name}: {len(cat.questions)}問")
```

## ライセンス

このプロジェクトは教育目的で作成されています。


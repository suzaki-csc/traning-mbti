# MBTI風性格診断Webアプリケーション

Flask + Bootstrap で構築したMBTI風の性格診断アプリです。

## 📋 概要

12問の質問に答えることで、4軸（E/I, S/N, T/F, J/P）のスコアを合算し、16タイプのMBTI性格タイプを判定します。

## 🚀 クイックスタート

### 必要な環境

- Python 3.12以上
- Poetry

### インストールと起動

1. **依存パッケージのインストール**
```bash
poetry install
```

2. **アプリケーションの起動**
```bash
poetry run python run.py
```

3. **ブラウザでアクセス**
```
http://localhost:5000
```

## 📁 ファイル構成

```
traning-mbti/
├── app/                      # アプリケーション本体
│   ├── __init__.py          # Flask初期化
│   ├── routes.py            # ルーティング
│   ├── questions.py         # 質問データ
│   ├── mbti_logic.py        # MBTI判定ロジック
│   ├── templates/           # HTMLテンプレート
│   │   ├── base.html
│   │   ├── index.html
│   │   ├── quiz.html
│   │   └── result.html
│   └── static/              # 静的ファイル
│       └── css/
│           └── style.css
├── config.py                # 設定ファイル
├── run.py                   # エントリポイント
├── pyproject.toml           # Poetry設定
└── SPECIFICATION.md         # 詳細仕様書
```

## 🎯 機能

- ✅ 12問の質問による性格診断
- ✅ 進捗バー表示
- ✅ リアルタイムスコア計算
- ✅ 16タイプの性格タイプ判定
- ✅ 各軸のスコア可視化
- ✅ レスポンシブデザイン（モバイル対応）

## 🛠 技術スタック

- **バックエンド**: Flask 3.1+
- **フロントエンド**: Bootstrap 5
- **セッション管理**: Flask Session
- **依存管理**: Poetry

## 📝 開発メモ

### Phase 1（完了）
- ✅ 基本的なルーティング
- ✅ 質問データと採点ロジック
- ✅ HTMLテンプレート
- ✅ セッション管理

### Phase 2（予定）
- データベース連携（MySQL）
- 診断結果の永続化
- マイグレーション設定

### Phase 3（予定）
- Docker化
- docker-compose設定

### Phase 4（予定）
- 管理画面
- 診断履歴表示
- 統計情報

## 📄 ライセンス

このプロジェクトは研修用です。

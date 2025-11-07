# traning-mbti
1 day研修で使用する研修テーマ案

## 概要
このリポジトリは研修向けWebアプリケーションの試作を行っています。  
段階的な機能追加を学習するため、試作はブランチごとに管理しています。

## 📁 プロジェクト一覧

### 1. パスワード強度チェッカー
パスワードの強度をリアルタイムで評価し、セキュリティ向上のためのアドバイスを提供するWebアプリケーション。

**起動方法（Docker Compose）:**
```bash
# macOS / Linux
./start_password_checker.sh start

# Windows
start_password_checker.bat start
```

**主要コマンド:**
```bash
./start_password_checker.sh start     # 起動
./start_password_checker.sh stop      # 停止
./start_password_checker.sh logs      # ログ表示
./start_password_checker.sh status    # 状態確認
```

**詳細ドキュメント:**
- [クイックスタート](QUICKSTART.md) - 最速で起動する方法
- [実装仕様書](README_APP.md) - 詳細な仕様とアルゴリズム
- [使用方法とテスト](README_PASSWORD_CHECKER.md) - テストガイド

**技術スタック:** Docker, Flask, Bootstrap 5, JavaScript (Vanilla)

---

### 2. MBTI性格診断アプリ
研修向けMBTI性格診断アプリの試作。

## ブランチ構成

### test/simple_mbti_app_01
**基本機能のみの実装**
- Flaskを使用したシンプルなWebアプリケーション
- セッションベースで回答を管理（データベースなし）
- MBTI診断の基本的な動作を実装

### test/simple_mbti_app_02
**データベースの追加**
- SQLAlchemy + MySQL/PostgreSQLによるデータベース連携
- 診断結果をDBに永続化（Diagnosisモデル）
- Docker ComposeによるアプリとDBのコンテナ構成

### test/simple_mbti_app_03
**管理機能とユーザー認証の追加**
- ユーザー認証機能（ログイン/新規登録）
- 個人の診断履歴表示機能
- 管理者機能（全ユーザーの履歴参照、統計ダッシュボード）

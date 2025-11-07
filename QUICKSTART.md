# パスワード強度チェッカー - クイックスタートガイド

## 🚀 最速で起動する方法（Docker版）

### 前提条件

- Docker Desktop がインストールされていること
- Docker Desktop が起動していること

### macOS / Linux

```bash
# プロジェクトディレクトリに移動
cd /Users/csc-r063/Documents/github/traning-mbti

# 起動スクリプトを実行（初回は自動でイメージをビルド）
./start_password_checker.sh start
```

### Windows

```batch
# プロジェクトディレクトリに移動
cd C:\Users\...\traning-mbti

# 起動スクリプトを実行
start_password_checker.bat start
```

または、エクスプローラーで `start_password_checker.bat` をダブルクリック

---

## 📖 アクセス方法

起動後、ブラウザで以下のURLにアクセス:

```
http://localhost:5000
```

---

## ⏹️ 停止方法

### macOS / Linux
```bash
./start_password_checker.sh stop
```

### Windows
```batch
start_password_checker.bat stop
```

---

## 🔧 その他のコマンド

### ログを表示
```bash
./start_password_checker.sh logs
```

### コンテナの状態を確認
```bash
./start_password_checker.sh status
```

### アプリケーションを再起動
```bash
./start_password_checker.sh restart
```

### イメージを再ビルド
```bash
./start_password_checker.sh build
```

### クリーンアップ（コンテナとイメージを削除）
```bash
./start_password_checker.sh clean
```

---

## 📁 プロジェクト構成

```
traning-mbti/
├── start_password_checker.sh      # 起動スクリプト（macOS/Linux）
├── start_password_checker.bat     # 起動スクリプト（Windows）
├── password_checker_app.py        # Flaskアプリケーション
├── templates/
│   └── password_checker.html      # メインページ
├── static/
│   ├── css/
│   │   └── password_style.css     # スタイルシート
│   └── js/
│       └── password_checker.js    # パスワード評価ロジック
├── README_APP.md                  # 実装仕様書
├── README_PASSWORD_CHECKER.md     # 使用方法とテストガイド
└── QUICKSTART.md                  # このファイル
```

---

## 🧪 クイックテスト

アプリケーションが起動したら、以下のパスワードで動作確認:

| 入力するパスワード | 期待される評価 | 理由 |
|------------------|--------------|------|
| `password` | 🔴 非常に弱い | よくある単語 |
| `Password1` | 🟠 弱い | 単純な変形 |
| `MySecret2024` | 🟡 普通 | まあまあ |
| `Tr!cky$P@ss` | 🔵 強い | 良好 |
| `xK9$mP2vQr#5bN` | 🟢 非常に強い | 優秀 |

---

## 🔧 トラブルシューティング

### Dockerがインストールされていない場合

**macOS/Windows:**
1. [Docker Desktop](https://www.docker.com/products/docker-desktop/) をダウンロード
2. インストーラーを実行
3. Docker Desktopを起動

**Linux:**
```bash
# Ubuntu/Debianの場合
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo systemctl start docker
sudo usermod -aG docker $USER
```

### Dockerデーモンが起動していない場合

**macOS/Windows:**
- Docker Desktopアプリケーションを起動

**Linux:**
```bash
sudo systemctl start docker
sudo systemctl enable docker  # 自動起動を有効化
```

### ポート5000が使用中の場合

起動スクリプトが自動で対処しますが、手動で確認する場合:

```bash
# macOS/Linux
lsof -i :5000
kill -9 <PID>

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

### イメージのビルドに失敗する場合

```bash
# キャッシュをクリアして再ビルド
./start_password_checker.sh build

# またはDocker Composeコマンドで
docker compose build --no-cache
```

### コンテナが起動しない場合

```bash
# ログを確認
./start_password_checker.sh logs

# コンテナの状態を詳細確認
docker ps -a
docker logs password_checker_app

# コンテナに入って調査
docker exec -it password_checker_app /bin/bash
```

### Poetry環境で起動したい場合（Docker未使用）

Dockerを使わずにPoetry環境で起動する場合:

```bash
# Poetry環境を作成
poetry install

# アプリケーションを起動
poetry run python password_checker_app.py
```

---

## 📚 詳細なドキュメント

- **実装仕様書**: [README_APP.md](README_APP.md)
- **使用方法とテスト**: [README_PASSWORD_CHECKER.md](README_PASSWORD_CHECKER.md)

---

## 🎓 学習ポイント

このアプリケーションから学べること:

1. **パスワードセキュリティの基礎**
   - エントロピーの概念
   - 総当たり攻撃とは
   - 安全なパスワードの条件

2. **Webアプリケーション開発**
   - Flask（Python）でのバックエンド開発
   - HTML/CSS/JavaScriptでのフロントエンド開発
   - Bootstrap 5の活用

3. **アクセシビリティ**
   - WCAG準拠のUI設計
   - キーボード操作対応
   - スクリーンリーダー対応

4. **セキュリティベストプラクティス**
   - クライアント側での処理
   - 暗号学的に安全な乱数生成
   - HTTPS通信の重要性

---

## 💡 よくある質問

**Q: パスワードはサーバーに送信されますか？**  
A: いいえ。すべての評価処理はブラウザ内で行われ、サーバーには送信されません。

**Q: 実際のパスワード管理に使えますか？**  
A: このアプリは教育目的です。実際のパスワード管理にはパスワードマネージャー（1Password、Bitwarden等）の使用を推奨します。

**Q: 評価アルゴリズムをカスタマイズできますか？**  
A: はい。`static/js/password_checker.js`ファイルを編集することで、スコアリングロジックや辞書をカスタマイズできます。

**Q: 本番環境で使用できますか？**  
A: 現在の設定は開発用です。本番環境で使用する場合は、以下を実施してください:
   - `debug=False`に設定
   - HTTPS通信を使用
   - Gunicornなどの本番用サーバーで実行
   - セキュリティヘッダーの追加

---

## 🤝 サポート

問題が発生した場合や質問がある場合は、プロジェクトのIssueを作成してください。

---

**開発環境:** Python 3.12 + Flask + Poetry  
**最終更新:** 2025年11月7日


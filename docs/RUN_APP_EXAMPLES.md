# run_app.sh 使用例

## 概要

`run_app.sh`は、Docker環境とネイティブPython環境の両方に対応した統合管理スクリプトです。

---

## 🔄 自動検出モード

環境を自動的に検出して適切な方法で起動します。

```bash
# 起動
./run_app.sh start

# 状態確認
./run_app.sh status

# 停止
./run_app.sh stop

# 再起動
./run_app.sh restart
```

**自動検出の仕組み:**
- `docker-compose.yml`が存在し、`docker-compose`コマンドが利用可能 → Docker環境
- それ以外 → ネイティブ環境

---

## 🐳 Docker環境

### 起動

```bash
./run_app.sh --docker start
```

**出力例:**
```
==========================================
  MBTI風性格診断
==========================================

[Docker環境]

✓ .envファイルを作成しました

✓ Dockerコンテナを起動しています...

[+] Building 45.2s (14/14) FINISHED
[+] Running 3/3
 ✔ Network mbti_mbti-network  Created
 ✔ Container mbti-db           Started
 ✔ Container mbti-app          Started

✓ Docker環境が起動しました！

ブラウザで以下のURLにアクセスしてください：
  → http://localhost:5000

コンテナ状態:
NAME       IMAGE      COMMAND                  SERVICE  CREATED        STATUS
mbti-db    mysql:8.0  "docker-entrypoint.s…"  db       5 seconds ago  Up 4 seconds (health: starting)
mbti-app   ...        "python app.py"          app      5 seconds ago  Up 3 seconds (health: starting)
==========================================
```

### 状態確認

```bash
./run_app.sh --docker status
```

**出力例:**
```
==========================================
  MBTI風性格診断
==========================================

[Docker環境]

✓ Docker環境は実行中です

  URL: http://localhost:5000

コンテナ状態:
NAME       IMAGE      STATUS                   PORTS
mbti-db    mysql:8.0  Up 5 minutes (healthy)   0.0.0.0:3306->3306/tcp
mbti-app   ...        Up 5 minutes (healthy)   0.0.0.0:5000->5000/tcp

リソース使用状況:
NAME       CPU %     MEM USAGE
mbti-app   0.05%     45.2MiB / 7.76GiB
mbti-db    0.12%     152.3MiB / 7.76GiB
==========================================
```

### 停止

```bash
./run_app.sh --docker stop
```

### ログ確認

```bash
# Dockerのログを確認
docker-compose logs -f app
```

---

## 🖥️ ネイティブ環境

### 起動

```bash
./run_app.sh --native start
```

**出力例:**
```
==========================================
  MBTI風性格診断
==========================================

[ネイティブ環境]

✓ Poetry環境を検出しました
✓ 依存パッケージを確認中...
✓ アプリケーションを起動しています...

✓ アプリケーションが起動しました！

ブラウザで以下のURLにアクセスしてください：
  → http://localhost:5000

PID: 12345
ログファイル: app.log
==========================================
```

### 状態確認

```bash
./run_app.sh --native status
```

**出力例:**
```
==========================================
  MBTI風性格診断
==========================================

[ネイティブ環境]

✓ アプリケーションは実行中です

  PID: 12345
  URL: http://localhost:5000
  ログ: app.log

プロセス情報:
  PID  PPID USER      %CPU %MEM ELAPSED COMMAND
12345     1 user       0.5  0.3   00:15 python app.py
==========================================
```

### 停止

```bash
./run_app.sh --native stop
```

### ログ確認

```bash
# ネイティブ環境のログを確認
tail -f app.log
```

---

## 📋 使用例シナリオ

### シナリオ1: 開発開始時（自動検出）

```bash
# プロジェクトディレクトリに移動
cd /path/to/traning-mbti

# 自動検出で起動
./run_app.sh start

# ブラウザでアクセス
open http://localhost:5000
```

### シナリオ2: Docker環境で本番テスト

```bash
# Docker環境で明示的に起動
./run_app.sh --docker start

# 状態確認
./run_app.sh --docker status

# コンテナのログを監視
docker-compose logs -f

# 停止
./run_app.sh --docker stop
```

### シナリオ3: ネイティブ環境で開発

```bash
# ネイティブ環境で起動
./run_app.sh --native start

# コードを編集...

# 変更を反映するため再起動
./run_app.sh --native restart

# ログを確認
tail -f app.log

# 開発終了、停止
./run_app.sh --native stop
```

### シナリオ4: Docker環境からネイティブ環境への切り替え

```bash
# Docker環境を停止
./run_app.sh --docker stop

# ネイティブ環境で起動
./run_app.sh --native start
```

---

## ❓ FAQ

### Q: どちらの環境を使うべきですか？

**Docker環境を推奨する場合:**
- 本番環境に近い状態でテストしたい
- データベースを含めた完全な環境が必要
- 環境の再現性を重視する
- 複数の開発者で同じ環境を共有したい

**ネイティブ環境を推奨する場合:**
- 軽量で高速な起動が必要
- コードの変更を即座に反映したい（ホットリロード）
- Dockerのオーバーヘッドを避けたい
- ローカルでのデバッグを重視する

### Q: 自動検出の優先順位は？

1. `docker-compose.yml`の存在をチェック
2. `docker-compose`コマンドの利用可能性をチェック
3. 両方が利用可能な場合 → Docker環境
4. それ以外 → ネイティブ環境

明示的に`--docker`または`--native`を指定することで、自動検出をオーバーライドできます。

### Q: 両方の環境を同時に起動できますか？

いいえ、ポート5000が競合するため、同時に起動することはできません。
一方を停止してから、もう一方を起動してください。

---

## 🔗 関連ドキュメント

- **詳細な使用方法**: `USAGE.md`
- **Docker運用ガイド**: `DOCKER_README.md`
- **クイックスタート**: `QUICKSTART_DOCKER.md`
- **設計書**: `README_APP.md`


-- MySQL初期化スクリプト
-- このファイルは、MySQLコンテナの初回起動時に自動実行されます

-- データベースとユーザーの作成は、docker-compose.ymlの環境変数で自動的に行われます
-- ここには追加の初期化処理を記述できます

-- 文字セットと照合順序の設定
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;


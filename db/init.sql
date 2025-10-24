-- 初期化SQL（オプション）
-- データベースとテーブルはFlaskのSQLAlchemyで自動作成されますが、
-- 追加の設定や初期データがあればここに記述します。

-- PostgreSQL拡張機能の有効化（必要に応じて）
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- インデックスの追加最適化（SQLAlchemyで作成されますが、明示的に記述する場合）
-- CREATE INDEX IF NOT EXISTS idx_diagnoses_mbti_type ON diagnoses(mbti_type);
-- CREATE INDEX IF NOT EXISTS idx_diagnoses_created_at ON diagnoses(created_at);
-- CREATE INDEX IF NOT EXISTS idx_diagnoses_session_id ON diagnoses(session_id);

-- タイムゾーン設定
SET timezone = 'UTC';

-- 完了メッセージ
SELECT 'Database initialization completed' AS status;


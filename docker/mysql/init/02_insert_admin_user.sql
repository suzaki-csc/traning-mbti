-- 管理者ユーザーの作成

USE mbti_db;

-- デフォルト管理者ユーザーを作成
-- パスワード: admin123 (bcrypt hash)
-- 注意: 本番環境では必ずパスワードを変更してください
INSERT INTO users (email, password_hash, username, role, is_active) 
VALUES (
    'admin@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oi3qF5xzjYCe', -- admin123
    'Administrator',
    'admin',
    TRUE
) ON DUPLICATE KEY UPDATE
    username = 'Administrator',
    role = 'admin',
    is_active = TRUE;

-- テスト用一般ユーザー（開発環境のみ）
INSERT INTO users (email, password_hash, username, role, is_active) 
VALUES (
    'user@example.com',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5oi3qF5xzjYCe', -- admin123
    'Test User',
    'user',
    TRUE
) ON DUPLICATE KEY UPDATE
    username = 'Test User',
    role = 'user',
    is_active = TRUE;

-- サンプル診断結果データ（開発環境のみ）
INSERT INTO diagnosis_results (user_id, mbti_type, score_ei, score_sn, score_tf, score_jp, answers) 
VALUES 
    (1, 'INTJ', -4, -2, 2, 4, '{"1": 2, "2": 4, "3": 4, "4": 4, "5": 5, "6": 2, "7": 5, "8": 1, "9": 2, "10": 5, "11": 5, "12": 2}'),
    (2, 'ENFP', 5, -3, -2, -4, '{"1": 5, "2": 2, "3": 2, "4": 4, "5": 3, "6": 4, "7": 2, "8": 5, "9": 4, "10": 4, "11": 2, "12": 5}')
ON DUPLICATE KEY UPDATE 
    mbti_type = VALUES(mbti_type);

SELECT 'Admin user and sample data created successfully!' as message;
SELECT 'Default admin credentials: admin@example.com / admin123' as info;
SELECT 'WARNING: Change the admin password in production!' as warning;


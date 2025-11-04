-- MBTI診断アプリケーション データベース初期化スクリプト

-- データベースの選択
USE mbti_db;

-- 文字セットの設定
SET NAMES utf8mb4;
SET CHARACTER SET utf8mb4;

-- ユーザーテーブル
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    username VARCHAR(100) NOT NULL,
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    INDEX idx_email (email),
    INDEX idx_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 診断結果テーブル
CREATE TABLE IF NOT EXISTS diagnosis_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NULL,
    mbti_type VARCHAR(4) NOT NULL,
    score_ei INT NOT NULL,
    score_sn INT NOT NULL,
    score_tf INT NOT NULL,
    score_jp INT NOT NULL,
    answers JSON NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    session_id VARCHAR(255) NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    INDEX idx_user_id (user_id),
    INDEX idx_mbti_type (mbti_type),
    INDEX idx_created_at (created_at),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 診断回答詳細テーブル（オプション：詳細分析用）
CREATE TABLE IF NOT EXISTS diagnosis_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    result_id INT NOT NULL,
    question_id INT NOT NULL,
    answer_value INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_result_id (result_id),
    FOREIGN KEY (result_id) REFERENCES diagnosis_results(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- セッションテーブル（Flask-Session用：将来の拡張）
CREATE TABLE IF NOT EXISTS sessions (
    id VARCHAR(255) PRIMARY KEY,
    data TEXT NOT NULL,
    expiry TIMESTAMP NOT NULL,
    INDEX idx_expiry (expiry)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 統計情報ビュー（集計用）
CREATE OR REPLACE VIEW diagnosis_statistics AS
SELECT 
    mbti_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM diagnosis_results), 2) as percentage
FROM diagnosis_results
GROUP BY mbti_type
ORDER BY count DESC;

-- ユーザー別診断履歴ビュー
CREATE OR REPLACE VIEW user_diagnosis_history AS
SELECT 
    u.id as user_id,
    u.email,
    u.username,
    dr.id as result_id,
    dr.mbti_type,
    dr.created_at,
    dr.score_ei,
    dr.score_sn,
    dr.score_tf,
    dr.score_jp
FROM users u
LEFT JOIN diagnosis_results dr ON u.id = dr.user_id
ORDER BY dr.created_at DESC;

-- 初期データの挿入完了メッセージ
SELECT 'Database initialization completed successfully!' as message;


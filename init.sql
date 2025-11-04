-- 文字コード設定
ALTER DATABASE mbti_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- テーブルが存在する場合は削除
DROP TABLE IF EXISTS diagnosis_answers;
DROP TABLE IF EXISTS diagnosis_sessions;

-- diagnosis_sessionsテーブル作成
CREATE TABLE diagnosis_sessions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) UNIQUE NOT NULL,
    mbti_type VARCHAR(4) NOT NULL,
    scores_json JSON NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45) NULL,
    INDEX idx_created_at (created_at),
    INDEX idx_mbti_type (mbti_type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- diagnosis_answersテーブル作成
CREATE TABLE diagnosis_answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id INT NOT NULL,
    question_id INT NOT NULL,
    axis VARCHAR(1) NOT NULL,
    score INT NOT NULL,
    answer_text TEXT NOT NULL,
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES diagnosis_sessions(id) ON DELETE CASCADE,
    INDEX idx_session_id (session_id),
    INDEX idx_question_id (question_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


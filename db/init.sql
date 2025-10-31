-- MBTI診断アプリケーション データベース初期化スクリプト

-- 質問テーブル
CREATE TABLE IF NOT EXISTS questions (
    id INT PRIMARY KEY AUTO_INCREMENT,
    question_text TEXT NOT NULL,
    axis VARCHAR(10) NOT NULL,
    direction VARCHAR(10) NOT NULL DEFAULT 'positive',
    order_num INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 診断結果テーブル
CREATE TABLE IF NOT EXISTS diagnosis_results (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_name VARCHAR(255) NOT NULL,
    mbti_type VARCHAR(4) NOT NULL,
    e_score INT DEFAULT 0,
    i_score INT DEFAULT 0,
    s_score INT DEFAULT 0,
    n_score INT DEFAULT 0,
    t_score INT DEFAULT 0,
    f_score INT DEFAULT 0,
    j_score INT DEFAULT 0,
    p_score INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- 回答テーブル
CREATE TABLE IF NOT EXISTS answers (
    id INT PRIMARY KEY AUTO_INCREMENT,
    result_id INT NOT NULL,
    question_id INT NOT NULL,
    answer_value INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (result_id) REFERENCES diagnosis_results(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- インデックスの作成
CREATE INDEX idx_result_id ON answers(result_id);
CREATE INDEX idx_question_id ON answers(question_id);
CREATE INDEX idx_mbti_type ON diagnosis_results(mbti_type);
CREATE INDEX idx_created_at ON diagnosis_results(created_at);

-- 初期質問データの投入（12問）

-- E/I軸の質問（外向性 vs 内向性）
INSERT INTO questions (question_text, axis, direction, order_num) VALUES
('パーティーや集まりでエネルギーを得ますか？', 'E', 'positive', 1),
('一人で過ごす時間が必要ですか？', 'I', 'positive', 2),
('初対面の人とすぐに打ち解けられますか？', 'E', 'positive', 3);

-- S/N軸の質問（感覚 vs 直感）
INSERT INTO questions (question_text, axis, direction, order_num) VALUES
('具体的な事実やデータを重視しますか？', 'S', 'positive', 4),
('可能性や未来のビジョンに興味がありますか？', 'N', 'positive', 5),
('実践的で現実的な解決策を好みますか？', 'S', 'positive', 6);

-- T/F軸の質問（思考 vs 感情）
INSERT INTO questions (question_text, axis, direction, order_num) VALUES
('論理的な分析を重視しますか？', 'T', 'positive', 7),
('他者の感情を考慮して判断しますか？', 'F', 'positive', 8),
('客観的な基準で物事を判断しますか？', 'T', 'positive', 9);

-- J/P軸の質問（判断 vs 知覚）
INSERT INTO questions (question_text, axis, direction, order_num) VALUES
('計画的に物事を進めますか？', 'J', 'positive', 10),
('柔軟に対応することを好みますか？', 'P', 'positive', 11),
('締め切り前にタスクを完了させますか？', 'J', 'positive', 12);


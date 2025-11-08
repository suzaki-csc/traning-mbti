/**
 * パスワード強度チェッカー - JavaScriptロジック
 * 
 * このファイルには、パスワードの強度を評価するためのすべてのロジックが含まれています。
 * 初心者が理解しやすいように、詳細なコメントを記載しています。
 */

// ========================================
// 定数定義
// ========================================

/**
 * よくあるパスワードの辞書
 * これらの単語が含まれている場合、パスワードは弱いと判定されます
 */
const COMMON_PASSWORDS = [
    'password', 'qwerty', '123456', 'admin', 'letmein',
    'welcome', 'iloveyou', 'monkey', 'dragon', 'master',
    'sunshine', 'princess', 'abc123', '111111', 'password123',
    '000000', '12345678', 'qwerty123', 'password1', '123123',
    'login', 'pass', 'root', 'test', 'user', 'guest'
];

/**
 * キーボード配列のパターン
 * これらのパターンが含まれている場合、推測されやすいと判定されます
 */
const KEYBOARD_PATTERNS = [
    'qwerty', 'asdf', 'zxcv', 'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
    'qwertz', 'azerty', '!@#$%^&*()', '1234567890',
    'qwe', 'asd', 'zxc', 'wer', 'sdf', 'xcv'
];

/**
 * 総当たり攻撃の想定速度（試行回数/秒）
 * 現代的なコンピューターの性能を想定
 */
const CRACK_SPEED = 1000000000; // 10億回/秒

// ========================================
// グローバル変数
// ========================================

/**
 * アクティブなパスワードポリシー
 * アプリケーション起動時にサーバーから取得
 */
let activePolicy = null;

// ========================================
// ポリシー取得
// ========================================

/**
 * アクティブなパスワードポリシーをサーバーから取得
 */
async function loadActivePolicy() {
    try {
        const response = await fetch('/api/policy');
        const data = await response.json();
        
        if (data.success) {
            activePolicy = data.data;
            console.log('アクティブなポリシーを取得しました:', activePolicy.name);
            
            // ポリシー情報を画面に表示
            displayPolicyInfo();
        } else {
            console.error('ポリシーの取得に失敗しました:', data.message);
        }
    } catch (error) {
        console.error('ポリシー取得エラー:', error);
    }
}

/**
 * ポリシー情報を画面に表示
 */
function displayPolicyInfo() {
    if (!activePolicy) return;
    
    // ページ内にポリシー情報表示エリアがあれば更新
    const policyInfoElement = document.getElementById('policyInfo');
    if (policyInfoElement) {
        let requirementsHtml = '<ul class="small mb-0">';
        requirementsHtml += `<li>最小文字数: ${activePolicy.min_length}文字</li>`;
        
        const requirements = [];
        if (activePolicy.require_lowercase) requirements.push('小文字');
        if (activePolicy.require_uppercase) requirements.push('大文字');
        if (activePolicy.require_digit) requirements.push('数字');
        if (activePolicy.require_symbol) requirements.push('記号');
        
        if (requirements.length > 0) {
            requirementsHtml += `<li>必須文字種: ${requirements.join('、')}</li>`;
        }
        
        requirementsHtml += `<li>最低スコア: ${activePolicy.min_score_required}点</li>`;
        requirementsHtml += '</ul>';
        
        policyInfoElement.innerHTML = `
            <div class="alert alert-info">
                <h6><i class="bi bi-shield-check"></i> 適用中のポリシー: ${activePolicy.name}</h6>
                ${requirementsHtml}
            </div>
        `;
    }
}

// ========================================
// DOM要素の取得
// ========================================

// デバウンス用タイマー
let debounceTimer = null;
const DEBOUNCE_DELAY = 2000; // 2秒（ミリ秒）

// ページ読み込み完了後に実行
document.addEventListener('DOMContentLoaded', function() {
    // アクティブなポリシーを取得
    loadActivePolicy();
    // 入力要素
    const passwordInput = document.getElementById('passwordInput');
    const togglePassword = document.getElementById('togglePassword');
    const copyPassword = document.getElementById('copyPassword');
    const generatePassword = document.getElementById('generatePassword');
    
    // 表示要素
    const strengthSection = document.getElementById('strengthSection');
    const detailsSection = document.getElementById('detailsSection');
    const adviceSection = document.getElementById('adviceSection');
    const strengthBar = document.getElementById('strengthBar');
    const strengthBadge = document.getElementById('strengthBadge');
    const scoreValue = document.getElementById('scoreValue');
    const entropyValue = document.getElementById('entropyValue');
    const crackTimeValue = document.getElementById('crackTimeValue');
    const adviceList = document.getElementById('adviceList');
    const generatedPasswords = document.getElementById('generatedPasswords');
    
    // トースト通知
    const toastElement = document.getElementById('notificationToast');
    const toastMessage = document.getElementById('toastMessage');
    const toast = new bootstrap.Toast(toastElement);
    
    // ========================================
    // イベントリスナーの設定
    // ========================================
    
/**
 * パスワード入力時のイベント（デバウンス付き）
 * 
 * デバウンス処理により、ユーザーが入力を停止してから2秒後に以下を実行:
 * 1. パスワード強度の評価
 * 2. 評価結果のUI表示
 * 3. データベースへの保存（チェック履歴）
 * 
 * これにより、連続入力時の無駄な処理とサーバーへのリクエストを削減します。
 */
passwordInput.addEventListener('input', function() {
    const password = this.value;
    
    // 既存のタイマーをクリア（連続入力時は前のタイマーをキャンセル）
    if (debounceTimer) {
        clearTimeout(debounceTimer);
    }
    
    // パスワードが空の場合、すべてのセクションを非表示
    if (password.length === 0) {
        strengthSection.style.display = 'none';
        detailsSection.style.display = 'none';
        adviceSection.style.display = 'none';
        return;
    }
    
    // 入力中であることを表示
    showEvaluatingStatus();
    
    // 2秒後に評価とデータベース保存を実行
    // 注意: updateUI() 内で saveCheckResult() が呼ばれるため、
    // チェック処理と保存処理の両方が2秒後に実行されます
    debounceTimer = setTimeout(function() {
        updateUI(password);  // 評価 + UI更新 + DB保存
    }, DEBOUNCE_DELAY);
});
    
    /**
     * パスワード表示/非表示トグルボタン
     */
    togglePassword.addEventListener('click', function() {
        const type = passwordInput.getAttribute('type') === 'password' ? 'text' : 'password';
        passwordInput.setAttribute('type', type);
        
        // アイコンを切り替え
        const icon = document.getElementById('toggleIcon');
        icon.classList.toggle('bi-eye');
        icon.classList.toggle('bi-eye-slash');
    });
    
    /**
     * クリップボードコピーボタン
     */
    copyPassword.addEventListener('click', function() {
        const password = passwordInput.value;
        
        if (password.length === 0) {
            showNotification('コピーするパスワードがありません');
            return;
        }
        
        copyToClipboard(password);
    });
    
    /**
     * ランダムパスワード生成ボタン
     */
    generatePassword.addEventListener('click', function() {
        // 3つのランダムパスワードを生成
        const passwords = [];
        for (let i = 0; i < 3; i++) {
            // 12～16文字のランダムな長さ
            const length = Math.floor(Math.random() * 5) + 12;
            passwords.push(generateRandomPassword(length));
        }
        
        // 生成されたパスワードを表示
        displayGeneratedPasswords(passwords);
        
        // ボタンにアニメーション効果を追加
        generatePassword.classList.add('pulse');
        setTimeout(() => {
            generatePassword.classList.remove('pulse');
        }, 500);
    });
    
    // キーボードナビゲーション対応（Enterキーで生成されたパスワードを適用）
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && passwordInput.getAttribute('type') === 'text') {
            // Escキーでパスワードを非表示に
            passwordInput.setAttribute('type', 'password');
            document.getElementById('toggleIcon').classList.remove('bi-eye-slash');
            document.getElementById('toggleIcon').classList.add('bi-eye');
        }
    });
    
    // 履歴更新ボタンのイベント
    const refreshHistoryBtn = document.getElementById('refreshHistory');
    if (refreshHistoryBtn) {
        refreshHistoryBtn.addEventListener('click', function() {
            loadHistory();
        });
    }
    
    // 初回の履歴読み込み
    loadHistory();
});

// ========================================
// メイン評価関数
// ========================================

/**
 * パスワードの強度スコアを計算する関数
 * 
 * この関数は以下の要素を評価してスコアを計算します:
 * 1. パスワードの長さ（長いほど高得点）
 * 2. 文字の種類（小文字、大文字、数字、記号）
 * 3. よくある単語が含まれていないか（含まれると減点）
 * 4. 簡単に推測できるパターンがないか（繰り返しや連番など）
 * 
 * @param {string} password - 評価するパスワード文字列
 * @returns {object} スコアと詳細情報を含むオブジェクト
 */
function calculatePasswordScore(password) {
    // スコアの初期値は0から始める
    let score = 0;
    
    // 評価の詳細を記録するオブジェクト
    const details = {
        length: 0,           // 長さによる得点
        variety: 0,          // 文字種の多様性による得点
        penalties: [],       // 減点項目のリスト
        bonus: 0,            // ボーナス得点
        hasLower: false,     // 小文字を含むか
        hasUpper: false,     // 大文字を含むか
        hasDigit: false,     // 数字を含むか
        hasSymbol: false,    // 記号を含むか
        poolSize: 0          // 文字プールのサイズ
    };
    
    // ========================================
    // 1. 長さによる評価（最大30点）
    // ========================================
    // パスワードが長いほどセキュリティは高くなる
    const length = password.length;
    if (length >= 16) {
        details.length = 30;  // 16文字以上: 満点
    } else if (length >= 12) {
        details.length = 20;  // 12-15文字: 良好
    } else if (length >= 8) {
        details.length = 10;  // 8-11文字: 最低限
    } else {
        details.length = 0;   // 7文字以下: 不十分
    }
    score += details.length;
    
    // ========================================
    // 2. 文字種の多様性による評価（最大30点）
    // ========================================
    const charTypes = checkCharacterTypes(password);
    details.hasLower = charTypes.hasLower;
    details.hasUpper = charTypes.hasUpper;
    details.hasDigit = charTypes.hasDigit;
    details.hasSymbol = charTypes.hasSymbol;
    details.poolSize = charTypes.poolSize;
    
    // 各文字種につき7.5点
    if (charTypes.hasLower) details.variety += 7.5;
    if (charTypes.hasUpper) details.variety += 7.5;
    if (charTypes.hasDigit) details.variety += 7.5;
    if (charTypes.hasSymbol) details.variety += 7.5;
    
    score += details.variety;
    
    // ========================================
    // 3. パターン検出による減点（最大-40点）
    // ========================================
    
    // よくある単語の検出（-15点）
    if (detectCommonWords(password)) {
        details.penalties.push({
            type: 'common_word',
            points: -15,
            message: '一般的な単語（password等）を避けてください'
        });
        score -= 15;
    }
    
    // 繰り返しパターンの検出（-10点）
    if (detectRepeatingPatterns(password)) {
        details.penalties.push({
            type: 'repeating',
            points: -10,
            message: '繰り返しパターン（aaa、111等）を避けてください'
        });
        score -= 10;
    }
    
    // 連番パターンの検出（-10点）
    if (detectSequentialPatterns(password)) {
        details.penalties.push({
            type: 'sequential',
            points: -10,
            message: '連番パターン（123、abc等）を避けてください'
        });
        score -= 10;
    }
    
    // キーボード並びパターンの検出（-5点）
    if (detectKeyboardPatterns(password)) {
        details.penalties.push({
            type: 'keyboard',
            points: -5,
            message: 'キーボード配列（qwerty等）を避けてください'
        });
        score -= 5;
    }
    
    // ========================================
    // 4. ボーナスポイント（最大20点）
    // ========================================
    
    // 20文字以上のボーナス
    if (length >= 20) {
        details.bonus += 10;
        score += 10;
    }
    
    // すべての文字種を含み、かつ16文字以上
    if (length >= 16 && charTypes.hasLower && charTypes.hasUpper && 
        charTypes.hasDigit && charTypes.hasSymbol) {
        details.bonus += 10;
        score += 10;
    }
    
    // スコアを0-100の範囲に制限
    score = Math.max(0, Math.min(100, score));
    
    return {
        score: score,
        details: details
    };
}

/**
 * パスワードに含まれる文字種を判定する関数
 * 
 * @param {string} password - チェックするパスワード
 * @returns {object} 文字種の情報を含むオブジェクト
 */
function checkCharacterTypes(password) {
    // 各文字種の存在をチェック
    const hasLower = /[a-z]/.test(password);      // 小文字
    const hasUpper = /[A-Z]/.test(password);      // 大文字
    const hasDigit = /[0-9]/.test(password);      // 数字
    const hasSymbol = /[^a-zA-Z0-9]/.test(password);  // 記号（上記以外）
    
    // 文字プールのサイズを計算
    // これはエントロピー計算に使用されます
    let poolSize = 0;
    if (hasLower) poolSize += 26;   // a-z
    if (hasUpper) poolSize += 26;   // A-Z
    if (hasDigit) poolSize += 10;   // 0-9
    if (hasSymbol) poolSize += 33;  // 一般的な記号の数
    
    return {
        hasLower,
        hasUpper,
        hasDigit,
        hasSymbol,
        poolSize
    };
}

/**
 * よくある単語が含まれているかチェックする関数
 * 
 * @param {string} password - チェックするパスワード
 * @returns {boolean} よくある単語が含まれている場合true
 */
function detectCommonWords(password) {
    // パスワードを小文字に変換して照合
    const lowerPassword = password.toLowerCase();
    
    // 辞書内の各単語をチェック
    for (const word of COMMON_PASSWORDS) {
        if (lowerPassword.includes(word)) {
            return true;
        }
    }
    
    return false;
}

/**
 * 繰り返しパターンを検出する関数
 * 例: "aaa", "111", "..." など
 * 
 * @param {string} password - チェックするパスワード
 * @returns {boolean} 繰り返しパターンが見つかった場合true
 */
function detectRepeatingPatterns(password) {
    // 同じ文字が3回以上連続しているかチェック
    // 正規表現: (.)\1{2,} は同じ文字が3回以上繰り返されるパターン
    return /(.)\1{2,}/.test(password);
}

/**
 * 連番パターンを検出する関数
 * 例: "123", "abc", "987", "zyx" など
 * 
 * @param {string} password - チェックするパスワード
 * @returns {boolean} 連番が見つかった場合true
 */
function detectSequentialPatterns(password) {
    // 3文字以上の連番をチェック
    for (let i = 0; i < password.length - 2; i++) {
        const char1 = password.charCodeAt(i);
        const char2 = password.charCodeAt(i + 1);
        const char3 = password.charCodeAt(i + 2);
        
        // 昇順の連番（例: 123, abc）
        if (char2 === char1 + 1 && char3 === char2 + 1) {
            return true;
        }
        
        // 降順の連番（例: 321, cba）
        if (char2 === char1 - 1 && char3 === char2 - 1) {
            return true;
        }
    }
    
    return false;
}

/**
 * キーボード並びパターンを検出する関数
 * 例: "qwerty", "asdf" など
 * 
 * @param {string} password - チェックするパスワード
 * @returns {boolean} キーボード並びが見つかった場合true
 */
function detectKeyboardPatterns(password) {
    const lowerPassword = password.toLowerCase();
    
    // キーボードパターン辞書の各パターンをチェック
    for (const pattern of KEYBOARD_PATTERNS) {
        if (lowerPassword.includes(pattern)) {
            return true;
        }
    }
    
    return false;
}

/**
 * パスワードのエントロピーを計算する関数
 * 
 * エントロピーは、パスワードの予測困難性を表す指標です。
 * 値が大きいほど、推測が難しくなります。
 * 
 * @param {string} password - パスワード文字列
 * @param {number} poolSize - 使用可能な文字の総数
 * @returns {number} エントロピー（ビット単位）
 */
function calculateEntropy(password, poolSize) {
    // エントロピーの計算式:
    // エントロピー = パスワード長 × log2(文字プールサイズ)
    // 
    // 例: 8文字のパスワードで、95種類の文字を使用可能な場合
    // エントロピー = 8 × log2(95) ≈ 8 × 6.57 ≈ 52.5 bits
    
    if (poolSize === 0) {
        return 0;
    }
    
    const entropy = password.length * Math.log2(poolSize);
    
    // 小数点第1位まで丸める
    return Math.round(entropy * 10) / 10;
}

/**
 * 総当たり攻撃の想定時間を計算する関数
 * 
 * @param {number} entropy - エントロピー（ビット）
 * @returns {string} 人間が読める形式の時間
 */
function estimateCrackTime(entropy) {
    // 想定試行回数 = 2 ^ エントロピー
    // 平均して50%の試行で見つかると仮定するため、2で割る
    const attempts = Math.pow(2, entropy) / 2;
    
    // 秒単位の時間を計算
    const seconds = attempts / CRACK_SPEED;
    
    // 時間を人間が読める形式に変換
    return formatTime(seconds);
}

/**
 * 秒数を人間が読める形式に変換する関数
 * 
 * @param {number} seconds - 秒数
 * @returns {string} フォーマットされた時間文字列
 */
function formatTime(seconds) {
    if (seconds < 1) {
        return '1秒未満';
    } else if (seconds < 60) {
        return `約${Math.round(seconds)}秒`;
    } else if (seconds < 3600) {
        return `約${Math.round(seconds / 60)}分`;
    } else if (seconds < 86400) {
        return `約${Math.round(seconds / 3600)}時間`;
    } else if (seconds < 31536000) {
        return `約${Math.round(seconds / 86400)}日`;
    } else if (seconds < 31536000000) {
        return `約${Math.round(seconds / 31536000).toLocaleString()}年`;
    } else if (seconds < 31536000000000) {
        return `約${Math.round(seconds / 31536000000).toLocaleString()}千年`;
    } else {
        return `約${(seconds / 31536000000000).toExponential(1)}百万年`;
    }
}

/**
 * スコアに基づいて強度レベルを返す関数
 * 
 * @param {number} score - パスワードスコア（0-100）
 * @returns {object} レベル情報を含むオブジェクト
 */
function getStrengthLevel(score) {
    if (score <= 20) {
        return {
            level: 'very-weak',
            color: 'strength-very-weak',
            text: 'Very Weak (非常に弱い)',
            bgColor: 'bg-danger'
        };
    } else if (score <= 40) {
        return {
            level: 'weak',
            color: 'strength-weak',
            text: 'Weak (弱い)',
            bgColor: 'bg-warning'
        };
    } else if (score <= 60) {
        return {
            level: 'fair',
            color: 'strength-fair',
            text: 'Fair (普通)',
            bgColor: 'bg-warning'
        };
    } else if (score <= 80) {
        return {
            level: 'strong',
            color: 'strength-strong',
            text: 'Strong (強い)',
            bgColor: 'bg-info'
        };
    } else {
        return {
            level: 'very-strong',
            color: 'strength-very-strong',
            text: 'Very Strong (非常に強い)',
            bgColor: 'bg-success'
        };
    }
}

/**
 * 改善アドバイスを生成する関数
 * ポリシー設定に基づいてアドバイスを生成
 * 
 * @param {string} password - パスワード文字列
 * @param {object} details - 評価の詳細情報
 * @returns {Array<string>} アドバイスの配列
 */
function generateAdvice(password, details) {
    const advice = [];
    
    // アクティブなポリシーがあればそれに基づいてアドバイス
    if (activePolicy) {
        // 長さに関するアドバイス（ポリシーベース）
        if (password.length < activePolicy.min_length) {
            advice.push(`${activePolicy.min_length}文字以上に延ばしてください（現在: ${password.length}文字）`);
        } else if (password.length < activePolicy.min_length + 4) {
            advice.push(`${activePolicy.min_length + 4}文字以上にすると更に強固になります`);
        }
        
        // 文字種に関するアドバイス（ポリシーベース）
        if (activePolicy.require_lowercase && !details.hasLower) {
            advice.push('小文字（a-z）を含めてください [ポリシー必須]');
        }
        if (activePolicy.require_uppercase && !details.hasUpper) {
            advice.push('大文字（A-Z）を含めてください [ポリシー必須]');
        }
        if (activePolicy.require_digit && !details.hasDigit) {
            advice.push('数字（0-9）を含めてください [ポリシー必須]');
        }
        if (activePolicy.require_symbol && !details.hasSymbol) {
            advice.push('記号（!@#$%等）を含めてください [ポリシー必須]');
        }
        
        // 推奨文字種（必須ではないがセキュリティ向上のため）
        if (!activePolicy.require_lowercase && !details.hasLower) {
            advice.push('小文字（a-z）を含めることを推奨します');
        }
        if (!activePolicy.require_uppercase && !details.hasUpper) {
            advice.push('大文字（A-Z）を含めることを推奨します');
        }
        if (!activePolicy.require_digit && !details.hasDigit) {
            advice.push('数字（0-9）を含めることを推奨します');
        }
        if (!activePolicy.require_symbol && !details.hasSymbol) {
            advice.push('記号（!@#$%等）を含めることを推奨します');
        }
        
        // カスタム禁止単語のチェック
        if (activePolicy.custom_blocked_words && activePolicy.custom_blocked_words.length > 0) {
            const lowerPassword = password.toLowerCase();
            for (const word of activePolicy.custom_blocked_words) {
                if (lowerPassword.includes(word.toLowerCase())) {
                    advice.push(`「${word}」を含めないでください [ポリシーで禁止]`);
                }
            }
        }
    } else {
        // デフォルトのアドバイス（ポリシーが読み込まれていない場合）
        if (password.length < 12) {
            advice.push('12文字以上に延ばしてください');
        } else if (password.length < 16) {
            advice.push('16文字以上にすると更に強固になります');
        }
        
        if (!details.hasLower) advice.push('小文字（a-z）を含めてください');
        if (!details.hasUpper) advice.push('大文字（A-Z）を含めてください');
        if (!details.hasDigit) advice.push('数字（0-9）を含めてください');
        if (!details.hasSymbol) advice.push('記号（!@#$%等）を含めてください');
    }
    
    // ペナルティに基づくアドバイス
    for (const penalty of details.penalties) {
        advice.push(penalty.message);
    }
    
    // 単純な文字種置換の警告
    if (/[@]/.test(password) && /[a]/.test(password.toLowerCase())) {
        advice.push('単純な置換（@→a等）はセキュリティ向上になりません');
    }
    if (/[0]/.test(password) && /[o]/.test(password.toLowerCase())) {
        advice.push('単純な置換（0→o等）はセキュリティ向上になりません');
    }
    if (/[1]/.test(password) && /[i|l]/.test(password.toLowerCase())) {
        advice.push('単純な置換（1→i/l等）はセキュリティ向上になりません');
    }
    
    // アドバイスがない場合（非常に強いパスワード）
    if (advice.length === 0) {
        advice.push('優れたパスワードです！');
    }
    
    return advice;
}

/**
 * 評価中の状態を表示する関数
 * ユーザーに評価処理が開始されることを通知
 */
function showEvaluatingStatus() {
    const strengthSection = document.getElementById('strengthSection');
    const strengthBar = document.getElementById('strengthBar');
    const strengthBadge = document.getElementById('strengthBadge');
    
    // 強度セクションを表示
    strengthSection.style.display = 'block';
    
    // 評価中の表示
    strengthBar.style.width = '100%';
    strengthBar.className = 'progress-bar progress-bar-striped progress-bar-animated bg-secondary';
    strengthBar.textContent = '評価中...';
    
    strengthBadge.textContent = '入力を停止してください';
    strengthBadge.className = 'badge fs-6 bg-secondary';
}

/**
 * UIを更新する関数
 * すべての評価結果をUIに反映します
 * 
 * @param {string} password - 評価するパスワード
 */
function updateUI(password) {
    // パスワードスコアを計算
    const result = calculatePasswordScore(password);
    const score = result.score;
    const details = result.details;
    
    // エントロピーを計算
    const entropy = calculateEntropy(password, details.poolSize);
    
    // 総当たり攻撃の想定時間を計算
    const crackTime = estimateCrackTime(entropy);
    
    // 強度レベルを取得
    const strengthLevel = getStrengthLevel(score);
    
    // 改善アドバイスを生成
    const advice = generateAdvice(password, details);
    
    // ========================================
    // UIの更新
    // ========================================
    
    // セクションを表示
    document.getElementById('strengthSection').style.display = 'block';
    document.getElementById('detailsSection').style.display = 'block';
    document.getElementById('adviceSection').style.display = 'block';
    
    // 強度バーを更新
    const strengthBar = document.getElementById('strengthBar');
    strengthBar.style.width = score + '%';
    strengthBar.setAttribute('aria-valuenow', score);
    strengthBar.textContent = Math.round(score) + '%';
    
    // 強度バーの色を変更
    strengthBar.className = 'progress-bar progress-bar-striped progress-bar-animated fw-bold ' + strengthLevel.color;
    
    // バッジを更新
    const strengthBadge = document.getElementById('strengthBadge');
    strengthBadge.textContent = strengthLevel.text;
    strengthBadge.className = 'badge fs-6 ' + strengthLevel.bgColor;
    
    // 詳細情報を更新
    document.getElementById('scoreValue').textContent = Math.round(score);
    document.getElementById('entropyValue').textContent = entropy.toFixed(1);
    document.getElementById('crackTimeValue').textContent = crackTime;
    
    // アドバイスリストを更新
    const adviceList = document.getElementById('adviceList');
    adviceList.innerHTML = '';
    
    advice.forEach(function(item) {
        const li = document.createElement('li');
        li.className = 'list-group-item';
        li.innerHTML = '<i class="bi bi-exclamation-triangle-fill"></i>' + item;
        adviceList.appendChild(li);
    });
    
    // ========================================
    // データベースに保存（デバウンス後の自動保存）
    // ========================================
    // 注意: この関数はデバウンス処理後に呼ばれるため、
    // ユーザーが入力を停止してから2秒後に実行されます。
    // これにより、連続入力時の無駄な保存を防ぎます。
    saveCheckResult(password, result, details, entropy, crackTime, strengthLevel);
}

/**
 * パスワードチェック結果をサーバーに保存する関数
 * 
 * この関数は updateUI() 内から呼ばれるため、デバウンス処理が適用されます。
 * つまり、ユーザーが入力を停止してから2秒後にのみ実行されます。
 * 
 * 保存される情報:
 * - パスワードのハッシュ値（SHA-256）
 * - パスワードのマスク表示（先頭1文字 + ***）
 * - スコア、強度レベル、エントロピー、クラック時間
 * - 文字種の使用状況（小文字/大文字/数字/記号）
 * - パターン検出結果（よくある単語/繰り返し/連番/キーボード並び）
 * 
 * @param {string} password - パスワード
 * @param {object} result - スコア結果
 * @param {object} details - 評価詳細
 * @param {number} entropy - エントロピー
 * @param {string} crackTime - 総当たり想定時間
 * @param {object} strengthLevel - 強度レベル
 */
function saveCheckResult(password, result, details, entropy, crackTime, strengthLevel) {
    // APIエンドポイントにPOSTリクエストを送信
    // 注意: この処理はデバウンス後（入力停止から2秒後）に実行されます
    fetch('/api/save-check', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            password: password,
            score: result.score,
            strength_level: strengthLevel.level,
            entropy: entropy,
            crack_time: crackTime,
            has_lowercase: details.hasLower,
            has_uppercase: details.hasUpper,
            has_digit: details.hasDigit,
            has_symbol: details.hasSymbol,
            has_common_word: details.penalties.some(p => p.type === 'common_word'),
            has_repeating: details.penalties.some(p => p.type === 'repeating'),
            has_sequential: details.penalties.some(p => p.type === 'sequential'),
            has_keyboard_pattern: details.penalties.some(p => p.type === 'keyboard')
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            console.log('チェック結果を保存しました:', data);
        } else {
            console.error('保存に失敗しました:', data.message);
        }
    })
    .catch(error => {
        console.error('保存エラー:', error);
    });
}

/**
 * 安全なランダムパスワードを生成する関数
 * 
 * ブラウザの暗号学的に安全な乱数生成器（crypto.getRandomValues）を使用します
 * 
 * @param {number} length - パスワードの長さ
 * @returns {string} 生成されたランダムパスワード
 */
function generateRandomPassword(length) {
    // 使用する文字セット
    const lowercase = 'abcdefghijklmnopqrstuvwxyz';
    const uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
    const digits = '0123456789';
    const symbols = '!@#$%^&*()_+-=[]{}|;:,.<>?';
    
    // すべての文字を結合
    const allChars = lowercase + uppercase + digits + symbols;
    
    // 暗号学的に安全な乱数を生成
    const array = new Uint8Array(length);
    window.crypto.getRandomValues(array);
    
    // パスワード文字列を構築
    let password = '';
    
    // 各文字種を最低1つ含めることを保証
    password += lowercase[array[0] % lowercase.length];
    password += uppercase[array[1] % uppercase.length];
    password += digits[array[2] % digits.length];
    password += symbols[array[3] % symbols.length];
    
    // 残りの文字をランダムに選択
    for (let i = 4; i < length; i++) {
        password += allChars[array[i] % allChars.length];
    }
    
    // パスワードをシャッフル（Fisher-Yatesアルゴリズム）
    password = shuffleString(password);
    
    return password;
}

/**
 * 文字列をシャッフルする関数
 * 
 * @param {string} str - シャッフルする文字列
 * @returns {string} シャッフルされた文字列
 */
function shuffleString(str) {
    const array = str.split('');
    
    // Fisher-Yatesアルゴリズムでシャッフル
    for (let i = array.length - 1; i > 0; i--) {
        // 暗号学的に安全な乱数を生成
        const randomArray = new Uint8Array(1);
        window.crypto.getRandomValues(randomArray);
        const j = randomArray[0] % (i + 1);
        
        // 要素を交換
        [array[i], array[j]] = [array[j], array[i]];
    }
    
    return array.join('');
}

/**
 * 生成されたパスワードを表示する関数
 * 
 * @param {Array<string>} passwords - 生成されたパスワードの配列
 */
function displayGeneratedPasswords(passwords) {
    const container = document.getElementById('generatedPasswords');
    container.innerHTML = '';
    
    passwords.forEach(function(password) {
        // パスワード要素を作成
        const div = document.createElement('div');
        div.className = 'generated-password-item';
        div.setAttribute('tabindex', '0');
        div.setAttribute('role', 'button');
        div.setAttribute('aria-label', `生成されたパスワード: ${password}。クリックで使用`);
        
        // パスワードテキスト
        const span = document.createElement('span');
        span.className = 'generated-password-text';
        span.textContent = password;
        
        // アイコン
        const icon = document.createElement('i');
        icon.className = 'bi bi-arrow-right-circle generated-password-icon';
        
        div.appendChild(span);
        div.appendChild(icon);
        
        // クリックイベント: パスワードを入力フィールドに適用
        div.addEventListener('click', function() {
            document.getElementById('passwordInput').value = password;
            document.getElementById('passwordInput').dispatchEvent(new Event('input'));
            
            // 成功のフラッシュアニメーション
            div.classList.add('success-flash');
            setTimeout(() => {
                div.classList.remove('success-flash');
            }, 600);
            
            showNotification('パスワードを適用しました');
        });
        
        // キーボードナビゲーション対応
        div.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                div.click();
            }
        });
        
        container.appendChild(div);
    });
}

/**
 * クリップボードにテキストをコピーする関数
 * 
 * @param {string} text - コピーするテキスト
 */
function copyToClipboard(text) {
    // モダンブラウザの Clipboard API を使用
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text).then(function() {
            showNotification('パスワードをクリップボードにコピーしました');
        }).catch(function(err) {
            console.error('コピーに失敗しました:', err);
            showNotification('コピーに失敗しました');
        });
    } else {
        // フォールバック: 古いブラウザ用
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        
        try {
            document.execCommand('copy');
            showNotification('パスワードをクリップボードにコピーしました');
        } catch (err) {
            console.error('コピーに失敗しました:', err);
            showNotification('コピーに失敗しました');
        }
        
        document.body.removeChild(textarea);
    }
}

/**
 * トースト通知を表示する関数
 * 
 * @param {string} message - 表示するメッセージ
 */
function showNotification(message) {
    const toastElement = document.getElementById('notificationToast');
    const toastMessage = document.getElementById('toastMessage');
    
    toastMessage.textContent = message;
    
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
}

/**
 * チェック履歴をサーバーから取得して表示する関数
 */
function loadHistory() {
    const historyList = document.getElementById('historyList');
    
    // ローディング表示
    historyList.innerHTML = '<div class="text-center py-3"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">読み込み中...</span></div></div>';
    
    // APIエンドポイントから履歴を取得
    fetch('/api/history?limit=5')
        .then(response => response.json())
        .then(data => {
            if (data.success && data.data.length > 0) {
                displayHistory(data.data);
            } else {
                historyList.innerHTML = '<div class="alert alert-info"><i class="bi bi-info-circle"></i> チェック履歴がありません</div>';
            }
        })
        .catch(error => {
            console.error('履歴取得エラー:', error);
            historyList.innerHTML = '<div class="alert alert-danger"><i class="bi bi-exclamation-triangle"></i> 履歴の読み込みに失敗しました</div>';
        });
}

/**
 * 履歴データを表示する関数
 * 
 * @param {Array} historyData - 履歴データの配列
 */
function displayHistory(historyData) {
    const historyList = document.getElementById('historyList');
    historyList.innerHTML = '';
    
    // 強度レベルに応じたバッジクラスを返す関数
    function getLevelBadgeClass(level) {
        const classes = {
            'very-weak': 'bg-danger',
            'weak': 'bg-warning',
            'fair': 'bg-warning',
            'strong': 'bg-info',
            'very-strong': 'bg-success'
        };
        return classes[level] || 'bg-secondary';
    }
    
    // 強度レベルの日本語表示を返す関数
    function getLevelText(level) {
        const texts = {
            'very-weak': '非常に弱い',
            'weak': '弱い',
            'fair': '普通',
            'strong': '強い',
            'very-strong': '非常に強い'
        };
        return texts[level] || '不明';
    }
    
    // 各履歴アイテムを表示
    historyData.forEach(function(item) {
        const card = document.createElement('div');
        card.className = 'card mb-2';
        
        const cardBody = document.createElement('div');
        cardBody.className = 'card-body p-3';
        
        // ヘッダー行（パスワード表示と強度バッジ）
        const headerRow = document.createElement('div');
        headerRow.className = 'd-flex justify-content-between align-items-center mb-2';
        
        const passwordMasked = document.createElement('code');
        passwordMasked.className = 'text-muted';
        passwordMasked.textContent = item.password_masked;
        
        const levelBadge = document.createElement('span');
        levelBadge.className = `badge ${getLevelBadgeClass(item.strength_level)}`;
        levelBadge.textContent = getLevelText(item.strength_level);
        
        headerRow.appendChild(passwordMasked);
        headerRow.appendChild(levelBadge);
        
        // 詳細行（スコア、エントロピー、時刻）
        const detailRow = document.createElement('div');
        detailRow.className = 'small text-muted';
        detailRow.innerHTML = `
            <div class="row">
                <div class="col-4">スコア: <strong>${item.score}</strong>/100</div>
                <div class="col-4">エントロピー: <strong>${item.entropy.toFixed(1)}</strong> bits</div>
                <div class="col-4"><i class="bi bi-clock"></i> ${formatDate(item.created_at)}</div>
            </div>
        `;
        
        cardBody.appendChild(headerRow);
        cardBody.appendChild(detailRow);
        card.appendChild(cardBody);
        historyList.appendChild(card);
    });
}

/**
 * 日時をフォーマットする関数
 * 
 * @param {string} dateString - ISO形式の日時文字列
 * @returns {string} フォーマット済みの日時文字列
 */
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    // 1分未満
    if (diff < 60000) {
        return 'たった今';
    }
    // 1時間未満
    if (diff < 3600000) {
        const minutes = Math.floor(diff / 60000);
        return `${minutes}分前`;
    }
    // 24時間未満
    if (diff < 86400000) {
        const hours = Math.floor(diff / 3600000);
        return `${hours}時間前`;
    }
    // それ以上
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    return `${year}/${month}/${day} ${hours}:${minutes}`;
}


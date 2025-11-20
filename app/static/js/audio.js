/**
 * 効果音管理モジュール
 * 
 * 正解・不正解時の効果音を管理します。
 * ローカルストレージに設定を保存し、ユーザーの好みを保持します。
 */

class AudioManager {
    constructor() {
        this.soundEnabled = this.loadSoundSetting();
        this.correctSound = null;
        this.incorrectSound = null;
        this.initSounds();
        this.updateUI();
    }
    
    /**
     * 音声ファイルを初期化
     */
    initSounds() {
        // 正解音
        this.correctSound = new Audio('/static/audio/correct.mp3');
        this.correctSound.volume = 0.5;
        
        // 不正解音
        this.incorrectSound = new Audio('/static/audio/incorrect.mp3');
        this.incorrectSound.volume = 0.5;
        
        // エラーハンドリング: 音声ファイルが読み込めない場合
        this.correctSound.addEventListener('error', () => {
            console.warn('正解音の読み込みに失敗しました');
        });
        
        this.incorrectSound.addEventListener('error', () => {
            console.warn('不正解音の読み込みに失敗しました');
        });
    }
    
    /**
     * 正解音を再生
     */
    playCorrect() {
        if (this.soundEnabled && this.correctSound) {
            this.correctSound.currentTime = 0; // 最初から再生
            this.correctSound.play().catch(error => {
                console.warn('正解音の再生に失敗しました:', error);
            });
        }
    }
    
    /**
     * 不正解音を再生
     */
    playIncorrect() {
        if (this.soundEnabled && this.incorrectSound) {
            this.incorrectSound.currentTime = 0; // 最初から再生
            this.incorrectSound.play().catch(error => {
                console.warn('不正解音の再生に失敗しました:', error);
            });
        }
    }
    
    /**
     * 効果音のON/OFFを切り替え
     */
    toggleSound() {
        this.soundEnabled = !this.soundEnabled;
        this.saveSoundSetting();
        this.updateUI();
    }
    
    /**
     * ローカルストレージから設定を読み込み
     */
    loadSoundSetting() {
        const saved = localStorage.getItem('quiz_sound_enabled');
        return saved !== null ? saved === 'true' : true; // デフォルトはON
    }
    
    /**
     * ローカルストレージに設定を保存
     */
    saveSoundSetting() {
        localStorage.setItem('quiz_sound_enabled', this.soundEnabled.toString());
    }
    
    /**
     * UIを更新（ボタンの表示を変更）
     */
    updateUI() {
        const soundIcon = document.getElementById('sound-icon');
        const soundText = document.getElementById('sound-text');
        
        if (soundIcon && soundText) {
            if (this.soundEnabled) {
                soundIcon.className = 'bi bi-volume-up';
                soundText.textContent = '効果音ON';
            } else {
                soundIcon.className = 'bi bi-volume-mute';
                soundText.textContent = '効果音OFF';
            }
        }
    }
}

// グローバルにオーディオマネージャーインスタンスを保持
let audioManager = null;

/**
 * オーディオマネージャーを初期化
 */
function initAudioManager() {
    audioManager = new AudioManager();
    
    // 効果音切り替えボタンのイベントリスナー
    const toggleButton = document.getElementById('toggle-sound');
    if (toggleButton) {
        toggleButton.addEventListener('click', () => {
            audioManager.toggleSound();
        });
    }
    
    return audioManager;
}

/**
 * 正解音を再生
 */
function playCorrectSound() {
    if (audioManager) {
        audioManager.playCorrect();
    }
}

/**
 * 不正解音を再生
 */
function playIncorrectSound() {
    if (audioManager) {
        audioManager.playIncorrect();
    }
}


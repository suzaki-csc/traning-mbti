/**
 * 設定管理
 * 
 * クイズの設定（タイマー、効果音）をlocalStorageで管理
 */

class SettingsManager {
    constructor() {
        this.settings = this.loadSettings();
    }

    loadSettings() {
        const defaults = {
            timerSeconds: 30,
            soundEnabled: true
        };

        try {
            const stored = localStorage.getItem('quizSettings');
            return stored ? { ...defaults, ...JSON.parse(stored) } : defaults;
        } catch (error) {
            console.error('設定の読み込みに失敗しました:', error);
            return defaults;
        }
    }

    saveSettings(settings) {
        try {
            this.settings = { ...this.settings, ...settings };
            localStorage.setItem('quizSettings', JSON.stringify(this.settings));
            return true;
        } catch (error) {
            console.error('設定の保存に失敗しました:', error);
            return false;
        }
    }

    getSetting(key) {
        return this.settings[key];
    }

    setSetting(key, value) {
        this.settings[key] = value;
        this.saveSettings(this.settings);
    }
}

// グローバルインスタンス
const settingsManager = new SettingsManager();

// 設定UIの初期化
document.addEventListener('DOMContentLoaded', function() {
    // 設定フォームが存在する場合
    const timerToggle = document.getElementById('timerToggle');
    const timerSlider = document.getElementById('timerSeconds');
    const soundToggle = document.getElementById('soundToggle');

    if (timerToggle && timerSlider && soundToggle) {
        // 保存された設定を読み込む
        const settings = settingsManager.loadSettings();
        
        timerToggle.checked = settings.timerSeconds > 0;
        timerSlider.value = settings.timerSeconds || 30;
        soundToggle.checked = settings.soundEnabled;

        // スライダーの値表示を更新
        const timerValue = document.getElementById('timerValue');
        if (timerValue) {
            timerValue.textContent = timerSlider.value;
        }

        // 設定変更時に保存
        timerToggle.addEventListener('change', function() {
            const seconds = this.checked ? parseInt(timerSlider.value) : 0;
            settingsManager.setSetting('timerSeconds', seconds);
        });

        timerSlider.addEventListener('change', function() {
            if (timerToggle.checked) {
                settingsManager.setSetting('timerSeconds', parseInt(this.value));
            }
        });

        soundToggle.addEventListener('change', function() {
            settingsManager.setSetting('soundEnabled', this.checked);
        });
    }
});


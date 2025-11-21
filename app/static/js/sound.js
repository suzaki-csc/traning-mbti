/**
 * 効果音機能
 */

let soundEnabled = true;

/**
 * 効果音を再生
 * @param {string} type - 効果音の種類 ('correct' または 'incorrect')
 */
function playSound(type) {
    if (!soundEnabled) {
        return;
    }
    
    const soundFile = type === 'correct' 
        ? '/static/sounds/correct.mp3' 
        : '/static/sounds/incorrect.mp3';
    
    const audio = new Audio(soundFile);
    audio.play().catch(function(error) {
        // 音声再生が失敗した場合は無視（ユーザーが操作していない場合など）
        console.log('Sound playback failed:', error);
    });
}

/**
 * 効果音のON/OFFを切り替え
 * @param {boolean} enabled - 有効にするかどうか
 */
function setSoundEnabled(enabled) {
    soundEnabled = enabled;
    localStorage.setItem('soundEnabled', enabled.toString());
}

// ページ読み込み時に設定を復元
document.addEventListener('DOMContentLoaded', function() {
    const savedSetting = localStorage.getItem('soundEnabled');
    if (savedSetting !== null) {
        soundEnabled = savedSetting === 'true';
    }
    
    // チェックボックスの状態を設定
    const toggle = document.getElementById('sound-toggle');
    if (toggle) {
        toggle.checked = soundEnabled;
        toggle.addEventListener('change', function() {
            setSoundEnabled(this.checked);
        });
    }
});


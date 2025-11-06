/**
 * アクセシビリティ機能
 * 
 * キーボードナビゲーションとスクリーンリーダー対応
 */

document.addEventListener('DOMContentLoaded', function() {
    // 選択肢のキーボードナビゲーション
    setupChoiceNavigation();
    
    // スキップリンクの設定
    setupSkipLinks();
    
    // フォーカス可能な要素のフォーカス表示を改善
    improveFocusVisibility();
});

/**
 * 選択肢の矢印キー操作を設定
 */
function setupChoiceNavigation() {
    document.addEventListener('keydown', function(e) {
        // クイズ画面でのみ有効
        const choices = document.querySelectorAll('input[name="choice"]');
        if (choices.length === 0) return;

        const currentIndex = Array.from(choices).findIndex(c => c === document.activeElement);
        
        if (currentIndex === -1) return;

        let nextIndex = currentIndex;

        switch(e.key) {
            case 'ArrowDown':
            case 'ArrowRight':
                e.preventDefault();
                nextIndex = (currentIndex + 1) % choices.length;
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
                e.preventDefault();
                nextIndex = (currentIndex - 1 + choices.length) % choices.length;
                break;
            case 'Enter':
            case ' ':
                e.preventDefault();
                choices[currentIndex].checked = true;
                choices[currentIndex].dispatchEvent(new Event('change', { bubbles: true }));
                return;
            default:
                return;
        }

        choices[nextIndex].focus();
        choices[nextIndex].checked = true;
        choices[nextIndex].dispatchEvent(new Event('change', { bubbles: true }));
    });
}

/**
 * スキップリンクを設定（メインコンテンツへのジャンプ）
 */
function setupSkipLinks() {
    const skipLink = document.createElement('a');
    skipLink.href = '#main';
    skipLink.className = 'skip-link sr-only sr-only-focusable';
    skipLink.textContent = 'メインコンテンツへスキップ';
    
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // メインコンテンツにIDを付与
    const mainContent = document.querySelector('main');
    if (mainContent && !mainContent.id) {
        mainContent.id = 'main';
        mainContent.setAttribute('tabindex', '-1');
    }
}

/**
 * フォーカス表示を改善
 */
function improveFocusVisibility() {
    // マウス操作時はフォーカスリングを非表示、キーボード操作時は表示
    let isUsingMouse = false;

    document.addEventListener('mousedown', function() {
        isUsingMouse = true;
        document.body.classList.add('using-mouse');
    });

    document.addEventListener('keydown', function(e) {
        if (e.key === 'Tab') {
            isUsingMouse = false;
            document.body.classList.remove('using-mouse');
        }
    });
}

/**
 * スクリーンリーダー用の通知
 * 
 * @param {string} message - 通知するメッセージ
 * @param {string} priority - 'polite' または 'assertive'
 */
function announceToScreenReader(message, priority = 'polite') {
    const announcer = document.getElementById('sr-announce');
    if (!announcer) return;

    announcer.setAttribute('aria-live', priority);
    announcer.textContent = message;

    // 短時間後にクリア
    setTimeout(() => {
        announcer.textContent = '';
    }, 1000);
}

/**
 * ページタイトルを動的に更新（タブに表示）
 * 
 * @param {string} title - 新しいタイトル
 */
function updatePageTitle(title) {
    document.title = title + ' - ITクイズアプリ';
}

// エクスポート（他のスクリプトから使用可能にする）
window.announceToScreenReader = announceToScreenReader;
window.updatePageTitle = updatePageTitle;


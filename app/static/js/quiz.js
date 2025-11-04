// MBTI性格診断アプリ - フロントエンドJavaScript

// ページ読み込み完了時の処理
document.addEventListener('DOMContentLoaded', function() {
    // 質問ボタンのアニメーション
    initQuizButtons();
    
    // プログレスバーのアニメーション
    animateProgressBars();
    
    // ツールチップの初期化
    initTooltips();
});

/**
 * 質問ボタンの初期化
 */
function initQuizButtons() {
    const quizOptions = document.querySelectorAll('.quiz-option');
    
    quizOptions.forEach((button, index) => {
        // フェードインアニメーション
        button.style.opacity = '0';
        button.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            button.style.transition = 'all 0.5s ease';
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, index * 100);
        
        // キーボードショートカット（1, 2キー）
        if (index < 2) {
            document.addEventListener('keypress', function(e) {
                if (e.key === String(index + 1)) {
                    button.click();
                }
            });
        }
    });
}

/**
 * プログレスバーのアニメーション
 */
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        
        setTimeout(() => {
            bar.style.transition = 'width 1s ease';
            bar.style.width = width;
        }, 100);
    });
}

/**
 * ツールチップの初期化（Bootstrap）
 */
function initTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * 結果ページのアニメーション
 */
function animateResults() {
    const mbtiType = document.querySelector('.display-3');
    if (mbtiType) {
        mbtiType.style.transform = 'scale(0.5)';
        mbtiType.style.opacity = '0';
        
        setTimeout(() => {
            mbtiType.style.transition = 'all 0.8s cubic-bezier(0.68, -0.55, 0.265, 1.55)';
            mbtiType.style.transform = 'scale(1)';
            mbtiType.style.opacity = '1';
        }, 100);
    }
}

// 結果ページの場合、アニメーションを実行
if (window.location.pathname.includes('/result/')) {
    document.addEventListener('DOMContentLoaded', animateResults);
}

/**
 * スムーススクロール
 */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

/**
 * フォーム送信時のローディング表示
 */
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const submitBtn = this.querySelector('button[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
            // ボタンを無効化してローディング表示
            const originalText = submitBtn.innerHTML;
            submitBtn.disabled = true;
            submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> 処理中...';
            
            // タイムアウト設定（10秒）
            setTimeout(() => {
                submitBtn.disabled = false;
                submitBtn.innerHTML = originalText;
            }, 10000);
        }
    });
});

/**
 * 結果のシェア機能（将来的な拡張用）
 */
function shareResult(mbtiType) {
    const shareData = {
        title: 'MBTI性格診断結果',
        text: `私の診断結果は ${mbtiType} でした！`,
        url: window.location.href
    };
    
    if (navigator.share) {
        navigator.share(shareData)
            .then(() => console.log('シェアしました'))
            .catch((error) => console.log('シェアエラー:', error));
    } else {
        // フォールバック: URLをコピー
        navigator.clipboard.writeText(window.location.href)
            .then(() => alert('URLをクリップボードにコピーしました'))
            .catch(() => alert('URLのコピーに失敗しました'));
    }
}

/**
 * コンソールにウェルカムメッセージを表示
 */
console.log('%cMBTI性格診断アプリ', 'color: #4a90e2; font-size: 24px; font-weight: bold;');
console.log('%c教育目的のデモンストレーションアプリケーションです', 'color: #7f8c8d; font-size: 14px;');

/**
 * エラーハンドリング
 */
window.addEventListener('error', function(e) {
    console.error('エラーが発生しました:', e.error);
});

/**
 * パフォーマンス測定（開発用）
 */
if (window.performance) {
    window.addEventListener('load', function() {
        const perfData = window.performance.timing;
        const pageLoadTime = perfData.loadEventEnd - perfData.navigationStart;
        console.log(`ページ読み込み時間: ${pageLoadTime}ms`);
    });
}


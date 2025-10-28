// MBTI性格診断アプリ カスタムJavaScript

// ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', function() {
    // Bootstrap tooltipの有効化
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // ラジオボタンの選択時にカードをハイライト
    initQuizOptions();
    
    // フラッシュメッセージの自動非表示
    autoHideAlerts();
});

/**
 * 診断オプションの初期化
 */
function initQuizOptions() {
    const radioInputs = document.querySelectorAll('.form-check-input[type="radio"]');
    
    radioInputs.forEach(function(radio) {
        radio.addEventListener('change', function() {
            // すべてのカードからactiveクラスを削除
            const allCards = document.querySelectorAll('.form-check-label .card');
            allCards.forEach(function(card) {
                card.classList.remove('border-primary', 'bg-light');
            });
            
            // 選択されたカードにactiveクラスを追加
            if (this.checked) {
                const label = this.nextElementSibling;
                const card = label.querySelector('.card');
                if (card) {
                    card.classList.add('border-primary', 'bg-light');
                }
            }
        });
        
        // 初期状態で選択されている場合
        if (radio.checked) {
            const label = radio.nextElementSibling;
            const card = label.querySelector('.card');
            if (card) {
                card.classList.add('border-primary', 'bg-light');
            }
        }
    });
}

/**
 * フラッシュメッセージの自動非表示
 */
function autoHideAlerts() {
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
    
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // 5秒後に自動非表示
    });
}

/**
 * 削除確認ダイアログ
 */
function confirmDelete(message) {
    return confirm(message || '本当に削除してもよろしいですか？');
}

/**
 * スコアバーのアニメーション
 */
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(function(bar) {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(function() {
            bar.style.width = width;
        }, 100);
    });
}

// 結果ページでスコアバーをアニメーション
if (document.querySelector('.progress-bar')) {
    animateProgressBars();
}

/**
 * フォームバリデーション
 */
function validateForm(formId) {
    const form = document.getElementById(formId);
    
    if (form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            
            form.classList.add('was-validated');
        }, false);
    }
}

/**
 * テーブル行のクリックでリンクに移動
 */
function initTableRowClick() {
    const tableRows = document.querySelectorAll('table tbody tr');
    
    tableRows.forEach(function(row) {
        const link = row.querySelector('a');
        
        if (link) {
            row.style.cursor = 'pointer';
            row.addEventListener('click', function(event) {
                // ボタンやリンクをクリックした場合は除外
                if (event.target.tagName !== 'BUTTON' && event.target.tagName !== 'A') {
                    window.location = link.href;
                }
            });
        }
    });
}

initTableRowClick();


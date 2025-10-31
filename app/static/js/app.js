// MBTI診断アプリケーション - JavaScript

// ページ読み込み時の初期化
document.addEventListener('DOMContentLoaded', function() {
    console.log('MBTI診断アプリケーションが読み込まれました');
    
    // アニメーション効果の追加
    addScrollAnimations();
    
    // ツールチップの初期化（Bootstrap）
    initializeTooltips();
    
    // プログレスバーのアニメーション
    animateProgressBars();
});

/**
 * スクロールアニメーションを追加
 */
function addScrollAnimations() {
    const elements = document.querySelectorAll('.card, .question-item');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, {
        threshold: 0.1
    });
    
    elements.forEach(element => {
        element.style.opacity = '0';
        element.style.transform = 'translateY(20px)';
        element.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
        observer.observe(element);
    });
}

/**
 * Bootstrapツールチップの初期化
 */
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(
        document.querySelectorAll('[data-bs-toggle="tooltip"]')
    );
    
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

/**
 * プログレスバーのアニメーション
 */
function animateProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach((bar, index) => {
        const width = bar.style.width;
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 1s ease-in-out';
            bar.style.width = width;
        }, index * 200);
    });
}

/**
 * 診断フォームのバリデーション
 */
function validateDiagnosisForm(form) {
    const questions = form.querySelectorAll('.question-item');
    let allAnswered = true;
    
    questions.forEach(question => {
        const radioButtons = question.querySelectorAll('input[type="radio"]');
        const isAnswered = Array.from(radioButtons).some(radio => radio.checked);
        
        if (!isAnswered) {
            allAnswered = false;
            question.classList.add('border-danger');
            question.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            question.classList.remove('border-danger');
        }
    });
    
    return allAnswered;
}

/**
 * ラジオボタンの選択時の視覚効果
 */
document.addEventListener('change', function(e) {
    if (e.target.type === 'radio' && e.target.name.startsWith('q_')) {
        const questionItem = e.target.closest('.question-item');
        
        if (questionItem) {
            questionItem.classList.add('border-success');
            questionItem.classList.remove('border-danger');
            
            // チェックマークアイコンを追加
            let checkIcon = questionItem.querySelector('.check-icon');
            if (!checkIcon) {
                checkIcon = document.createElement('i');
                checkIcon.className = 'bi bi-check-circle-fill text-success check-icon ms-2';
                const label = questionItem.querySelector('.form-label');
                if (label) {
                    label.appendChild(checkIcon);
                }
            }
        }
    }
});

/**
 * スムーズスクロール
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
 * アラートの自動非表示
 */
document.querySelectorAll('.alert').forEach(alert => {
    setTimeout(() => {
        const bsAlert = new bootstrap.Alert(alert);
        bsAlert.close();
    }, 5000);
});

/**
 * ローディングスピナーの表示
 */
function showLoadingSpinner(button) {
    const originalText = button.innerHTML;
    button.disabled = true;
    button.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>処理中...';
    
    return function hideSpinner() {
        button.disabled = false;
        button.innerHTML = originalText;
    };
}

/**
 * フォーム送信時の処理
 */
document.addEventListener('submit', function(e) {
    const form = e.target;
    
    if (form.id === 'diagnosisForm') {
        const submitButton = form.querySelector('button[type="submit"]');
        const hideSpinner = showLoadingSpinner(submitButton);
        
        // バリデーション
        if (!validateDiagnosisForm(form)) {
            e.preventDefault();
            hideSpinner();
            
            // エラーメッセージを表示
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert alert-danger alert-dismissible fade show';
            alertDiv.innerHTML = `
                <i class="bi bi-exclamation-triangle"></i>
                すべての質問に回答してください
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            form.insertBefore(alertDiv, form.firstChild);
            
            setTimeout(() => {
                alertDiv.remove();
            }, 5000);
        }
    }
});

/**
 * テーブルの行をクリックで詳細ページに遷移
 */
document.querySelectorAll('.table tbody tr').forEach(row => {
    row.style.cursor = 'pointer';
    
    row.addEventListener('click', function(e) {
        // ボタンクリック時は無視
        if (e.target.closest('a, button')) {
            return;
        }
        
        const detailLink = this.querySelector('a[href*="/result/"]');
        if (detailLink) {
            window.location.href = detailLink.href;
        }
    });
});

/**
 * 検索フォームのリアルタイムバリデーション
 */
const searchInputs = document.querySelectorAll('input[name="name"], select[name="type"]');
searchInputs.forEach(input => {
    input.addEventListener('input', function() {
        const form = this.closest('form');
        const hasValue = Array.from(searchInputs).some(inp => inp.value.trim() !== '');
        
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = !hasValue;
        }
    });
});

/**
 * MBTIタイプのカラーマッピング
 */
const mbtiColors = {
    'INTJ': '#6f42c1', 'INTP': '#6610f2', 'ENTJ': '#d63384', 'ENTP': '#dc3545',
    'INFJ': '#fd7e14', 'INFP': '#ffc107', 'ENFJ': '#198754', 'ENFP': '#20c997',
    'ISTJ': '#0dcaf0', 'ISFJ': '#0d6efd', 'ESTJ': '#6c757d', 'ESFJ': '#adb5bd',
    'ISTP': '#495057', 'ISFP': '#343a40', 'ESTP': '#212529', 'ESFP': '#f8f9fa'
};

/**
 * MBTIタイプバッジに色を適用
 */
document.querySelectorAll('.badge').forEach(badge => {
    const text = badge.textContent.trim();
    if (mbtiColors[text]) {
        badge.style.backgroundColor = mbtiColors[text];
    }
});

// デバッグ用のコンソールログ
console.log('MBTI診断アプリ - 初期化完了');
console.log('利用可能な機能: スクロールアニメーション, フォームバリデーション, プログレスバーアニメーション');


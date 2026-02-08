// 瀏覽次數統計：呼叫自己的 API（由 Vercel 轉發 CountAPI），每次打開網頁 +1
function initVisitorCount() {
    var el = document.getElementById('visitorCount');
    if (!el) return;
    el.textContent = '載入中…';
    var apiUrl = (typeof window !== 'undefined' && window.location.origin)
        ? window.location.origin + '/api/visit'
        : '/api/visit';
    fetch(apiUrl)
        .then(function(res) { return res.json(); })
        .then(function(data) {
            if (typeof data.value === 'number' && data.value >= 0) {
                // 若 API 回傳 0 可能是「剛建立」或「這次造訪已 +1 但回傳舊值」，至少顯示 1
                var n = data.value < 1 ? 1 : data.value;
                el.textContent = n.toLocaleString('zh-TW');
            } else {
                el.textContent = '—';
            }
        })
        .catch(function() {
            el.textContent = '—';
        });
}

// 頁面載入完成後的初始化
document.addEventListener('DOMContentLoaded', function() {
    initVisitorCount();
    // 為所有區塊添加動畫效果
    const sections = document.querySelectorAll('.section');
    
    // 使用 Intersection Observer 實現滾動動畫
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // 初始化所有區塊的樣式並開始觀察
    sections.forEach((section, index) => {
        section.style.opacity = '0';
        section.style.transform = 'translateY(20px)';
        section.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        section.style.transitionDelay = `${index * 0.1}s`;
        observer.observe(section);
    });

    // 為設備項目添加點擊效果
    const equipmentItems = document.querySelectorAll('.equipment-item');
    equipmentItems.forEach(item => {
        item.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // 為特工標籤添加點擊效果
    const agentBadges = document.querySelectorAll('.agent-badge');
    agentBadges.forEach(badge => {
        badge.addEventListener('click', function() {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = '';
            }, 150);
        });
    });

    // 處理品牌logo圖片載入
    const brandLogos = document.querySelectorAll('.brand-logo');
    brandLogos.forEach(logo => {
        logo.addEventListener('load', function() {
            const fallback = this.nextElementSibling;
            if (fallback && fallback.classList.contains('fallback-icon')) {
                fallback.style.display = 'none';
            }
        });
        logo.addEventListener('error', function() {
            this.style.display = 'none';
            const fallback = this.nextElementSibling;
            if (fallback && fallback.classList.contains('fallback-icon')) {
                fallback.style.display = 'block';
            }
        });
    });
});

// 添加頁面載入動畫
window.addEventListener('load', function() {
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    setTimeout(() => {
        document.body.style.opacity = '1';
    }, 100);
});

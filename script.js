// 牌位等級對應圖片
const RANK_TIER_MAP = {
    0: '0_牌階未定.png',
    3: '3_鐵牌1.png', 4: '4_鐵牌2.png', 5: '5_鐵牌3.png',
    6: '6_銅牌1.png', 7: '7_銅牌2.png', 8: '8_銅牌3.png',
    9: '9_銀牌1.png', 10: '10_銀牌2.png', 11: '11_銀牌3.png',
    12: '12_金牌1.png', 13: '13_金牌2.png', 14: '14_金牌3.png',
    15: '15_白金1.png', 16: '16_白金2.png', 17: '17_白金3.png',
    18: '18_鑽石1.png', 19: '19_鑽石2.png', 20: '20_鑽石3.png',
    21: '21_超凡入聖1.png', 22: '22_超凡入聖2.png', 23: '23_超凡入聖3.png',
    24: '24_神話1.png', 25: '25_神話2.png', 26: '26_神話3.png',
    27: '27_輻能戰魂.png'
};

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

// 自動更新牌位資料
function updateRanks() {
    const accountItems = document.querySelectorAll('.account-item');
    
    // 顯示載入狀態
    accountItems.forEach(item => {
        const rankBadges = item.querySelectorAll('.rank-badge span');
        rankBadges.forEach(badge => {
            badge.textContent = '載入中...';
            badge.style.opacity = '0.5';
        });
    });
    
    // 從 Vercel API 獲取即時牌位
    const apiUrl = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
        ? 'http://localhost:8080/api/my-ranks'  // 本地開發
        : '/api/ranks';  // Vercel 部署
    
    fetch(apiUrl)
        .then(res => res.json())
        .then(data => {
            if (data.accounts && Array.isArray(data.accounts)) {
                // 更新在線狀態（使用第一個帳號的狀態）
                if (data.accounts.length > 0) {
                    updateOnlineStatus(data.accounts[0]);
                }
                
                data.accounts.forEach((account, index) => {
                    if (index < accountItems.length) {
                        updateAccountDisplay(accountItems[index], account);
                    }
                });
            }
        })
        .catch(error => {
            console.error('無法獲取牌位資料:', error);
            // 發生錯誤時恢復原始顯示
            accountItems.forEach(item => {
                const rankBadges = item.querySelectorAll('.rank-badge span');
                rankBadges.forEach(badge => {
                    badge.style.opacity = '1';
                });
            });
            updateOnlineStatus({ is_online: false });
        });
}

// 更新在線狀態
function updateOnlineStatus(accountData) {
    const statusElement = document.getElementById('onlineStatus');
    if (!statusElement) return;
    
    const indicator = statusElement.querySelector('.status-indicator');
    const text = statusElement.querySelector('.status-text');
    
    // 移除所有狀態類別
    statusElement.classList.remove('online', 'offline', 'in-game');
    
    if (accountData.is_online) {
        statusElement.classList.add('online');
        text.textContent = '在線';
    } else {
        statusElement.classList.add('offline');
        text.textContent = '離線';
    }
}

// 更新單個帳號的顯示
function updateAccountDisplay(accountItem, accountData) {
    if (accountData.error) {
        console.error(`${accountData.display_name}: ${accountData.error}`);
        const rankBadges = accountItem.querySelectorAll('.rank-badge span');
        rankBadges.forEach(badge => {
            badge.textContent = '無法載入';
            badge.style.opacity = '1';
        });
        return;
    }
    
    // 更新當前牌位
    const currentRankBadge = accountItem.querySelector('.current-rank .rank-badge');
    if (currentRankBadge) {
        const rankIcon = currentRankBadge.querySelector('.rank-icon');
        const rankText = currentRankBadge.querySelector('span');
        
        if (rankIcon && accountData.current_tier) {
            const iconPath = RANK_TIER_MAP[accountData.current_tier] || RANK_TIER_MAP[0];
            rankIcon.src = `配備圖片/${iconPath}`;
            rankIcon.style.display = 'block';
        }
        
        if (rankText) {
            rankText.textContent = accountData.current_rank;
            rankText.style.opacity = '1';
            
            // 顯示 RR 分數
            if (accountData.rr !== undefined) {
                rankText.textContent = `${accountData.current_rank} (${accountData.rr} RR)`;
            }
        }
    }
    
    // 更新最高牌位
    const peakRankBadge = accountItem.querySelector('.peak-rank .rank-badge');
    if (peakRankBadge) {
        const rankIcon = peakRankBadge.querySelector('.rank-icon');
        const rankText = peakRankBadge.querySelector('span');
        
        if (rankIcon && accountData.peak_tier) {
            const iconPath = RANK_TIER_MAP[accountData.peak_tier] || RANK_TIER_MAP[0];
            rankIcon.src = `配備圖片/${iconPath}`;
            rankIcon.style.display = 'block';
        }
        
        if (rankText) {
            rankText.textContent = accountData.peak_rank;
            rankText.style.opacity = '1';
        }
    }
    
    // 添加動畫效果
    accountItem.style.animation = 'rankUpdate 0.5s ease';
    setTimeout(() => {
        accountItem.style.animation = '';
    }, 500);
}

// 頁面載入完成後的初始化
document.addEventListener('DOMContentLoaded', function() {
    initVisitorCount();
    updateRanks(); // 自動更新牌位
    
    // 每5分鐘自動更新一次牌位
    setInterval(updateRanks, 5 * 60 * 1000);
    
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

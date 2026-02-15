// Vercel Serverless Function - 獲取 VALORANT 牌位
const https = require('https');

const HENRIK_BASE = 'https://api.henrikdev.xyz/valorant';

// 你的帳號設定
const ACCOUNTS = [
    { region: 'ap', name: 'Hex Strike', tag: '都是土豆', displayName: 'Hex Strike#都是土豆' },
    { region: 'ap', name: 'ChenYou', tag: '1227', displayName: 'ChenYou#1227' }
];

// 牌位等級對應
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

function httpsGet(url) {
    return new Promise((resolve, reject) => {
        https.get(url, (res) => {
            let data = '';
            res.on('data', (chunk) => { data += chunk; });
            res.on('end', () => {
                try {
                    resolve(JSON.parse(data));
                } catch (e) {
                    reject(e);
                }
            });
        }).on('error', reject);
    });
}

async function fetchAccountRank(account, apiKey) {
    try {
        const encodedName = encodeURIComponent(account.name);
        const encodedTag = encodeURIComponent(account.tag);
        
        // 獲取 MMR 資料
        const mmrUrl = `${HENRIK_BASE}/v3/mmr/${account.region}/${encodedName}/${encodedTag}?api_key=${apiKey}`;
        const mmrData = await httpsGet(mmrUrl);
        
        if (mmrData.status !== 200 || !mmrData.data) {
            return {
                display_name: account.displayName,
                error: '無法獲取牌位資料'
            };
        }
        
        const currentData = mmrData.data.current_data || {};
        const highestRank = mmrData.data.highest_rank || {};
        
        return {
            display_name: account.displayName,
            current_rank: currentData.currenttier_patched || currentData.currenttier || '未定',
            current_tier: currentData.currenttier || 0,
            rr: currentData.ranking_in_tier || 0,
            peak_rank: highestRank.patched_tier || highestRank.currenttier_patched || '未定',
            peak_tier: highestRank.tier || 0,
            elo: currentData.elo || 0,
            mmr_change: currentData.mmr_change_to_last_game || 0
        };
    } catch (error) {
        return {
            display_name: account.displayName,
            error: error.message || '獲取資料時發生錯誤'
        };
    }
}

module.exports = async (req, res) => {
    // 設定 CORS
    res.setHeader('Access-Control-Allow-Origin', '*');
    res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
    res.setHeader('Access-Control-Allow-Headers', 'Content-Type');
    
    if (req.method === 'OPTIONS') {
        return res.status(200).end();
    }
    
    if (req.method !== 'GET') {
        return res.status(405).json({ error: '只支援 GET 請求' });
    }
    
    // 從環境變數獲取 API Key
    const apiKey = process.env.HENRIK_API_KEY;
    
    if (!apiKey) {
        return res.status(500).json({ 
            error: '未設定 HENRIK_API_KEY 環境變數',
            message: '請在 Vercel 專案設定中加入 HENRIK_API_KEY'
        });
    }
    
    try {
        // 並行獲取所有帳號的牌位
        const results = await Promise.all(
            ACCOUNTS.map(account => fetchAccountRank(account, apiKey))
        );
        
        res.status(200).json({ 
            accounts: results,
            timestamp: new Date().toISOString()
        });
    } catch (error) {
        res.status(500).json({ 
            error: '伺服器錯誤',
            message: error.message 
        });
    }
};


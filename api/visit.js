// Vercel Serverless：轉發計數 API，每次 GET +1 並回傳次數（避免瀏覽器 CORS）
// 使用穩定替代：countapi.mileshilliard.com（CountAPI.xyz 可能不穩）
const https = require('https');

const COUNTER_KEY = 'chenyou-about-me-visits';
const HIT_API = `https://countapi.mileshilliard.com/api/v1/hit/${COUNTER_KEY}`;

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

module.exports = async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-store');

  try {
    const data = await httpsGet(HIT_API);
    // 此 API 回傳 value 可能是字串
    const raw = data.value;
    const value = typeof raw === 'number' ? raw : parseInt(raw, 10);
    if (!Number.isNaN(value) && value >= 0) {
      res.status(200).json({ value });
    } else {
      res.status(502).json({ error: true });
    }
  } catch (e) {
    res.status(500).json({ error: true });
  }
}

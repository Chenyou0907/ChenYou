// Vercel Serverless：轉發 CountAPI，避免瀏覽器 CORS，每次 GET 會 +1 並回傳次數
const COUNT_API = 'https://api.countapi.xyz/hit/chenyou/about-me';

export default async function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Cache-Control', 'no-store');

  try {
    const r = await fetch(COUNT_API);
    const data = await r.json();
    const value = typeof data.value === 'number' ? data.value : 0;
    res.status(200).json({ value });
  } catch (e) {
    res.status(500).json({ value: 0 });
  }
}

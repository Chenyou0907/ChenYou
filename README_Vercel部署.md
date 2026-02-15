# 部署到 Vercel - 自動更新牌位

## 🚀 快速部署步驟

### 1. 準備 API Key
1. 加入 HenrikDev Discord：https://discord.gg/henrikdev
2. 前往 `#get-a-key` 頻道獲取免費 API Key

### 2. 部署到 Vercel

#### 方法一：使用 Vercel CLI（推薦）
```bash
# 安裝 Vercel CLI
npm install -g vercel

# 登入 Vercel
vercel login

# 部署專案
vercel

# 設定環境變數
vercel env add HENRIK_API_KEY

# 重新部署以套用環境變數
vercel --prod
```

#### 方法二：使用 Vercel 網頁介面
1. 前往 https://vercel.com
2. 點擊「New Project」
3. 匯入你的 GitHub 儲存庫（或直接上傳資料夾）
4. 在「Environment Variables」中加入：
   - Name: `HENRIK_API_KEY`
   - Value: `你的API_KEY`
5. 點擊「Deploy」

### 3. 修改帳號設定（可選）

如果要修改追蹤的帳號，編輯 `api/ranks.js` 的第 6-9 行：

```javascript
const ACCOUNTS = [
    { region: 'ap', name: '你的名字', tag: '你的TAG', displayName: '顯示名稱#TAG' },
    { region: 'ap', name: '第二個帳號', tag: 'TAG', displayName: '顯示名稱#TAG' }
];
```

支援的 region：
- `ap` - 亞太/台服
- `na` - 北美
- `eu` - 歐洲
- `kr` - 韓國
- `br` - 巴西
- `latam` - 拉丁美洲

## 📁 專案結構

```
關於我/
├── api/
│   ├── visit.js          # 瀏覽次數統計
│   └── ranks.js          # 牌位查詢 API（新增）
├── 配備圖片/
├── index.html
├── script.js
├── styles.css
└── vercel.json           # Vercel 設定檔（新增）
```

## ✨ 功能說明

### 自動切換 API 端點
- **本地開發**：使用 `http://localhost:8080/api/my-ranks`
- **Vercel 部署**：使用 `/api/ranks`

### 顯示內容
每個帳號會顯示：
- ✅ 當前牌位 + RR 分數
- ✅ 最高牌位
- ✅ 對應的牌位圖示
- ✅ 自動更新（每 5 分鐘）

## 🔧 本地測試

### 測試 Vercel Function（本地）
```bash
# 安裝 Vercel CLI
npm install -g vercel

# 設定環境變數
$env:HENRIK_API_KEY="你的API_KEY"

# 本地運行 Vercel 開發伺服器
vercel dev
```

然後開啟 http://localhost:3000

### 測試 Python 後端（本地）
```bash
# 設定環境變數
$env:HENRIK_API_KEY="你的API_KEY"

# 啟動 Python 伺服器
python valorant_rank_server.py
```

然後開啟 `index.html`

## 🌐 部署後檢查

1. **檢查 API 是否正常**：
   訪問 `https://你的網域.vercel.app/api/ranks`
   應該會看到 JSON 格式的牌位資料

2. **檢查環境變數**：
   在 Vercel Dashboard → Settings → Environment Variables
   確認 `HENRIK_API_KEY` 已設定

3. **查看部署日誌**：
   在 Vercel Dashboard → Deployments → 點擊最新部署
   查看是否有錯誤訊息

## ⚠️ 注意事項

### API 使用限制
- 免費版 API Key：每分鐘 30 次請求
- 網站每 5 分鐘自動更新一次（不會超過限制）

### 安全性
- ✅ API Key 儲存在 Vercel 環境變數中（安全）
- ✅ 不會暴露在前端程式碼中
- ❌ 不要將 API Key 寫在程式碼裡並上傳到 GitHub

### 快取
Vercel 會自動快取 API 回應，可以在 `api/ranks.js` 中加入：

```javascript
res.setHeader('Cache-Control', 's-maxage=300, stale-while-revalidate');
```

這樣可以減少 API 呼叫次數。

## 🐛 疑難排解

### 問題：部署後顯示「載入中...」不會消失
**解決方法**：
1. 開啟瀏覽器開發者工具（F12）
2. 查看 Console 是否有錯誤
3. 查看 Network 標籤，檢查 `/api/ranks` 請求狀態
4. 確認 Vercel 環境變數是否正確設定

### 問題：API 回傳 500 錯誤
**解決方法**：
1. 檢查 Vercel 部署日誌
2. 確認 `HENRIK_API_KEY` 環境變數已設定
3. 測試 API Key 是否有效

### 問題：顯示「無法獲取牌位資料」
**解決方法**：
1. 確認帳號名稱和 TAG 正確
2. 確認該帳號已打過積分賽
3. 確認 region 設定正確（台灣用 `ap`）

## 📊 監控與優化

### 查看 API 使用情況
在 Vercel Dashboard → Analytics 可以看到：
- API 呼叫次數
- 回應時間
- 錯誤率

### 優化建議
1. 啟用快取減少 API 呼叫
2. 調整自動更新間隔（目前是 5 分鐘）
3. 考慮使用 Vercel Edge Functions 提升速度

## 🎉 完成！

部署完成後，你的網站會自動從 VALORANT API 獲取即時牌位資料！

網站網址：`https://你的專案名稱.vercel.app`


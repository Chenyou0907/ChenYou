# 自動更新牌位功能

## 功能說明
你的自我介紹網站現在可以自動從 VALORANT API 獲取即時牌位資料！

## 設定步驟

### 1. 獲取 API Key
1. 加入 HenrikDev Discord 伺服器：https://discord.gg/henrikdev
2. 前往 `#get-a-key` 頻道
3. 輸入指令獲取免費 API Key

### 2. 設定環境變數
在 Windows PowerShell 中執行：
```powershell
$env:HENRIK_API_KEY="你的API_KEY"
```

或在 Windows CMD 中執行：
```cmd
set HENRIK_API_KEY=你的API_KEY
```

### 3. 啟動後端伺服器
```bash
python valorant_rank_server.py
```

伺服器會在 `http://localhost:8080` 啟動

### 4. 開啟網站
在瀏覽器中打開 `index.html`，牌位資料會自動載入！

## 功能特色

✅ **自動更新**：頁面載入時自動獲取最新牌位
✅ **定時刷新**：每 5 分鐘自動更新一次
✅ **顯示 RR 分數**：顯示當前階級內的分數
✅ **動畫效果**：更新時有流暢的動畫
✅ **錯誤處理**：API 失敗時顯示友善提示

## 顯示內容

每個帳號會顯示：
- 當前牌位 + RR 分數
- 最高牌位
- 對應的牌位圖示

## 修改帳號

如果要修改追蹤的帳號，編輯 `valorant_rank_server.py` 的第 68-71 行：

```python
accounts = [
    {"region": "ap", "name": "你的名字", "tag": "你的TAG", "display_name": "顯示名稱#TAG"},
    {"region": "ap", "name": "第二個帳號", "tag": "TAG", "display_name": "顯示名稱#TAG"}
]
```

## 部署到線上

如果要部署到 Vercel 或其他平台：
1. 在平台的環境變數設定中加入 `HENRIK_API_KEY`
2. 確保後端 API 可以被前端訪問
3. 修改 `script.js` 中的 API 網址（第 54 行）

## 注意事項

⚠️ API Key 有使用次數限制（免費版通常是每分鐘 30 次）
⚠️ 不要將 API Key 上傳到公開的 GitHub 儲存庫
⚠️ 後端伺服器需要保持運行才能獲取資料

## 疑難排解

**問題：顯示「載入中...」不會消失**
- 檢查後端伺服器是否正在運行
- 檢查瀏覽器控制台是否有錯誤訊息
- 確認 API Key 是否正確設定

**問題：顯示「無法載入」**
- 確認帳號名稱和 TAG 是否正確
- 確認該帳號已經打過積分賽
- 檢查 API Key 是否有效

**問題：圖示無法顯示**
- 確認 `配備圖片/` 資料夾中有對應的牌位圖片
- 檢查圖片檔名是否正確


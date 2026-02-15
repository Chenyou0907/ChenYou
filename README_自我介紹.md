# 特戰英豪 自我介紹

填寫 **擅長特務、偏愛武器、電腦配備、帳號名字、牌位**，產生自我介紹卡。**牌位、特務、武器會從 `valorant_assets` 顯示圖片**（需先執行 `fetch_valorant_assets.py` 抓取）。資料存於瀏覽器本機，無需後端。

---

## 使用方式

**直接以瀏覽器開啟** `valorant_intro.html` 即可（與 `valorant_assets` 同一層）。

1. 填寫各欄位（或編輯程式碼內的 `CODE_DATA` 後按「從程式碼載入」）
2. 點「儲存並更新預覽」
3. 下方介紹卡會顯示 **特務頭像、武器圖、牌位圖**；重新開啟會載入上次儲存

---

## 在程式碼改資料

打開 `valorant_intro.html`，在 `<script>` 最上方找到 **`CODE_DATA`**，直接改 `account`、`rank`、`agents`、`weapons`、`pc`。存檔後在網頁按 **「從程式碼載入」** 即套用。首次開啟且尚未存過任何內容時，也會自動用 `CODE_DATA` 當預設。

---

## 圖片來源（valorant_assets）

- **擅長特務**：`valorant_assets/agents/{名稱}/icon.png`
- **偏愛武器**：`valorant_assets/weapons/{名稱}.png`
- **牌位**：`valorant_assets/competitivetiers/{檔名}.png`

請先執行 `python fetch_valorant_assets.py` 產生 `valorant_assets`（特務、武器、competitivetiers）。  
擅長特務、武器可填 **英文**（如 Jett、Vandal）或 **中文**（如 婕提、重砲），程式會對應到 fetch 時用的名稱。

---

## 欄位說明

| 欄位 | 說明 |
|------|------|
| **帳號名字** | Riot ID，例：玩家名#TAG1 |
| **牌位** | 從選單選擇，或選「其他」自填 |
| **擅長特務** | 每行一個，或頓號、逗號分隔；例：婕提、聖祈、歐門 或 Jett、Sage、Omen |
| **偏愛武器** | 例：重砲、幻象、警長 或 Vandal、Phantom、Sheriff |
| **電腦配備** | 自由填寫 CPU、GPU、RAM、螢幕、滑鼠、鍵盤等 |

---

## 儲存

- 資料存在瀏覽器的 **localStorage**
- 清除瀏覽資料或無痕模式時需重新填寫或從程式碼載入

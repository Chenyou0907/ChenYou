# 特戰英豪 (Valorant) 元素圖抓取

從 [valorant-api.com](https://valorant-api.com) 下載遊戲素材，包含：

| 類別 | 內容 |
|------|------|
| **agents** | 特務頭像、半身、全身、技能圖示、職責圖示 |
| **weapons** | 武器圖示 |
| **weapon_skins** | 武器造型（全部） |
| **maps** | 地圖圖示、橫幅、列表圖 |
| **playercards** | 玩家名牌 |
| **sprays** | 噴漆 |
| **buddies** | 武器吊飾 |
| **competitivetiers** | 競技牌位圖示 |

## 使用方式

1. 安裝依賴：
   ```
   pip install -r requirements.txt
   ```

2. 執行腳本：
   ```
   python fetch_valorant_assets.py
   ```

3. 圖片會存到 `valorant_assets` 資料夾，依類型分子資料夾。

## 注意

- 素材來自非官方 API，僅供個人、非商業使用，請遵守 Riot 使用規範。
- 若只要部分類型，可編輯 `fetch_valorant_assets.py` 的 `main()`，註解掉不需要的 `fetch_*` 呼叫。
- 武器造型預設抓全部；若不想抓造型可改 `fetch_weapon_skins(0)`，或改 `fetch_weapon_skins(10)` 限制每種武器數量。

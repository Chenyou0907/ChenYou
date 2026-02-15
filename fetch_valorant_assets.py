# -*- coding: utf-8 -*-
"""
特戰英豪 (Valorant) 元素圖抓取腳本
使用 valorant-api.com 非官方 API 下載特務、武器、地圖等遊戲素材
"""

import os
import re
import requests
from pathlib import Path
from urllib.parse import urlparse

# 儲存目錄（與腳本同層的 valorant_assets 資料夾）
BASE_URL = "https://valorant-api.com/v1"
OUTPUT_DIR = Path(__file__).resolve().parent / "valorant_assets"


def sanitize_filename(name: str) -> str:
    """將字串轉成安全的檔案名"""
    name = re.sub(r'[<>:"/\\|?*]', "_", str(name))
    return name.strip() or "unnamed"


def download_image(url: str, filepath: Path) -> bool:
    """下載圖片到指定路徑，跳過空 URL"""
    if not url or not url.startswith("http"):
        return False
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "wb") as f:
            f.write(r.content)
        print(f"  ✓ {filepath.name}")
        return True
    except Exception as e:
        print(f"  ✗ {filepath.name}: {e}")
        return False


def fetch_json(endpoint: str, params: dict = None) -> dict:
    """取得 API JSON，可選 language=zh-TW"""
    url = f"{BASE_URL}/{endpoint}"
    params = params or {}
    if "language" not in params:
        params["language"] = "zh-TW"
    try:
        r = requests.get(url, params=params, timeout=15)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        print(f"  API 錯誤 {endpoint}: {e}")
        return {"status": 0}


def fetch_agents():
    """特務：頭像、半身、全身、技能圖示、職責圖示"""
    print("\n--- 特務 (Agents) ---")
    data = fetch_json("agents")
    if data.get("status", 200) != 200:
        return
    root = OUTPUT_DIR / "agents"
    for a in data.get("data", []):
        if not a.get("isPlayableCharacter", True):
            continue
        name = sanitize_filename(a.get("displayName", "unknown"))
        sub = root / name

        for key, fname in [
            ("displayIcon", "icon.png"),
            ("bustPortrait", "bust.png"),
            ("fullPortrait", "full.png"),
            ("background", "background.png"),
        ]:
            url = a.get(key)
            if url:
                download_image(url, sub / fname)

        role = a.get("role") or {}
        if role.get("displayIcon"):
            download_image(role["displayIcon"], sub / "role.png")

        for ab in a.get("abilities", []) or []:
            url = ab.get("displayIcon")
            if not url:
                continue
            slot = sanitize_filename(ab.get("slot", "ability"))
            download_image(url, sub / "abilities" / f"{slot}.png")


def fetch_weapons():
    """武器：圖示、造型（可選，數量多）"""
    print("\n--- 武器 (Weapons) ---")
    data = fetch_json("weapons")
    if data.get("status", 200) != 200:
        return
    root = OUTPUT_DIR / "weapons"
    for w in data.get("data", []) or []:
        name = sanitize_filename(w.get("displayName", "unknown"))
        url = w.get("displayIcon")
        if url:
            download_image(url, root / f"{name}.png")

    # 可選：只下載「預設造型」的武器圖，避免太多
    # 上面已用 displayIcon，通常已是預設圖


def fetch_weapon_skins(limit_per_weapon=None):
    """武器造型：抓取所有造型的展示圖。limit_per_weapon=None 表示全部，0=跳過，正整數=每種武器最多幾個。"""
    print("\n--- 武器造型 (Skins，全部) ---")
    data = fetch_json("weapons")
    if data.get("status", 200) != 200:
        return
    root = OUTPUT_DIR / "weapon_skins"
    for w in data.get("data", []) or []:
        wname = sanitize_filename(w.get("displayName", "unknown"))
        skins = w.get("skins") or []
        if limit_per_weapon is not None:
            skins = skins[:limit_per_weapon]
        for s in skins:
            if not s.get("displayIcon"):
                continue
            sname = sanitize_filename(s.get("displayName", "skin"))
            uuid = (s.get("uuid") or "")[:8]
            fname = f"{sname}_{uuid}.png" if uuid else f"{sname}.png"
            download_image(s.get("displayIcon"), root / wname / fname)


def fetch_maps():
    """地圖：圖示、橫幅、座標圖"""
    print("\n--- 地圖 (Maps) ---")
    data = fetch_json("maps")
    if data.get("status", 200) != 200:
        return
    root = OUTPUT_DIR / "maps"
    for m in data.get("data", []) or []:
        name = sanitize_filename(m.get("displayName", "unknown"))
        sub = root / name
        for key, fname in [
            ("displayIcon", "icon.png"),
            ("splash", "splash.png"),
            ("listViewIcon", "list.png"),
        ]:
            url = m.get(key)
            if url:
                download_image(url, sub / fname)


def fetch_playercards():
    """玩家名牌"""
    print("\n--- 玩家名牌 (Player Cards) ---")
    data = fetch_json("playercards")
    if data.get("status", 200) != 200:
        return
    root = OUTPUT_DIR / "playercards"
    for c in data.get("data", []) or []:
        name = sanitize_filename(c.get("displayName", "unknown"))
        sub = root / name
        for key, fname in [("smallArt", "small.png"), ("largeArt", "large.png"), ("displayIcon", "icon.png")]:
            url = c.get(key)
            if url:
                download_image(url, sub / fname)


def fetch_sprays():
    """噴漆"""
    print("\n--- 噴漆 (Sprays) ---")
    data = fetch_json("sprays")
    if data.get("status", 200) != 200:
        return
    root = OUTPUT_DIR / "sprays"
    for s in data.get("data", []) or []:
        url = s.get("displayIcon") or s.get("fullTransparentIcon")
        if not url:
            continue
        name = sanitize_filename(s.get("displayName", "unknown"))
        download_image(url, root / f"{name}.png")


def fetch_buddies():
    """武器吊飾"""
    print("\n--- 武器吊飾 (Buddies) ---")
    data = fetch_json("buddies")
    if data.get("status", 200) != 200:
        return
    root = OUTPUT_DIR / "buddies"
    for b in data.get("data", []) or []:
        url = b.get("displayIcon")
        if not url:
            continue
        name = sanitize_filename(b.get("displayName", "unknown"))
        download_image(url, root / f"{name}.png")


def fetch_competitive_tiers():
    """競技牌位圖示"""
    print("\n--- 競技牌位 (Competitive Tiers) ---")
    data = fetch_json("competitivetiers")
    if data.get("status", 200) != 200:
        return
    root = OUTPUT_DIR / "competitivetiers"
    for t in data.get("data", []) or []:
        for tier in t.get("tiers", []) or []:
            url = tier.get("largeIcon") or tier.get("smallIcon")
            if not url:
                continue
            num = tier.get("tier", 0)
            name = sanitize_filename(tier.get("tierName", f"tier_{num}"))
            download_image(url, root / f"{num}_{name}.png")


def main():
    print("特戰英豪 (Valorant) 元素圖抓取")
    print("來源: valorant-api.com")
    print("輸出: ", OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    fetch_agents()
    fetch_weapons()
    fetch_maps()
    fetch_playercards()
    fetch_sprays()
    fetch_buddies()
    fetch_competitive_tiers()

    # 造型：None = 全部，設 0 可跳過，設數字則限制每種武器數量
    fetch_weapon_skins(limit_per_weapon=None)

    print("\n完成。圖片已儲存至:", OUTPUT_DIR.resolve())


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-
"""
特戰英豪 (Valorant) 牌位查詢
輸入伺服器 + 遊戲名 + Tag，查詢帳號牌位、等級等（使用 HenrikDev 非官方 API）
"""

import argparse
import os
import re
import sys
from typing import Optional, Tuple

import requests

HENRIK_BASE = "https://api.henrikdev.xyz/valorant"

# 伺服器代碼對照（不區分大小寫）
REGION_ALIAS = {
    "ap": "ap", "亞太": "ap", "台服": "ap", "台灣": "ap", "apac": "ap",
    "na": "na", "北美": "na", "美服": "na", "americas": "na",
    "eu": "eu", "歐洲": "eu", "歐服": "eu", "europe": "eu",
    "kr": "kr", "韓服": "kr", "韓國": "kr", "korea": "kr",
    "br": "br", "巴西": "br", "brazil": "br",
    "latam": "latam", "拉丁": "latam", "拉丁美洲": "latam",
}


def normalize_region(s: str) -> Optional[str]:
    s = (s or "").strip().lower()
    return REGION_ALIAS.get(s) or (s if s in ("ap", "na", "eu", "kr", "br", "latam") else None)


def parse_riot_id(s: str) -> Optional[Tuple[str, str]]:
    """解析 "Name#TAG" 或 "Name # TAG" -> (name, tag)。若無 # 則回傳 None。"""
    s = (s or "").strip()
    if "#" in s:
        parts = s.split("#", 1)
        name, tag = parts[0].strip(), (parts[1] or "").strip()
        if name and tag:
            return (name, tag)
    return None


def get_api_key() -> Optional[str]:
    return os.environ.get("HENRIK_API_KEY", "").strip() or None


def _req(method: str, path: str, api_key: Optional[str], **kwargs) -> requests.Response:
    url = f"{HENRIK_BASE}{path}"
    params = dict(kwargs.pop("params", {}))
    if api_key:
        params["api_key"] = api_key
    return requests.request(method, url, timeout=15, params=params or None, **kwargs)


def fetch_account(name: str, tag: str, api_key: Optional[str]) -> Optional[dict]:
    """GET /v1/account/{name}/{tag} 取得 puuid、account_level、region 等"""
    name = requests.utils.quote(name, safe="")
    tag = requests.utils.quote(tag, safe="")
    r = _req("GET", f"/v1/account/{name}/{tag}", api_key)
    if r.status_code != 200:
        return None
    try:
        j = r.json()
    except Exception:
        return None
    if j.get("status") != 200:
        return None
    return j.get("data")


def fetch_mmr(region: str, name: str, tag: str, api_key: Optional[str]) -> Optional[dict]:
    """GET /v3/mmr/{region}/{name}/{tag} 取得牌位、RR、ELO、上場變動等"""
    name = requests.utils.quote(name, safe="")
    tag = requests.utils.quote(tag, safe="")
    r = _req("GET", f"/v3/mmr/{region}/{name}/{tag}", api_key)
    if r.status_code != 200:
        return None
    try:
        j = r.json()
    except Exception:
        return None
    if j.get("status") != 200:
        return None
    return j.get("data")


def run(region: str, name: str, tag: str, api_key: Optional[str]) -> int:
    region = normalize_region(region)
    if not region:
        print("錯誤：不支援的伺服器，請用 ap / 亞太 / 台服、na / 北美、eu / 歐服、kr / 韓服、br / 拉丁、latam")
        return 1

    if not name or not tag:
        print("錯誤：請提供 遊戲名 與 Tag（可用 Name#TAG 或分開）")
        return 1

    if not api_key:
        print("提示：未設定 HENRIK_API_KEY，若 401 請至 HenrikDev Discord #get-a-key 取得免費 Key")
        print("      設定： set HENRIK_API_KEY=你的key  或  --api-key 你的key\n")

    # 1) 帳號
    acc = fetch_account(name, tag, api_key)
    if acc:
        lv = acc.get("account_level") or acc.get("level")
        print(f"--- 帳號 ---")
        print(f"  Riot ID: {acc.get('name', name)}#{acc.get('tag', tag)}")
        print(f"  帳號等級: {lv or '-'}")
        print(f"  Region: {acc.get('region', '-')}")
        print()
    else:
        print("（無法取得帳號資訊，請確認 Name#Tag 正確且已設 API Key）\n")

    # 2) 牌位
    mmr = fetch_mmr(region, name, tag, api_key)
    if not mmr:
        # 再試一次用 account 回傳的 region（若有的話）當備援
        alt_region = (acc or {}).get("region")
        if alt_region and normalize_region(alt_region):
            mmr = fetch_mmr(normalize_region(alt_region) or region, name, tag, api_key)
        if not mmr:
            print("無法取得牌位（請確認：1) 伺服器、Name#Tag 正確  2) 已打過積分  3) 已設定 API Key；401 表示需 Key）")
            return 1

    cur = (mmr.get("current_data") or {}) if isinstance(mmr.get("current_data"), dict) else {}
    rank = cur.get("currenttier_patched") or cur.get("currenttier") or "-"
    rr = cur.get("ranking_in_tier")
    rr_str = str(rr) if rr is not None else "-"
    elo = cur.get("elo")
    elo_str = str(elo) if elo is not None else "-"
    change = cur.get("mmr_change_to_last_game")
    if change is not None:
        change_str = f"+{change}" if change >= 0 else str(change)
    else:
        change_str = "-"

    peak = mmr.get("highest_rank", {}) if isinstance(mmr.get("highest_rank"), dict) else mmr.get("highest_rank") or {}
    if isinstance(peak, dict):
        peak_patched = peak.get("patched_tier") or peak.get("currenttier_patched") or "-"
        peak_season = peak.get("season") or "-"
    else:
        peak_patched, peak_season = "-", "-"

    print("--- 牌位 ---")
    print(f"  當前牌位: {rank}")
    print(f"  階級內分數 (RR): {rr_str}")
    print(f"  ELO: {elo_str}")
    print(f"  上場變動: {change_str}")
    print(f"  最高牌位: {peak_patched}  (賽季: {peak_season})")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="特戰英豪：輸入伺服器 + 遊戲名 + Tag 查牌位")
    ap.add_argument("--region", "-r", help="伺服器：ap/亞太/台服、na、eu、kr、br、latam")
    ap.add_argument("--name", "-n", help="遊戲名")
    ap.add_argument("--tag", "-t", help="Tag（# 後面的）")
    ap.add_argument("riot_id", nargs="?", help='可改為一組 "Name#TAG" 取代 --name 與 --tag')
    ap.add_argument("--api-key", "-k", help="HenrikDev API Key（或設 HENRIK_API_KEY）")
    args = ap.parse_args()

    api_key = (args.api_key or "").strip() or get_api_key()

    region = (args.region or "").strip()
    name = (args.name or "").strip()
    tag = (args.tag or "").strip()

    if args.riot_id:
        parsed = parse_riot_id(args.riot_id)
        if parsed:
            name, tag = parsed
        else:
            # 沒 # 就當成 name，tag 仍要另給
            if not name:
                name = args.riot_id.strip()

    if not region or not name or not tag:
        print("範例：")
        print('  python valorant_rank_lookup.py -r ap -n 玩家名 -t TAG1')
        print('  python valorant_rank_lookup.py -r 台服 "玩家名#TAG1"')
        print("  set HENRIK_API_KEY=你的key  （需至 HenrikDev Discord #get-a-key 取得）\n")
        region = region or input("伺服器 (ap/亞太/台服/na/eu/kr/br/latam): ").strip()
        if not name or not tag:
            rid = input('Riot ID (Name#TAG 或只打名字後續再輸 Tag): ').strip()
            p = parse_riot_id(rid)
            if p:
                name, tag = p
            elif rid:
                name = name or rid
            if not tag:
                tag = input("Tag: ").strip()

    return run(region, name, tag, api_key)


if __name__ == "__main__":
    sys.exit(main())

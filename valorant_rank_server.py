# -*- coding: utf-8 -*-
"""
特戰英豪 牌位查詢 — 網頁版後端
執行後開啟 http://localhost:8080 使用 valorant_rank.html 查詢
"""

import os
from pathlib import Path

from flask import Flask, jsonify, request, send_from_directory

# 與 valorant_rank_lookup 同一目錄，可直接 import
from valorant_rank_lookup import fetch_account, fetch_mmr, normalize_region

app = Flask(__name__, static_folder=None)
ROOT = Path(__file__).resolve().parent


@app.route("/")
def index():
    return send_from_directory(ROOT, "valorant_rank.html")


@app.route("/api/lookup", methods=["POST"])
def lookup():
    try:
        body = request.get_json(force=True, silent=True) or {}
    except Exception:
        body = {}
    region = (body.get("region") or "").strip()
    name = (body.get("name") or "").strip()
    tag = (body.get("tag") or "").strip()
    api_key = (body.get("api_key") or "").strip() or os.environ.get("HENRIK_API_KEY", "").strip() or None

    if not name or not tag:
        return jsonify({"error": "請提供 遊戲名 與 Tag"}), 400

    reg = normalize_region(region)
    if not reg:
        return jsonify({"error": "不支援的伺服器，請用 ap/亞太/台服、na、eu、kr、br、latam"}), 400

    if not api_key:
        return jsonify({"error": "請在頁面下方輸入 API Key，或設定環境變數 HENRIK_API_KEY（至 HenrikDev Discord #get-a-key 取得）"}), 400

    acc = fetch_account(name, tag, api_key)
    mmr = fetch_mmr(reg, name, tag, api_key)
    if not mmr and acc:
        alt = normalize_region((acc.get("region") or ""))
        if alt:
            mmr = fetch_mmr(alt, name, tag, api_key)

    if not mmr:
        return jsonify({
            "error": "無法取得牌位，請確認：1) 伺服器、Name#Tag 正確 2) 已打過積分 3) API Key 有效（401 表示 Key 有誤或過期）"
        }), 200  # 200 + error 讓前端可顯示 error 文案

    return jsonify({"account": acc, "mmr": mmr})


@app.route("/api/my-ranks", methods=["GET"])
def my_ranks():
    """獲取預設帳號的牌位資料（用於自我介紹網站）"""
    api_key = os.environ.get("HENRIK_API_KEY", "").strip() or None
    
    if not api_key:
        return jsonify({"error": "未設定 HENRIK_API_KEY 環境變數"}), 500
    
    # 你的兩個帳號
    accounts = [
        {"region": "ap", "name": "Hex Strike", "tag": "都是土豆", "display_name": "Hex Strike#都是土豆"},
        {"region": "ap", "name": "ChenYou", "tag": "1227", "display_name": "ChenYou#1227"}
    ]
    
    results = []
    for account in accounts:
        try:
            acc = fetch_account(account["name"], account["tag"], api_key)
            mmr = fetch_mmr(account["region"], account["name"], account["tag"], api_key)
            
            if mmr:
                cur = (mmr.get("current_data") or {}) if isinstance(mmr.get("current_data"), dict) else {}
                peak = mmr.get("highest_rank", {}) if isinstance(mmr.get("highest_rank"), dict) else {}
                
                results.append({
                    "display_name": account["display_name"],
                    "current_rank": cur.get("currenttier_patched") or cur.get("currenttier") or "未定",
                    "current_tier": cur.get("currenttier", 0),
                    "rr": cur.get("ranking_in_tier", 0),
                    "peak_rank": peak.get("patched_tier") or peak.get("currenttier_patched") or "未定",
                    "peak_tier": peak.get("tier", 0),
                    "elo": cur.get("elo", 0),
                    "mmr_change": cur.get("mmr_change_to_last_game", 0)
                })
            else:
                results.append({
                    "display_name": account["display_name"],
                    "error": "無法獲取牌位資料"
                })
        except Exception as e:
            results.append({
                "display_name": account["display_name"],
                "error": str(e)
            })
    
    return jsonify({"accounts": results})


def main():
    port = int(os.environ.get("PORT", 8080))
    print("特戰英豪 牌位查詢 — 網頁版")
    print("請開啟: http://localhost:%d" % port)
    print("關閉: Ctrl+C\n")
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)


if __name__ == "__main__":
    main()

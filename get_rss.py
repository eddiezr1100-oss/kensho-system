import feedparser
import json
import os

def get_rss():
    # 懸賞生活のRSS
    RSS_URL = "https://www.knshow.com/index.xml"
    # feedparserはGASと違い、ブロックされにくいライブラリです
    feed = feedparser.parse(RSS_URL)
    
    results = []
    for entry in feed.entries:
        results.append({
            "title": entry.title,
            "link": entry.link,
            "date": entry.get("published", "不明")
        })
    
    # JSONとして保存（GASから読み取りやすい形式）
    with open("kensho_data.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"{len(results)} 件のデータを保存しました。")

if __name__ == "__main__":
    get_rss()
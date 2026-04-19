import feedparser
import json
import os
from datetime import datetime

# 調査対象のRSS（テスト用にYahoo!ニュースを設定）
RSS_URLS = [
    "https://news.yahoo.co.jp/rss/topics/it.xml",
]

# 保存するファイル名
DATA_FILE = "kensho_data.json"

def get_news():
    news_list = []
    
    for url in RSS_URLS:
        print(f"Checking: {url}")
        feed = feedparser.parse(url)
        
        for entry in feed.entries:
            # 必要な情報だけを抽出
            item = {
                "title": entry.title,
                "link": entry.link,
                "date": entry.published if hasattr(entry, 'published') else datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                "source": feed.feed.title if hasattr(feed.feed, 'title') else "Unknown"
            }
            news_list.append(item)

    return news_list

def save_to_json(data):
    # 既存のデータを読み込む（差分管理をしたい場合はここで処理）
    # 今回は確実に動作を確認するため、常に最新の20件を上書き保存します
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data[:20], f, ensure_ascii=False, indent=4)
    
    print(f"{len(data[:20])} 件のデータを保存しました。")

if __name__ == "__main__":
    results = get_news()
    if results:
        save_to_json(results)
    else:
        print("ニュースが見つかりませんでした。")
        # デバッグ用に空のリストを保存
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

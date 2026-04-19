import feedparser
import json
from datetime import datetime

# 2026年4月19日現在、確実にRSSが生きているサイトに絞り込み
RSS_URLS = [
    "https://www.ken-kaku.com/rss.xml",      # 懸賞当確
    "https://www.sample-fan.com/feed"        # サンプルファン
]

DATA_FILE = "kensho_data.json"

def get_kensho():
    items = []
    print(f"--- 懸賞スキャン開始: {datetime.now()} ---")
    
    for url in RSS_URLS:
        try:
            print(f"Checking: {url}")
            feed = feedparser.parse(url)
            for entry in feed.entries:
                items.append({
                    "title": entry.title,
                    "link": entry.link,
                    "date": entry.published if hasattr(entry, 'published') else "日付不明",
                    "source": feed.feed.title if hasattr(feed.feed, 'title') else url
                })
        except Exception as e:
            print(f"Error: {url} - {e}")
    return items

if __name__ == "__main__":
    results = get_kensho()
    if results:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(results[:30], f, ensure_ascii=False, indent=4)
        print(f"成功！ {len(results[:30])} 件の懸賞情報を保存しました。")
    else:
        print("有効な情報が見つかりませんでした。")

import feedparser
import json
import os
from datetime import datetime

# 偵察対象の懸賞サイトリスト（RSS対応サイトを一括登録）
RSS_URLS = [
    "https://www.knshow.com/index.xml",      # 懸賞生活
    "https://www.ken-kaku.com/rss.xml",      # 懸賞当確
    "https://kenshobox.net/feed/",           # 懸賞ボックス
    "https://prizm.jp/feed",                 # ぷりずむ
    "https://www.sample-fan.com/feed"        # サンプルファン
]

# 報告書（保存ファイル名）
DATA_FILE = "kensho_data.json"

def scan_all_kensho():
    all_kensho_items = []
    
    print(f"--- 懸賞情報の一括スキャン開始: {datetime.now()} ---")
    
    for url in RSS_URLS:
        try:
            print(f"Scanning: {url}")
            feed = feedparser.parse(url)
            
            # サイト名を取得
            source_name = feed.feed.title if hasattr(feed.feed, 'title') else url
            
            for entry in feed.entries:
                item = {
                    "title": entry.title,
                    "link": entry.link,
                    "date": entry.published if hasattr(entry, 'published') else "日付不明",
                    "source": source_name
                }
                all_kensho_items.append(item)
        except Exception as e:
            print(f"Error scanning {url}: {e}")

    return all_kensho_items

def save_report(data):
    # 最新の50件程度を保存（まずは量を確認するため多めに設定）
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data[:50], f, ensure_ascii=False, indent=4)
    
    print(f"--- スキャン完了: 合計 {len(data)} 件中、最新 {len(data[:50])} 件を保存しました ---")

if __name__ == "__main__":
    results = scan_all_kensho()
    if results:
        save_report(results)
    else:
        print("有効な懸賞情報が見つかりませんでした。")
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)

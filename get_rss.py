import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

def scrape_kensho_seikatsu():
    url = "https://www.knshow.com/"
    headers = {'User-Agent': 'Mozilla/5.0'} # ブラウザのふりをする
    
    print(f"--- 懸賞生活を直接スキャン中: {url} ---")
    
    try:
        response = requests.get(url, headers=headers)
        response.encoding = 'shift_jis' # 懸賞生活はSJIS形式が多いため
        
        soup = BeautifulSoup(response.text, 'html.parser')
        items = []
        
        # サイト内の「新着懸賞」などのリンクやテキストを探す
        # ※サイトの構造に合わせて調整済み
        for link in soup.find_all('a', href=True):
            title = link.get_text(strip=True)
            href = link['href']
            
            # 懸賞情報っぽリンクだけを抽出
            if "item" in href and len(title) > 5:
                full_url = f"https://www.knshow.com{href}" if href.startswith('/') else href
                items.append({
                    "title": title,
                    "link": full_url,
                    "date": datetime.now().strftime('%Y-%m-%d'),
                    "source": "懸賞生活"
                })
        
        return items
    except Exception as e:
        print(f"エラー発生: {e}")
        return []

if __name__ == "__main__":
    results = scrape_kensho_seikatsu()
    
    if results:
        with open("kensho_data.json", "w", encoding="utf-8") as f:
            json.dump(results[:30], f, ensure_ascii=False, indent=4)
        print(f"{len(results[:30])} 件の情報を直接取得しました！")
    else:
        print("情報が取得できませんでした。構造が変わっている可能性があります。")

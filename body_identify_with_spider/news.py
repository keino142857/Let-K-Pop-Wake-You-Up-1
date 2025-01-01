import requests
from bs4 import BeautifulSoup

def fetch_latest_news():
    # 設定目標網站的 URL（自由時報即時新聞）
    url = "https://news.ltn.com.tw/list/breakingnews"

    # 增加 User-Agent 標頭模擬瀏覽器請求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0 Safari/537.36"
    }

    # 發送 GET 請求
    response = requests.get(url, headers=headers)
    print(response)
    if response.status_code != 200:
        print("Failed to fetch news from the website.")
        return None

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到新聞列表
    news_items = soup.find_all('li', class_='lipic')[:3]  # 限制三個新聞
    news_data = []

    if not news_items:
        print("No news items found. Please check the website structure.")
        return None

    for item in news_items:
        title = item.find('a').get('title')
        link = item.find('a').get('href')
        time = item.find('span', class_='time').text if item.find('span', class_='time') else ""
        news_data.append({"title": title, "link": link, "time": time})

    return news_data

if __name__ == "__main__":
    # 爬取即時新聞
    news = fetch_latest_news()
    if news:
        print("Latest News:")
        for idx, item in enumerate(news, start=1):
            print(f"{idx}. {item['title']} ({item['time']})")
            print(f"   Link: {item['link']}")

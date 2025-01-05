import requests
from bs4 import BeautifulSoup

def fetch_latest_news():
    url = "https://news.ltn.com.tw/list/breakingnews"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0 Safari/537.36",
        "Referer": "https://news.ltn.com.tw/"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("Failed to fetch news from the website.")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    # 更新選擇器以匹配新聞項目
    news_items = soup.select('ul.list li')[:3]  # 使用 CSS 選擇器匹配新聞項目
    news_data = []

    if not news_items:
        print("No news items found. Please check the website structure.")
        print("Fetched HTML snippet:")
        print(response.text[:1000])  # 打印部分 HTML 內容進行調試
        return None

    for item in news_items:
        a_tag = item.find('a')
        title = a_tag.get('title', 'No Title')
        time = item.find('span', class_='time').text if item.find('span', class_='time') else "No Time"
        news_data.append({"title": title, "time": time})

    return news_data

if __name__ == "__main__":
    news = fetch_latest_news()
    if news:
        print("Latest News:")
        for idx, item in enumerate(news, start=1):
            print(f"{idx}. {item['title']} ({item['time']})")

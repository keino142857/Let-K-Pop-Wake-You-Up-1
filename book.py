import requests
from bs4 import BeautifulSoup

def fetch_book():
    # 目標網址
    url = 'https://www.books.com.tw/web/sys_newtopb/books/'

    # 發送請求
    response = requests.get(url)
    if response.status_code != 200:
        print(f"無法成功連接目標網址，HTTP 狀態碼：{response.status_code}")
        return None
    else:
        # 解析 HTML
        soup = BeautifulSoup(response.text, 'html.parser')

        # 找到包含書籍資料的區域
        books = soup.find_all('div', class_='type02_bd-a', limit=3)  # 限制抓取3筆

        book_info = []
        # 提取書名和作者資訊
        for book in books:
            # 提取書名
            title_tag = book.find('h4').find('a')
            title = title_tag.text.strip() if title_tag else None

            # 提取作者
            author_tag = book.find('ul', class_='msg').find('li')
            author = None
            if author_tag and '作者：' in author_tag.text:
                author = author_tag.find('a').text.strip()

            # 檢查是否找到資料
            if title and author:
                book_info.append({'title': title, 'author': author})
            else:
                book_info.append({'title': '未知', 'author': '未知'})

        return book_info

if __name__ == "__main__":
    books = fetch_book()
    if books:
        print("New books:")
        for idx, item in enumerate(books, start=1):
            print(f"{idx}. 書名: {item['title']}, 作者: {item['author']}")

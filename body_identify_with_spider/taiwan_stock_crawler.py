import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime

def fetch_taiwan_stock_data():
    # 設定目標網站的 URL（此處以台灣證交所每日收盤行情為例）
    url = "https://www.twse.com.tw/exchangeReport/MI_INDEX"
    
    # 設定查詢參數（以今日日期為例）
    today = datetime.datetime.now().strftime("%Y%m%d")
    params = {
        "response": "html",
        "date": today,
        "type": "ALLBUT0999"
    }

    # 發送 GET 請求
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print("Failed to fetch data from the website.")
        return None

    # 使用 BeautifulSoup 解析 HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # 找到股市資料表格
    table = soup.find('table', {'class': 'table'})
    if not table:
        print("No data table found.")
        return None

    # 解析表格中的資料
    rows = table.find_all('tr')
    data = []
    headers = [header.text.strip() for header in rows[0].find_all('th')]

    for row in rows[1:]:
        cols = [col.text.strip() for col in row.find_all('td')]
        if cols:  # 過濾空行
            data.append(cols)

    # 將資料轉為 DataFrame
    df = pd.DataFrame(data, columns=headers)

    return df

if __name__ == "__main__":
    df = fetch_taiwan_stock_data()
    if df is not None:
        # 將資料儲存為 CSV
        df.to_csv("taiwan_stock_data.csv", index=False, encoding="utf-8-sig")
        print("Stock data saved to taiwan_stock_data.csv")
        print(df.head())

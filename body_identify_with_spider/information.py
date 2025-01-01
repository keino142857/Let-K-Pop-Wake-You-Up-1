import pyttsx3
import time

# 初始化文字轉語音引擎
engine = pyttsx3.init()

# 設置語音速度
engine.setProperty('rate', 150)  # 預設值約 200，可調整快慢

def speak_weather_info(fetch_weather):
    engine = pyttsx3.init()
    engine.say(fetch_weather)  # 這裡會讀出爬取的天氣資訊
    engine.runAndWait()  # 等待語音合成完畢

def speak_news_info(fetch_latest_news):
    engine = pyttsx3.init()
    engine.say(fetch_latest_news)  
    engine.runAndWait()  

def speak_book_info(fetch_book):
    engine = pyttsx3.init()
    engine.say(fetch_book)  
    engine.runAndWait() 

def play_countdown():
    for i in range(5, 0, -1):
        engine.say(f"倒數：{i}")
        engine.runAndWait()  # 執行語音
        time.sleep(1)  # 倒數間隔
    engine.say("挑戰開始！")
    engine.runAndWait()
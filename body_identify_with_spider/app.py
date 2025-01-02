from flask import Flask, render_template, redirect, url_for, request
import threading
import time
from playsound import playsound
import pygame
from information import speak_weather_info, speak_news_info, speak_book_info, play_countdown
from weather import fetch_weather  
#from news import fetch_latest_news
from book import fetch_book  
from action_recognition import handle_action_check, start_camera
from motion_detection import motion_detected
import webbrowser

app = Flask(__name__)

# 共享變數來控制鬧鐘音效的播放
alarm_playing = False
alarm_thread = None

# 播放鬧鐘音效
def play_alarm():
    global alarm_playing
    alarm_playing = True
    while alarm_playing:
        pygame.mixer.Sound("alarm.m4a").play()
        time.sleep(1)

# 當手機發送 HTTP 請求時觸發
@app.route('/alarm', methods=['POST'])
def alarm():
    global alarm_playing, alarm_thread
    print("收到鬧鐘通知！")
    start_camera()

    # 播放鬧鐘直到偵測到使用者
    if not alarm_playing:
        alarm_thread = threading.Thread(target=play_alarm)
        alarm_thread.start()
    
    webbrowser.open('http://192.168.100.79:5000/')
    
    # 偵測是否有人
    while not motion_detected():
        print("沒有人在鏡頭前，繼續播放警報音！")
        time.sleep(1)  # 每秒檢查一次

    # 偵測到有人後停止鬧鐘並播放倒數 5 秒
    print("偵測到有人！停止鬧鐘並開始倒數。")
    alarm_playing = False  # 停止鬧鐘音效
    if alarm_thread.is_alive():
        alarm_thread.join()

    return redirect(url_for('challenge'))
    
@app.route('/')
def index():
    # 顯示初始頁面
    return render_template('index.html')

@app.route('/challenge')
def challenge():
    # 播放倒數音效
    play_countdown()

    print("開始動作辨識...")
    action_time_points = {
        4: 'supernova1',
        7: 'supernova2',
        20: 'supernova3',
    }

    start_time = time.time()  # 記錄開始時間
    completed_action = False

    action_images = {
        'supernova1': 'static/photo/supernova1.png',
        'supernova2': 'static/photo/supernova2.png',
        'supernova3': 'static/photo/supernova3.png',
    }

    while time.time() - start_time < 60:  # 60 秒內進行動作辨識
        print("檢查動作是否完成...")
        pose_landmarks = motion_detected()  # 獲取用戶的姿勢標記

        # 假設我們使用 handle_action_check 函數來檢查動作
        action_completed = handle_action_check(action_time_points, pose_landmarks)
        if action_completed:
            print("完成動作！")
            pygame.mixer.Sound("static/sound/correct.mp3").play()
            completed_action = True
            break
        time.sleep(1)

    # 如果在 60 秒內沒完成動作，播放鬧鐘並繼續偵測
    if not completed_action:
        print("未完成動作，播放鬧鐘並繼續偵測！")
        alarm_playing = True
        while not motion_detected():
            playsound("static/music/alarm.m4a")  # 播放鬧鐘
            time.sleep(1)
        print("偵測到人，停止鬧鐘並重新開始挑戰")

    # 設定圖片依照時間點動態變化
    current_image = None
    elapsed_time = time.time() - start_time
    if elapsed_time >= 4:
        current_image = action_images['supernova1']
    elif elapsed_time >= 7:
        current_image = action_images['supernova2']
    elif elapsed_time >= 20:
        current_image = action_images['supernova3']

    # 返回頁面並顯示相應圖片
    pause_time = request.args.get('pause_time', default=11, type=int)
    return render_template('challenge.html', pause_time=pause_time, action_image=current_image)


# 語音播放
speak_weather_info(fetch_weather())
#speak_news_info(fetch_latest_news())
speak_book_info(fetch_book())

try:
    if __name__ == "__main__":
        app.run(host="0.0.0.0", port=5001,debug=True)
except Exception as e:
    print(f"Error: {e}")


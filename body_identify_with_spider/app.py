from flask import Flask, render_template, redirect, url_for, request, jsonify
import threading
import time
import os
import pygame
from information import speak_weather_info, speak_book_info, play_countdown
from weather import fetch_weather
from book import fetch_book
import webbrowser

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = Flask(__name__)

# 共享變數來控制鬧鐘音效的播放
alarm_playing = False
alarm_thread = None
pygame.init()
person_detected = False
motion_detected_flag = False

def initialize_audio():
    try:
        # 在初始化前先確保清理任何現有的 pygame 實例
        pygame.mixer.quit()
        
        # 設定音訊參數
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=2048)
        
        # 測試音訊系統
        pygame.mixer.music.set_volume(1.0)
        print("音訊系統初始化成功")
        
    except Exception as e:
        print(f"音訊初始化錯誤: {e}")
        
        # 嘗試使用備用設定
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=4096)
            print("使用備用音訊設定初始化成功")
        except Exception as e:
            print(f"備用音訊初始化也失敗: {e}")
            return False
    return True

def play_alarm():
    global alarm_playing
    alarm_playing = True
    
    # 建構音效檔案的完整路徑
    alarm_sound_path = os.path.join(BASE_DIR, 'static', 'music', 'alarm.m4a')
    
    try:
        if os.path.exists(alarm_sound_path):
            sound = pygame.mixer.Sound(alarm_sound_path)
            while alarm_playing:
                sound.play()
                time.sleep(1)
        else:
            print(f"找不到音效檔案: {alarm_sound_path}")
            print(f"當前目錄: {BASE_DIR}")
            print(f"嘗試訪問的完整路徑: {alarm_sound_path}")
    except Exception as e:
        print(f"播放音效時發生錯誤: {e}")

# 停止鬧鐘音效
def stop_alarm():
    global alarm_playing
    alarm_playing = False
    pygame.mixer.stop()

@app.route('/motion_detected', methods=['POST'])
def handle_motion():
    global motion_detected_flag
    data = request.get_json()
    motion_detected_flag = data.get("detected", False)  # 從前端請求中獲得偵測結果
    print(f"收到的運動偵測結果: {motion_detected_flag}")
    return jsonify({"status": "success"}), 200

# 當手機發送 HTTP 請求時觸發
@app.route('/alarm', methods=['POST'])
def alarm():
    global alarm_playing, alarm_thread
    print("收到鬧鐘通知！")

    # 播放鬧鐘直到偵測到使用者
    if not alarm_playing:
        alarm_thread = threading.Thread(target=play_alarm)
        alarm_thread.start()
    
    webbrowser.open('http://192.168.100.79:5000/')
    
    # 偵測是否有人
    while not motion_detected_flag():
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
        # 前端應通知後端檢測結果，此處假設後端僅等待通知
        if person_detected:
            print("完成動作！")
            pygame.mixer.Sound("static/sound/correct.mp3").play()
            completed_action = True
            break
        time.sleep(1)

    # 如果在 60 秒內沒完成動作，播放鬧鐘並繼續偵測
    if not completed_action:
        print("未完成動作，播放鬧鐘並繼續偵測！")
        play_alarm()

    # 設定圖片依照時間點動態變化
    elapsed_time = time.time() - start_time
    current_image = None
    if elapsed_time >= 20:
        current_image = action_images['supernova3']
    elif elapsed_time >= 7:
        current_image = action_images['supernova2']
    elif elapsed_time >= 4:
        current_image = action_images['supernova1']

    return render_template('challenge.html', action_image=current_image)

if __name__ == "__main__":
    # 初始化音訊系統
    if initialize_audio():
        # 語音播放
        speak_weather_info(fetch_weather())
        speak_book_info(fetch_book())
        
        try:
            app.run(host="0.0.0.0", port=5001, debug=True, use_reloader=False)
        except Exception as e:
            print(f"Error: {e}")
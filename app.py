from flask import Flask, render_template, redirect, url_for, request, jsonify
import threading, time, os, subprocess 
from information import speak_weather_info, speak_book_info, speak_news_info, play_countdown
from weather import fetch_weather
from book import fetch_book
from news import fetch_latest_news
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)

# 設定資料庫配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/alarm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.urandom(24)  # 用於加密 session

# 初始化資料庫
db = SQLAlchemy(app)

class Log(db.Model):
    __tablename__ = 'log'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    
# 共享變數來控制鬧鐘音效的播放
alarm_playing = False
alarm_thread = None
person_detected = False
motion_detected_flag = False
vlc_process = None
timer_thread = None  ##新增計時器的線程
start_time = 0  ## 用來記錄計時開始的時間

# vlc_path = "/usr/bin/vlc"  # VLC 安裝的路徑
vlc_path = r"C:\Program Files\VideoLAN\VLC\vlc.exe"  # 使用正確的 VLC 路徑

def play_with_vlc():
    """使用 VLC 播放 .m4a 音效檔案"""
    global start_time, timer_thread  ##新增計時器
    alarm_sound_path = os.path.join(BASE_DIR, 'static', 'music', 'alarm.m4a')  # 音效檔案路徑

    try:
        # 使用 subprocess 執行 VLC 播放
        subprocess.Popen([vlc_path, alarm_sound_path, '--intf', 'dummy'])  # 使用 dummy 介面不顯示 VLC 視窗
        print("音效正在播放...")
        start_time = time.time()  ## 記錄開始時間
        timer_thread = threading.Thread(target=update_timer) ##
        timer_thread.start() ##
    except Exception as e:
        print(f"無法啟動 VLC 播放音效: {e}")

def update_timer(): ##新增計時def
    """計時器更新時間"""
    while alarm_playing:
        elapsed_time = time.time() - start_time
        print(f"播放時間：{elapsed_time:.2f} 秒")
        time.sleep(1)  # 每秒更新一次

def stop_vlc_alarm():
    """停止 VLC 播放音效"""
    global vlc_process
    if vlc_process:
        vlc_process.terminate()
        vlc_process = None
        print("VLC 音效已停止")
    if timer_thread:
        timer_thread.join()  ## 等待計時器線程結束
        print("計時器已停止")
        
def save_time_to_logs(): ##新增進資料庫
    """將計時器的時間值儲存到資料庫中的 logs 表"""
    global start_time
    elapsed_time = int(time.time() - start_time)  # 計算經過的秒數，並轉換為整數

    # 創建新的 Log 實例並儲存
    new_log = Log(time=elapsed_time)
    db.session.add(new_log)
    db.session.commit()  # 提交到資料庫
    print(f"時間 {elapsed_time} 秒已儲存到資料庫")

@app.route('/end_timer', methods=['POST'])
def end_timer():##
    """處理計時器終止並儲存時間到資料庫"""
    print("收到終止計時的請求")

    # 停止 VLC 播放音效並儲存時間
    stop_vlc_alarm()

    return jsonify({"status": "success", "message": "時間已儲存"})
    
# def countdown_and_redirect():
#     """倒數計時並返回重定向URL"""
#     engine = pyttsx3.init()
#     engine.setProperty('rate', 80)
#     engine.setProperty('volume', 1.0)
    
#     # 先說"倒數計時"
#     engine.say("倒數計時:五。四。三。二。一。")
#     engine.runAndWait()
    
#     return url_for('challenge')

@app.route('/motion_detected', methods=['POST'])
def handle_motion_detected():
    global person_detected, motion_detected_flag
    data = request.get_json()  # 接收前端發送的 JSON 資料
    detected = data.get("detected", False)

    if detected:
        person_detected = True
        motion_detected_flag = True  # 偵測到人，更新標誌
        print("偵測到人！")
        return jsonify({"status": "success", "show_button": True})
    else:
        person_detected = False
        motion_detected_flag = False  # 偵測不到人，繼續播放警報
        print("沒有人！")
        return jsonify({"status": "success", "show_button": False})

# 當手機發送 HTTP 請求時觸發
@app.route('/alarm', methods=['POST'])
def alarm():
    global alarm_playing, motion_detected_flag
    print("收到鬧鐘通知！")
    try:
        if not alarm_playing:
            alarm_playing = True
            #play_with_vlc()

        # 如果偵測到人
        if motion_detected_flag:
            print("偵測到人！停止鬧鐘，顯示按鈕供跳轉。")
            #stop_vlc_alarm()
            alarm_playing = False
        
            # 返回顯示按鈕的指令
            return jsonify({"status": "success", "show_button": True,"stop_alarm": True})
    
        # 偵測不到人則繼續警報
        return jsonify({"status": "success", "show_button": False, "stop_alarm": False})
    
    except Exception as e:
        print(f"警報處理過程發生錯誤: {e}")
        return jsonify({"error": str(e)}), 500

    
@app.route('/')
def index():
    # 顯示初始頁面
    return render_template('index.html')

@app.route('/challenge')
def challenge():
    return render_template('challenge.html')

@app.route('/rank')
def rank():
    # 從資料庫中查詢 time 欄位
    logs = Log.query.with_entities(Log.time).all()  # 只查詢 time 欄位
    readable_logs = [{"time": log.time} for log in logs]  # 直接顯示 int 格式
    return render_template('rank.html', logs=readable_logs)


if __name__ == "__main__":
    # 語音播放
    speak_weather_info(fetch_weather())
    speak_book_info(fetch_book())
    # speak_news_info(fetch_latest_news())
    
    try:
        app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
    except Exception as e:
        print(f"Error: {e}")

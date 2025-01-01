import pygame
import time
import tkinter as tk
from tkinter import PhotoImage
import cv2
import mediapipe as mp

# 初始化 pygame mixer
pygame.mixer.init()

# 創建 Tkinter 視窗
root = tk.Tk()
root.title("動作提示")

# 設定顯示圖片的Label
image_label = tk.Label(root)
image_label.pack()

# 初始化姿勢檢測
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# 顯示對應動作的圖片
def show_action_image(action):
    if action == "supernova1":
        img = PhotoImage(file="static/photo/supernova1.png") 
    elif action == "supernova2":
        img = PhotoImage(file="static/photo/supernova2.png")
    elif action == "supernova3":
        img = PhotoImage(file="static/photo/supernova3.png")
    else:
        return

    image_label.config(image=img)
    image_label.image = img  # 保證圖片能夠持續顯示

#check supernova1
def supernova1(pose_landmarks, action_type):
    if action_type == 'arm_flexing':
        # 獲取主要的關鍵點
        left_shoulder = pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.LEFT_WRIST]
        right_shoulder = pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = pose_landmarks.landmark[mp.solutions.pose.PoseLandmark.RIGHT_WRIST]

        # 檢查手臂的角度以確保符合屈曲姿勢
        def angle_between_points(a, b, c):
            """計算三個點 a、b 和 c 形成的 b 點角度。"""
            import math
            ab = (a.x - b.x, a.y - b.y)
            cb = (c.x - b.x, c.y - b.y)
            dot_product = ab[0] * cb[0] + ab[1] * cb[1]
            mag_ab = math.sqrt(ab[0]**2 + ab[1]**2)
            mag_cb = math.sqrt(cb[0]**2 + cb[1]**2)
            if mag_ab * mag_cb == 0:
                return 0
            angle = math.acos(dot_product / (mag_ab * mag_cb))
            return math.degrees(angle)
        
        left_arm_angle = angle_between_points(left_shoulder, left_elbow, left_wrist)
        right_arm_angle = angle_between_points(right_shoulder, right_elbow, right_wrist)
        
        # 判斷屈曲動作的條件（通常角度在 60 至 120 度之間）
        if 60 <= left_arm_angle <= 120 and 60 <= right_arm_angle <= 120:
            return True

    return False

#check supernova2
def supernova2(pose_landmarks, action_type):
    if action_type == 'arms_crossed':
        left_elbow = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        right_elbow = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        left_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        # 檢查手臂是否交叉 (例如：左手腕的 x 值大於右手腕的 x 值)
        if left_wrist.x > right_wrist.x and right_wrist.x < left_wrist.x:
            return True

    return False

#check supernova3
def supernova3(pose_landmarks, action_type):
    if action_type == 'hand_up':
        left_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]
        right_shoulder = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_wrist = pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        # 檢查手是否舉起 (例如：手腕的 y 值是否小於肩膀的 y 值)
        if left_wrist.y < left_shoulder.y and right_wrist.y < right_shoulder.y:
            return True
            
    return False

# 動作檢查的映射
ACTION_CHECKERS = {
    "supernova1": supernova1,
    "supernova2": supernova2,
    "supernova3": supernova3,
}

# 檢查動作是否完成
def check_action(action, pose_landmarks):
    checker = ACTION_CHECKERS.get(action)
    if checker:
        return checker(pose_landmarks)
    return False

# 音樂進度與動作檢查
def handle_action_check(action, pose_landmarks):
    action_completed = False
    while not action_completed:
        action_completed = check_action(action, pose_landmarks)
        if not action_completed:
            print(f"動作 {action} 尚未完成，請繼續嘗試")
            show_action_image(action)
            pygame.mixer.Sound("static/sound/error.mp3").play()  # 播放錯誤音效
            time.sleep(1)  # 每秒提示一次
        else:
            print(f"動作 {action} 已完成！")
            pygame.mixer.Sound("static/sound/correct.mp3").play()  # 播放正確音效

def play_music_with_progress_and_check_actions(music_file, action_time_points, pose_landmarks):
    pygame.mixer.music.load(music_file)
    pygame.mixer.music.play()

    start_time = time.time()

    while pygame.mixer.music.get_busy():
        elapsed_time = time.time() - start_time

        for time_point, action in list(action_time_points.items()):
            if elapsed_time >= time_point:
                pygame.mixer.music.pause()
                print(f"檢查動作: {action}")

                handle_action_check(action, pose_landmarks)

                del action_time_points[time_point]
                pygame.mixer.music.unpause()

        time.sleep(0.5)  # 每 0.5 秒檢查一次時間進度

# 用戶在需要時開啟攝影機
def start_camera():
    cap = cv2.VideoCapture(1)
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        try:
            start_time = time.time()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(image)
                pose_landmarks = results.pose_landmarks

                if pygame.mixer.music.get_busy():
                    elapsed_time = time.time() - start_time
                    for time_point, action in list(action_time_points.items()):
                        if elapsed_time >= time_point:
                            pygame.mixer.music.pause()
                            handle_action_check(action, pose_landmarks)
                            del action_time_points[time_point]
                            pygame.mixer.music.unpause()

                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()

# 主程式
action_time_points = {
    4: 'supernova1',
    7: 'supernova2',
    20: 'supernova3',
}
music_file = "static/music/supernova.m4a"

start_camera()

root.mainloop()

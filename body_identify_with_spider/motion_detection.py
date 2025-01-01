import cv2
import mediapipe as mp

# 初始化 mediapipe 姿勢檢測
mp_pose = mp.solutions.pose

def motion_detected():
    cap = cv2.VideoCapture(1)
    ret, frame = cap.read()
    if not ret:
        cap.release()
        return False

    # 初始化 Pose 模型
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(frame_rgb)  # 使用 pose 進行處理

    cap.release()  # 釋放攝像頭

    # 檢查是否有偵測到姿勢標記
    return results.pose_landmarks is not None


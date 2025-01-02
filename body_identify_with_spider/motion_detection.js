// 載入 MediaPipe 的 Pose 解決方案
import { Pose } from "@mediapipe/pose";
import { Camera } from "@mediapipe/camera_utils";

async function motionDetected() {
  // 取得影片流 (Camera)
  const videoElement = document.createElement("video");
  videoElement.style.display = "none";
  document.body.appendChild(videoElement);

  const stream = await navigator.mediaDevices.getUserMedia({ video: true });
  videoElement.srcObject = stream;

  return new Promise((resolve) => {
    // 初始化 MediaPipe Pose
    const pose = new Pose({
      locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
    });

    pose.setOptions({
      modelComplexity: 1,
      minDetectionConfidence: 0.5,
      minTrackingConfidence: 0.5,
    });

    pose.onResults((results) => {
      // 檢查是否檢測到姿勢標記
      const detected = results.poseLandmarks && results.poseLandmarks.length > 0;
      stream.getTracks().forEach((track) => track.stop()); // 停止攝像頭
      videoElement.remove(); // 移除 video 元素

      // 發送結果到後端
      fetch('/motion_detected', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ detected: detected })
      });

      resolve(detected);
    });

    const camera = new Camera(videoElement, {
      onFrame: async () => {
        await pose.send({ image: videoElement });
      },
      width: 640,
      height: 480,
    });

    camera.start();
  });
}

// 使用範例
motionDetected().then((detected) => {
  console.log("Motion detected:", detected);
});

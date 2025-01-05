import { Pose } from "@mediapipe/pose";
import { Camera } from "@mediapipe/camera_utils";

async function motionDetected() {
  const stream = await navigator.mediaDevices.getUserMedia({ video: true }).catch(error => {
    console.error("無法取得鏡頭權限:", error);
  });

  if (stream) {
    console.log("鏡頭已開啟");
    const videoElement = document.createElement("video");
    videoElement.srcObject = stream;
    videoElement.play().catch((error) => {
      console.error("無法播放鏡頭:", error);
    });
    videoElement.style.display = "none";
    document.body.appendChild(videoElement);

    return new Promise((resolve) => {
      const pose = new Pose({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`,
      });

      pose.setOptions({
        modelComplexity: 1,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5,
      });

      pose.onResults((results) => {
        const detected = results.poseLandmarks && results.poseLandmarks.length > 0;
        stream.getTracks().forEach((track) => track.stop());
        videoElement.remove();

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
}

motionDetected().then((detected) => {
  if (detected) {
    console.log("有人在鏡頭前，停止警報！");
    // fetch("/motion_detected", { method: "POST" });
  }
});

// 初始化
const videoElement = document.createElement('video');
const canvasElement = document.createElement('canvas');
const canvasCtx = canvasElement.getContext('2d');
const actionImages = {
    supernova1: 'static/photo/supernova1.png',
    supernova2: 'static/photo/supernova2.png',
    supernova3: 'static/photo/supernova3.png'
};
const actionSounds = {
    correct: new Audio('static/sound/correct.mp3'),
    error: new Audio('static/sound/error.mp3')
};

// 顯示對應動作的圖片
function showActionImage(action) {
    const imageElement = document.getElementById('actionImage');
    if (action in actionImages) {
        imageElement.src = actionImages[action];
    } else {
        imageElement.src = '';
    }
}

// 計算三點形成的角度
function angleBetweenPoints(a, b, c) {
    const ab = { x: a.x - b.x, y: a.y - b.y };
    const cb = { x: c.x - b.x, y: c.y - b.y };
    const dotProduct = ab.x * cb.x + ab.y * cb.y;
    const magAB = Math.sqrt(ab.x ** 2 + ab.y ** 2);
    const magCB = Math.sqrt(cb.x ** 2 + cb.y ** 2);
    if (magAB * magCB === 0) return 0;
    const angle = Math.acos(dotProduct / (magAB * magCB));
    return (angle * 180) / Math.PI;
}

// 動作檢查函數
function checkSupernova1(poseLandmarks) {
    const leftArmAngle = angleBetweenPoints(
        poseLandmarks.leftShoulder,
        poseLandmarks.leftElbow,
        poseLandmarks.leftWrist
    );
    const rightArmAngle = angleBetweenPoints(
        poseLandmarks.rightShoulder,
        poseLandmarks.rightElbow,
        poseLandmarks.rightWrist
    );
    return leftArmAngle >= 60 && leftArmAngle <= 120 && rightArmAngle >= 60 && rightArmAngle <= 120;
}

function checkSupernova2(poseLandmarks) {
    return (
        poseLandmarks.leftWrist.x > poseLandmarks.rightWrist.x &&
        poseLandmarks.rightWrist.x < poseLandmarks.leftWrist.x
    );
}

function checkSupernova3(poseLandmarks) {
    return (
        poseLandmarks.leftWrist.y < poseLandmarks.leftShoulder.y &&
        poseLandmarks.rightWrist.y < poseLandmarks.rightShoulder.y
    );
}

const ACTION_CHECKERS = {
    supernova1: checkSupernova1,
    supernova2: checkSupernova2,
    supernova3: checkSupernova3
};

async function startCamera() {
    const stream = await navigator.mediaDevices.getUserMedia({ video: true });
    videoElement.srcObject = stream;
    videoElement.play();

    const pose = new Pose({
        locateFile: (file) => `https://cdn.jsdelivr.net/npm/@mediapipe/pose/${file}`
    });
    pose.setOptions({
        modelComplexity: 1,
        smoothLandmarks: true,
        enableSegmentation: false,
        smoothSegmentation: false,
        minDetectionConfidence: 0.5,
        minTrackingConfidence: 0.5
    });
    pose.onResults((results) => {
        const poseLandmarks = results.poseLandmarks;

        if (poseLandmarks) {
            Object.keys(ACTION_CHECKERS).forEach((action) => {
                if (ACTION_CHECKERS[action](poseLandmarks)) {
                    console.log(`動作 ${action} 已完成！`);
                    actionSounds.correct.play();
                    showActionImage(action);
                } else {
                    actionSounds.error.play();
                }
            });
        }
    });

    const camera = new Camera(videoElement, {
        onFrame: async () => {
            await pose.send({ image: videoElement });
        },
        width: 640,
        height: 480
    });
    camera.start();
}

// 啟動相機
startCamera();

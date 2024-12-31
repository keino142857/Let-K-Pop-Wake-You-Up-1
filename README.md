# 讓 K-Pop 叫你起床 


### apt install 與 pip install
- sudo apt install：在哪裡都可以執行
- pip install：只能在虛擬環境執行
    - 原因：error: externally-managed-environment

### 下載時遇到的困難

- 第一次下載 Mediapipe 失敗，因為版本不相容（Raspberry Pi 3 的 Python 版本是 3.11.2）
- Mediapipe 支援最高的 Python 版本是 3.9，所以降了版本再下載一次，終於成功了
- 開始下載 TensorFlow 失敗
- 下載並重新編譯了 Python3.7（超級久） ，然後再重裝了 Mediapipe（超級久）跟 TensorFlow
- 

### 下載前可以先看這裡

- 有些下載的時間會很久，可以下這個指令看詳細的下載，可以增加信心並在出錯的時候可以即時知道XD
    - `--verbose`

### 下載並重新編譯 Python3.7

- 因為 Raspberry Pi 3 是基於 ARM 架構，
- `wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz`

### 建置虛擬環境（Python 3.7）

- `python3.7 -m venv lsa_p3.7`
    - lsa_p3.7 可以根據自己的需求更換

### 進入虛擬環境（Python 3.7）

-  `source lsa_p3.7/bin/activate`

### 下載 mediapipe

- `pip install mediapipe-rpi3`

### 下載 TensorFlow

- `pip install tensorflow`

### 下載 opencv

- `sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev`
- `sudo apt-get install build-essential cmake git pkg-config libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev gfortran openexr libatlas-base-dev python3-dev python3-numpy libtbbmalloc2 libtbb-dev` 

- 接下來下載時如果出現這個錯誤：<font color = #ff00>ERROR: Failed building wheel for opencv-contrib-python</font>，可以用這個指令升級，或是你可以一剛開始就先升級，避免睡一覺起來發現沒有裝成功（就是我）
    - `pip install --upgrade pip setuptools wheel`
- 可以順便檢查 pip 的版本
    -  `pip --version`
    - 如果版本低於 24.0 記得升級，不升級好像也可以，但它出錯的時候我就一起升級了，下面兩個可以二選一
    - `pip install upgrade pip`
    -  `python3.7 -m pip install --upgrade pip`
- 接下來會下載很久，可以邊下載邊做別的事情，或是去睡覺XD
    - `pip install opencv-contrib-python`
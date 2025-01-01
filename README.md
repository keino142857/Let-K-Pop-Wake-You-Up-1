# README




## 環境架設

以下參考了 [Cockroach_play_tetris](https://github.com/NCNU-OpenSource/Cockroach_play_tetris.git) 中的 openCV 安裝方式，感謝 [@UncleHanWei](https://github.com/UncleHanWei) 學長提供連結及技術上的支援

***

### apt install 與 pip install

- sudo apt install：在哪裡都可以執行
- pip install：只能在虛擬環境執行
    - 原因：error: externally-managed-environment

***

### 下載時遇到的困難


#### 在 Raspberry Pi 3 上安裝 Mediapipe、TensorFlow、OpenCV
- 第一次下載 Mediapipe 失敗，因為版本不相容（Raspberry Pi 3 的 Python 版本是 3.11.2）
- Mediapipe 支援最高的 Python 版本是 3.9，所以降了版本再下載一次，終於成功了
- 開始下載 TensorFlow 失敗，因為版本不相容
- 下載並重新編譯了 Python3.7 ，然後再重裝了 Mediapipe（超級久）跟 TensorFlow
- 開始下載 OpenCV，五六個小時後因為相依套件版本不相容安裝失敗
:::info
- 更新版本後再重新安裝，結果卡在 Building 100% 快兩個小時所以取消
- 上網找了相關資料以後，有人叫我 Be Patient 所以重新安裝
- 因為中間跳了一串資訊，有點好奇是什麼原因想複製起來所以按了 Ctrl + C 結果五個小時就這樣再見
- 崩潰完後再安裝一次，安心的去睡覺，結果一早起來還在 Building
- 發現可能是記憶體不夠，為了確認猜想再裝一次，還真的卡在 99%
:::
- 換成 Raspberry Pi 4，感謝柏瑋學長幫忙我們在 MOLi 挖出 Raspberry Pi 4

#### 在 Raspberry Pi 4 上安裝 Mediapipe、TensorFlow、OpenCV
- 找不到安裝包
- 官方不提供 ARM 架構的安裝包，所以 pip install 無法成功安裝

[]
<!-- ### 下載前可以先看這裡

- 有些下載的時間會很久，可以下這個指令看詳細的下載，可以增加信心並在出錯的時候可以即時知道XD
    - `--verbose`

### 下載並重新編譯 python3.7

- 因為 Raspberry Pi 3 是基於 ARM 架構，
- `wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz`
- `tar -xvf Python-3.7.9.tgz`


### 建置虛擬環境（python 3.7）

- `python3.7 -m venv lsa_p3.7`
    - lsa_p3.7 可以根據自己的需求更換

### 進入虛擬環境（python 3.7）

-  `source lsa_p3.7/bin/activate`

### 下載 mediapipe

- `pip install mediapipe-rpi3`

### 下載 TensorFlow

- `pip install tensorflow`

### 下載 opencv

- `sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng-dev`
- `sudo apt-get install build-essential cmake git pkg-config libgtk-3-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libjpeg-dev libpng-dev libtiff-dev gfortran openexr libatlas-base-dev python3-dev python3-numpy libtbb2 libtbb-dev` 

- 接下來下載時如果出現這個錯誤：<font color = #ff00>ERROR: Failed building wheel for opencv-contrib-python</font>，可以用這個指令升級，或是你可以一剛開始就先升級，避免睡一覺起來發現沒有裝成功（就是我）
    - `pip install --upgrade pip setuptools wheel`
- 可以順便檢查 pip 的版本
    -  `pip --version`
    - 如果版本低於 24.0 記得升級，不升級好像也可以，但它出錯的時候我就一起升級了，下面兩個可以二選一
    - `pip install upgrade pip`
    -  `python3.7 -m pip install --upgrade pip`
- 接下來會下載很久，可以邊下載邊做別的事情，或是去睡覺XD
    - `pip install opencv-contrib-python`
 -->
 
 
 
## 爬蟲

### 爬天氣

天氣的爬蟲參考了[中央氣象局 Open API 取得當地的天氣狀況](https://gist.github.com/louis70109/d165be10be06d71708804e89410c969e)

- 首先，進入中央氣象局的[氣象資料開放平台](https://opendata.cwa.gov.tw/devManual/insrtuction)，註冊帳號。
![螢幕擷取畫面 2025-01-01 211052](https://hackmd.io/_uploads/rkYXl6M8yl.png)

- 登入按下去就對了。
![螢幕擷取畫面 2025-01-01 211733](https://hackmd.io/_uploads/B1bEWaf81l.png)

- 按加入會員。
![螢幕擷取畫面 2025-01-01 211820](https://hackmd.io/_uploads/B1aS-pfLJl.png)

- 同意按下去就對了。
![image](https://hackmd.io/_uploads/HJKnW6GI1x.png)

- 填完送出，等收到郵件。
![image](https://hackmd.io/_uploads/rkLWfpzL1l.png)

- 郵件長這樣，按<font color = #00aeff>成為正式會員。</font>
![photo_2025-01-01_21-25-40](https://hackmd.io/_uploads/SyDImaGUJl.jpg =300x)

- 回到網站登入，然後就可以取得授權碼了。
![螢幕擷取畫面 2025-01-01 213112](https://hackmd.io/_uploads/Hy1GEpMLkx.png)

- 取得授權碼後，參考上面網址提供的程式碼。
- import 那行再加這個
    -  `from dotenv import load_dotenv`
- 然後程式碼裡面再加這行。
    - `load_dotenv()`
- 看起來像這樣，或是可以直接用我們的檔案。
![image](https://hackmd.io/_uploads/rkqrLpz8Jl.png)

- 開一個 .env 檔案，把金鑰放在 .env 檔案中，避免你的金鑰就這樣被看光光。
    - ```shell=
      OPEN_API=<你的金鑰>
      ```
    - 這裡的 OPEN_API 可以根據自己的需求更改，但程式碼中`"Authorization": os.getenv('OPEN_API')` 這裡的 OPEN_API 也要一起改。
    - .env 就叫 .env 就好，不要在前面亂加字

- 這裡可以選擇要找哪個縣市的
    ![image](https://hackmd.io/_uploads/HJToSRGUkl.png)
    - 改這裡，記得只能從上面的 locations 選擇要查詢的地點。
    - ```shell= 
      text='南投縣'
      ```

 

# 讓 K-Pop 叫你起床

## Concept Development

由於平時鬧鐘響了只會伸手關掉，繼續賴床，根本無法有效起床。
為了改善賴床問題，我們設計了一個鬧鐘系統，讓使用者必須做出指定動作才能關掉鬧鐘，最後會播報今日新聞。

## Implementation Resources

- 手機：價格不等（ios 系統跟 Android 系統方法不一樣）。
- 電腦：價格不等，看你要用哪種，但一定要有鏡頭。
- RaspBerry Pi 4：拿 MOLi 現成的。
- 喇叭：連接到樹莓派用。

## Existing Library/Software

### 使用 Python Libraries
- `requests`：進行 HTTP 請求。
- `os`：處理檔案路徑與環境變數。
- `re`：處理正則表達式，解析或匹配特定格式的資料。
- `datetime`：處理日期與時間資訊。
- `dotenv`：載入 .env 檔案中的環境變數，用於設定 API 金鑰或其他敏感資訊。
- `BeautifulSoup （bs4）`：解析 HTML 文件並提取所需的資料。
- `pyttsx3`：文字轉語音，用於將天氣、書籍或新聞資訊轉換為語音播報。
- `Flask`：用於建立 Web 伺服器，支援前端與後端互動。
- `threading`：實現多線程處理，用於同時運行語音播報和其他後端任務。
- `time`：延遲操作或測量執行時間。
- `vlc`：控制 VLC 媒體播放器。


## Implementation Process

原本打算使用 Python 架後端，所以用 RaspBerry Pi 3 下載 MediaPipe、OpenCV、TensorFlow，但因為 Pi 3 的記憶體不夠，所以改成 RaspBerry Pi 4，但因為 RaspBerry Pi 4 的版本不相容，最後只好用 JavaScript 寫後端。



## Knowledge from Lecture

- RaspBerry Pi 4 環境架設
- MediaPipe 動作辨識：參考了 [Playing Classic Game with Body Gestures using Pose Detection](https://github.com/NCNU-OpenSource/BobyGamer)，感謝第八組組員提供協助
- Flask
- JavaScript
- Python


## Installation

- 請先安裝需要的模組
    - `pip install requests`
    - `pip install python-dotenv`
    - `pip install beautifulsoup4`
    - `pip install pyttsx3`
    - `pip install flask`
    - `pip install python-vlc`

- 在樹梅派輸入指令，下載專案
    - 如果之前都沒有用過 git 指令的話，可以先下載
        - `sudo apt install git`
    - `git cline https://github.com/NCNU-OpenSource/Let-K-Pop-Wake-You-Up.git`

- 因為天氣爬蟲需要會員的私人金鑰才能使用，請先參考以下步驟設定

<details>
<summary>天氣爬蟲的金鑰設定</summary>

天氣的爬蟲參考了[中央氣象局 Open API 取得當地的天氣狀況](https://gist.github.com/louis70109/d165be10be06d71708804e89410c969e)

- 首先，進入中央氣象局的[氣象資料開放平台](https://opendata.cwa.gov.tw/devManual/insrtuction)，註冊帳號。
![螢幕擷取畫面 2025-01-01 211052](https://hackmd.io/_uploads/HJUd7bFLJx.png)

- 登入按下去就對了。
![螢幕擷取畫面 2025-01-01 211733](https://hackmd.io/_uploads/B1bEWaf81l.png)

- 按加入會員。
![螢幕擷取畫面 2025-01-01 211820](https://hackmd.io/_uploads/B1aS-pfLJl.png)

- 同意按下去就對了。
![image](https://hackmd.io/_uploads/HJKnW6GI1x.png)

- 填完送出，等收到郵件。
![image](https://hackmd.io/_uploads/rkLWfpzL1l.png)

- 郵件長這樣，按<font color = #00aeff>成為正式會員。</font>
![photo_2025-01-01_21-25-40](https://hackmd.io/_uploads/SyDImaGUJl.jpg=300x)

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
</details>




## Usage

- 手機、筆電、RaspBerry Pi 4 都要連到同一個 Wi-Fi

- 把 RaspBerry Pi 4 開機並接上音響

- 先找 RaspBerry Pi 4 的 ip 位址
    - `hostname -I`
    - 或是 `ifconfig` 也可以

- 進入檔案
    - `cd Let-K-Pop-Wake-You-Up.git`
- 執行
    - `python app.py`

- 在電腦的瀏覽器打入 `<RaspBerry Pi 4 的 ip>:5000`
    - 如果鏡頭無法開啟請參考以下方法

<details>
<summary>如何讓 Chrome 瀏覽器允許 http 打開鏡頭及麥克風</summary>

[參考資料](https://blog.csdn.net/qq_43530326/article/details/130974058)

- 進入 Google 瀏覽器的實驗性功能（直接複製網址貼上就好）
    - `chrome://flags/#unsafely-treat-insecure-origin-as-secure`
- 在  Insecure origins treated as secure（黃色底的那邊）填入
    - `http://<你的 RaspBerry Pi 4 ip>:5000`
- 把「已停用」改成「已啟用」，如下圖所示
    - ![螢幕擷取畫面 2025-01-07 223630](https://hackmd.io/_uploads/H1Exa25Ike.png)

</details>

- 再來就是用手機鬧鐘發送 http 請求給樹莓派啦

<details>
<summary>透過 iPhone 的快捷指令發送 http 請求至樹莓派</summary>


步驟 1：準備樹莓派的 Flask Server
1. 在 Flask server 中設定好 /alarm 的路由並確保能接收 HTTP POST 請求。
2. 確保樹莓派和手機在同一 Wi-Fi 網路中，並知道其 IP 地址。如果樹莓派的 IP 地址是 192.168.100.79，那麼完整的 URL 是： `http://192.168.100.79:5000/alarm`

步驟 2：在 iPhone 上設定快捷指令
1. 打開「快捷指令 (Shortcuts)」App。
2. 點擊右上角的 +，創建一個新快捷指令。
3. 添加「取得 URL 的內容 (Get Contents of URL)」操作，並設置：
- URL：輸入: `http://<RaspBerry Pi 4 的 ip>:5000/alarm`
- 方法 (Method)：選擇 POST。

步驟 3：整合快捷指令與鬧鐘
1. 打開快捷指令 App，進入「自動化」功能。點擊 +，建立「個人自動化」。
2. 設定鬧鐘觸發事件，添加剛剛建立的快捷指令，保存並啟用自動化。
</details>

<details>
<summary>安卓要透過專案中的 alarm.html 發送 http 請求</summary>

- 請用手機開啟`http://<RaspBerry Pi 4 的 ip>:5000/alarm`
- 設定你想要的時間、星期，並按下 Add Alarm

</details>



## Job Assignment

| 學號 | 姓名 | 分工 |
| -------- | -------- | -------- |
|111213008| 楊璇蓁|圖片音樂剪輯、程式整合、MediaPipe 動作辨識、README 撰寫|
|111213009|黃昕|ppt 製作、找音效、程式整合、README 撰寫|
|111213034|孫睿君|UI、最後影片 Demo、程式整合、MediaPipe 動作辨識、README 撰寫、樹莓派環境架設|
|111213086|陳莉榛|UI、爬蟲、資料庫(最後未實現)、做ppt|
|111213089|徐碧君|UI、爬蟲、資料庫(最後未實現)、做ppt|

## 特別感謝

- 柏瑋學長
- 漢偉學長
- 第八組的組員
- ChatGpt
- 感謝 MOLi 提供 RaspBerry Pi 4 讓我們不用花錢花時間

## References

- https://blog.csdn.net/qq_43530326/article/details/130974058
- https://github.com/NCNU-OpenSource/BobyGamer
- https://gist.github.com/louis70109/d165be10be06d71708804e89410c969e




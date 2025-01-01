from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/challenge')
def challenge():
    # 暫停時間設置的地方，目前測試預設11秒
    pause_time = request.args.get('pause_time', default=11, type=int)
    return render_template('challenge.html', pause_time=pause_time)

if __name__ == '__main__':
    app.run(debug=True)

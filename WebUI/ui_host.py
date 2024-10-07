from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/')
def login():
    return render_template('login.html')

if __name__ == '__main__':
    app.run(threaded=True, port=4998)
from flask import Flask

app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/home')
def galaxy():
    return app.send_static_file('temp.html')

if __name__ == '__main__':
    app.run(threaded=True, port=5000)
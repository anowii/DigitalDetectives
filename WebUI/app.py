from flask import Flask, render_template, redirect, request, session
app = Flask(__name__)

@app.route('/')
def home():
    if not session.get("logged_in"):
        return render_template("login.html")
    


@app.route('/login', methods="POST")
    request.form['password']





if __name__ == "__main__":
    app.run(host='0.0.0.0', port=4000)
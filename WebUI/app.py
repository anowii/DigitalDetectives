from flask import Flask, render_template, session, flash, redirect, url_for, request
import os
app = Flask(__name__)

@app.route('/')
def home():
    
    if not session.get('logged_in'):
        print("HELOLOLOLOLOLOLOLOLOL")
        return redirect("/login")
    else:
        print("YOU DID IT")
    


@app.route('/login', methods=['POST'])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        next_url = request.form.get("next")

        print(username)
        print(password)
        print(next_url)
        return redirect("/")


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=4000)
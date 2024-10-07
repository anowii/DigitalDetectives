from flask import Flask, render_template, request, session, flash, redirect, url_for
import os
app = Flask(__name__)

@app.route('/')
def home():
    
    if not session.get('logged_in'):
        print("HELOLOLOLOLOLOLOLOLOL")
        return render_template("login.html")
    else:
        print("YOU DID IT")
    


@app.route('/login', methods=['POST'])
def login():
    print("HELOLOLOLOLOLOLOLOLOL")
    print(request.form.get("username"))
    print(request.form.get("password"))
    if request.method == "POST":
        print("AANVDKNAKVDJN")
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
            session ['logged_in'] = True
        else:
            flash('wrong password')
        return render_template('home.html')





if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=4000)
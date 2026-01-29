
from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import config
import db
import sqlite3

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    
    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            message = "VIRHE: salasanat eivät ole samat. Yritä uudelleen."
            return render_template("register.html", message=message)
        password_hash = generate_password_hash(password1)

        try:
            sql = "INSERT INTO users (username, password_hash) VALUES (?, ?)"
            db.execute(sql, [username, password_hash])
        except sqlite3.IntegrityError:
            message = "VIRHE: tunnus on jo varattu. Yritä uudelleen."
            return render_template("register.html", message=message)
            
        message = "Tunnus luotu"
        return render_template("register.html", message=message)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message="")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        try:
            sql = "SELECT password_hash FROM users WHERE username = ?"
            password_hash = db.query(sql, [username])[0][0]
        except IndexError:
            message = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", message=message)

        if check_password_hash(password_hash, password):
            session["username"] = username
            return redirect("/")
        else:
            message = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

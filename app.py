
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

@app.route("/new_team_invite", methods=["GET", "POST"])
def new_invite():
    if request.method == "GET":
        return render_template("new_team_invite.html", message="")
    
    if request.method == "POST":
        series = request.form["serie_id"]
        team_name = request.form["team_name"]
        description = request.form["description"]
        
        try:
            sql = "INSERT INTO teams (serie_id, user_id, name, description) VALUES (?, ?, ?, ?)"
            db.execute(sql, [series, session["user_id"], team_name, description])
        except sqlite3.IntegrityError:
            message = "VIRHE: Joukkue on jo ilmoittautunut tähän lähtöön"
            return render_template("new_team_invite.html", message=message)
            
        # message = "Joukkuekutsu luotu. Tsemppiä kisaan!"
        # return render_template("new_team_invite.html", message=message)

        return redirect("/")

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
            message = "VIRHE:Tunnus on jo varattu. Yritä uudelleen."
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
            sql = "SELECT id, password_hash FROM users WHERE username = ?"
            result = db.query(sql, [username])[0]
            user_id = result["id"]
            password_hash = result["password_hash"]
        except:
            message = "VIRHE: Tunnusta ei löydy. Yritä uudelleen."
            return render_template("login.html", message=message)

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            message = "VIRHE: väärä tunnus tai salasana"
            return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

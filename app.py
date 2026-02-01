
from flask import Flask
from flask import render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import config
import db
import team


app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    teams = team.get_teams()
    return render_template("index.html", teams=teams)

@app.route("/create_team", methods=["GET", "POST"])
def new_invite():
    if request.method == "GET":
        return render_template("create_team.html", message="")
    
    if request.method == "POST":
        series = request.form["serie_id"]
        team_name = request.form["team_name"]
        description = request.form["description"]
        captain = session["user_id"]

        try:
            team.create(team_name, captain, series, description)
        except sqlite3.IntegrityError:
            message = "VIRHE: Joukkueen nimi on jo varattu tässä sarjassa"
            return render_template("create_team.html", message=message)

        return redirect("/")
    
@app.route("/team/<int:team_id>")
def show_team(team_id):
    team_details = team.get_team_by_id(team_id)

    return render_template("show_team.html", team=team_details)

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
        except IndexError:
            message = "VIRHE: Tunnusta ei ole olemassa"
            return render_template("login.html", message=message)

        if check_password_hash(password_hash, password):
            session["username"] = username
            session["user_id"] = user_id
            return redirect("/")
        else:
            message = "VIRHE: Virheellinen tunnus tai salasana"
            return render_template("login.html", message=message)

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

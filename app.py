
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
    teams = team.get_all()
    return render_template("index.html", teams=teams)

@app.route("/create_team", methods=["GET", "POST"])
def new_invite():
    if request.method == "GET":
        return render_template("create_team.html", message="")
    
    if request.method == "POST":
        if "cancel" in request.form:
            return redirect("/")
        
        serie_id = request.form["serie_id"]
        team_name = request.form["team_name"].strip()
        description = request.form["description"].strip()
        captain = session["user_id"]

        if not team.is_name_free_in_serie(team_name, serie_id):
            message = "VIRHE: Joukkueen nimi on jo varattu tässä sarjassa"
            return render_template("create_team.html", message=message)
        
        team.create(team_name, captain, serie_id, description)
        return redirect("/")

@app.route("/find_team")
def find_team():
    query = request.args.get("query")
    if query:
        results = team.search(query)
    else:
        results = []
        query = ""
    return render_template("find_team.html", query=query, results=results)

@app.route("/team/<int:team_id>")
def show_team(team_id):
    team_details = team.get_by_id(team_id)
    return render_template("show_team.html", team=team_details)

@app.route("/edit_team/<int:team_id>", methods=["GET", "POST"])
def edit_team(team_id):
    if request.method == "GET":
        team_details = team.get_by_id(team_id)
        return render_template("edit_team.html", team=team_details, message="")

    if request.method == "POST":
        if "cancel" in request.form:
            return redirect("/")
        
        serie_id = request.form["serie_id"]
        name = request.form["team_name"].strip()
        description = request.form["description"].strip()

        if not team.is_name_free_in_serie(name, serie_id):
            message = "VIRHE: Joukkueen nimi on jo varattu tässä sarjassa"
            team_details = team.get_by_id(team_id)
            return render_template("edit_team.html", team=team_details,
                                   message=message)

        team.update(team_id, name, serie_id, description)
        return redirect(f"/team/{team_id}")
    
@app.route("/remove_team/<int:team_id>", methods=["GET", "POST"])
def remove_team(team_id):
    if request.method == "GET":
        team_details = team.get_by_id(team_id)
        return render_template("remove_team.html", team=team_details)

    if request.method == "POST":
        if "cancel" in request.form:
            return redirect(f"/team/{team_id}")
        team.remove(team_id)
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    
    if request.method == "POST":
        if "cancel" in request.form:
            return redirect("/")

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
        if "cancel" in request.form:
            return redirect("/")
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

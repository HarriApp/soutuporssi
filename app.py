
from flask import Flask
from flask import abort, render_template, request, redirect, session
import config
import teams
import users

app = Flask(__name__)
app.secret_key = config.secret_key

@app.route("/")
def index():
    all_teams = teams.get_all_teams()
    return render_template("index.html", teams=all_teams)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    teams = users.get_teams(user_id)
    return render_template("show_user.html", user=user, teams=teams)

@app.route("/create_team", methods=["GET", "POST"])
def new_invite():
    users.require_login()

    if request.method == "GET":
        return render_template("create_team.html", message="")
    
    if request.method == "POST":
        serie_id = int(request.form["serie_id"])
        team_name = request.form["team_name"].strip()
        description = request.form["description"].strip()
        captain = session["user_id"]

        if len(team_name) < 1 or len(team_name) > 50 or len(description) > 480: 
            abort(403)        

        if not teams.is_name_available(team_name, serie_id):
            message = "VIRHE: Joukkueen nimi on jo varattu tässä sarjassa"
            return render_template("create_team.html", message=message)
        
        teams.create_team(team_name, captain, serie_id, description)
        return redirect("/")

@app.route("/find_team")
def find_team():
    query = request.args.get("query")
    if query:
        results = teams.search(query)
    else:
        results = []
        query = ""
    return render_template("find_team.html", query=query, results=results)

@app.route("/team/<int:team_id>")
def show_team(team_id):
    team = teams.get_team_by_id(team_id)
    if not team:
        abort(404)
    return render_template("show_team.html", team=team)

@app.route("/edit_team/<int:team_id>", methods=["GET", "POST"])
def edit_team(team_id):
    users.require_login()

    team = teams.get_team_by_id(team_id)
    if not team:
        abort(404)

    if request.method == "GET":
        return render_template("edit_team.html", team=team, message="")

    if request.method == "POST":
        if "cancel" in request.form:
            return redirect("/")
        if team.captain_id != session["user_id"]:
            abort(403)

        new_serie_id = int(request.form["serie_id"])
        new_name = request.form["team_name"].strip()
        new_description = request.form["description"].strip()

        if (len(new_name) < 1 or len(new_name) > 50 or
            len(new_description) > 480): 
            abort(403)

        name_or_serie_changed = (new_name != team.name or
                                 new_serie_id != team.serie_id)

        if (name_or_serie_changed and not
            teams.is_name_available(new_name, new_serie_id)):
            message = f"VIRHE: Nimi {new_name} on jo käytössä tässä sarjassa"
            team.serie_id = new_serie_id
            team.description = new_description
            return render_template("edit_team.html", team=team,
                                   message=message)

        teams.update_team(team_id, new_name, new_serie_id, new_description)
        return redirect(f"/team/{team_id}")
    
@app.route("/remove_team/<int:team_id>", methods=["GET", "POST"])
def remove_team(team_id):
    users.require_login()

    team = teams.get_team_by_id(team_id)
    if not team:
        abort(404)

    if request.method == "GET":
        return render_template("remove_team.html", team=team)

    if request.method == "POST":
        if "cancel" in request.form:
            return redirect(f"/team/{team_id}")
        if team.captain_id != session["user_id"]:
            abort(403)

        teams.remove_team(team_id)
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", message="")
    
    if request.method == "POST":
        username = request.form["username"].strip()
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if len(username) < 2:
            message = "VIRHE: Tunnuksen vähimmäispituus on kaksi merkkiä. "
            message += "Tyhjää tilaa tunnksen alussa ja lopussa ei huomioida."
            return render_template("register.html", message=message)
        
        if len(username) > 20:
            abort(403)

        if not users.is_username_available(username):
            message = "VIRHE: Tunnus on jo varattu. Yritä uudelleen."
            return render_template("register.html", message=message)

        if password1 != password2:
            message = "VIRHE: salasanat eivät ole samat. Yritä uudelleen."
            return render_template("register.html", message=message)

        users.register(username, password1)          
        message = "Tunnus luotu"
        return render_template("register.html", message=message)
    
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", message="")

    if request.method == "POST":
        if "cancel" in request.form:
            return redirect("/")
        
        username = request.form["username"].strip()
        password = request.form["password"]
        user_id = users.login(username, password)

        if not user_id:
            message = "VIRHE: Virheellinen tunnus tai salasana"
            return render_template("login.html", message=message)
            
        session["user_id"] = user_id
        session["username"] = username
        return redirect("/")

@app.route("/logout")
def logout():
    users.require_login()
    del session["user_id"]
    del session["username"]
    return redirect("/")

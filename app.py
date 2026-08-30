import secrets
from flask import Flask
from flask import abort, flash, make_response, render_template, request, \
                  redirect, session
import config
import teams
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def check_csrf():
    if "csrf_token" not in request.form or "csrf_token" not in session:
        abort(403)
    if request.form["csrf_token"] != session["csrf_token"]:
        abort(403)

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
    memberships = users.get_memberships(user_id)
    return render_template("show_user.html", user=user, teams=teams,
                           memberships=memberships)

@app.route("/create_team", methods=["GET", "POST"])
def create_team():
    users.require_login()

    series = teams.get_series()
    classes = teams.get_all_classes()

    if request.method == "GET":
        return render_template("create_team.html", classes=classes,
                               series=series)

    if request.method == "POST":
        check_csrf()
        serie_id = int(request.form["serie_id"])
        team_name = request.form["team_name"].strip()
        description = request.form["description"].strip()
        captain = session["user_id"]

        team_classes = []
        all_classes = teams.get_all_classes()
        for title in all_classes:
            value = request.form.get(title)
            if value:
                if value not in all_classes[title]:
                    abort(403)
                team_classes.append((title, value))

        if len(team_name) < 1 or len(team_name) > 50 or len(description) > 480:
            abort(403)

        if users.is_in_serie(captain, serie_id):
            flash("VIRHE: Olet jo mukana sarjassa " + \
                  teams.get_serie_description(serie_id) + \
                  ". Valitse toinen sarja.")
            return render_template("create_team.html", serie_id = serie_id,
                                   team_name = team_name, 
                                   description = description,
                                   classes = classes, 
                                   team_classes = team_classes,
                                   series = series)

        if not teams.is_name_available(team_name, serie_id):
            flash("VIRHE: Joukkueen nimi on jo varattu tässä sarjassa")
            return render_template("create_team.html", serie_id = serie_id,
                                   team_name = team_name, 
                                   description = description,
                                   classes = classes, 
                                   team_classes = team_classes,
                                   series = series)

        teams.create_team(team_name, captain, serie_id, description,
                          team_classes)
        return redirect("/")

@app.route("/team/<int:team_id>")
def show_team(team_id):
    team = teams.get_team_by_id(team_id)
    if not team:
        abort(404)

    if "user_id" in session:
        team.is_user_member = users.is_in_team(session.get("user_id"), team_id)
        team.is_user_in_serie = users.is_in_serie(session.get("user_id"),
                                             team.serie_id)
    else:
        team.is_user_member = False
        team.is_user_in_serie = False

    return render_template("show_team.html", team = team)

@app.route("/edit_team/<int:team_id>", methods=["GET", "POST"])
def edit_team(team_id):
    users.require_login()

    team = teams.get_team_by_id(team_id)
    if not team:
        abort(404)

    if request.method == "GET":
        series = teams.get_series()
        classes = teams.get_all_classes()
        return render_template("edit_team.html", team = team,
                               classes = classes, series=series)

    if request.method == "POST":
        check_csrf()
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

        serie_changed = new_serie_id != team.serie_id
        if serie_changed and users.is_in_serie(session["user_id"],
                                               new_serie_id):
            flash("VIRHE: Olet jo mukana sarjassa. Valitse toinen sarja.")
            team.serie_id = new_serie_id
            team.description = new_description
            series = teams.get_series()
            classes = teams.get_all_classes()
            return render_template("edit_team.html", team =team, series=series,
                                   classes = classes)

        name_or_serie_changed = new_name != team.name or serie_changed

        if name_or_serie_changed and not \
            teams.is_name_available(new_name, new_serie_id):
            flash(f"VIRHE: Nimi {new_name} on jo käytössä tässä sarjassa")
            team.serie_id = new_serie_id
            team.description = new_description
            series = teams.get_series()
            classes = teams.get_all_classes()
            return render_template("edit_team.html", team = team,
                                   series = series, classes = classes)

        if serie_changed:
            for member_user_id, member_user_name in team.crew_list:
                if users.is_in_serie(member_user_id, new_serie_id):
                    teams.remove_member(team_id, member_user_id)

        all_classes = teams.get_all_classes()
        new_team_classes = []
        for class_title in all_classes:
            value = request.form.get(class_title)
            if value:
                if value not in all_classes[class_title]:
                    abort(403)
                new_team_classes.append((class_title, value))

        teams.update_team(team_id, new_name, new_serie_id, new_description,
                          new_team_classes)
        return redirect(f"/team/{team_id}")

@app.route("/find_team")
def find_team():
    query = request.args.get("query")
    if query:
        results = teams.search(query)
    else:
        results = []
        query = ""
    return render_template("find_team.html", query = query, results = results)

@app.route("/join_team/<int:team_id>", methods=["POST"])
def join_team(team_id):
    check_csrf()
    users.require_login()

    team = teams.get_team_by_id(team_id)
    if not team:
        abort(404)

    if team.captain_id == session["user_id"]:
        abort(403)

    if team.is_full:
        abort(403)

    if users.is_in_team(session["user_id"], team_id):
        abort(403)

    if users.is_in_serie(session["user_id"], team.serie_id):
        abort(403)

    teams.add_member(team_id, session["user_id"])
    return redirect(f"/team/{team_id}")

@app.route("/leave_team/<int:team_id>", methods=["POST"])
def leave_team(team_id):
    check_csrf()
    users.require_login()

    team = teams.get_team_by_id(team_id)
    if not team:
        abort(404)

    if team.captain_id == session["user_id"]:
        abort(403)

    if not users.is_in_team(session["user_id"], team_id):
        abort(403)

    teams.remove_member(team_id, session["user_id"])
    return redirect(f"/team/{team_id}")

@app.route("/remove_team/<int:team_id>", methods=["GET", "POST"])
def remove_team(team_id):
    users.require_login()

    team = teams.get_team_by_id(team_id)
    if not team:
        abort(404)

    if request.method == "GET":
        return render_template("remove_team.html", team = team)

    if request.method == "POST":
        check_csrf()
        if "cancel" in request.form:
            return redirect(f"/team/{team_id}")
        if team.captain_id != session["user_id"]:
            abort(403)

        teams.remove_team(team_id)
        return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"].strip()
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if len(username) < 2:
            flash("VIRHE: Tunnuksen vähimmäispituus on kaksi merkkiä. " + 
                  "Tyhjää tilaa tunnksen alussa ja lopussa ei huomioida.")
            return render_template("register.html", username = username,
                                   password1 = password1,
                                   password2 = password2)

        if len(username) > 20:
            flash("VIRHE: Tunnuksen enimmäispituus on 20 merkkiä. " + 
                  "Tyhjää tilaa tunnksen alussa ja lopussa ei huomioida.")
            return render_template("register.html", username = username,
                                   password1 = password1,
                                   password2 = password2)

        if not users.is_username_available(username):
            flash("VIRHE: Tunnus on jo varattu. Yritä uudelleen.")
            return render_template("register.html", username = username,
                                   password1 = password1,
                                   password2 = password2)

        if password1 != password2:
            flash("VIRHE: salasanat eivät ole samat. Yritä uudelleen.")
            return render_template("register.html", username = username,
                                   password1 = password1,
                                   password2 = password2)

        users.register(username, password1)
        flash("Tunnus luotu. Voit nyt kirjautua sisään.")
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        if "cancel" in request.form:
            return redirect("/")

        username = request.form["username"].strip()
        password = request.form["password"]
        user_id = users.login(username, password)

        if not user_id:
            flash("VIRHE: Virheellinen tunnus tai salasana")
            return render_template("login.html", username = username, 
                                   password = password)

        session["user_id"] = user_id
        session["username"] = username
        session["csrf_token"] = secrets.token_hex(16)
        return redirect("/")

@app.route("/set_profile_image", methods=["GET", "POST"])
def set_profile_image():
    users.require_login()

    if request.method == "GET":
        return render_template("set_profile_image.html")

    if request.method == "POST":
        check_csrf()

        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: väärä tiedostomuoto")
            return render_template("set_profile_image.html")
        
        image = file.read()
        if len(image) > 1024 * 1024:
            flash("VIRHE: liian suuri kuva")
            return render_template("set_profile_image.html")

        user_id = session["user_id"]
        users.update_image(user_id, image)

        return redirect("/user/" + str(user_id))

@app.route("/show_profile_image/<int:user_id>")
def show_profile_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

@app.route("/remove_profile_image", methods=["POST"])
def remove_profile_image():
    users.require_login()
    check_csrf()
    user_id = session["user_id"]
    users.remove_image(user_id)
    return redirect("/user/" + str(user_id))

@app.route("/logout")
def logout():
    users.require_login()
    session.clear()
    return redirect("/")

from flask import abort, session
from werkzeug.security import generate_password_hash, check_password_hash
import db

def get_user(user_id):
    sql = '''SELECT id, username, image IS NOT NULL has_image
             FROM users
             WHERE id = ?'''
    result = db.query(sql, [user_id])
    if not result:
        return None
    return result[0]

def is_username_available(username):
    sql = '''SELECT id FROM users WHERE username = ?'''
    return len(db.query(sql, [username])) == 0

def register(username, password):
    password_hash = generate_password_hash(password)
    sql = '''INSERT INTO users (username, password_hash) VALUES (?, ?)'''
    db.execute(sql, [username, password_hash])

def login(username, password):
    try:
        sql = "SELECT id, password_hash FROM users WHERE username = ?"
        result = db.query(sql, [username])[0]
        user_id = result["id"]
        password_hash = result["password_hash"]
        if check_password_hash(password_hash, password):
            return user_id
        return None
    except IndexError:
        return None

def get_teams(user_id):
    sql = '''SELECT T.id AS team_id, T.name AS team_name, S.description
             AS serie_name
             FROM teams T JOIN series S ON T.serie_id = S.id
             WHERE T.user_id = ? ORDER BY T.id'''
    return db.query(sql, [user_id])

def get_memberships(user_id):
    sql = '''SELECT T.id AS team_id, T.name AS team_name, S.description
             AS serie_name
             FROM teams T JOIN series S ON T.serie_id = S.id JOIN crews C
             ON T.id = C.team_id
             WHERE C.user_id = ? ORDER BY C.id'''
    return db.query(sql, [user_id])

def is_in_team(user_id, team_id):
    sql = '''SELECT id FROM teams WHERE user_id = ? AND id = ?'''
    if len(db.query(sql, [user_id, team_id])) > 0:
        return True
    sql = '''SELECT id FROM crews WHERE user_id = ? AND team_id = ?'''
    return len(db.query(sql, [user_id, team_id])) > 0

def is_in_serie(user_id, serie_id):
    sql = '''SELECT id FROM teams WHERE user_id = ? AND id IN
             (SELECT id FROM teams WHERE serie_id = ?)'''
    if len(db.query(sql, [user_id, serie_id])) > 0:
        return True
    sql = '''SELECT id FROM crews WHERE user_id = ? AND team_id IN
             (SELECT id FROM teams WHERE serie_id = ?)'''
    return len(db.query(sql, [user_id, serie_id])) > 0

def update_image(user_id, image):
    sql = '''UPDATE users SET image = ? WHERE id = ?'''
    db.execute(sql, [image, user_id])

def require_login():
    if "user_id" not in session:
        abort(403)

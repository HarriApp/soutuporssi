import db
from flask import abort, session
from werkzeug.security import generate_password_hash, check_password_hash

def get_user(user_id):
    sql = '''SELECT id, username FROM users WHERE id = ?'''
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
        else:
            return None
    except IndexError:
        return None
    
def get_teams(user_id):
    sql = '''SELECT T.id AS team_id, T.name AS team_name, S.description AS serie_name
             FROM teams T JOIN series S ON T.serie_id = S.id
             WHERE T.user_id = ? AND T.active = 1 ORDER BY T.id DESC'''
    return db.query(sql, [user_id])

def require_login():
    if "user_id" not in session:
        abort(403)

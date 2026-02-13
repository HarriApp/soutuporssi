import db
from flask import abort, session
from werkzeug.security import generate_password_hash, check_password_hash

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

def require_login():
    if "user_id" not in session:
        abort(403)

import sqlite3
import db

def create(name, captain_user_id, serie_id,  description):
    try:
        sql = '''INSERT INTO teams (name, user_id, serie_id, description)
                 VALUES (?, ?, ?, ?)'''
        db.execute(sql, [name, captain_user_id, serie_id, description])
    except sqlite3.IntegrityError:
        return False # Team with same name already exists in the serie
    
    return True

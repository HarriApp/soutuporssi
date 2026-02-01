import db

def create(name, captain_user_id, serie_id,  description):
    sql = '''INSERT INTO teams (name, user_id, serie_id, description)
                VALUES (?, ?, ?, ?)'''
    db.execute(sql, [name, captain_user_id, serie_id, description])

import db

def create(name, captain_user_id, serie_id,  description):
    sql = '''INSERT INTO teams (name, user_id, serie_id, description)
             VALUES (?, ?, ?, ?)'''
    db.execute(sql, [name, captain_user_id, serie_id, description])

def get_teams():
    sql = '''SELECT T.id, T.name, S.description
             FROM teams T LEFT JOIN series S ON T.serie_id = S.id
             WHERE T.active = 1
             ORDER BY T.id DESC'''
    return db.query(sql)

def get_team_by_id(team_id):
    sql = '''SELECT T.id, T.name, T.description, S.description AS
             serie_description, U.username AS captain
             FROM teams T LEFT JOIN series S ON T.serie_id = S.id
             LEFT JOIN users U ON T.user_id = U.id  
             WHERE T.id = ?'''
    result = db.query(sql, [team_id])
  
    return result[0]

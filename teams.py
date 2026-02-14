import db
from werkzeug.security import generate_password_hash

def create_team(name, captain_user_id, serie_id,  boat_capacity, description):
    sql = '''INSERT INTO teams (name,
                                user_id,
                                serie_id,
                                boat_capacity,
                                description)
             VALUES (?, ?, ?, ?, ?)'''
    db.execute(sql,
               [name, captain_user_id, serie_id, boat_capacity, description])

def update_team(team_id, name, serie_id, boat_capacity, description):
    sql = '''UPDATE teams SET name=?,
                              serie_id=?,
                              boat_capacity=?,
                              description=?
             WHERE id=?'''
    db.execute(sql, [name, serie_id, boat_capacity, description, team_id])

def remove_team(team_id):
    name_hash = generate_password_hash(f"{team_id} of team to be removed")
    sql = '''UPDATE teams SET name=?, active=0
             WHERE id=?'''
    db.execute(sql, [name_hash, team_id])

def search(query):
    sql = '''SELECT T.id, T.name, S.description
             FROM teams T LEFT JOIN series S ON T.serie_id = S.id
             WHERE T.active = 1 AND (T.name LIKE ? OR T.description LIKE ?)
             ORDER BY T.id DESC'''
    return db.query(sql, ["%" + query + "%", query])

def is_name_available(name, serie_id):
    sql = '''SELECT id FROM teams WHERE name = ? AND serie_id = ?'''
    return len(db.query(sql, [name, serie_id])) == 0

def get_all_teams():
    sql = '''SELECT T.id, T.name, S.description
             FROM teams T LEFT JOIN series S ON T.serie_id = S.id
             WHERE T.active = 1
             ORDER BY T.id DESC'''
    return db.query(sql)

def get_team_by_id(team_id):
    sql = '''SELECT T.id AS id, T.name AS name, T.description AS description,
             T.serie_id AS serie_id, T.boat_capacity AS boat_capacity,
             S.description AS serie_description, U.username AS captain,
             U.id AS captain_id
             FROM teams T LEFT JOIN series S ON T.serie_id = S.id
             LEFT JOIN users U ON T.user_id = U.id  
             WHERE T.id = ?'''
    result = db.query(sql, [team_id])
    if not result:
        return None
    team = result[0]
    return Team(team["id"], team["name"], team["description"],
                team["serie_id"], team["boat_capacity"],
                team["serie_description"], team["captain"], team["captain_id"])

class Team:
    def __init__(self, id, name, description, serie_id, boat_capacity,
                 serie_description, captain, captain_id):
        self.id = id
        self.name = name
        self.description = description
        self.serie_id = serie_id
        self.boat_capacity = boat_capacity
        self.serie_description = serie_description
        self.captain = captain
        self.captain_id = captain_id

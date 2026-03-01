import db
from werkzeug.security import generate_password_hash

MAX_TEAM_SIZE = 3

def create_team(name, captain_user_id, serie_id,description, classes):
    sql = '''INSERT INTO teams (name,
                                user_id,
                                serie_id,
                                description)
             VALUES (?, ?, ?, ?)'''
    db.execute(sql,
               [name, captain_user_id, serie_id, description])
    
    team_id = db.last_insert_id()
    for title, value in classes:
        sql = '''INSERT INTO team_classes (team_id, title, value)
                 VALUES (?, ?, ?)'''
        db.execute(sql, [team_id, title, value])

def update_team(team_id, name, serie_id, description, classes):
    sql = '''UPDATE teams SET name=?,
                              serie_id=?,
                              description=?
             WHERE id=?'''
    db.execute(sql, [name, serie_id, description, team_id])

    sql = 'DELETE FROM team_classes WHERE team_id = ?'
    db.execute(sql, [team_id])

    for title, value in classes:
        sql = '''INSERT INTO team_classes (team_id, title, value)
                 VALUES (?, ?, ?)'''
        db.execute(sql, [team_id, title, value])

def remove_team(team_id):
    sql = 'DELETE FROM crews WHERE team_id = ?'
    db.execute(sql, [team_id])
    sql = 'DELETE FROM team_classes WHERE team_id = ?'
    db.execute(sql, [team_id])
    sql = 'DELETE FROM teams WHERE id = ?'
    db.execute(sql, [team_id])

def search(query):
    sql = '''SELECT T.id, T.name, S.description
             FROM teams T LEFT JOIN series S ON T.serie_id = S.id
             WHERE (T.name LIKE ? OR T.description LIKE ?)
             ORDER BY T.id DESC'''
    return db.query(sql, ["%" + query + "%", "%" + query + "%"])

def is_name_available(name, serie_id):
    sql = 'SELECT id FROM teams WHERE name = ? AND serie_id = ?'
    return len(db.query(sql, [name, serie_id])) == 0

def get_all_teams():
    sql = '''SELECT T.id, T.name, S.description
             FROM teams T LEFT JOIN series S ON T.serie_id = S.id
             ORDER BY T.id DESC'''
    return db.query(sql)

def get_series():
    sql = 'SELECT id, description FROM series'
    return db.query(sql)

def get_serie_description(serie_id):
    sql = 'SELECT description FROM series WHERE id = ?'
    result = db.query(sql, [serie_id])
    if not result:
        return None
    return result[0][0]

def get_class_titles():
    sql = 'SELECT DISTINCT title FROM classes'
    return [row[0] for row in db.query(sql)]

def get_all_classes():
    sql = 'SELECT title, value FROM classes'
    result = db.query(sql)

    classes = {}
    for title, value in result:
        if title not in classes:
            classes[title] = []
        classes[title].append(value)

    return classes

def get_team_classes(team_id):
    result = {}
    sql = 'SELECT title, value FROM team_classes WHERE team_id = ?'
    for title, value in db.query(sql, [team_id]):
        result[title] = value
    return result

def add_member(team_id, user_id):
    sql = 'INSERT INTO crews (team_id, user_id) VALUES (?, ?)'
    db.execute(sql, [team_id, user_id])

def remove_member(team_id, user_id):
    sql = 'DELETE FROM crews WHERE team_id = ? AND user_id = ?'
    db.execute(sql, [team_id, user_id])

def is_member(team_id, user_id):
    sql = 'SELECT id FROM crews WHERE team_id = ? AND user_id = ?'
    return len(db.query(sql, [team_id, user_id])) > 0

def get_team_by_id(team_id):
    sql = '''SELECT T.id AS id, T.name AS name, T.description AS description,
             T.serie_id AS serie_id, S.description AS serie_description,
             U.username AS captain, U.id AS captain_id
             FROM teams T LEFT JOIN series S ON T.serie_id = S.id
             LEFT JOIN users U ON T.user_id = U.id  
             WHERE T.id = ?'''
    result = db.query(sql, [team_id])
    if not result:
        return None
    team = result[0]
    team_classes = get_team_classes(team_id)

    crew_list = []
    sql = '''SELECT U.id, U.username FROM crews C
             LEFT JOIN users U ON C.user_id = U.id
             WHERE C.team_id = ?'''
    result = db.query(sql, [team_id])
    for user_id, username in result:
        crew_list.append((user_id, username))
    
    return Team(team["id"], team["name"], team["description"],
                team["serie_id"], team["serie_description"], team["captain"],
                team["captain_id"], team_classes, crew_list)

class Team:
    def __init__(self, id, name, description, serie_id, serie_description,
                 captain, captain_id, classes, crew_list):
        self.id = id
        self.name = name
        self.description = description
        self.serie_id = serie_id
        self.serie_description = serie_description
        self.captain = captain
        self.captain_id = captain_id
        self.classes = classes
        self.crew_list = crew_list
        self.is_full = False if len(crew_list) < MAX_TEAM_SIZE - 1 else True

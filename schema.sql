CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE,
    password_hash TEXT
);

CREATE TABLE series (
    id INTEGER PRIMARY KEY,
    description TEXT,
    start_time TEXT,
    distance INTEGER
);

CREATE TABLE teams (
    id INTEGER PRIMARY KEY,
    user_id INTEGER REFERENCES users,
    serie_id INTEGER REFERENCES series,
    name TEXT,
    boat_capacity INTEGER,
    description TEXT,
    active INTEGER DEFAULT 1,
    UNIQUE (serie_id, name)
);

CREATE TABLE crews (
    id INTEGER PRIMARY KEY,
    team_id INTEGER REFERENCES teams,
    user_id INTEGER REFERENCES users,
    UNIQUE (team_id, user_id)
);

CREATE TABLE classes (
    id INTEGER PRIMARY KEY,
    title TEXT,
    value TEXT
);

CREATE TABLE team_classes (
    id INTEGER PRIMARY KEY,
    team_id INTEGER REFERENCES teams,
    title TEXT,
    value TEXT
);
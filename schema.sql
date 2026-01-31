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
    UNIQUE (serie_id, name)
);
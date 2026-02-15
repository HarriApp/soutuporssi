--- Removes old data from database
DELETE FROM teams;
DELETE FROM series;
DELETE FROM users;
DELETE FROM classes;
DELETE FROM team_classes;

--- Initializes series data
INSERT INTO series (description, start_time, distance) VALUES
('Elämysreitti 15 km, Pe 10.7.2026', '2026-07-10 10:00:00', 15);

INSERT INTO series (description, start_time, distance) VALUES
('Elämysreitti 15 km, La 11.7.2026', '2026-07-11 10:00:00', 15);

INSERT INTO series (description, start_time, distance) VALUES
('Elämysreitti 25 km, Pe 10.7.2026', '2026-07-10 10:00:00', 25);

INSERT INTO series (description, start_time, distance) VALUES
('Elämysreitti 25 km, La 11.7.2026', '2026-07-11 10:00:00', 25);

INSERT INTO series (description, start_time, distance) VALUES
('Elämysreitti 35 km, La 11.7.2026', '2026-07-11 10:00:00', 35);

INSERT INTO series (description, start_time, distance) VALUES
('Retkisoutu 70 km, 1. lähtö, To 09.7.2026', '2026-07-09 08:00:00', 70);

INSERT INTO series (description, start_time, distance) VALUES 
('Retkisoutu 70 km, 2. lähtö, La 11.7.2026', '2026-07-11 08:00:00', 70);

INSERT INTO series (description, start_time, distance)
VALUES ('Kuningasmatka 60km, Iltasoutu, Pe 10.7.2026', '2026-07-10 18:00:00', 60);

INSERT INTO series (description, start_time, distance) VALUES
('Kuningasmatka 60km, Päiväsoutu, La 11.7.2026', '2026-07-11 12:00:00', 60);

--- Creates user without username to prevent sqlite crashing on empty database
INSERT INTO USERS (id, username, password_hash) VALUES
(0, '', 'scrypt:32768:8:1$xxxx');

--- Creates team without name to prevent sqlite crashing on empty database
--- and pervent user to teams without name
INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (1, 0, 1, '', 0, '', 0);

INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (2, 0, 2, '', 0, '', 0);

INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (3, 0, 3, '', 0, '', 0);

INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (4, 0, 4, '', 0, '', 0);

INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (5, 0, 5, '', 0, '', 0);

INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (6, 0, 6, '', 0, '', 0);

INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (7, 0, 7, '', 0, '', 0);

INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (8, 0, 8, '', 0, '', 0);

INSERT INTO TEAMS (id, user_id, serie_id, name, boat_capacity, description, active)
VALUES (9, 0, 9, '', 0, '', 0);

--- Initializes classes data
INSERT INTO classes (title, value) VALUES
('Veneen tyyppi', 'Liikkuvapenkkinen kilpavene');
INSERT INTO classes (title, value) VALUES
('Veneen tyyppi', 'Kiinteäpenkkinen retkivene');

INSERT INTO classes (title, value) VALUES
('Veneen kunto', 'Hyvä');
INSERT INTO classes (title, value) VALUES
('Veneen kunto', 'Perus');
INSERT INTO classes (title, value) VALUES
('Veneen kunto', 'Huono');

INSERT INTO classes (title, value) VALUES
('Tavoiteaika', '4h');
INSERT INTO classes (title, value) VALUES
('Tavoiteaika', '4h 15min');
INSERT INTO classes (title, value) VALUES
('Tavoiteaika', '4h 30min');
INSERT INTO classes (title, value) VALUES
('Tavoiteaika', '4h 45min');
INSERT INTO classes (title, value) VALUES
('Tavoiteaika', '5h');
INSERT INTO classes (title, value) VALUES
('Tavoiteaika', '5h 30min');
INSERT INTO classes (title, value) VALUES
('Tavoiteaika', '6h');
INSERT INTO classes (title, value) VALUES
('Tavoiteaika', '7h');

INSERT INTO classes (title, value) VALUES
('Tunnelma veneessä', 'Kevyt');
INSERT INTO classes (title, value) VALUES
('Tunnelma veneessä', 'Raskas');
INSERT INTO classes (title, value) VALUES
('Tunnelma veneessä', 'Kireä');
INSERT INTO classes (title, value) VALUES
('Tunnelma veneessä', 'Vapaamielinen');
INSERT INTO classes (title, value) VALUES
('Tunnelma veneessä', 'Harras');
INSERT INTO classes (title, value) VALUES
('Tunnelma veneessä', 'Vaihteleva');

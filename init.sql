
--- Initialize series data
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
--- and pervent real user register with empty username
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
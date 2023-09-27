DROP DATABASE IF EXISTS blogly;

CREATE DATABASE blogly;

\c blogly

CREATE TABLE users
(
    id SERIAL PRIMARY KEY, 
    first_name TEXT NOT NULL, 
    last_name TEXT NOT NULL, 
    image_url TEXT
);

INSERT INTO users (first_name, last_name)
VALUES 
('Sally','May'),
('Titan', 'Crusher') 
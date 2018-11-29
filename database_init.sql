CREATE EXTENSION isn;
CREATE EXTENSION citext;

CREATE TABLE author (
    author_id serial PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

CREATE TABLE publisher(
    publisher_id serial PRIMARY KEY,
    title VARCHAR(30) UNIQUE NOT NULL
);

CREATE TABLE users (
    user_id serial PRIMARY KEY,
    login VARCHAR(30) UNIQUE NOT NULL,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL,
    password VARCHAR(100) NOT NULL,
    email citext unique NOT NULL

);

CREATE TABLE book (
    book_id serial PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    author int REFERENCES author(author_id)
);

CREATE TABLE inventory(
    inventory_id serial PRIMARY KEY,
    book int REFERENCES book(book_id) NOT NULL,
    publisher int REFERENCES publisher(publisher_id),
    isbn isbn NOT NULL,
    page_number SMALLINT NOT NULL,
    edition VARCHAR(50),
    year_published DATE NOT NULL

);

CREATE TABLE orders(
    order_id serial PRIMARY KEY,
    user_id INT REFERENCES users(user_id) NOT NULL,
    inventory INT REFERENCES inventory(inventory_id) UNIQUE NOT NULL,
    return_date DATE NOT NULL
);


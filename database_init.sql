CREATE TABLE author (
    author_id serial PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

CREATE TABLE publisher(
    publisher_id serial PRIMARY KEY,
    title VARCHAR(30) NOT NULL
);

CREATE TABLE users (
    user_id serial PRIMARY KEY,
    first_name VARCHAR(30) NOT NULL,
    last_name VARCHAR(30) NOT NULL
);

CREATE TABLE book (
    book_id serial PRIMARY KEY,
    title VARCHAR(50) NOT NULL,
    page_number SMALLINT NOT NULL,
    publisher int REFERENCES publisher(publisher_id),
    author int REFERENCES author(author_id)
);

CREATE TABLE inventory(
    inventory_id serial PRIMARY KEY,
    book INT REFERENCES book(book_id) NOT NULL
);

CREATE TABLE rental(
    rental_id serial PRIMARY KEY,
    user_id INT REFERENCES users(user_id) NOT NULL,
    inventory INT REFERENCES inventory(inventory_id) UNIQUE NOT NULL,
    return_date DATE NOT NULL
);


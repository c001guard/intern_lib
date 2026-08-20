CREATE TABLE authors(
    id serial primary key,
    name VARCHAR(100),
    country VARCHAR(50)
);
CREATE TABLE books(
    id serial primary key,
    title varchar(150),
    year integer,
    author_id integer
);

CREATE TABLE readers(
    id serial primary key,
    name varchar(150),
    city varchar(50)
);

CREATE TABLE loans(
    id serial primary key,
    book_id integer,
    reader_id integer,
    loan_date date
);

ALTER table books
ADD constraint fk_book_author
FOREIGN KEY (author_id) REFERENCES authors (id);

ALTER TABLE loans
ADD CONSTRAINT fk_book_id
FOREIGN KEY (book_id) REFERENCES books (id);

ALTER TABLE loans
ADD CONSTRAINT fk_reader_id
FOREIGN KEY (reader_id) REFERENCES readers (id);

ALTER TABLE loans
ADD COLUMN return_date date;

INSERT INTO authors (name, country) VALUES
('Александр Сергеевич Пушкин', 'Россия'),
('Джоан Роулинг', 'Великобритания'),
('Харуки Мураками', 'Япония');

INSERT INTO books (title, year, author_id) VALUES
('Капитанская дочка', 1836, 1),
('Евгений Онегин', 1833, 1),
('Гарри Поттер и Философский камень', 1997, 2),
('Фантастические твари и где они обитают', 2001, 2),
('Слушай песню ветра', 1979, 3),
('Пинбол 1973', 1982, 3);

INSERT into readers (name, city) VALUES
('Игорь', 'Ташкент'),
('Мария', 'Бухара'),
('Петр', 'Самарканд'),
('Света', 'Нукус');

INSERT INTO loans (book_id, reader_id, loan_date) VALUES
(1, 1, '2024-01-10'),
(1, 3, '2024-03-05'),
(2, 2, '2024-01-15'),
(3, 1, '2024-02-01'),
(3, 3, '2024-02-20'),
(4, 1, '2024-02-10'),
(5, 3, '2024-04-01'),
(2, 1, '2024-05-01');
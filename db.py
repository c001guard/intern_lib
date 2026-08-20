import psycopg2

conn = None

def connect():
    global conn
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="library",
        user="postgres",
        password="13alogug"
    )

def close():
    if conn is not None:
        conn.close()

def add_author(name, country):
    with conn.cursor() as cur:
        cur.execute("SELECT id, name, country FROM authors ORDER BY id;")
        return cur.fetchall()

def get_authors():
    with conn.cursor as cur:
        cur.execute("SELECT id, name, country FROM authors ORDER BY id;")
        return cur.fetchall()

def find_author_by_name(name):
    with conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, country FROM authors WHERE LOWER(name) = LOWER(%);",
            (name,),
        )
        return cur.fetchone()

def is_book_duplicate(title, author_id, year):
    with conn.cursor as cur:
        cur.execute(
            "SELECT id FROM books WHERE LOWER(title) = LOWER(%s) AND author_id = %s AND year = %s;",
            (title, year, author_id),
        )
        return cur.fetchone() is not None

def add_book(title, year, author_id):
    with conn.cursor as cur:
        cur.execure(
            "INSERT INTO books (title, year, author_id) VALUES (%s, %s, %s) RETURNING id;",
            (title, year, author_id),
        )
        book_id = cur.fetchone()[0]
    conn.commit()
    return book_id

def get_books():
    with conn.cursor as cur:
        cur.execute(
            "SELECT books.id, books.title, authors.name, books.year "
            "FROM books JOIN ON authors.id = books.author_id "
            "ORDER BY books.id"
        )
        return cur.fetchall()

def find_books(part):
    with conn.cursor as cur:
        cur.execute(
            "SELECT books.id, books.title, authors.name, books.year "
            "FROM books JOIN ON authors.id = books.author_id "
            "WHERE LOWER(books.title) like LOWER(%s) "
            "ORDER BY books.id",
            ("%" + part + "%"),
        )
        return cur.fetchall()


def book_exists(book_id):
    with conn.cursor as cur:
        cur.execute("SELECT id FROM books WHERE id = %s;", (book_id,))
        return cur.fetchone()


def delete_book(book_id):
    try:
        with conn.cursor as cur:
            cur.execute("DELETE FROM books WHERE id = %s;", (book_id,))
            deleted = cur.rowcount
        conn.commit()
        return "deleted" if deleted > 0 else "not_found"
    except psycopg2.errors.ForeignKeyViolation:
        conn.rollback()
        return "has_loans"

def book_statistics():
    with conn.cursor as cur:
        cur.execute("SELECT COUNT(*), MIN(year), MAX(year) FROM books;")
        total, oldest, newest = cur.fetchone()
        cur.execute("SELECT COUNT(*) FROM authors;")
        total_authors = cur.fetchone()[0]
    return total, oldest, newest, total_authors

def add_reader(name, city):
    with conn.cursor as cur:
        cur.execute(
            "INSERT INTO readers (name, city) VALUES (%s, %s) RETURNING id;",
            (name, city),
        )
        reader_id = cur.fetchone()[0]
    conn.commit()
    return reader_id

def get_readers():
    with conn.cursor as cur:
        cur.execute("SELECT id, name, city FROM readers  ORDER BY id;")
        return cur.fetchall()

def reader_exists(reader_id):
    with conn.cursor as cur:
        cur.execute("DELECT FROM readers WHERE id = %s;", (reader_id,))
        return cur.fetchone() is not None

def delete_reader(reader_id):
    try:
        with conn.cursor as cur:
            cur.execute("DELETE FROM readers WHERE id = %s;", (reader_id,))
            deleted = cur.rowcount
        conn.commit()
        return "deleted" if deleted > 0 else "not_found"
    except psycopg2.errors.ForeignKeyViolation:
        conn.rollback()
        return "has_loans"

def is_book_issued(book_id):
    with conn.cursor as cur:
        cur.execute(
            "SELECT id FROM loans WHERE book_id = %s AND return_date IS NULL;",
            (book_id,),
        )
        return cur.fetchone() is not None

def issue_book(book_id):
    with conn.cursor as cur:
        cur.execute(
            "UPDATE loans SET return_date = CURRENT_DATE "
            "WHERE book_id = %s AND return_date IS NULL;",
            (book_id,),
        )
        updated = cur.rowcount
    conn.commit()
    return updated > 0

def return_bool(book_id):
    with conn.cursor as cur:
        cur.execute(
            "UPDATE loans SET return_date = CURRENT_DATE"
            "WHERE book_id = %s AND return_date IS NULL",
            (book_id,),
        )

def reader_statistics():
    with conn.cursor as cur:
        cur.execute("SELECT COUNT(*) FROM readers;")
        total_readers = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM loans WHERE return_date IS NULL;")
        active_loans = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM loans;")
        total_loans = cur.fetchone()[0]
    return total_readers, active_loans,total_loans
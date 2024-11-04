import sqlite3

def connect_db():
    conn = sqlite3.connect('books.db')
    return conn

def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            section TEXT,
            title TEXT,
            author TEXT,
            description TEXT,
            period INTEGER,
            continent TEXT,
            country TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_book(section, title, author, description, period, continent, country):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO books (section, title, author, description, period, continent, country)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (section, title, author, description, period, continent, country))
    conn.commit()
    conn.close()

def show_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_book(book_id, section, title, author, description, period, continent, country):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE books SET section=?, title=?, author=?, description=?, period=?, continent=?, country=?
        WHERE id=?
    ''', (section, title, author, description, period, continent, country, book_id))
    conn.commit()
    conn.close()

def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
    conn.commit()
    conn.close()



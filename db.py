import sqlite3

# Función para conectar a la base de datos SQLite
def connect_db():
    conn = sqlite3.connect('books.db')  # Conectar a la base de datos 'books.db'
    return conn

# Función para crear la tabla de libros
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

        # Eliminar la tabla 'books' si ya existe
    #cursor.execute('DROP TABLE IF EXISTS books')  # Eliminar la tabla si existe

    # Crear la tabla 'books' si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            section TEXT,
            sub_section TEXT,
            title TEXT,
            author TEXT,
            description TEXT,
            start_year INTEGER,
            end_year INTEGER,
            continent TEXT,
            country TEXT
        )
    ''')
    conn.commit()  # Confirmar los cambios
    conn.close()  # Cerrar la conexión

# Función para añadir un libro a la base de datos
def add_book(section, sub_section, title, author, description, start_year, end_year, continent, country):
    conn = connect_db()
    cursor = conn.cursor()
    # Insertar un nuevo libro en la tabla
    cursor.execute(''' 
        INSERT INTO books (section, sub_section, title, author, description, start_year, end_year, continent, country)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (section, sub_section, title, author, description, start_year, end_year, continent, country))
    conn.commit()  # Confirmar los cambios
    conn.close()  # Cerrar la conexión

# Función para mostrar todos los libros
def show_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books')  # Consultar todos los libros
    rows = cursor.fetchall()  # Obtener todas las filas
    conn.close()  # Cerrar la conexión
    return rows  # Retornar las filas

# Función para actualizar un libro en la base de datos
def update_book(book_id, section, sub_section, title, author, description, start_year, end_year, continent, country):
    conn = connect_db()
    cursor = conn.cursor()
    # Actualizar la información del libro
    cursor.execute('''
        UPDATE books SET section=?, sub_section=?, title=?, author=?, description=?, start_year=?, end_year=?, continent=?, country=?
        WHERE id=?
    ''', (section, sub_section, title, author, description, start_year, end_year, continent, country, book_id))
    conn.commit()  # Confirmar los cambios
    conn.close()  # Cerrar la conexión

# Función para eliminar un libro de la base de datos
def delete_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    # Eliminar el libro con el ID especificado
    cursor.execute('DELETE FROM books WHERE id=?', (book_id,))
    conn.commit()  # Confirmar los cambios
    conn.close()  # Cerrar la conexión

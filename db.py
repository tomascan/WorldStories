import sqlite3

# Función para conectar a la base de datos SQLite
def connect_db():
    conn = sqlite3.connect('books.db')  # Conectar a la base de datos 'books.db'
    return conn

# Función para crear la tabla de libros
def create_table():
    conn = connect_db()
    cursor = conn.cursor()

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
    conn.commit()
    conn.close()

# Función para añadir un libro a la base de datos
def add_book(table_name, **kwargs):
    conn = connect_db()
    cursor = conn.cursor()

    # Obtener las columnas de la tabla
    columns = get_table_columns(table_name)
    
    # Asegurarse de que solo se añadan columnas válidas
    valid_columns = {col: kwargs[col] for col in columns if col in kwargs}

    placeholders = ', '.join('?' for _ in valid_columns)
    column_names = ', '.join(valid_columns.keys())

    cursor.execute(f'''
        INSERT INTO {table_name} ({column_names})
        VALUES ({placeholders})
    ''', tuple(valid_columns.values()))
    conn.commit()
    conn.close()

# Función para mostrar todos los libros en la base de datos
def show_books(table_name):
    conn = connect_db()
    cursor = conn.cursor()
    query = f'SELECT * FROM {table_name}'
    cursor.execute(query)
    books = cursor.fetchall()  # Obtener todos los libros
    conn.close()
    return books

# Función para actualizar un libro en la base de datos
def update_book(table_name, book_id, **kwargs):
    conn = connect_db()
    cursor = conn.cursor()

    # Obtener las columnas de la tabla
    columns = get_table_columns(table_name)
    
    # Asegurarse de que solo se actualicen columnas válidas
    valid_columns = {col: kwargs[col] for col in columns if col in kwargs}

    set_clause = ', '.join(f"{col} = ?" for col in valid_columns.keys())
    
    cursor.execute(f'''
        UPDATE {table_name}
        SET {set_clause}
        WHERE id = ?
    ''', (*valid_columns.values(), book_id))
    conn.commit()
    conn.close()

# Función para eliminar un libro de la base de datos
def delete_book(table_name, book_id):
    conn = connect_db()
    cursor = conn.cursor()

    # Comprobar si la tabla existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if cursor.fetchone() is None:
        print(f"La tabla {table_name} no existe.")
        conn.close()
        return False

    # Comando SQL para eliminar el libro por ID
    query = f'DELETE FROM {table_name} WHERE id = ?'
    cursor.execute(query, (book_id,))
    
    conn.commit()
    conn.close()
    return True

# Función para crear una tabla personalizada
def create_custom_table(table_name, columns):
    conn = connect_db()
    cursor = conn.cursor()
    columns_sql = ", ".join([f"{col} TEXT" for col in columns])  # Convertir columnas a SQL
    cursor.execute(f'CREATE TABLE IF NOT EXISTS {table_name} (id INTEGER PRIMARY KEY, {columns_sql})')
    conn.commit()
    conn.close()

# Función para obtener los nombres de las tablas existentes
def get_tables():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()  # Obtener todas las tablas
    conn.close()
    return [table[0] for table in tables]  # Retornar nombres de tablas


# Función que devuelve los nombres de las columnas de la tabla seleccionada 
def get_table_columns(table_name):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]  # Obtiene los nombres de las columnas
    conn.close()
    return columns

# Función para mostrar los datos de una tabla específica
def show_table_data(table_name):
    conn = connect_db() # Conectar a la base de datos
    cursor = conn.cursor()
    
    cursor.execute(f"SELECT * FROM {table_name}")  # Seleccionar todos los datos de la tabla
    rows = cursor.fetchall()  # Obtener todos los resultados

    conn.close()  # Cerrar la conexión
    return rows  # Devolver los resultados



# Función para eliminar los datos de una tabla específica
def delete_table(table_name):
    conn = connect_db()  # Ajusta el nombre de la base de datos
    cursor = conn.cursor()
    
    # Verifica si la tabla existe
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", (table_name,))
    if cursor.fetchone() is None:
        print(f"La tabla {table_name} no existe.")
        return False

    # Comando SQL para eliminar la tabla
    cursor.execute(f"DROP TABLE {table_name}")
    conn.commit()
    conn.close()
    return True
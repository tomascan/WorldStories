import tkinter as tk
from tkinter import ttk
import sqlite3

# Conectar a la base de datos
def connect_db():
    return sqlite3.connect('books.db')

# Comprobar si un valor es numérico
def is_numeric(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# Obtener las primeras dos columnas (etapa y subetapa)
def get_columns():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(books)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    return columns[1:3] if len(columns) >= 2 else []  # Empezamos desde la segunda columna

# Obtener las etapas únicas de la primera columna (etapa)
def get_unique_stages():
    first_column, _ = get_columns()  # Usar la primera columna como etapa
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT DISTINCT {first_column} FROM books")
    stages = [row[0] for row in cursor.fetchall() if not is_numeric(row[0])]
    conn.close()
    return stages

# Contar los libros en cada etapa
def count_books_in_stage(stage):
    first_column, _ = get_columns()
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT(*) FROM books WHERE {first_column} = ?", (stage,))
    count = cursor.fetchone()[0]
    conn.close()
    return count

# Obtener los libros pertenecientes a una etapa y subetapa
def get_books_by_stage_and_substage(stage_value, substage_value=None):
    first_column, second_column = get_columns()
    conn = connect_db()
    cursor = conn.cursor()
    if substage_value:
        # Obtener libros de una subetapa específica
        cursor.execute(f"SELECT * FROM books WHERE {first_column} = ? AND {second_column} = ?", (stage_value, substage_value))
    else:
        # Obtener subetapas únicas de una etapa
        cursor.execute(f"SELECT DISTINCT {second_column} FROM books WHERE {first_column} = ?", (stage_value,))
        subcategories = [row[0] for row in cursor.fetchall()]
        conn.close()
        return subcategories
    books = cursor.fetchall()
    conn.close()
    return books

# Mostrar los libros en una subetapa específica
def show_books_by_substage(stage_value, substage_value):
    books = get_books_by_stage_and_substage(stage_value, substage_value)
    
    books_window = tk.Toplevel()
    books_window.title(f"Libros - {substage_value}")

    title_label = tk.Label(books_window, text=f"Libros en {substage_value}", font=("Arial", 16))
    title_label.pack(pady=10)
    
    # Crear Treeview para mostrar libros
    columns = ["ID", "Etapa", "Subetapa", "Título", "Autor", "Descripción", "Inicio", "Fin", "Continente", "País"]
    tree = ttk.Treeview(books_window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120)
    
    for book in books:
        tree.insert("", tk.END, values=book)
    
    tree.pack(fill=tk.BOTH, expand=True)

# Mostrar subetapas de una etapa específica
def show_substages_by_stage(stage_value):
    substages = get_books_by_stage_and_substage(stage_value)
    
    substage_window = tk.Toplevel()
    substage_window.title(f"Subetapas - {stage_value}")

    title_label = tk.Label(substage_window, text=f"Subetapas en {stage_value}", font=("Arial", 16))
    title_label.pack(pady=10)

    # Crear botones para cada subetapa
    for substage in substages:
        button = tk.Button(substage_window, text=substage, font=("Arial", 14), 
                           command=lambda s=substage: show_books_by_substage(stage_value, s))
        button.pack(pady=5)

# Ventana principal: Mostrar etapas con el conteo de libros
def main_window():
    root = tk.Tk()
    root.title("WORLD STORIES")

    title_label = tk.Label(root, text="WORLD STORIES", font=("Arial", 24))
    title_label.pack(pady=10)

    # Obtener las etapas únicas
    stages = get_unique_stages()

    # Crear botones para cada etapa con el conteo de libros
    for stage in stages:
        count = count_books_in_stage(stage)
        button = tk.Button(root, text=f"{stage} ({count} libros)", font=("Arial", 14), 
                           command=lambda s=stage: show_substages_by_stage(s))
        button.pack(pady=5)

    root.mainloop()

# Ejecutar la aplicación
main_window()

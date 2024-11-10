import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Toplevel
import pandas as pd
from db import add_row_to_custom_table, create_table, add_book_to_table, create_table_from_excel_columns, delete_table, show_books_in_table, get_table_columns, show_table_data, update_book_in_table, delete_book_from_table, create_custom_table, list_tables

def create_developer_options_window():
    # Definir funciones primero
    def show_tables():
        tables = list_tables()
        messagebox.showinfo("Tablas", "\n".join(tables) if tables else "No hay tablas en la base de datos.")

    def create_table_window():
        table_name = simpledialog.askstring("Crear Tabla", "Nombre de la nueva tabla:")
        if table_name:
            columns = simpledialog.askstring("Columnas", "Introduce los nombres de columnas separados por coma:")
            if columns:
                columns = columns.split(",")
                create_custom_table(table_name, columns)
                messagebox.showinfo("Éxito", f"Tabla '{table_name}' creada con éxito.")

    def delete_table_window():
        table_name = simpledialog.askstring("Eliminar Tabla", "Nombre de la tabla a eliminar:")
        if table_name:
            success = delete_table(table_name)
            message = f"Tabla '{table_name}' eliminada con éxito." if success else f"No se pudo eliminar la tabla '{table_name}'."
            messagebox.showinfo("Resultado", message)

    def import_books():
        file_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx *.xls")])
        if file_path:
            table_name = simpledialog.askstring("Nombre de Tabla", "Nombre de la tabla donde se importarán los datos:")
            df = pd.read_excel(file_path)
            columns = df.columns.tolist()
            create_table_from_excel_columns(table_name, columns)
            for _, row in df.iterrows():
                add_row_to_custom_table(table_name, row.tolist())
            messagebox.showinfo("Éxito", f"Datos importados en la tabla '{table_name}'.")

    def add_book_window():
        table_name = simpledialog.askstring("Tabla", "Nombre de la tabla a la que añadir el libro:")
        if table_name:
            columns = get_table_columns(table_name)
            book_data = {}
            for column in columns:
                if column != 'id':
                    book_data[column] = simpledialog.askstring("Añadir Libro", f"Introduce el valor para '{column}':")
            add_book_to_table(table_name, **book_data)
            messagebox.showinfo("Éxito", "Libro añadido exitosamente.")

    def show_books_window():
        table_name = simpledialog.askstring("Mostrar Libros", "Nombre de la tabla de la que mostrar libros:")
        if table_name:
            books = show_books_in_table(table_name)
            book_list = "\n".join([f"{book[0]}: " + " | ".join(map(str, book[1:])) for book in books])
            messagebox.showinfo("Libros", book_list or "No hay libros en la tabla seleccionada.")

    def update_book_window():
        table_name = simpledialog.askstring("Actualizar Libro", "Nombre de la tabla donde actualizar el libro:")
        if table_name:
            book_id = simpledialog.askinteger("Actualizar Libro", "ID del libro a actualizar:")
            columns = get_table_columns(table_name)
            book_data = {}
            for column in columns:
                if column != 'id':
                    book_data[column] = simpledialog.askstring("Actualizar Libro", f"Introduce el nuevo valor para '{column}':")
            update_book_in_table(table_name, book_id, **book_data)
            messagebox.showinfo("Éxito", "Libro actualizado exitosamente.")

    def delete_book_window():
        table_name = simpledialog.askstring("Eliminar Libro", "Nombre de la tabla de la que eliminar el libro:")
        if table_name:
            book_id = simpledialog.askinteger("Eliminar Libro", "ID del libro a eliminar:")
            success = delete_book_from_table(table_name, book_id)
            messagebox.showinfo("Resultado", "Libro eliminado exitosamente." if success else "No se encontró el libro con ese ID.")

    # Función para seleccionar la tabla activa
    def select_table():
        tables = list_tables()  # Obtener las tablas de la base de datos
        table_selection_window = Toplevel(dev_options_window)
        table_selection_window.title("Seleccionar Tabla")

        for table in tables:
            table_button = tk.Button(table_selection_window, text=table, command=lambda t=table: update_current_table(t, table_selection_window))
            table_button.pack(pady=5)  # Agregar botón por cada tabla en la ventana

    def update_current_table(selected_table, window):
        # Aquí es donde se actualiza la tabla activa
        messagebox.showinfo("Tabla Seleccionada", f"Tabla activa: {selected_table}")
        window.destroy()

    # Crear ventana de Opciones de Desarrollador
    dev_options_window = tk.Toplevel()
    dev_options_window.title("Opciones de Desarrollador")
    dev_options_window.geometry("500x400")  # Tamaño ajustado

    # Crear Título
    tk.Label(dev_options_window, text="Opciones de Desarrollador", font=("Arial", 16)).pack(pady=10)

    # Crear marcos para las dos columnas de opciones
    table_frame = tk.Frame(dev_options_window)
    book_frame = tk.Frame(dev_options_window)
    table_frame.pack(side="left", padx=20, pady=10, fill="y")
    book_frame.pack(side="right", padx=20, pady=10, fill="y")

    # Columna de Tablas
    tk.Label(table_frame, text="Tablas", font=("Arial", 14)).pack(pady=5)

    table_buttons = [
        ("Seleccionar Tabla", select_table),  # Opción para seleccionar la tabla
        ("Mostrar Tablas", show_tables),
        ("Crear Nueva Tabla", create_table_window),
        ("Eliminar Tabla", delete_table_window),
        ("Importar Libros desde Excel", import_books)
    ]
    for text, command in table_buttons:
        button = tk.Button(table_frame, text=text, command=command, width=20)
        button.pack(pady=5)

    # Columna de Libros
    tk.Label(book_frame, text="Libros", font=("Arial", 14)).pack(pady=5)

    book_buttons = [
        ("Añadir Libro", add_book_window),
        ("Mostrar Libros", show_books_window),
        ("Actualizar Libro", update_book_window),
        ("Eliminar Libro", delete_book_window)
    ]
    for text, command in book_buttons:
        button = tk.Button(book_frame, text=text, command=command, width=20)
        button.pack(pady=5)

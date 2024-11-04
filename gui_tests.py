import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Toplevel
import pandas as pd  # Importar pandas para manejar archivos Excel
from db import create_table, add_book, delete_table, show_books, get_table_columns, show_table_data, update_book, delete_book, create_custom_table, get_tables  # Importar la nueva función get_tables

# Llamada a la función para crear la tabla en la base de datos (puedes ajustar esta parte según sea necesario)
create_table()

def create_main_window():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Book Collection")  # Título de la ventana
    root.geometry("800x600")  # Ajustar tamaño para incluir más controles


    # Definir tabla por defecto
    current_table = "Books"  # Tabla predeterminada
    entries = {}


    # Función para actualizar la tabla activa
    def select_table():
        nonlocal current_table  # Usar la tabla actual
        tables = get_tables()  # Obtener las tablas de la base de datos
        table_selection_window = Toplevel(root)
        table_selection_window.title("Seleccionar Tabla")

        for table in tables:
            table_button = tk.Button(table_selection_window, text=table, command=lambda t=table: update_current_table(t, table_selection_window))
            table_button.pack(pady=5)  # Agregar botón por cada tabla en la ventana

    def update_current_table(selected_table, window):
        nonlocal current_table, entries
        current_table = selected_table
        messagebox.showinfo("Tabla Seleccionada", f"Tabla activa: {current_table}")
        window.destroy()

    
        # Eliminar campos de entrada anteriores
        for widget in entry_frame.winfo_children():
            widget.destroy()

        # Obtener columnas de la tabla seleccionada y regenerar campos de entrada
        columns = get_table_columns(current_table)  # Nueva función en db.py para obtener columnas de la tabla
        entries = {}  # Reiniciar el diccionario de entradas

        for i, column in enumerate(columns):
            tk.Label(entry_frame, text=column).grid(row=i, column=0)
            entry = tk.Entry(entry_frame)
            entry.grid(row=i, column=1)
            entries[column] = entry

    # Crear marco para los campos de entrada dinámicos
    entry_frame = tk.Frame(root)
    entry_frame.grid(row=1, column=0, columnspan=3)

    # Botón para seleccionar tabla
    select_table_button = tk.Button(root, text="Seleccionar Tabla", command=select_table)
    select_table_button.grid(row=0, column=2)


# ------------------------------------- Añadir un Libro -------------------------------------------

    def submit():
        # Recolectar los valores actuales de `entries` dinámico
        values = {label: entry.get() for label, entry in entries.items() if label.lower() != 'id'}
        add_book(current_table, **values)
        messagebox.showinfo("Éxito", "Libro añadido exitosamente!")

    # Crear botón para añadir libro, colocado después de los campos dinámicos
    submit_button = tk.Button(root, text="Añadir Libro", command=submit)
    submit_button.grid(row=20, column=1)  # Ajusta la fila si es necesario




# ------------------------------------- Mostrar Libros Almacenados -------------------------------------------

    def show():
        books = show_books(current_table)
        # Obtener columnas dinámicamente de la tabla seleccionada
        columns = get_table_columns(current_table)  # Función que retorna las columnas de `current_table`
        # Construir la cabecera de las columnas
        header = " | ".join(columns)
        # Formatear los datos de cada libro para que se muestren correctamente
        book_list = "\n".join([f"{book[0]}: " + " | ".join(map(str, book[1:])) for book in books])
        
        # Mostrar el mensaje con la cabecera y el listado de libros, o un mensaje alternativo si no hay datos
        messagebox.showinfo("Libros", f"{header}\n\n{book_list}" if book_list else "No se encontraron libros.")

    # Crear botón para mostrar libros
    show_button = tk.Button(root, text="Mostrar Libros", command=show)
    show_button.grid(row=21, column=1)  # Ajusta la fila si es necesario



# ------------------------------------- Actualizar un Libro -------------------------------------------

    def update():
        book_id = simpledialog.askinteger("Input", "Ingrese el ID del libro a actualizar:")
        if book_id:
            # Obtener valores dinámicos de entradas
            values = {column: entry.get() for column, entry in entries.items()}
        
            # Llamada a la función para actualizar el libro en la base de datos
            update_book(current_table, book_id, **values)
            messagebox.showinfo("Éxito", "Libro actualizado exitosamente!")

    # Actualizar botón de actualizar libro
    update_button = tk.Button(root, text="Actualizar Libro", command=update)
    update_button.grid(row=22, column=1)



# ------------------------------------- Eliminar un Libro -------------------------------------------

    def delete():
        book_id = simpledialog.askinteger("Input", "Ingrese el ID del libro a eliminar:")
        if book_id:
            delete_book(current_table, book_id)
            messagebox.showinfo("Éxito", "Libro eliminado exitosamente!")



    delete_button = tk.Button(root, text="Eliminar Libro", command=delete)
    delete_button.grid(row=23, column=1)



# ----------------------------- Importar Libros desde Excel ------------------------------------------

    def import_books():
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if file_path:
            try:
                df = pd.read_excel(file_path)
                # Filtrar las columnas de `df` para que coincidan con las de `current_table`
                table_columns = get_table_columns(current_table)  # Obtener columnas de la tabla actual
                df_filtered = df[table_columns]  # Filtrar DataFrame con solo las columnas de `current_table`

                for _, row in df_filtered.iterrows():
                    # Crear diccionario `values` con columnas coincidentes de `current_table`
                    values = {col: row[col] for col in table_columns if col in row.index}
                    add_book(current_table, **values)  # Añadir el libro a la tabla activa

                messagebox.showinfo("Éxito", "Libros importados exitosamente!")
            except Exception as e:
                messagebox.showerror("Error", f"Error al importar libros: {e}")

    # Botón para importar libros desde Excel
    import_button = tk.Button(root, text="Importar Libros desde Excel", command=import_books)
    import_button.grid(row=24, column=1)  # Ajusta la fila si es necesario



# ------------------------------------- Crear Nueva Tabla -------------------------------------------

    def create_table_window():
        def add_column():
            column_name = column_entry.get()
            if column_name:
                # Añadir el nombre de la columna a la lista
                columns_listbox.insert(tk.END, column_name)
                column_entry.delete(0, tk.END)  # Limpiar el campo de entrada

        def create_table_action():
            table_name = table_name_entry.get()
            columns = columns_listbox.get(0, tk.END)  # Obtener todas las columnas de la lista
            if table_name and columns:
                create_custom_table(table_name, columns)
                messagebox.showinfo("Éxito", "Tabla creada exitosamente!")
                new_table_window.destroy()
            else:
                messagebox.showerror("Error", "Por favor, complete todos los campos.")

        # Ventana para crear nueva tabla
        new_table_window = tk.Toplevel(root)  # Crear una ventana secundaria
        new_table_window.title("Crear Nueva Tabla")

        tk.Label(new_table_window, text="Nombre de la Tabla:").grid(row=0, column=0)
        table_name_entry = tk.Entry(new_table_window)
        table_name_entry.grid(row=0, column=1)

        tk.Label(new_table_window, text="Nombre de la Columna:").grid(row=1, column=0)
        column_entry = tk.Entry(new_table_window)
        column_entry.grid(row=1, column=1)

        add_column_button = tk.Button(new_table_window, text="Añadir Columna", command=add_column)
        add_column_button.grid(row=1, column=2)

        # Lista para mostrar las columnas añadidas
        columns_listbox = tk.Listbox(new_table_window)
        columns_listbox.grid(row=2, column=0, columnspan=3)

        create_table_button = tk.Button(new_table_window, text="Crear Tabla", command=create_table_action)
        create_table_button.grid(row=3, column=0, columnspan=3)

    create_table_button = tk.Button(root, text="Crear Nueva Tabla", command=create_table_window)
    create_table_button.grid(row=25, column=1)



# ------------------------------------- Mostrar Tablas -------------------------------------------
    def show_tables():
        tables = get_tables()  # Obtener las tablas de la base de datos
        
        def show_table_data_window(table_name):
            data = show_table_data(table_name)  # Obtener los datos de la tabla seleccionada
            if data:
                data_list = "\n".join([str(row) for row in data])  # Formatear los datos
                messagebox.showinfo(f"Datos de la Tabla: {table_name}", data_list)
            else:
                messagebox.showinfo(f"Datos de la Tabla: {table_name}", "La tabla está vacía.")

        # Ventana para mostrar las tablas
        tables_window = Toplevel(root)
        tables_window.title("Tablas en la Base de Datos")

        for table in tables:
            table_button = tk.Button(tables_window, text=table, command=lambda t=table: show_table_data_window(t))
            table_button.pack(pady=5)

    show_tables_button = tk.Button(root, text="Mostrar Tablas", command=show_tables)
    show_tables_button.grid(row=15, column=1)



# ------------------------------------- Eliminar Tabla -------------------------------------------
    def delete_table_window():
        def delete_action():
            table_name = table_name_entry.get()
            if delete_table(table_name):
                messagebox.showinfo("Éxito", f"Tabla '{table_name}' eliminada exitosamente.")
                delete_window.destroy()
            else:
                messagebox.showerror("Error", f"No se pudo eliminar la tabla '{table_name}'.")

        # Ventana para eliminar tabla
        delete_window = Toplevel(root)
        delete_window.title("Eliminar Tabla")

        tk.Label(delete_window, text="Nombre de la Tabla:").grid(row=0, column=0)
        table_name_entry = tk.Entry(delete_window)
        table_name_entry.grid(row=0, column=1)

        delete_button = tk.Button(delete_window, text="Eliminar Tabla", command=delete_action)
        delete_button.grid(row=1, column=0, columnspan=2)

    delete_table_button = tk.Button(root, text="Eliminar Tabla", command=delete_table_window)
    delete_table_button.grid(row=16, column=1)  # Ajusta la fila según sea necesario



    # Iniciar el bucle de eventos de la GUI
    root.mainloop()


# Llamar a la función para crear la ventana principal
if __name__ == "__main__":
    create_main_window()


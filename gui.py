import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Toplevel
import pandas as pd  # Importar pandas para manejar archivos Excel
from db import create_table, add_book, delete_table, show_books, show_table_data, update_book, delete_book, create_custom_table, get_tables  # Importar la nueva función get_tables

# Llamada a la función para crear la tabla en la base de datos (puedes ajustar esta parte según sea necesario)
create_table()

def create_main_window():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Book Collection")  # Título de la ventana
    root.geometry("800x600")  # Ajustar tamaño para incluir más controles


    # Definir tabla por defecto
    current_table = "Books"  # Tabla predeterminada


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
        nonlocal current_table
        current_table = selected_table
        messagebox.showinfo("Tabla Seleccionada", f"Tabla activa: {current_table}")
        window.destroy()

    # Botón para seleccionar tabla
    select_table_button = tk.Button(root, text="Seleccionar Tabla", command=select_table)
    select_table_button.grid(row=0, column=2)

    # --- Campos de entrada para la información del libro ---
    tk.Label(root, text="Etapa").grid(row=0, column=0)
    section_entry = tk.Entry(root)
    section_entry.grid(row=0, column=1)

    tk.Label(root, text="Subetapa").grid(row=1, column=0)
    sub_section_entry = tk.Entry(root)
    sub_section_entry.grid(row=1, column=1)

    tk.Label(root, text="Título").grid(row=2, column=0)
    title_entry = tk.Entry(root)
    title_entry.grid(row=2, column=1)

    tk.Label(root, text="Autor").grid(row=3, column=0)
    author_entry = tk.Entry(root)
    author_entry.grid(row=3, column=1)

    tk.Label(root, text="Descripción").grid(row=4, column=0)
    description_entry = tk.Entry(root)
    description_entry.grid(row=4, column=1)

    tk.Label(root, text="Año Inicio").grid(row=5, column=0)
    start_year_entry = tk.Entry(root)
    start_year_entry.grid(row=5, column=1)

    tk.Label(root, text="Año Fin").grid(row=6, column=0)
    end_year_entry = tk.Entry(root)
    end_year_entry.grid(row=6, column=1)

    tk.Label(root, text="Continente").grid(row=7, column=0)
    continent_entry = tk.Entry(root)
    continent_entry.grid(row=7, column=1)

    tk.Label(root, text="País").grid(row=8, column=0)
    country_entry = tk.Entry(root)
    country_entry.grid(row=8, column=1)


# ------------------------------------- Añadir un Libro -------------------------------------------

    def submit():
        section = section_entry.get()
        sub_section = sub_section_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        description = description_entry.get()
        start_year = int(start_year_entry.get())
        end_year = int(end_year_entry.get())
        continent = continent_entry.get()
        country = country_entry.get()

        # Llamada a la función para añadir el libro a la base de datos
        add_book(current_table, section, sub_section, title, author, description, start_year, end_year, continent, country)
        messagebox.showinfo("Éxito", "Libro añadido exitosamente!")  # Mensaje de éxito


    submit_button = tk.Button(root, text="Añadir Libro", command=submit)
    submit_button.grid(row=9, column=1)



# ------------------------------------- Mostrar Libros Almacenados -------------------------------------------

    def show():
        books = show_books(current_table)
        book_list = "\n".join([f"{book[0]}: {book[1]} - {book[2]} - {book[3]} - {book[4]}" for book in books])
        messagebox.showinfo("Libros", book_list or "No se encontraron libros.")



    show_button = tk.Button(root, text="Mostrar Libros", command=show)
    show_button.grid(row=10, column=1)




# ------------------------------------- Actualizar un Libro -------------------------------------------

    def update():
        book_id = simpledialog.askinteger("Input", "Ingrese el ID del libro a actualizar:")
        if book_id:
            section = section_entry.get()
            sub_section = sub_section_entry.get()
            title = title_entry.get()
            author = author_entry.get()
            description = description_entry.get()
            start_year = int(start_year_entry.get())
            end_year = int(end_year_entry.get())
            continent = continent_entry.get()
            country = country_entry.get()

            # Llamada a la función para actualizar el libro en la base de datos
            update_book(current_table, book_id, section, sub_section, title, author, description, start_year, end_year, continent, country)
            messagebox.showinfo("Éxito", "Libro actualizado exitosamente!")



    update_button = tk.Button(root, text="Actualizar Libro", command=update)
    update_button.grid(row=11, column=1)



# ------------------------------------- Eliminar un Libro -------------------------------------------

    def delete():
        book_id = simpledialog.askinteger("Input", "Ingrese el ID del libro a eliminar:")
        if book_id:
            delete_book(current_table, book_id)
            messagebox.showinfo("Éxito", "Libro eliminado exitosamente!")



    delete_button = tk.Button(root, text="Eliminar Libro", command=delete)
    delete_button.grid(row=12, column=1)



# ----------------------------- Importar Filas desde Excel ------------------------------------------

    def import_books():
        # Abrir un cuadro de diálogo para seleccionar el archivo Excel
        file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx;*.xls")])
        if file_path:
            # Leer el archivo Excel usando pandas
            try:
                df = pd.read_excel(file_path)  # Cargar el archivo en un DataFrame
                # Iterar sobre las filas del DataFrame e insertar en la base de datos
                for index, row in df.iterrows():
                    # Extraer datos de cada fila
                    section = row['Etapa']
                    sub_section = row['Subetapa']
                    title = row['Título']
                    author = row['Autor']
                    description = row['Breve Descripción']
                    start_year = int(row['Año Inicio'])
                    end_year = int(row['Año Fin'])
                    continent = row['Continente']
                    country = row['País']
                    
                    # Llamar a la función para añadir el libro a la base de datos
                    add_book(section, sub_section, title, author, description, start_year, end_year, continent, country)
                
                messagebox.showinfo("Éxito", "Libros importados exitosamente!")  # Mensaje de éxito
            except Exception as e:
                messagebox.showerror("Error", f"Error al importar libros: {e}")  # Mensaje de error



    import_button = tk.Button(root, text="Importar Libros desde Excel", command=import_books)
    import_button.grid(row=13, column=1)



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
            columns = [col for col in columns]  # Convertir a lista normal
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
    create_table_button.grid(row=14, column=1)



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


import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import pandas as pd  # Importar pandas para manejar archivos Excel
from db import create_table, add_book, show_books, update_book, delete_book

# Llamada a la función para crear la tabla en la base de datos
create_table()


def create_main_window():
    # Crear la ventana principal
    root = tk.Tk()
    root.title("Book Collection")

    # Campos de entrada para la información del libro
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




    # Función para añadir un libro a la base de datos
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
        add_book(section, sub_section, title, author, description, start_year, end_year, continent, country)
        messagebox.showinfo("Éxito", "Libro añadido exitosamente!")  # Mensaje de éxito

    submit_button = tk.Button(root, text="Añadir Libro", command=submit)
    submit_button.grid(row=9, column=1)




    # Función para mostrar los libros almacenados en la base de datos
    def show():
        books = show_books()
        book_list = "\n".join([f"{book[0]}: {book[1]} - {book[2]} - {book[3]} - {book[4]}" for book in books])
        messagebox.showinfo("Libros", book_list or "No se encontraron libros.")

    show_button = tk.Button(root, text="Mostrar Libros", command=show)
    show_button.grid(row=10, column=1)




    # Función para actualizar un libro existente
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
            update_book(book_id, section, sub_section, title, author, description, start_year, end_year, continent, country)
            messagebox.showinfo("Éxito", "Libro actualizado exitosamente!")

    update_button = tk.Button(root, text="Actualizar Libro", command=update)
    update_button.grid(row=11, column=1)




    # Función para eliminar un libro
    def delete():
        book_id = simpledialog.askinteger("Input", "Ingrese el ID del libro a eliminar:")
        if book_id:
            delete_book(book_id)
            messagebox.showinfo("Éxito", "Libro eliminado exitosamente!")

    delete_button = tk.Button(root, text="Eliminar Libro", command=delete)
    delete_button.grid(row=12, column=1)



    # Función para importar libros desde un archivo Excel
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

    return root

import tkinter as tk
from tkinter import messagebox, simpledialog
from db import create_table, add_book, show_books, update_book, delete_book

# Llama a la función para crear la tabla
create_table()

def create_main_window():
    root = tk.Tk()
    root.title("Book Collection")

    # Campos de entrada
    tk.Label(root, text="Section").grid(row=0, column=0)
    section_entry = tk.Entry(root)
    section_entry.grid(row=0, column=1)

    tk.Label(root, text="Title").grid(row=1, column=0)
    title_entry = tk.Entry(root)
    title_entry.grid(row=1, column=1)

    tk.Label(root, text="Author").grid(row=2, column=0)
    author_entry = tk.Entry(root)
    author_entry.grid(row=2, column=1)

    tk.Label(root, text="Description").grid(row=3, column=0)
    description_entry = tk.Entry(root)
    description_entry.grid(row=3, column=1)

    tk.Label(root, text="Period (as a number)").grid(row=4, column=0)
    period_entry = tk.Entry(root)
    period_entry.grid(row=4, column=1)

    tk.Label(root, text="Continent").grid(row=5, column=0)
    continent_entry = tk.Entry(root)
    continent_entry.grid(row=5, column=1)

    tk.Label(root, text="Country").grid(row=6, column=0)
    country_entry = tk.Entry(root)
    country_entry.grid(row=6, column=1)

    def submit():
        section = section_entry.get()
        title = title_entry.get()
        author = author_entry.get()
        description = description_entry.get()
        period = int(period_entry.get())
        continent = continent_entry.get()
        country = country_entry.get()

        add_book(section, title, author, description, period, continent, country)
        messagebox.showinfo("Success", "Book added successfully!")

    submit_button = tk.Button(root, text="Add Book", command=submit)
    submit_button.grid(row=7, column=1)

    def show():
        books = show_books()
        book_list = "\n".join([f"{book[0]}: {book[1]} - {book[2]}" for book in books])
        messagebox.showinfo("Books", book_list or "No books found.")

    show_button = tk.Button(root, text="Show Books", command=show)
    show_button.grid(row=8, column=1)

    def update():
        book_id = simpledialog.askinteger("Input", "Enter the ID of the book to update:")
        if book_id:
            section = section_entry.get()
            title = title_entry.get()
            author = author_entry.get()
            description = description_entry.get()
            period = int(period_entry.get())
            continent = continent_entry.get()
            country = country_entry.get()

            update_book(book_id, section, title, author, description, period, continent, country)
            messagebox.showinfo("Success", "Book updated successfully!")

    update_button = tk.Button(root, text="Update Book", command=update)
    update_button.grid(row=9, column=1)

    def delete():
        book_id = simpledialog.askinteger("Input", "Enter the ID of the book to delete:")
        if book_id:
            delete_book(book_id)
            messagebox.showinfo("Success", "Book deleted successfully!")

    delete_button = tk.Button(root, text="Delete Book", command=delete)
    delete_button.grid(row=10, column=1)

    return root



from Modules.Biblioteca import main_biblioteca_window  # Importar la ventana principal de biblioteca
from  Modules.Developer import create_developer_options_window  # Importar las opciones de desarrollador
import tkinter as tk
#from gui_tests import main_window  # Importar la ventana principal de biblioteca


def create_main_window():
    root = tk.Tk()
    root.title("WORLD STORIES")

    # Crear los botones en la ventana principal
    biblioteca_button = tk.Button(root, text="Biblioteca", font=("Arial", 14), command=main_biblioteca_window)
    biblioteca_button.pack(pady=10)

    opciones_button = tk.Button(root, text="Opciones de Desarrollador", font=("Arial", 14), command=create_developer_options_window)
    opciones_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()

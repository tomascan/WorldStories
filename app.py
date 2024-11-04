from db import create_table  # Importar la función para crear la tabla
from gui_tests import create_main_window  # Importar la función para crear la GUI

# Llamada a la función para crear la tabla en la base de datos
create_table()

# Crear la interfaz gráfica
if __name__ == "__main__":
    create_main_window()
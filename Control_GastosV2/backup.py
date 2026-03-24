import shutil
import os
from datetime import datetime
from tkinter import messagebox

def hacer_backup():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    origen = os.path.join(base_dir, "gastos.db")
    carpeta_backup = os.path.join(base_dir, "backup")

    if not os.path.exists(carpeta_backup):
        os.makedirs(carpeta_backup)

    fecha = datetime.now().strftime("%Y-%m-%d_%H-%M")
    destino = os.path.join(carpeta_backup, f"gastos_backup_{fecha}.db")

    shutil.copy2(origen, destino)

    messagebox.showinfo("Backup", "Backup realizado correctamente")
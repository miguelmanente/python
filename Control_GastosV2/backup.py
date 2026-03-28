import shutil
import os
import sys
from tkinter import filedialog, messagebox

def obtener_ruta_db():
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)
    else:
        base_path = os.path.dirname(__file__)

    return os.path.join(base_path, "gastos.db")


def hacer_backup():
    origen = obtener_ruta_db()

    destino = filedialog.asksaveasfilename(
        defaultextension=".db",
        filetypes=[("Base de datos", "*.db")],
        title="Guardar backup"
    )

    if destino:
        shutil.copy2(origen, destino)
        messagebox.showinfo("Backup", "Backup realizado correctamente")
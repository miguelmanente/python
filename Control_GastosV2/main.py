import tkinter as tk
from tkinter import ttk
from database import crear_tablas, obtener_categorias
from categorias import abrir_ventana_categorias
from gastos import agregar_gasto, obtener_gastos, calcular_total_gastos

crear_tablas()

ventana = tk.Tk()
ventana.title("Control de Gastos")
ventana.geometry("800x600")
ventana.minsize(700, 500)

# Menú superior
menu_bar = tk.Menu(ventana)
ventana.config(menu=menu_bar)

menu_config = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Configuración", menu=menu_config)

menu_config.add_command(
    label="Administrar Categorías",
    command=lambda: abrir_ventana_categorias(ventana, refrescar_combobox)
)

# ----------- FORMULARIO GASTOS -----------
ventana.columnconfigure(0, weight=1)
ventana.rowconfigure(0, weight=1)

frame_principal = tk.Frame(ventana)
frame_principal.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

frame_principal.columnconfigure(0, weight=1)
frame_principal.columnconfigure(1, weight=2)
frame_principal.rowconfigure(0, weight=1)

frame_form = tk.Frame(frame_principal)
frame_form.grid(row=0, column=0, sticky="nsew", padx=10)

frame_form.columnconfigure(1, weight=1)


# Combobox de categorías
combo_categoria = ttk.Combobox(frame_form)
combo_categoria.grid(row=0, column=1, sticky="ew", pady=8)
#frame_form.columnconfigure(0, weight=1)
#frame_form.rowconfigure(0, weight=1)

def refrescar_combobox():
    combo_categoria["values"] = obtener_categorias()

refrescar_combobox()

tk.Label(frame_form, text="Fecha").grid(row=1, column=0, sticky="w", pady=8)
entry_fecha = tk.Entry(frame_form)
entry_fecha.grid(row=1, column=1, sticky="ew", pady=8)

tk.Label(frame_form, text="Descripción").grid(row=2, column=0, sticky="w", pady=8)
entry_descripcion = tk.Entry(frame_form)
entry_descripcion.grid(row=2, column=1, sticky="ew", pady=8)

# Configurar expansión
frame_form.columnconfigure(1, weight=1)

# Categoría
tk.Label(frame_form, text="Categoría").grid(row=3, column=0, sticky="w", pady=8)

combo_categoria = ttk.Combobox(frame_form, state="readonly")
combo_categoria.grid(row=3, column=1, sticky="ew", pady=8)

combo_categoria["values"] = obtener_categorias()

tk.Label(frame_form, text="Monto").grid(row=4, column=0, sticky="w", pady=8)
entry_monto = tk.Entry(frame_form)
entry_monto.grid(row=4, column=1, sticky="ew", pady=8)

#print("Total gastos:", calcular_total_gastos())

from gastos import agregar_gasto, calcular_total_gastos

def agregar():
    try:
        fecha = entry_fecha.get()
        descripcion = entry_descripcion.get().strip()
        categoria = combo_categoria.get()
        monto_texto = entry_monto.get().strip()

        if monto_texto == "":
            print("Debe ingresar un monto")
            return

        monto_texto = monto_texto.replace(",", ".")
        monto = float(monto_texto)

        if descripcion == "":
            descripcion = categoria

        agregar_gasto(fecha, descripcion, categoria, monto)

        print("Total actual:", calcular_total_gastos())

        entry_descripcion.delete(0, tk.END)
        entry_monto.delete(0, tk.END)

    except ValueError:
        print("Monto inválido")

tk.Button(frame_form, text="Agregar Gasto", command=agregar)\
    .grid(row=5, column=0, columnspan=2, pady=20)


ventana.mainloop()
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import crear_tablas, obtener_categorias
from categorias import abrir_ventana_categorias
from gastos import agregar_gasto, obtener_gastos, calcular_total_gastos, eliminar_gasto
from gastos import actualizar_gasto
#from gastos import agregar_gasto, obtener_gastos, calcular_total_gastos
from ingresos import ventana_ingresos
from ingresos import total_ingresos, total_gastos


def formatear_monto(valor):
    return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def salir():
    if messagebox.askyesno("Salir", "¿Desea cerrar la aplicación?"):
        ventana.destroy()

crear_tablas()

ventana = tk.Tk()
ventana.title("Control de Gastos")
ventana.geometry("800x600")
ventana.minsize(700, 500)

# Menú superior
menu_bar = tk.Menu(ventana)
ventana.config(menu=menu_bar)


menu_archivo = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Archivo", menu=menu_archivo)

menu_archivo.add_command(label="Salir", command=salir)
ventana.config(menu=menu_bar)


menu_config = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Configuración", menu=menu_config)

menu_config.add_command(
    label="Administrar Categorías",
    command=lambda: abrir_ventana_categorias(ventana, combo_categoria)
)

menu_movimientos = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Movimientos", menu=menu_movimientos)

menu_movimientos.add_command(
    label="Ingresos",
    command=ventana_ingresos
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

# Configurar expansión treeview a la derecha
frame_tabla = tk.Frame(frame_principal)
frame_tabla.grid(row=0, column=1, sticky="nsew", padx=10)

frame_tabla.rowconfigure(0, weight=1)
frame_tabla.columnconfigure(0, weight=1)

frame_resumen = tk.LabelFrame(frame_tabla, text="Resumen financiero")
frame_resumen.grid(row=1, column=0, sticky="ew", pady=10)

tk.Label(frame_resumen, text="Ingresos del mes").grid(row=0, column=0, sticky="w")
#lbl_ingresos = tk.Label(frame_resumen, text="$ 0", font=("Arial", 11, "bold"))
lbl_ingresos = tk.Label(frame_resumen, text="$ 0", font=("Arial", 11, "bold"), anchor="e")
lbl_ingresos.grid(row=0, column=1, sticky="e")

tk.Label(frame_resumen, text="Gastos del mes").grid(row=1, column=0, sticky="w")
#lbl_gastos = tk.Label(frame_resumen, text="$ 0", font=("Arial", 11, "bold"))
lbl_gastos = tk.Label(frame_resumen, text="$ 0", font=("Arial", 11, "bold"), anchor="e")
lbl_gastos.grid(row=1, column=1, sticky="e")

tk.Label(frame_resumen, text="Saldo disponible").grid(row=2, column=0, sticky="w")
#lbl_saldo = tk.Label(frame_resumen, text="$ 0", font=("Arial", 13, "bold"))
lbl_saldo = tk.Label(frame_resumen, text="$ 0", font=("Arial", 13, "bold"), anchor="e")
lbl_saldo.grid(row=2, column=1, sticky="e")

#Treeview para mostrar gastos
tree = ttk.Treeview(
    frame_tabla,
    columns=("id","fecha", "descripcion", "categoria", "monto"),
    show="headings"
)

tree.heading("fecha", text="Fecha")
tree.heading("descripcion", text="Descripción")
tree.heading("categoria", text="Categoría")
tree.heading("monto", text="Monto")

tree.column("fecha", width=80)
tree.column("descripcion", width=150)
tree.column("categoria", width=100)
tree.column("monto", width=80, anchor="e")  # alineado derecha
tree.column("id", width=0, stretch=False)

#Scrollbar para el treeview
scrollbar = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

scrollbar.grid(row=0, column=1, sticky="ns")

tree.grid(row=0, column=0, sticky="nsew")
frame_form.columnconfigure(1, weight=1)



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

def cargar_treeview():

    for fila in tree.get_children():
        tree.delete(fila)

    for gasto in obtener_gastos():

        id_gasto, fecha, descripcion, categoria, monto = gasto

        tree.insert(
            "",
            "end",
            values=(id_gasto, fecha, descripcion, categoria, formatear_monto(monto))
        )

from gastos import agregar_gasto, calcular_total_gastos

def agregar():
    try:
        fecha = entry_fecha.get()
        descripcion = entry_descripcion.get()
        categoria = combo_categoria.get()
        monto = float(entry_monto.get())

        agregar_gasto(fecha, descripcion, categoria, monto)

        cargar_treeview()

        actualizar_resumen()

        entry_descripcion.delete(0, tk.END)
        entry_monto.delete(0, tk.END)

    except ValueError:
        print("Monto inválido")

    except ValueError:
        print("Monto inválido")

tk.Button(frame_form, text="Agregar Gasto", command=agregar)\
    .grid(row=5, column=0, columnspan=2, pady=20)

def seleccionar_gasto(event):

    global id_gasto_seleccionado

    item = tree.selection()

    if not item:
        return

    valores = tree.item(item[0], "values")

    id_gasto_seleccionado = valores[0]

    entry_fecha.delete(0, tk.END)
    entry_fecha.insert(0, valores[1])

    entry_descripcion.delete(0, tk.END)
    entry_descripcion.insert(0, valores[2])

    combo_categoria.set(valores[3])

    entry_monto.delete(0, tk.END)
    entry_monto.insert(0, valores[4].replace(".", "").replace(",", "."))

tree.bind("<<TreeviewSelect>>", seleccionar_gasto)



from gastos import obtener_gastos


def actualizar_resumen():

    ingresos = total_ingresos()
    gastos = total_gastos()

    saldo = ingresos - gastos

    lbl_ingresos.config(text=f"$ {formatear_monto(ingresos)}")
    lbl_gastos.config(text=f"$ {formatear_monto(gastos)}")
    lbl_saldo.config(text=f"$ {formatear_monto(saldo)}")

      # Colores automáticos del saldo
    if saldo > 0:
        lbl_saldo.config(fg="green")
    elif saldo < 0:
        lbl_saldo.config(fg="red")
    else:
        lbl_saldo.config(fg="black")

actualizar_resumen()

def eliminar():

    seleccion = tree.selection()

    if not seleccion:
        messagebox.showwarning("Aviso", "Seleccione un gasto")
        return

    item = seleccion[0]

    valores = tree.item(item, "values")

    id_gasto = valores[0]

    respuesta = messagebox.askyesno(
        "Eliminar",
        "¿Desea eliminar el gasto seleccionado?"
    )

    if respuesta:

        eliminar_gasto(id_gasto)

        cargar_treeview()

        actualizar_resumen()

tk.Button(frame_form, text="Eliminar", command=eliminar).grid(row=6, column=0, columnspan=2, pady=5)

def actualizar():

    global id_gasto_seleccionado

    if id_gasto_seleccionado is None:
        messagebox.showwarning("Aviso", "Seleccione un gasto")
        return

    try:

        fecha = entry_fecha.get()
        descripcion = entry_descripcion.get()
        categoria = combo_categoria.get()
        monto = float(entry_monto.get())

        actualizar_gasto(
            id_gasto_seleccionado,
            fecha,
            descripcion,
            categoria,
            monto
        )

        cargar_treeview()
        actualizar_resumen()

        entry_descripcion.delete(0, tk.END)
        entry_monto.delete(0, tk.END)

        id_gasto_seleccionado = None

    except ValueError:
        messagebox.showerror("Error", "Monto inválido")

tk.Button(frame_form, text="Actualizar", command=actualizar).grid(row=7, column=0, columnspan=2, pady=5)

cargar_treeview()
actualizar_resumen()

ventana.mainloop()
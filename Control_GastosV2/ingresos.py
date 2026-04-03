import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from database import conectar, conn
from database import insertar_ingreso
from database import total_gastos, total_ingresos


def limpiar_ingresos_mes(mes, anio):
            conn = conectar()
            cursor = conn.cursor()

            mes = str(mes).zfill(2)
            anio = str(anio)

            cursor.execute("""
                DELETE FROM ingresos
                WHERE substr(fecha, 6, 2)=?
                AND substr(fecha, 1, 4)=?
            """, (mes, anio))

            conn.commit()
            conn.close()


def ventana_ingresos(mes, anio):

    id_ingreso_seleccionado = None

    # Crear ventana de ingresos
    ventana = tk.Toplevel()
    ventana.title("Gestión de Ingresos")
    ventana.geometry("900x600")

    # Crear frames para organizar la ventana
    frame_principal = tk.Frame(ventana)
    frame_principal.pack(fill="both", expand=True, padx=10, pady=10)

    # frames para el formulario y la tabla
    frame_form = tk.Frame(frame_principal)
    frame_form.grid(row=0, column=0, sticky="nsew", padx=10)

    frame_tabla = tk.Frame(frame_principal)
    frame_tabla.grid(row=0, column=1, sticky="nsew", padx=10)

    frame_principal.columnconfigure(0, weight=1)
    frame_principal.columnconfigure(1, weight=2)

    
    # formulario para agregar o actualizar ingresos
    tk.Label(frame_form, text="Fecha").grid(row=0, column=0, sticky="w")
    entry_fecha = tk.Entry(frame_form)
    entry_fecha.grid(row=0, column=1, sticky="ew")

    tk.Label(frame_form, text="Descripción").grid(row=1, column=0, sticky="w")
    entry_desc = tk.Entry(frame_form)
    entry_desc.grid(row=1, column=1, sticky="ew")

    tk.Label(frame_form, text="Monto").grid(row=2, column=0, sticky="w")
    entry_monto = tk.Entry(frame_form)
    entry_monto.grid(row=2, column=1, sticky="ew")

  
    # treeview para mostrar los ingresos
    tree = ttk.Treeview(
    frame_tabla,
    columns=("id","fecha","descripcion","monto"),
    show="headings"
)

    tree.heading("fecha", text="Fecha")
    tree.heading("descripcion", text="Descripción")
    tree.heading("monto", text="Monto")

    tree.column("id", width=0, stretch=False)   # columna oculta
    tree.column("fecha", width=100)
    tree.column("descripcion", width=200)
    tree.column("monto", width=100, anchor="e")
   
    tree.grid(row=0, column=0, sticky="nsew")

    scroll = ttk.Scrollbar(frame_tabla, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.grid(row=0, column=1, sticky="ns")


    # función para formatear el monto con separadores de miles y decimales
    def formatear_monto(valor):
        return f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    
    def obtener_ingresos_mes(mes, anio):
        conn = conectar()
        cursor = conn.cursor()

        mes = str(mes).zfill(2)
        anio = str(anio)

        cursor.execute("""
            SELECT id, fecha, descripcion, monto
            FROM ingresos
            WHERE substr(fecha, 6, 2)=?
            AND substr(fecha, 1, 4)=?
            ORDER BY fecha DESC
        """, (mes, anio))

        datos = cursor.fetchall()

        conn.close()
        return datos




    #función para cargar los ingresos en el Treeview   
    def cargar_treeview_ingresos():

        for fila in tree.get_children():
            tree.delete(fila)

        datos = obtener_ingresos_mes(mes, anio)

        for ingreso in datos:
            id_ingreso, fecha, descripcion, monto = ingreso

            tree.insert(
                "",
                "end",
                values=(
                    id_ingreso,
                    fecha,
                    descripcion,
                    f"{monto:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                )
            )
    
   
    # función para calcular el total de ingresos mostrada abajo del Treeview
    def seleccionar_ingreso(event):

        global id_ingreso_seleccionado

        item = tree.selection()

        if not item:
            return

        valores = tree.item(item[0], "values")

        id_ingreso_seleccionado = valores[0]

        entry_fecha.delete(0, tk.END)
        entry_fecha.insert(0, valores[1])

        entry_desc.delete(0, tk.END)
        entry_desc.insert(0, valores[2])

        entry_monto.delete(0, tk.END)
        entry_monto.insert(0, valores[3].replace(".", "").replace(",", "."))

    tree.bind("<<TreeviewSelect>>", seleccionar_ingreso)

    # marco para mostrar el total de ingresos
    frame_total = tk.Frame(frame_tabla)
    frame_total.grid(row=1, column=0, sticky="ew", pady=10)

    tk.Label(frame_total, text="Total ingresos del mes:").pack(side="left")

    lbl_total_ingresos = tk.Label(
        frame_total,
        text="$ 0",
        font=("Arial", 11, "bold")
    )
    lbl_total_ingresos.pack(side="right")
    
    # función para agregar un ingreso a la base de datos y refrescar el Treeview con los nuevos datos
    # def agregar():

    #     fecha = entry_fecha.get()
    #     descripcion = entry_desc.get()
    #     monto = float(entry_monto.get())

    #     insertar_ingreso(fecha, descripcion, monto)

    #     cargar_treeview_ingresos()   # ← refresca la tabla

    #     entry_fecha.delete(0, tk.END)
    #     entry_desc.delete(0, tk.END)
    #     entry_monto.delete(0, tk.END)
            
    #     cargar_treeview_ingresos()
    #     actualizar_total()

    from datetime import datetime

    def agregar():
        fecha = datetime.now().strftime("%Y-%m-%d")  # 🔥 clave
        descripcion = entry_desc.get()
        monto = float(entry_monto.get())

        insertar_ingreso(fecha, descripcion, monto)

        cargar_treeview_ingresos()
        actualizar_total()

    # función para eliminar un ingreso seleccionado en el Treeview  
    def eliminar():

        global id_ingreso_seleccionado

        if id_ingreso_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un ingreso")
            return

        respuesta = messagebox.askyesno(
            "Eliminar",
            "¿Eliminar ingreso seleccionado?"
        )

        if respuesta:

            eliminar_ingreso(id_ingreso_seleccionado)

            cargar_treeview_ingresos()
            actualizar_total()

            id_ingreso_seleccionado = None

    # función para eliminar un ingreso de la base de datos y refrescar el Treeview con los nuevos datos
    def eliminar_ingreso(id_ingreso):

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM ingresos WHERE id=?",
            (id_ingreso,)
        )

        conn.commit()
    
        cargar_treeview_ingresos()

    # función para actualizar un ingreso en la base de datos y refrescar el Treeview con los nuevos datos
    def actualizar_ingreso(id_ingreso, fecha, descripcion, monto):

        cursor = conn.cursor()

        cursor.execute(
            """
            UPDATE ingresos
            SET fecha=?, descripcion=?, monto=?
            WHERE id=?
            """,
            (fecha, descripcion, monto, id_ingreso)
        )
        tree.insert(
        "",
        "end",
        values=(id_ingreso, fecha, descripcion,formatear_monto(monto))
        )

        conn.commit()


    # función para actualizar un ingreso seleccionado en el Treeview
    def actualizar():

        global id_ingreso_seleccionado

        if id_ingreso_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un ingreso")
            return

        try:

            fecha = entry_fecha.get()
            descripcion = entry_desc.get()
            monto = float(entry_monto.get())

            actualizar_ingreso(
                id_ingreso_seleccionado,
                fecha,
                descripcion,
                monto
            )

            cargar_treeview_ingresos()

            entry_fecha.delete(0, tk.END)
            entry_desc.delete(0, tk.END)
            entry_monto.delete(0, tk.END)

            id_ingreso_seleccionado = None

        except ValueError:
            messagebox.showerror("Error", "Monto inválido")
    
        cargar_treeview_ingresos()
        actualizar_total()
        

    # función para calcular el total de ingresos mostrada abajo del Treeview
    def calcular_total_ingresos(mes, anio):

        cursor = conn.cursor()

        fecha_inicio = f"{anio}-{str(mes).zfill(2)}-01"

        if mes == 12:
            fecha_fin = f"{anio+1}-01-01"
        else:
            fecha_fin = f"{anio}-{str(mes+1).zfill(2)}-01"

        cursor.execute("""
            SELECT SUM(monto)
            FROM ingresos
            WHERE fecha >= ? AND fecha < ?
        """, (fecha_inicio, fecha_fin))

        total = cursor.fetchone()[0]

        if total is None:
            total = 0

        return total
     
    # función para actualizar el total de ingresos cada vez que se agrega, elimina o actualiza un ingreso
    def actualizar_total():
        total = calcular_total_ingresos(mes, anio)

        total_formateado = formatear_monto(total)

        lbl_total_ingresos.config(text=f"$ {total_formateado}")

        cargar_treeview_ingresos()


    cargar_treeview_ingresos()
    actualizar_total()




    # def limpiar_mes_actual():
    #     messagebox.askyesno(
    #         "Confirmar",
    #         "Se borrarán TODOS los datos del mes actual.\n¿Continuar?"
    #     )

    #      # Limpiar tabla
    #     for row in tree.get_children():
    #         tree.delete(row)

            
    #     messagebox.showinfo("OK", "Mes limpio")


    # función para cerrar la ventana de ingresos
    def salir():
            if messagebox.askyesno("Salir", "¿Desea la ventana Ingresos?"):
                ventana.destroy()



    # botones para agregar, actualizar, eliminar y salir
    tk.Button(frame_form, text="Agregar ingreso", command=agregar).grid(row=3, column=0, columnspan=2, pady=10)
    tk.Button(frame_form, text="Actualizar", command=actualizar).grid(row=4,column=0, columnspan=2,pady=5)
    tk.Button(frame_form, text="Eliminar", command=eliminar).grid(row=5,column=0, columnspan=2,pady=5)
    # tk.Button(frame_form, text="Nuevo Mes", command=nuevo_mes_limpio).grid(row=6,column=0, columnspan=2,pady=5)
    # tk.Button(frame_form, text="Limpiar Ingresos", command=limpiar_mes_actual).grid(row=7,column=0, columnspan=2,pady=5)
    tk.Button(frame_form, text="Salir", command=salir).grid(row=8, column=0, columnspan=2, pady=20)

    

   
  
 


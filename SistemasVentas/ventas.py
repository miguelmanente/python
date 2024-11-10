import sqlite3
from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from PIL import Image, ImageTk
import datetime
import sys
import os

class Ventas(tk.Frame):

    db_name ="SistemasVentas/database.db" 

    def __init__(self, parent):
        super().__init__(parent)
        self.numero_factura_actual = self.obtener_numero_factura_actual()
        self.widgets()
        self.mostrar_numero_factura()
    
    #Rutas para iconos del sistemas de ventas
    def rutas(self, ruta):
        try:
            rutabase = sys.__MEIPASS
        except Exception:
            rutabase = os.path.abspath(".")
        return os.path.join(rutabase, ruta)
    
    
    def widgets(self):
        frame1= tk.Frame(self, bg="#dddddd", highlightbackground="gray", highlightthickness=1)
        frame1.pack()
        frame1.place(x=0, y=0, width=1100, height=100)
        
        titulo = tk.Label(self, text="VENTAS", bg="#dddddd", font="sans 30 bold", anchor="center")
        titulo.pack()
        titulo.place(x=5, y=0, width=1090, height=90)

        frame2 = tk.Frame(self, bg="#C6D9E3", highlightbackground="gray", highlightthickness=1)
        frame2.place(x=0, y=100, width=1100, height=550)

        lblframe = LabelFrame(frame2, text="Información de la Venta", bg="#C6D9E3", font="sans 16 bold")
        lblframe.place(x=10 , y=10, width=1060, height=80)

        label_numero_factura = tk.Label(lblframe, text="Número de \nFactura", bg="#C6D9E3", font="sans 12 bold")
        label_numero_factura.place(x=10 , y=5)
        self.numero_factura = tk.StringVar()

        self.entry_numero_factura =ttk.Entry(lblframe, textvariable=self.numero_factura, state="readonly", font="sans 12 bold")
        self.entry_numero_factura.place(x=100 , y=10, width=80)

        label_nombre = tk.Label(lblframe, text="Productos: ", bg="#C6D9E3", font="sans 12 bold")
        label_nombre.place(x=200, y=13)
        self.entry_nombre = ttk.Combobox(lblframe, font="sans 12 bold", state="readonly")
        self.entry_nombre.place(x=295, y=10, width=180)

        self.cargar_productos()

        label_valor = tk.Label(lblframe, text="Precio: ", bg="#C6D9E3", font="sans 12 bold")
        label_valor.place(x=480, y=13)
        self.entry_valor = ttk.Entry(lblframe, font="sans 12 bold", state="readonly")
        self.entry_valor.place(x=540, y=10, width=180)

        self.entry_nombre.bind("<<ComboboxSelected>>", self.actualizar_precio)

        label_cantidad = tk.Label(lblframe, text="Cantidad: ", bg="#C6D9E3", font="sans 12 bold")
        label_cantidad.place(x=730, y=13)
        self.entry_cantidad = ttk.Entry(lblframe, font="sans 12 bold")
        self.entry_cantidad.place(x=820, y=10, width=180)

        treFrame = tk.Frame(frame2, bg="#C6D9E3" )
        treFrame.place(x=150, y=120, width=800, height=200)

        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x =ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        self.tree =ttk.Treeview(treFrame, columns=("#1", "#2", "#3", "#4"), show ="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=self.tree.yview)
        scrol_x.config(command=self.tree.xview)

        self.tree.heading("#1", text="Producto")
        self.tree.heading("#2", text="Precio")
        self.tree.heading("#3", text="Cantidad")
        self.tree.heading("#4", text="Subtotal")

        self.tree.column("#1", width= 100 ,anchor="center")
        self.tree.column("#2", width= 100 ,anchor="center")
        self.tree.column("#3", width= 100 ,anchor="center")
        self.tree.column("#4", width= 100 ,anchor="center")

        self.tree.pack(expand=True, fill=BOTH)

        lblframe1 = LabelFrame(frame2, text="Opciones", bg="#C6D9E3", font="sans 12 bold")
        lblframe1.place(x=10, y=380, width=1060, height=100)

        ruta = self.rutas(r"SistemasVentas/icono/AgregarProducto.ico")
        imagen_pil = Image.open(ruta)
        imagen_resize =imagen_pil.resize((40,40))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        boton_agregar = tk.Button(lblframe1, text="Agregar Artículo",bg="#dddddd", font="sans 12 bold", command=self.registrar)
        boton_agregar.config(image=imagen_tk, compound=LEFT, padx=10)
        boton_agregar.image = imagen_tk
        boton_agregar.place(x=50, y=10, width=240, height=50)
        
        ruta = self.rutas(r"SistemasVentas/icono/pagar.ico")
        imagen_pil = Image.open(ruta)
        imagen_resize =imagen_pil.resize((35,35))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        boton_pagar = tk.Button(lblframe1, text="Pagar",bg="#dddddd", font="sans 12 bold", command=self.abrir_ventana_pago)
        boton_pagar.config(image=imagen_tk, compound=LEFT, padx=20)
        boton_pagar.image = imagen_tk
        boton_pagar.place(x=400, y=10, width=240, height=50)
        

        ruta = self.rutas(r"SistemasVentas/icono/facturas.ico")
        imagen_pil = Image.open(ruta)
        imagen_resize =imagen_pil.resize((35,35))
        imagen_tk = ImageTk.PhotoImage(imagen_resize)

        boton_ver_facturas = tk.Button(lblframe1, text="Ver Facturas", bg="#dddddd", font="sans 12 bold", command=self.abrir_ventana_factura)
        boton_ver_facturas.config(image=imagen_tk, compound=LEFT, padx=20)
        boton_ver_facturas.image = imagen_tk
        boton_ver_facturas.place(x=750, y=10, width=240, height=50)

        self.label_suma_total = tk.Label(frame2, text="Total a pagar: $", bg="#C6D9E3", font="sans 25 bold")
        self.label_suma_total.place(x=330, y=335)

    def cargar_productos(self):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT nombre FROM inventario")
            productos = c.fetchall()
            self.entry_nombre["values"] = [producto[0] for producto in productos]
            if not productos:
                print ("No se encontraron productos en la base de datos")
            conn.close()
        except sqlite3.Error as e:
            print("Error al cargar productos desde la base de datos:", e)

    def actualizar_precio(self, event):
        nombre_producto = self.entry_nombre.get()
        try:
            conn =sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT precio FROM inventario WHERE nombre = ?", (nombre_producto,))
            precio = c.fetchall()
            if (precio):
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, precio[0])
                self.entry_valor.config(state="readonly")
            else:
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.insert(0, "Precio no disponible")
                self.entry_valor.config(state="readonly")
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Errro al obtener el precio {e}") 
        finally:
            conn.close()

    
    def actualizar_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal =float(self.tree.item(child, "values")[3])
            total += subtotal
        self.label_suma_total.config(text=f"Total a pagar: $ {total:.0f}")
    
    def registrar(self):
        producto = self.entry_nombre.get()
        precio = self.entry_valor.get()
        cantidad = self.entry_cantidad.get()

        if producto and precio and cantidad:
            try:
                cantidad = int(cantidad)
                if not self.verificar_stock(producto, cantidad):
                    messagebox.showerror("Error", "Stock insuficiente para el producto seleccionado")
                    return
                precio = float(precio)
                subtotal = cantidad * precio

                self.tree.insert("", "end", values = (producto, f"{precio:.0f}", cantidad, f"{subtotal:.0f}"))
                self.entry_nombre.set("")
                self.entry_valor.config(state="normal")
                self.entry_valor.delete(0, tk.END)
                self.entry_valor.config(state="readonly")
                self.entry_cantidad.delete(0, tk.END)

                self.actualizar_total()
            except ValueError:
                messagebox.showerror("Error", "Cantidad o precio no validos")
        else:
            messagebox.showerror("Error", "Debe completar todos los campos")

    def verificar_stock(self, producto, cantidad):
        try:
            conn =sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT stock FROM inventario WHERE nombre = ?", (producto,))
            stock = c.fetchone()
            if stock and stock[0] >= cantidad:
                return True
            return False
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al verificar el stock: {e}")
            return False
        finally:
            conn.close()
    
    def obtener_total(self):
        total = 0.0
        for child in self.tree.get_children():
            subtotal = float(self.tree.item(child, "values")[3])
            total += subtotal
        return total
    
    def abrir_ventana_pago(self):
        if not self.tree.get_children():
            messagebox.showerror("Error", " No hay articulos para pagar")
            return 
    
        ventana_pago = Toplevel(self)
        ventana_pago.title("Realizar Pago")
        ventana_pago.geometry("400x400")
        ventana_pago.config(bg="#C6D9E3")
        ventana_pago.resizable(False, False)

        label_total = tk.Label(ventana_pago, bg="#C6D9E3", text=f"Total a pagar: $ {self.obtener_total():.0f}",font="sans 18 bold")
        label_total.place(x=70, y=20)
        label_cantidad_pagada = tk.Label(ventana_pago, bg="#C6D9E3", text="Cantidad pagada: ",font="sans 14 bold")
        label_cantidad_pagada.place(x=100, y=90)
        entry_cantidad_pagada = ttk.Entry(ventana_pago, font="sans 14 bold")
        entry_cantidad_pagada.place(x=100, y=130)

        label_cambio =  tk.Label(ventana_pago, bg="#C6D9E3", text="", font="sans 14 bold")
        label_cambio.place(x=100, y=190)

        def calcular_cambio():
            try:
                cantidad_pagada = float(entry_cantidad_pagada.get())
                total = self.obtener_total()
                cambio = cantidad_pagada - total
                if cambio < 0:
                    messagebox.showerror("Error", "La cantidad pagada es suficiente")
                    return
                label_cambio.config(text=f"Vuelto: $ {cambio:.0f}")
            except ValueError:
                messagebox.showerror("Error", "Cantidad pagada no valida")
        
        boton_calcular = tk.Button(ventana_pago, text="Calcular Vuelto", bg="white", font="sans 12 bold", command=calcular_cambio) 
        boton_calcular.place(x=100, y=240, width=240, height=40)

        boton_pagar = tk.Button(ventana_pago, text="Pagar", bg="white", font="sans 12 bold", command=lambda: self.pagar(ventana_pago, entry_cantidad_pagada, label_cambio)) 
        boton_pagar.place(x=100, y=300, width=240, height=40)

    def pagar(self, ventana_pago, entry_cantidad_pagada, label_cambio):
        try:
            cantidad_pagada = float(entry_cantidad_pagada.get())
            total = self.obtener_total()
            cambio = cantidad_pagada - total
            if cambio <0:
                messagebox.showerror("Error", "Cantidad pagada es insuficiente")
            
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            try:
                productos1 = []
                for child in self.tree.get_children():
                    item = self.tree.item(child, "values")
                    producto = item[0]
                    precio = item[1]
                    cantidad_vendida = int(item[2])
                    subtotal = float(item[3])
                    productos1.append([producto, precio, cantidad_vendida, subtotal])
                  
                    c.execute("INSERT INTo ventas (factura, nombre_articulo, valor_articulo, cantidad, subtotal) VALUES (?,?,?,?,?)",
                              (self.numero_factura_actual, producto, float(precio), cantidad_vendida, subtotal))

                    c.execute("UPDATE inventario SET stock = stock - ? WHERE nombre =?",(cantidad_vendida, producto))

                conn.commit()
                messagebox.showinfo("Exito", "Venta registrada exitosamente")
                
                self.numero_factura_actual += 1
                self.mostrar_numero_factura()

                for child in self.tree.get_children():
                    self.tree.delete(child)
                self.label_suma_total.config(text="Total a pagar: $ 0")
                
                ventana_pago.destroy()

                fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.generar_factura_pdf(productos1, total, self.numero_factura_actual - 1, fecha)

            except sqlite3.Error as e:
                conn.rollback()
                messagebox.showerror("Error", f"Error al registrar la venta: {e}")
            finally:
                conn.close()
        except ValueError:
            messagebox.showerror("Error", " Cantidad pagada no valida")    
         
    def generar_factura_pdf(self, productos1, total, factura_numero, fecha):
        archivo_pdf = f"SistemasVentas/facturas/factura_{factura_numero}.pdf" #SistemasVentas\facturas

        c = canvas.Canvas(archivo_pdf, pagesize=letter)
        width, height = letter

        styles = getSampleStyleSheet()
        estilo_titulo = styles["Title"]
        estilo_normal = styles["Normal"]

        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 50, f"Factura #{factura_numero} ")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, height - 70, f"Fecha: {fecha}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, height - 100, "Información de la venta")

        data = [["Producto", "Precio", "Cantidad", "Subtotal"]] + productos1
        table = Table(data)
        table.wrapOn(c, width, height)
        table.drawOn(c, 100, height - 200)

        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 250, f"Total a pagar: $ {total:.0f}")

        c.setFont("Helvetica-Bold", 12)
        c.drawString(100, height - 400, "Gracias por su compra, vuelva pronto")

        c.save()

        messagebox.showinfo("Factura Generada", f"La factura #{factura_numero} ha sido creada exitosamente")

        os.startfile(os.path.abspath(archivo_pdf))


    def obtener_numero_factura_actual(self):
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        try:
            c.execute("SELECT MAX(factura) FROM ventas")
            factura = c.fetchone()[0]
            max_factura = int(factura)
            if max_factura:
                return max_factura + 1
            else:
                return 1
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al obtener el numero de factura: {e}" )
            return 1
        finally:
            conn.close()
    
    def mostrar_numero_factura(self):
        self.numero_factura.set(self.numero_factura_actual)


    def abrir_ventana_factura(self):    
        ventana_facturas =Toplevel(self)
        ventana_facturas.title("Factura")
        ventana_facturas.geometry("800x500")
        ventana_facturas.config(bg="#C6D9E3")
        ventana_facturas.resizable(False, False)

        facturas = Label(ventana_facturas, bg="#C6D9E3", text="Facturas Registradas", font="sans 36 bold")
        facturas.place(x=150, y=150)

        treFrame = tk.Frame(ventana_facturas, bg="#C6D9E3")
        treFrame.place(x=10, y=100, width=780, height=380)

        scrol_y = ttk.Scrollbar(treFrame, orient=VERTICAL)
        scrol_y.pack(side=RIGHT, fill=Y)

        scrol_x =ttk.Scrollbar(treFrame, orient=HORIZONTAL)
        scrol_x.pack(side=BOTTOM, fill=X)

        tree_facturas =ttk.Treeview(treFrame, columns=("ID", "Factura", "Producto", "Precio", "Cantidad", "Subtotal"), show ="headings", height=10, yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)
        scrol_y.config(command=tree_facturas.yview)
        scrol_x.config(command=tree_facturas.xview)

        tree_facturas.heading("#1", text="ID")
        tree_facturas.heading("#2", text="Factura")
        tree_facturas.heading("#3", text="Producto")
        tree_facturas.heading("#4", text="Precio")
        tree_facturas.heading("#5", text="Cantidad")
        tree_facturas.heading("#6", text="Subtotal")

        tree_facturas.column("ID", width=70, anchor="center")
        tree_facturas.column("Factura", width=100, anchor="center")
        tree_facturas.column("Producto", width=200, anchor="center")
        tree_facturas.column("Precio", width=130, anchor="center")
        tree_facturas.column("Cantidad", width=130, anchor="center")
        tree_facturas.column("Subtotal", width=130, anchor="center")

        tree_facturas.pack(expand=True, fill=BOTH)

        self.cargar_facturas(tree_facturas)

    def cargar_facturas(self, tree):
        try:
            conn = sqlite3.connect(self.db_name)
            c = conn.cursor()
            c.execute("SELECT * FROM ventas")
            facturas = c.fetchall()
            for factura in facturas:
                tree.insert("", "end", values=factura)
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error al cargar las facturas: {e}")

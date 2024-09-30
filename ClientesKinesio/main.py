from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3


################################  CREACIÓN VENTANA PRINCIPAL ############################
root = Tk()
root.config(width="800", height="600")
root.title("Turnos Kinesiologia")
root.iconbitmap("ClientesKinesio/icono2.ico")

id=StringVar()
dia = StringVar()
fecha = StringVar()
hora = StringVar()
nombres = StringVar()
asistencia = StringVar()

#################################  CREAR Y CONECTAR LA BASE DE DATOS ###########################
def conexionBBDD():
    miConexion = sqlite3.connect("/Users/migue/OneDrive/Escritorio/Python/ClientesKinesio/ckinesio")
    miCursor = miConexion.cursor()

    try:
        miCursor.execute("CREATE TABLE clientes (ID INTEGER PRIMARY KEY AUTOINCREMENT, DIA VARCHAR(10) NOT NULL, FECHA VARCHAR(10) NOT NULL, HORA VARCHAR(5) NOT NULL, NOMBRES VARCHAR(50) NOT NULL, ASISTENCIA INT NOT NULL)")

        messagebox.showinfo("CONEXIÓN","Base de datos Creada Exitosamente")
    except:
        messagebox.showinfo("CONEXIÓN"," Conexión exitoxa con la base de datos")

####################################### ELIMINAR LA BASE DE DATOS  #################################

def eliminarBBDD():
    miConexion = sqlite3.connect("/Users/migue/OneDrive/Escritorio/Python/ClientesKinesio/ckinesio")
    miCursor = miConexion.cursor()
    
    if messagebox.askyesno(message="¿Los datos se perderán definitivamente, Desea continuar?", title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE clientes")
        limpiarDatos()
    else:
        messagebox.askyesno(message="LA BASE DE DATOS NO SE ELIMINÓ, VERIFIQUE...?")
        pass

###########################  SALIR DE LA APLICACIÓN  ##########################################
 
def salirAplicación():
    valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir de la Aplicación?")
    if valor == "yes":
        root.destroy()
    else:
        pass


########################  LIMPIAR CAMPOS TREEVIEW  ############################################
def limpiarCampos():
    dia.set("")
    fecha.set("")
    hora.set("")
    nombres.set("")
    asistencia.set("")

########################  LIMPRIAR CAMPOS DEL TREEVIEW  ############################################
def limpiarDatos():
    tree.delete(*tree.get_children())
    dia.set('')
    fecha.set('')
    hora.set('')
    nombres.set('')
    asistencia.set('')

############################### MOSTRAR LOS CAMPOS INSERTADOS ###################################
def mostrar():
    miConexion = sqlite3.connect("/Users/migue/OneDrive/Escritorio/Python/ClientesKinesio/ckinesio")
    miCursor = miConexion.cursor()
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        miCursor.execute("SELECT * FROM clientes")
        for row in miCursor:
            tree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5]))
    except:
        pass

#################################   AGREGAR O INSERTAR REGISTRO A LA BD #########################
def crear():
    miConexion = sqlite3.connect("/Users/migue/OneDrive/Escritorio/Python/ClientesKinesio/ckinesio")
    miCursor = miConexion.cursor()
    try:
        datos = dia.get(), fecha.get(), hora.get(), nombres.get(), asistencia.get()
        miCursor.execute("INSERT INTO clientes VALUES(NULL,?,?,?,?,?)",(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al crear el registro, verifique la conexión BBDD")
        pass
    limpiarCampos()
    mostrar()

def acerca():
    acerca = '''
    Aplicación para Kinesiólogos
    Versión 1.0
    Copyright MAM 
    '''
    messagebox.showinfo(title="INFORMACIÓN", message=acerca)


#######################   BARRA DE MENÚES  ######################
frame4 = Frame(root, width=500, height=20)
frame4.place(x=0, y=0)

menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command = conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command = eliminarBBDD )
menubasedat.add_command(label="Salir", command = salirAplicación)
menubar.add_cascade(label="Inicio", menu=menubasedat)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Recuperar Campos", command = limpiarDatos)
ayudamenu.add_command(label="Acerca", command = acerca)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

#################   TITULO PRINCIPAL DE LA APLICACIÓN  ###########################

lblTitPpal = Label(root, text="TURNOS PARA CLIENTES DE KINESIOLOGÍA", bg="#6A9C89", fg="white", bd=5, font=("Comic Snas MS", 16, 'bold'))
lblTitPpal.place(x=200, y=10)
lblTitPpal.config(relief="sunken")

######################  CUADRO IZQUIERDO FRAME1  ##########################
frame1 = Frame(root, width=305, height=350)

frame1.pack(padx=10, pady=80, side="left", anchor="n")
frame1.config(bg="#C1CFA1")

frame1.config(bd="3")
frame1.config(relief="sunken") 

lbltit = Label(frame1, text="INGRESO DE DATOS A BASE DE DATOS", anchor='center')
lbltit.place(x=50, y=10)

lblDia = Label(frame1, text="DÍA")
lblDia.place(x=10, y=40)

textDia = Entry(frame1, textvariable=dia)
textDia.place(x=10, y=70, width=150)

lblFecha = Label(frame1, text="FECHA")
lblFecha.place(x=10, y=100)

textFecha = Entry(frame1, textvariable=fecha)
textFecha.place(x=10, y=130, width=100)

lblHora = Label(frame1, text="HORA")
lblHora.place(x=10, y=160)

textHora = Entry(frame1, textvariable=hora)
textHora.place(x=10, y=190, width=50)

lblNombres = Label(frame1, text="NOMBRES")
lblNombres.place(x=10, y=220)

textNombres = Entry(frame1, textvariable=nombres)
textNombres.place(x=10, y=250, width=200)

lblAsist = Label(frame1, text="ASISTENCIA")
lblAsist.place(x=10, y=280)

textAsist = Entry(frame1, textvariable=asistencia)
textAsist.place(x=10, y=310, width=50)


######### TREEVIEW PARA MOSTRAR LOS DATOS AGREGADOS - FRAME2  #############

frame2 = Frame(root, width=650, height=550)
frame2.pack(padx=10, pady=80, side="left", anchor="n")

tree = ttk.Treeview(frame2, height=10, columns=('#0','#1','#2','#3','#4'))
tree.place(x=10, width=620, height=520)
tree.column('#0', width=50)
tree.heading('#0',text="ID", anchor=CENTER)
tree.column('#1', width=100, anchor='center')
tree.heading('#1',text="DIA", anchor=CENTER)
tree.column('#2', width=100, anchor='center')
tree.heading('#2',text="FECHA", anchor=CENTER)
tree.column('#3', width=70, anchor='center')
tree.heading('#3',text="HORA", anchor=CENTER)
tree.column('#4', width=200, anchor='center')
tree.heading('#4',text="NOMBRES", anchor=CENTER)
tree.column('#5', width=100, anchor='center')
tree.heading('#5',text="ASISTENCIA", anchor=CENTER)

def seleccionarUsandoClick(event):
    item = tree.identify('item',event.x,event.y)
    id.set(tree.item(item,"text"))
    dia.set(tree.item(item,"values")[0])
    fecha.set(tree.item(item,"values")[1])
    hora.set(tree.item(item,"values")[2])
    nombres.set(tree.item(item,"values")[3])
    asistencia.set(tree.item(item,"values")[4])

tree.bind("<Double-1>", seleccionarUsandoClick)


###############################  BORRAR REGISTROS  #############################################
def borrarReg():
    miConexion = sqlite3.connect("/Users/migue/OneDrive/Escritorio/Python/ClientesKinesio/ckinesio")
    miCursor = miConexion.cursor()
       
    try:
        if messagebox.askyesno(message="¿Realmente desea eliminar el registro?", title="ADVERTENCIA"):
            
            selected_item = tree.selection()
            tree.delete(selected_item)
            miCursor.execute("DELETE FROM clientes WHERE ID="+id.get())
            miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al tratar de eliminar el registro...")
        pass
    
    limpiarCampos()
    mostrar()
    

###########################  MARCO DE BOTONES  -  FRAME3  ##################################

frame3 = Frame(root, width=450, height=350)
frame3.place(x=10, y=450)
frame3.config(bg="#C1CFA1")
frame3.config(bd="3")
frame3.config(relief="sunken") 

lblCtrl = Label(frame3, text = 'Botones de Control',fg='white', bg ='black', font=('Rockwell',12,'bold'))
lblCtrl.grid(columnspan=3, column=0,row=0, pady=1, padx=4)         
btnRegistrar = Button(frame3, command= crear, text=' REGISTRAR ', font=('Arial',8,'bold'), bg='green', fg='white')
btnRegistrar.grid(column=0,row=1, pady=10, padx=4)
btnLimpiar =Button(frame3, text=' LIMPIAR ', command = limpiarDatos, font=('Arial',8,'bold'), bg='orange red') 
btnLimpiar.grid(column=1,row=1, padx=10)        
btnEliminar = Button(frame3, text=' ELIMINAR ', command = borrarReg, font=('Arial',8,'bold'), bg='red', fg='white') 
btnEliminar.grid(column=2,row=1, padx=4)
btnBuscar = Button(frame3, text=' BUSCAR POR NOMBRE ', font=('Arial',8), bg='orange') #'command = buscar_nombre',
btnBuscar.grid(columnspan=2,column = 1, row=2)
EtiBuscar = Entry(frame3, font=('Arial',8), width=23) #'textvariable=buscar' ,
EtiBuscar.grid(column=0,row=2, pady=1, padx=1)
btnListar = Button(frame3, command = mostrar, text=' MOSTRAR LISTA DE CLIENTES ', font=('Arial',8,'bold'), bg='green2') #
btnListar.grid(columnspan=3,column=0,row=3, pady=8)

root.config(menu=menubar)
root.mainloop()


      

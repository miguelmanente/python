################################### IMPORTAR LA BIBLIOTECAS A UTILIZAR ##########################

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import functools
import sqlite3


################################  CREACIÓN VENTANA PRINCIPAL ############################
root = Tk()
root.config(width=1300, height=800)
root.title("TURNOS - CLIENTES")
#root.resizable(0,0)

############################  DEFINICIÓN DE VARIABLES UTILIZADAS EN LA APLICACIÓN #####################
id = StringVar()
mes = StringVar()
dia = StringVar()
fecha = StringVar()
hora = StringVar()
nombres = StringVar()
asistencia = StringVar()
turno = StringVar()
miDia = StringVar()
miFecha = StringVar()
Meses = StringVar()


#################################  CREAR Y CONECTAR LA BASE DE DATOS ###########################
def conexionBBDD():

    '''Esta función crea la base de datos tclientes SI ESTA NO se ha creado previamente 
       en caso, de haber sido creada anteriormente, si ejecutamos nuevamente esta función
       nos avisará que ya esta conectada la BD'''

    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()

    try:
        miCursor.execute("CREATE TABLE clientes (ID INTEGER PRIMARY KEY AUTOINCREMENT, MES VARCHAR(10) NOT NULL, DIA VARCHAR(10) NOT NULL, FECHA VARCHAR(10) NOT NULL, HORA VARCHAR(5) NOT NULL, NOMBRES VARCHAR(50) NOT NULL, ASISTENCIA INT NOT NULL)")

        messagebox.showinfo("CONEXIÓN","Base de datos Creada Exitosamente")
    except:
        messagebox.showinfo("CONEXIÓN"," Conexión exitosa con la base de datos")

####################################### ELIMINAR LA BASE DE DATOS  #################################

def eliminarBBDD():

    ''' Esta función ELIMINA la BD por completo, perdiendose toda la información'''

    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()
    
    if messagebox.askyesno(message="¿Los datos se perderán definitivamente, Desea continuar?", title="ADVERTENCIA"):
        miCursor.execute("DROP TABLE clientes")
        limpiarDatos()
    else:
        messagebox.askyesno(message="LA BASE DE DATOS NO SE ELIMINÓ, VERIFIQUE...?")
        pass
    miConexion.close()
###########################  SALIR DE LA APLICACIÓN  ##########################################
 
def salirAplicación():
    valor = messagebox.askquestion("Salir", "¿Está seguro que desea salir de la Aplicación?")
    if valor == "yes":
        root.destroy()
    else:
        pass
    

########################  LIMPIAR CAMPOS TREEVIEW  ############################################
def limpiarCampos():
    mes.set("")
    dia.set("")
    fecha.set("")
    hora.set("")
    nombres.set("")
    asistencia.set("")

########################  LIMPRIAR CAMPOS DEL TREEVIEW  ############################################
def limpiarDatos():
    tree.delete(*tree.get_children())
    mes.set('')
    dia.set('')
    fecha.set('')
    hora.set('')
    nombres.set('')
    asistencia.set('')

############################  ORDENAR LA BASE DE DATOS #####################################
def ordenarBD():

    ''' Al agregar registro a la BD, estos quedarán visualmente en la primera línea de la tabla(treeview)
        si queremos visualizar esta función para que los registros salgan ordenados por fecha, debemos 
        cliquear en el botón MOSTRAR LISTA DE CLIENTES para que se muestren los registros ordenados'''

    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()

    try:
        limpiarDatos()
        miCursor.execute("SELECT * FROM clientes ORDER BY fecha DESC")
        for row in miCursor:
            tree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5],row[6]))
    except:
        pass
 
    miConexion.close()

############################### MOSTRAR LOS CAMPOS INSERTADOS ###################################
def mostrar():
    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()
    
    registros = tree.get_children()
    for elemento in registros:
        tree.delete(elemento)
    try:
        miCursor.execute("SELECT * FROM clientes")
        for row in miCursor:
            tree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5],row[6]))
    except:
        pass
    
    miConexion.close()

#################################   AGREGAR O INSERTAR REGISTRO A LA BD #########################
def crear():

    '''Inserta/Agrega registros a la BD, estos quedarán visualmente en la primera línea de la tabla(treeview)
        si queremos visualizar esta función para que los registros salgan ordenados por fecha, debemos 
        cliquear en el botón MOSTRAR LISTA DE CLIENTES para que se muestren los registros ordenados '''

    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()
    try:  
        datos = mes.get(), dia.get(), fecha.get(), hora.get(), nombres.get(), asistencia.get()
        miCursor.execute("INSERT INTO clientes VALUES(NULL,?,?,?,?,?,?)",(datos))
        miConexion.commit()
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al crear el registro, verifique la conexión BBDD")
        pass
    mostrar()
    miConexion.close()

#####################################  Manual del Usuario ###############################################
def documenta():
    import os
    path = "/home/miguel/python/TurnosClientes/Documentacion.pdf"
    os.system(path)

######################################  Acerca de la Aplicación #############################
def acerca():
    acerca = '''
    Aplicación Agrega Clientes
          Versión 1.1
    Copyright:
         Miguel Manente
    '''
    messagebox.showinfo(title="ACERCA DE LA APLICACIÓN", message=acerca)

###################  Función que llama a la aplicación de Historias clínicas ################
def hc():
    import BlocNotas as hc

    hc.blockNotas()

 
#######################   BARRA DE MENÚES  ######################
frame4 = Frame(root, width=100, height=20)
frame4.pack()
frame4.place(x=0, y=0)

menubar = Menu(root)
menubasedat = Menu(menubar, tearoff=0)
menubasedat.add_command(label="Crear/Conectar Base de Datos", command = conexionBBDD)
menubasedat.add_command(label="Eliminar Base de Datos", command = eliminarBBDD )
menubasedat.add_command(label="Salir", command = salirAplicación)
menubar.add_cascade(label="Inicio", menu=menubasedat)

hclinica = Menu(menubar, tearoff=0)
hclinica.add_command(label="Historias Clínicas", command= hc)
menubar.add_cascade(label="Datos Personales", menu=hclinica)

ayudamenu = Menu(menubar, tearoff=0)
ayudamenu.add_command(label="Documentación", command = documenta)
ayudamenu.add_command(label="Acerca", command = acerca)
menubar.add_cascade(label="Ayuda", menu=ayudamenu)

#################   TITULO PRINCIPAL DE LA APLICACIÓN  ###########################

#lblTitPpal = Label(root, text="TURNOS PARA CLIENTES DE KINESIOLOGÍA", bg="#6A9C89", fg="white", bd=5, font=("Comic Snas MS", 16, 'bold'))
#lblTitPpal.place(x=270, y=20)
#lblTitPpal.config(relief="sunken")

######################  CUADRO IZQUIERDO FRAME1  ##########################
frame1 = Frame(root)

frame1.pack()
frame1.place(x=10, y=10, width=410, height=300)
frame1.config(bg="#C1CFA1")

frame1.config(bd="3")
frame1.config(relief="sunken") 

lbltit = Label(frame1, text="INGRESO DE DATOS A BASE DE DATOS", anchor='center', bg="green", fg='white', font=('Rockwell',12,'bold'))
lbltit.place(x=10, y=10)

lblMes = Label(frame1, text="MES")
lblMes.place(x=10, y=50, width=100)
lblMes.focus()

textDia = Entry(frame1, textvariable=mes)
textDia.place(x=10, y=80, width=100)

lblDia = Label(frame1, text="DÍA")
lblDia.place(x=150, y=50)

textDia = Entry(frame1, textvariable=dia)
textDia.place(x=150, y=80, width=100)

lblFecha = Label(frame1, text="FECHA")
lblFecha.place(x=10, y=110)

textFecha = Entry(frame1, textvariable=fecha)
textFecha.place(x=10, y=140, width=100)

lblHora = Label(frame1, text="HORA")
lblHora.place(x=150, y=110)

textHora = Entry(frame1, textvariable=hora)
textHora.place(x=150, y=140, width=50)

lblNombres = Label(frame1, text="NOMBRES")
lblNombres.place(x=10, y=170)

textNombres = Entry(frame1, textvariable=nombres)
textNombres.place(x=10, y=200, width=200)

lblAsist = Label(frame1, text="ASISTENCIA")
lblAsist.place(x=10, y=230)

textAsist = Entry(frame1, textvariable=asistencia)
textAsist.place(x=30, y=260, width=50)


######### TREEVIEW PARA MOSTRAR LOS DATOS AGREGADOS - FRAME2  #############

frame2 = Frame(root)
frame2.pack()
frame2.place(x=430, y=10, width=690, height=710)

scrol_y = ttk.Scrollbar(frame2, orient=VERTICAL)
scrol_y.pack(side=RIGHT, fill=Y)

scrol_x =ttk.Scrollbar(frame2, orient=HORIZONTAL)
scrol_x.pack(side=BOTTOM, fill=X)

tree = ttk.Treeview(frame2, columns=('ID','MES','DIA','FECHA','HORA','NOMBRES','ASISTENCIAS'), show ="headings", yscrollcommand=scrol_y.set, xscrollcommand=scrol_x.set)

scrol_y.config(command=tree.yview)
scrol_x.config(command=tree.xview)

tree.column('#0', width=50)
tree.heading('#0',text="ID", anchor=CENTER)
tree.column('#1', width=100, anchor='center')
tree.heading('#1',text="MES", anchor=CENTER)
tree.column('#2', width=100, anchor='center')
tree.heading('#2',text="DIA", anchor=CENTER)
tree.column('#3', width=100, anchor='center')
tree.heading('#3',text="FECHA", anchor=CENTER)
tree.column('#4', width=70, anchor='center')
tree.heading('#4',text="HORA", anchor=CENTER)
tree.column('#5', width=200, anchor='center')
tree.heading('#5',text="NOMBRES", anchor=CENTER)
tree.column('#6', width=100, anchor='center')
tree.heading('#6',text="ASISTENCIA", anchor=CENTER)

tree.pack(expand=True, fill=BOTH)

def seleccionarUsandoClick(event):
    item = tree.identify('item',event.x,event.y)
    id.set(tree.item(item,"text"))
    mes.set(tree.item(item,"values")[0])
    dia.set(tree.item(item,"values")[1])
    fecha.set(tree.item(item,"values")[2])
    hora.set(tree.item(item,"values")[3])
    nombres.set(tree.item(item,"values")[4])
    asistencia.set(tree.item(item,"values")[5])

tree.bind("<Double-1>", seleccionarUsandoClick)

###############################  Actualizar campos(modificar)  ######################################

def actualizar():
    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()
       
    try:
        if mes.get() != '':
            datos = mes.get(), dia.get(), fecha.get(), hora.get(), nombres.get(), asistencia.get()
            miCursor.execute("UPDATE clientes SET MES=?, DIA=?, FECHA=?, HORA=?, NOMBRES=?, ASISTENCIA=? WHERE ID="+id.get(), (datos))
            miConexion.commit()
        else:
            msg = "Los campos están vacios, elija un cliente en la tabla haciendo dobleclic sobre el cliente!!!"
            messagebox.showerror("Error", msg)
    except:
        messagebox.showwarning("ADVERTENCIA", "Ocurrió un error al actualizar el registro...")
        pass
    limpiarDatos()
    mostrar()
    miConexion.close()



###############################  BORRAR REGISTROS  #############################################
def borrarReg():
    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
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
    
    mostrar()
    miConexion.close()

##################################################   BUSCAR POR CAMPOS ####################################  
def buscarNombre():
    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()

    limpiarDatos()
    buscar = EtiBuscar.get()
    EtiBuscar.delete(0, END)
    miCursor.execute("SELECT * FROM clientes WHERE nombres=?", (buscar, ))
    fila=miCursor.fetchall()
    try: 
        for row in fila:
            tree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5],row[6])) 
    except:
        msg ="El nombre del cliente buscado NO EXISTE..."
        messagebox.showerror("ADVERTENCIA", msg)
    miConexion.close()
    #limpiarCampos()

####################################### CONTADOR DE ASISTENCIAS DE CLIENTES ######################################
def contadorAsistencia():
    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()

    tAsistencia = 0
    tsesiones = 0
    buscar = textAsist.get()
    bnombre =textNombres.get()
    limpiarDatos()
    miCursor.execute("SELECT * FROM clientes WHERE ASISTENCIA=?", ( buscar,))
    fila=miCursor.fetchall()
    for row in fila:
        if row[5] == bnombre:
            tAsistencia = tAsistencia + row[6]
                                      
    if tAsistencia > 0 and tAsistencia <= 30:
            tsesiones = tAsistencia

    ventana = Tk()
    ventana.title("TOTAL DE ASISTENCIA")
    ventana.config(width="500", height="250")
    lbl1 = Label(ventana, text="ASISTENCIA DE: ", font=('Rockwell',10,'bold'), fg='blue')
    lbl1.place(x=20, y=50)
    lbl2 =Label(ventana, text=bnombre, font=('Rockwell',10,'bold'),  fg='blue')
    lbl2.place(x=240, y=50)
    lbl3 = Label(ventana, text="Total Asistencias:   ", font=('Rockwell',10,'bold'), fg='blue')
    lbl3.place(x=20, y=80)
    lbl4 =Label(ventana, text=tAsistencia, font=('Rockwell',10,'bold'),  fg='blue')
    lbl4.place(x=240, y=80)
    lbl5 =Label(ventana, text="Asistencias",font=('Rockwell',10,'bold'), fg='blue')
    lbl5.place(x=260, y=80)
    lbl6 = Label(ventana, text="Cantidad de Sesiones:  ", font=('Rockwell',10,'bold'), fg='blue')
    lbl6.place(x=20, y=110)
    lbl7 =Label(ventana, text=tsesiones, font=('Rockwell',10,'bold'),  fg='blue')
    lbl7.place(x=240, y=110)
    lbl5 =Label(ventana, text="por 10 Sesiones",font=('Rockwell',10,'bold'), fg='blue')
    lbl5.place(x=260, y=110)
  
    miConexion.close()

#########################################   LISTADO POR TURNOS #################################################
def listarTurnos():
    miConexion = sqlite3.connect("/home/miguel/python/TurnosClientes/tclientes")
    miCursor = miConexion.cursor()

    try:
        Meses = txtMeses.get()
        miTurno = txtTurno.get()
        miDia = txtMidia.get()
        miFecha = txtMifecha.get()
        limpiarDatos()
        miCursor.execute("SELECT * FROM clientes")
        fila=miCursor.fetchall()
        for row in fila:
            if row[1] == Meses and miTurno.upper() == 'M' and row[2] == miDia and row[3] == miFecha:
                if row[4]>='08:00' and row[4]<='12:00':
                    tree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5],row[6])) 

            if row[1] == Meses and miTurno.upper() == 'T' and row[2] == miDia and row[3] == miFecha:
                if row[4]>='15:00' and row[4]<='20:00':
                    tree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5],row[6])) 

            if row[1] == Meses and miTurno.upper() =='MT' and row[2] == miDia and row[3] == miFecha:
                    if row[4]>='08:00' and row[4]<='20:00':
                        tree.insert("",0,text=row[0], values=(row[1],row[2],row[3],row[4],row[5],row[6])) 
        txtTurno.delete(0, END)
        txtMidia.delete(0, END)
        txtMifecha.delete(0, END)
        txtMeses.delete(0, END)
        txtTurno.focus()
    except:
        messagebox.showwarning("ADVERTENCIA", "El registros buscado NO EXISTE...")
        pass

    miConexion.close()


###########################  MARCO DE BOTONES  -  FRAME3  ##################################

frame3 = Frame(root)
frame3.pack()
frame3.place(x=10, y=320, width=410, height=400)
frame3.config(bg="#C1CFA1")
frame3.config(bd="3")
frame3.config(relief="sunken") 

lblCtrl = Label(frame3, text = 'BOTONES DE CONTROL',fg='white', bg ='green', font=('Rockwell',12,'bold'))
lblCtrl.grid(columnspan=3, column=0,row=0, pady=3, padx=1)         
btnRegistrar = Button(frame3, command= crear, text=' REGISTRAR CLIENTES ', font=('Arial',8,'bold'))
btnRegistrar.grid(column=0,row=1, pady=10, padx=1)
btnLimpiar =Button(frame3, text=' LIMPIAR TABLA ', command = limpiarDatos, font=('Arial',8,'bold')) 
btnLimpiar.grid(column=1,row=1, padx=1)        
btnBuscar = Button(frame3, text=' BUSCAR POR NOMBRE ',command = buscarNombre, font=('Arial',8), bg='orange') 
btnBuscar.grid(column = 1, row=2)
EtiBuscar = Entry(frame3, font=('Arial',8), width=23) 
EtiBuscar.grid(column=0,row=2, pady=1, padx=1)
btnListar = Button(frame3, command = ordenarBD, text=' MOSTRAR LISTA DE CLIENTES ', font=('Arial',8,'bold')) 
btnListar.grid(column=0,row=3, padx=10, pady=8)
btnEliminar = Button(frame3, text=' ELIMINAR ', command = borrarReg, font=('Arial',8,'bold'), bg='red', fg='white') 
btnEliminar.grid(column=1,row=3, padx=5, pady=8)
btnModificar = Button(frame3, text=' ACTUALIZAR REGISTROS',  command = actualizar, font=('Arial',8,'bold')) 
btnModificar.grid(column=0,row=4, padx=1, pady=8)
btnTAsis= Button(frame3,  text='TOTAL ASISTENCIAS', command=contadorAsistencia, font=('Arial',8,'bold')) 
btnTAsis.grid(column=1,row=4, padx=1, pady=8)
lblTurnos = Label(frame3, text='LISTAR POR TURNOS',  fg='white', bg ='green', font=('Arial',12,'bold'))
lblTurnos.grid(columnspan=2,column=0,row=6, pady=3, padx=1)
lblTurno = Label(frame3, text='Ingrese el turno (M / T / MT)')
lblTurno.grid(column=0,row=7, padx=2, pady=3)
txtTurno = Entry(frame3, textvariable=turno)
txtTurno.grid(columnspan=3,column=1,row=7, padx=5, pady=3)
lblMidia = Label(frame3, text='Ingrese el día de la semana')
lblMidia.grid(column=0,row=8, padx=2, pady=3)
txtMidia = Entry(frame3, textvariable=miDia)
txtMidia.grid(columnspan=3,column=1,row=8, padx=5, pady=3)
lblMifecha = Label(frame3, text='Ingrese la fecha de la semana')
lblMifecha.grid(column=0,row=9, padx=2, pady=3)
txtMifecha = Entry(frame3, textvariable=miFecha)
txtMifecha.grid(columnspan=3,column=1,row=9, padx=5, pady=3)
lblMeses = Label(frame3, text='Ingrese el mes a listar       ')
lblMeses.grid(column=0,row=10, padx=2, pady=3)
txtMeses = Entry(frame3, textvariable=Meses)
txtMeses.grid(columnspan=3,column=1,row=10, padx=5, pady=3)


btnListarTurnos= Button(frame3, command = listarTurnos,  text=' LISTAR POR TURNOS ', font=('Arial',8,'bold')) 
btnListarTurnos.grid(columnspan=3, column=0,row=11, padx=10, pady=1)


##################################################################################################


root.config(menu=menubar)
root.mainloop()

##    Para hacer una paquete de un solo archivo y ejecutable debemos usar la siguiente línea en la consola
####  pyinstaller --windowed --onefile main.py
      

from tkinter import Entry, Label, Frame, Tk, Button, ttk, Scrollbar, VERTICAL, HORIZONTAL, StringVar, END
from conexionBD import*

root = Tk()
root.config(width="800", height="600")

dia = StringVar()
fecha = StringVar()
hora = StringVar()
nombres = StringVar()
asistencia = StringVar()

#################   Titulo principal del formulario  ###########################

lblTitPpal = Label(root, text="TURNOS PARA CLIENTES DE KINESIOLOGÍA", bg="#6A9C89", fg="white", bd=5, font=("Comic Snas MS", 16, 'bold'))
lblTitPpal.place(x=200, y=10)
lblTitPpal.config(relief="sunken")

######################  Cuadro Izquierdo - Carga de datos   ##########################
frame1 = Frame(root, width=300, height=350)

frame1.pack(padx=10, pady=80, side="left", anchor="n")
frame1.config(bg="#C1CFA1")

frame1.config(bd="2")
frame1.config(relief="sunken") 

lbltit = Label(frame1, text="DATOS DE LA BASE DE DATOS", anchor='center')
lbltit.place(x=70, y=10)

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

textAsist = Entry(frame1, textvariable=hora)
textAsist.place(x=10, y=310, width=50)


######### Armado de cuadro derecho para mostrar lista de datos #############

frame2 = Frame(root, width=500, height=250)

frame2.pack(padx=10, pady=80, side="left", anchor="n")

lista = ttk.Treeview(frame2, height=21)
lista.grid(column=0, row=0)

ladox = Scrollbar(frame2, orient = HORIZONTAL, command= lista.xview)
ladox.grid(column=0, row = 1, sticky='ew') 
ladoy = Scrollbar(frame2, orient =VERTICAL, command = lista.yview)
ladoy.grid(column = 1, row = 0, sticky='ns')

lista.configure(xscrollcommand = ladox.set, yscrollcommand = ladoy.set)

lista['columns'] = ('dia', 'fecha', 'hora', 'nombres','asistencia')

lista.column('#0',minwidth=1, width=1)
lista.column('dia', minwidth=100, width=100 , anchor='center')
lista.column('fecha', minwidth=100, width=100, anchor='center' )
lista.column('hora', minwidth=50, width=50 , anchor='center')
lista.column('nombres', minwidth=150, width=150, anchor='center')
lista.column('asistencia', minwidth=100, width=100, anchor='center')

lista.column('#0',minwidth=1, width=1)
lista.heading('dia',  text='DIA', anchor ='center')
lista.heading('fecha', text='FECHA', anchor ='center')
lista.heading('hora', text='HORA', anchor ='center')
lista.heading('nombres', text='NOMBRES', anchor ='center')
lista.heading('asistencia', text='ASISTENCIA', anchor ='center')

estilo = ttk.Style(frame2)
estilo.theme_use('alt') #  ('clam', 'alt', 'default', 'classic')
estilo.configure(".",font= ('Helvetica', 12, 'bold'), foreground='red2')        
estilo.configure("Treeview", font= ('Helvetica', 10, 'bold'), foreground='black',  background='white')
estilo.map('Treeview',background=[('selected', 'green2')], foreground=[('selected','black')] )

lista.bind("<<TreeviewSelect>>", 'obtener_fila')  # seleccionar  fila

###########################  MARCO DE BOTONES ##################################

frame3 = Frame(root, width=450, height=350)
frame3.place(x=10, y=450)
frame3.config(bg="#C1CFA1")
frame1.config(bd="2")
frame1.config(relief="sunken") 

lblCtrl = Label(frame3, text = 'Botones de Control',fg='white', bg ='black', font=('Rockwell',12,'bold'))
lblCtrl.grid(columnspan=3, column=0,row=0, pady=1, padx=4)         
btnRegistrar = Button(frame3, text=' REGISTRAR ', font=('Arial',8,'bold'), bg='green', fg='white')#'command= agregar_datos',
btnRegistrar.grid(column=0,row=1, pady=10, padx=4)
btnLimpiar =Button(frame3, text=' LIMPIAR ', font=('Arial',8,'bold'), bg='orange red') #'command = limpiar_datos',
btnLimpiar.grid(column=1,row=1, padx=10)        
btnEliminar = Button(frame3, text=' ELIMINAR ', font=('Arial',8,'bold'), bg='red', fg='white') #'activebackground=command = eliminar_fila',
btnEliminar.grid(column=2,row=1, padx=4)
btnBuscar = Button(frame3, text=' BUSCAR POR NOMBRE ', font=('Arial',8), bg='orange') #'command = buscar_nombre',
btnBuscar.grid(columnspan=2,column = 1, row=2)
EtiBuscar = Entry(frame3, font=('Arial',8), width=23) #'textvariable=buscar' ,
EtiBuscar.grid(column=0,row=2, pady=1, padx=1)
btnListar = Button(frame3, text=' MOSTRAR LISTA DE CLIENTES ', font=('Arial',8,'bold'), bg='green2') #'command = mostrar_todo',
btnListar.grid(columnspan=3,column=0,row=3, pady=8)



root.mainloop()


      

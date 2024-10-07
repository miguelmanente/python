#-*- coding: utf  -8 -*-
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
 
root = Tk()
root.title('Ejemplos de tablas')
root.geometry('400x60')
 
#cambie las dimensiones porque es más rápido que ponerme a agregar elementos
 
tv = ttk.Treeview(root, columns=("col1", "col2"))
tv.column("#0", width=200)
tv.column("col1", width=80, anchor=CENTER)
tv.column("col2", width=80, anchor=CENTER)
 
 
tv.heading("#0", text="Producto", anchor=CENTER)
tv.heading("col1", text="Precio", anchor=CENTER)
tv.heading("col2", text="Stock", anchor=CENTER)
 
tv.insert("", END, text="Leche Ylolay TB x 1 litro", values=("130.50", "29"))
tv.insert("", END, text="Tomate Arcor lata x 410 grs.", values=("106.00", "48"))
tv.insert("", END, text="Aceite Zanoni botella x 900 cc.", values=("230.00", "11"))
tv.insert("", END, text="Leche Ylolay TB x 1 litro", values=("130.50", "29"))
tv.insert("", END, text="Tomate Arcor lata x 410 grs.", values=("106.00", "48"))
tv.insert("", END, text="Aceite Zanoni botella x 900 cc.", values=("230.00", "11"))
tv.insert("", END, text="Leche Ylolay TB x 1 litro", values=("130.50", "29"))
tv.insert("", END, text="Tomate Arcor lata x 410 grs.", values=("106.00", "48"))
tv.insert("", END, text="Aceite Zanoni botella x 900 cc.", values=("230.00", "11"))
tv.insert("", END, text="Leche Ylolay TB x 1 litro", values=("130.50", "29"))
tv.insert("", END, text="Tomate Arcor lata x 410 grs.", values=("106.00", "48"))
tv.insert("", END, text="Aceite Zanoni botella x 900 cc.", values=("230.00", "11"))
 
tv.pack(side='left') # supongo que sabes usar pack
ejscrollbar= ttk.Scrollbar(root,orient=VERTICAL,command=tv.yview)
ejscrollbar.pack(side='right',fill='y')
tv.configure(yscrollcommand=ejscrollbar.set)
 
root.mainloop()
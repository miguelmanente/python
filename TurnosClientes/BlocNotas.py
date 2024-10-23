import os
from tkinter import *
from tkinter import filedialog, colorchooser, font
from tkinter.messagebox import *
from tkinter.filedialog import *

def blockNotas():
    def change_color():
        color = colorchooser.askcolor(title="Colores")
        text_area.config(fg=color[1])

    def change_font(*args):
        text_area.config(font=(font_name.get(), size_box.get()))

    def new_file():
        window.title("Sin Nombre")
        text_area.delete(1.0, END)


    def open_file():
        file = askopenfilename(defaultextension=".txt",
                                file=[("All Files", "*.*"),
                                ("Text Documents", "*.txt")])
        try:
            window.title(os.path.basename(file))
            text_area.delete(1.0, END)   
            file = open(file, "r")
            text_area.insert(1.0, file.read()) 
        except:
            showinfo("ERROR","No se puede leer el archivo") 
        finally:
            file.close()
                    

    def save_file():
        file = filedialog.asksaveasfilename(initialfile="sinNombre.txt",
                                            defaultextension=".txt",
                                            filetypes=[("All Files", "*.*"),
                                            ("Text Documents", "*.txt")])
        if file is None:
            return
        else:
            try:
                window.title(os.path.basename(file))
                file = open(file, "w")
                file.write(text_area.get(1.0, END))
            except:
                showinfo("ERROR","No se puedo grabar el archivo") 
            finally:
                file.close()
        
    def cut():
        text_area.event_generate("<<Cut>>")

    def copy():
        text_area.event_generate("<<Copy>>")

    def paste():
        text_area.event_generate("<<Paste>>")

    def about():
        showinfo("Acerca del block de notas", 
            '''Block de Notas es un editor de texo incluído en el sistema de
        clientes.Su funcionalidad es la de poder tipear información 
            sobre las historias clínicas de los pacientes que vendrán
            hacer los tratamientos kinesiológicos ''')

    def quit():
        window.destroy()

    window = Tk()
    window.title("Bloc de Notas")
    file = None

    font_name = StringVar(window)     #variable para el tipo de letra a usar en el block de notas
    font_name.set("Arial")

    font_size = StringVar(window)     #Variable que se usará para saber el tamaño de la letra
    font_size.set("12")

    window_width = 500     #Medidas que queremos darle a nuestra ventana
    window_height = 500
    screen_width =window.winfo_screenwidth()  #Ancho y alto de la pantalla que tenemos
    screen_height =window.winfo_screenheight()

    x = int((screen_width / 2) - (window_width / 2))  #Calcula el centro de la pantalla
    y = int((screen_height / 2) - (window_height / 2))
    window.geometry("{}x{}+{}+{}".format(window_width, window_height, x, y))  #Posicionamos la ventana en el centro de la pantalla

    text_area = Text(window, font=(font_name.get(), font_size.get()))  #Definimos el área de texto con tipo de fuente y tamaño de la misma
    scroll_bar = Scrollbar(text_area)

    window.grid_rowconfigure(0, weight=1)    #redimensiona el área del texto para los renglones com las columnas
    window.grid_columnconfigure(0, weight=1)

    text_area.grid(sticky = N + E + S + W )  #Acomodamos todo el área de escritura a toda la ventana 

    frame =Frame(window)          #Creamos un frame para botones        
    frame.grid()

    color_button = Button(frame, text="color", command=change_color) #Botón que va a cambiar el color del texto
    color_button.grid(row=0, column=0)

    font_box = OptionMenu(frame, font_name, *font.families(), command=change_font) #Menu de opciones que nos permite cambiar la tipografía por defecto(Arial)
    font_box.grid(row=0, column=1)

    size_box = Spinbox(frame, from_=1, to=100, textvariable=font_size, command=change_font)  #Control para cambiar el tamaño del texto en el área de texto
    size_box.grid(row=0, column=2)

    scroll_bar.pack(side=RIGHT, fill=Y)     #Barra de sroll vertical con el texto supere el alto de la ventana elegido
    text_area.config(yscrollcommand=scroll_bar.set)

    #######################  BARRA DE MENÚES ###################################################
    menu_bar = Menu(window)
    window.config(menu=menu_bar)

    file_menu = Menu(menu_bar,tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="New", command=new_file)
    file_menu.add_command(label="Open", command=open_file)
    file_menu.add_command(label="Save", command=save_file)
    file_menu.add_separator()
    file_menu.add_command(label="Exit", command=quit)

    edit_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Edit", menu=edit_menu)
    edit_menu.add_command(label="Cut", command=cut)
    edit_menu.add_command(label="Copy", command=copy)
    edit_menu.add_command(label="Paste", command=paste)

    help_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=about)


    window.mainloop()
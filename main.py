from tkinter import filedialog
from tkinter import *
import os

# parent window
root = Tk()
root.title('Canis')
root.geometry('500x700')

def open_file():
    global filename
    currentdir = str(os.getcwd())
    filename = filedialog.askopenfilename(initialdir=currentdir, title="Select file to open...", filetypes=(
        ('All Files', '*.*'),
        ('C', '*.c'),
        ('C++','*.cpp'),
        ('Header files', '*.h'),
    )
                                          )

    if filename == "":
        filename = None # Absence of file
    else:
        root.title(os.path.basename(filename) + ' - Canis') # return file basename
        textpad.delete(1.0, END)
        filehandle = open(filename, "r")
        textpad.insert(1.0, filehandle.read())
        filehandle.close()


def save():
    global filename
    try:
        f = open(filename, 'w')
        letter = textpad.get(1.0, END)
        f.write(letter)
        f.close()
    except:
        save_as()

def save_as():
    try:
        f = filedialog.asksaveasfilename(initialfile='untitled.c', defaultextension='.c')
    except:
        pass

# edit menu functions
def cut():
    textpad.event_generate("<<Cut>>")

def copy():
    textpad.event_generate("<<Copy>>")

def paste():
    textpad.event_generate("<<Paste>>")

def undo():
    textpad.event_generate("<<Undo>>")

def redo():
    textpad.event_generate("<<Redo>>")

def select_all():
    textpad.tag_add('sel', '1.0', END)

def on_find():
    t2 = Toplevel(root)
    t2.title('Find')
    t2.geometry('350x70+500+300')
    t2.transient(root)
    Label(t2, text="Find All:").grid(row=0, column=0, sticky='e')
    v = StringVar()
    e = Entry(t2, width=25, textvariable=v)
    e.grid(row=0, column=1, padx=2, pady=2, sticky='we')
    e.focus_set()
    c = IntVar()
    Checkbutton(t2, text='Ignore Case', variable=c).grid(row=1, column=1, sticky='e', padx=2, pady=2)
    Button(t2, text="Find All", underline=0, command=lambda: search_for(v.get(), c.get(), textpad, t2, e)).grid(row=0, column=2, sticky='e'+'w', padx=2, pady=2)

    def close_search():
        textpad.tag_remove('match', '1.0', END)
        t2.destroy()

    t2.protocol('WM_DELETE_WINDOW', close_search) # override close btn to unselect searched word

def search_for(needle, cssnstv, textpad, t2, e):
    textpad.tag_remove('match', '1.0', END)
    count = 0
    if needle:
        pos = '1.0'
        while True:
            pos = textpad.search(needle, pos, nocase=cssnstv, stopindex=END)
            if not pos: break
            lastpos = '%s+%dc' % (pos, len(needle))
            textpad.tag_add('match', pos, lastpos)
            count += 1
            pos = lastpos
    textpad.tag_config('match', foreground='red', background='yellow')
    e.focus_set()
    t2.title('%d matches found' %count)



# create a menu bar
menubar = Menu(root)

# file menu
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT,  underline=0)
filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT,  underline=0, command=open_file)
filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT,  underline=0)
filemenu.add_command(label="Save As", compound=LEFT,  underline=0)
filemenu.add_command(label="Quit", accelerator='Ctrl+Q', compound=LEFT,  underline=0)

# edit menu
editmenu = Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo", accelerator='Ctrl+Z', compound=LEFT,  underline=0, command=undo)
editmenu.add_command(label="Redo", accelerator='Ctrl+Y', compound=LEFT,  underline=0, command=redo)
editmenu.add_command(label="Cut", accelerator='Ctrl+X', compound=LEFT,  underline=0, command=cut)
editmenu.add_command(label="Copy", accelerator = 'Ctrl+C',compound=LEFT,  underline=0, command=copy)
editmenu.add_command(label="Paste", accelerator = 'Ctrl+V',compound=LEFT,  underline=0, command=paste)
editmenu.add_command(label="Find", accelerator = 'Ctrl+F',compound=LEFT,  underline=0, command=on_find)
editmenu.add_command(label="Select All", accelerator = 'Ctrl+A',compound=LEFT,  underline=0, command=select_all)

# view menu
viewmenu = Menu(menubar, tearoff=0)
viewmenu.add_checkbutton(label='Line numbers')
viewmenu.add_checkbutton(label='Status Bar')
viewmenu.add_checkbutton(label='Highlight current line')
themesmenu = Menu(viewmenu, tearoff=0)
viewmenu.add_cascade(label='Themes', menu=themesmenu)
themesmenu.add_radiobutton(label="Default White")
themesmenu.add_radiobutton(label="Dark Lord")
themesmenu.add_radiobutton(label="Vivacious Violet")
themesmenu.add_radiobutton(label="Gregory Dark")
themesmenu.add_radiobutton(label="Solarised")
themesmenu.add_radiobutton(label="Monokai")


# about menu
aboutmenu = Menu(menubar, tearoff=0)

menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="View", menu=viewmenu)
menubar.add_cascade(label="About", menu=aboutmenu)

# shortcut bar
shortcutbar = Frame(root, height=25, bg="light sea green")
shortcutbar.pack(expand=NO, fill=X)

# line numbers column
linelabel = Label(root, width=2, bg='antique white')
linelabel.pack(side=LEFT, anchor='nw', fill=Y)

# textpad and scroll bar
textpad = Text(root, undo=True)
textpad.pack(expand=YES, fill=BOTH)
scroll = Scrollbar(textpad)
textpad.configure(yscrollcommand=scroll.set)
scroll.config(command=textpad.yview)
scroll.pack(side=RIGHT, fill=Y)

root.config(menu=menubar) # display menu
root.mainloop()
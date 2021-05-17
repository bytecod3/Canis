from tkinter import filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
import PIL
from tkinter import *
import os

# parent window
root = Tk()
ico = PhotoImage(file='icons/logo.png') # setting window icon
root.iconphoto(False, ico)
root.title('Canis')
root.geometry('500x700')


# help and about
def about(event=None):
    messagebox.showinfo("About", "Canis is a customisable minimal C and C++ editor with just enough features for your development needs.\nVisit www.canis.org for more info.")

def help(event=None):
    messagebox.showinfo("Help", "Visit www.canis.org for help.")

def quit_editor(event=None):
    if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
        root.destroy()


root.protocol('WM_DELETE_WINDOW', quit_editor)

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
        root.title(str(os.path.basename(filename)) + ' - Canis') # return file basename
        textpad.delete(1.0, END)
        filehandle = open(filename, "r")
        textpad.insert(1.0, filehandle.read())
        filehandle.close()
    
    update_linenumbers()


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
        f = filedialog.asksaveasfilename(initialfile='untitled', defaultextension='.c', filetypes=(
            ('All Files', '*.*'),
            ('C', '*.c'),
            ('C++', '*.cpp'),
            ('Header files', '*.h')
        ))

        filehandler = open(f, 'w')
        textoutput = textpad.get(1.0, END)
        filehandler.write(textoutput)
        filehandler.close(f)
        root.title(os.path.basename(f) + ' - Canis')

    except:
        pass

def new_file():
    root.title('Untitled')
    global filename
    filename = None
    textpad.delete(1.0, END)
    update_linenumbers()


# edit menu functions
def cut():
    textpad.event_generate("<<Cut>>")
    update_linenumbers()

def copy():
    textpad.event_generate("<<Copy>>")
    update_linenumbers()

def paste():
    textpad.event_generate("<<Paste>>")
    update_linenumbers()

def undo():
    textpad.event_generate("<<Undo>>")
    update_linenumbers()

def redo():
    textpad.event_generate("<<Redo>>")
    update_linenumbers()

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
filemenu.add_command(label="New", accelerator='Ctrl+N', compound=LEFT,  underline=0, command=new_file)
filemenu.add_command(label="Open", accelerator='Ctrl+O', compound=LEFT,  underline=0, command=open_file)
filemenu.add_command(label="Save", accelerator='Ctrl+S', compound=LEFT,  underline=0, command=save)
filemenu.add_command(label="Save As", accelerator='Shift+Ctrl+S', compound=LEFT,  underline=0, command=save_as)
filemenu.add_command(label="Quit", accelerator='Ctrl+Q', compound=LEFT,  underline=0, command=quit_editor)

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
showln = IntVar()
showln.set(1)
viewmenu.add_checkbutton(label='Line numbers', variable=showln)
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


# about and help menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="About", command=about)
helpmenu.add_command(label="Help", command=help)


menubar.add_cascade(label="File", menu=filemenu)
menubar.add_cascade(label="Edit", menu=editmenu)
menubar.add_cascade(label="View", menu=viewmenu)
menubar.add_cascade(label="Help", menu=helpmenu)

# shortcut bar
shortcutbar = Frame(root, height=25)

icons = ['new_file', 'open_file', 'save', 'cut', 'copy', 'paste', 'undo', 'redo', 'on_find', 'about']
width = 25
height = 25

for i, icon in enumerate(icons):
    ic = ImageTk.PhotoImage(PIL.Image.open('icons/' + icon + '.png').resize((width, height)))
    cmd =eval(icon) # convert to expression
    toolbar = Button(shortcutbar, image=ic, command=cmd)
    toolbar.image = ic
    toolbar.pack(side=LEFT)

shortcutbar.pack(expand=NO, fill=X)

# line numbers column
linelabel = Label(root, width=2)
linelabel.pack(side=LEFT, anchor='nw', fill=Y)

# line numbers
def update_linenumbers(event=None):
    txt = ''
    if showln.get():
        endline, endcolumn = textpad.index('end-lc').split('.')
        txt = '\n'.join(map(str, range(1, int(endline))))
    linelabel.config(text=txt, anchor='nw')


# textpad and scroll bar
textpad = Text(root, undo=True)
# binding for line numbers
textpad.bind("<Any-KeyPress>", update_linenumbers)
textpad.pack(expand=YES, fill=BOTH)
scroll = Scrollbar(textpad)
textpad.configure(yscrollcommand=scroll.set)
scroll.config(command=textpad.yview)
scroll.pack(side=RIGHT, fill=Y)



root.config(menu=menubar) # display menu
root.mainloop()
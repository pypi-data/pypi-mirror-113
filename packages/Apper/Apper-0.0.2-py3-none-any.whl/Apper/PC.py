from tkinter import *
apper = Tk()
apper.title('Apper')
def setting(icon=None,title='Apper',bground='#ECF0F1',width=500,height=500):
    apper.config(bg=bground,width=width,height=height)
    apper.iconbitmap(icon)
    apper.title(title)
def text(textvar=None,text='Apper_text',bground=None,fground='black',width=None,height=5,x=0,y=0):
    Label(apper,textvariable=textvar,text=text,width=width,height=height).place(x=x,y=y)
def button(textvar=None,text='Apper_butoon',bground=None,fground='black',width=10,height=2,x=0,y=0):
    Button(apper,textvariable=textvar,text=text,bg=bground,fg=fground,width=width,height=height).place(x=x,y=y)
def textline(textvar=None,bground='white',fground='black',x=0,y=0,width=20):
    e=Entry(apper,textvariable=textvar,width=width,bg=bground,fg=fground)
    e.place(x=x,y=y)
def textbox(textvar=None,bground='white',fground='black',x=0,y=0,width=50,height=10):
    b=Text(apper,textvariable=textvar,width=width,height=height,bg=bground,fg=fground)
    b.place(x=x,y=y)
def run():
    apper.mainloop()







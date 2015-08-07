# -*- coding: utf-8 -*-
from Tkinter import *
import tkFileDialog
from PIL.ImageTk import PhotoImage,Image
from csv import *
import Tix
import tkMessageBox
import webbrowser
import csv
from copy import *

class Configurer():
    """
    Configurer is a module that helps you to create a configuration file to use in the OMR script.
    @author Romualdo André da Costa
    @version 1.0
    """
    def __init__(self):
        """
        Constructor
        """

    
        self.images=[]#keeps image references and avoids garbage colector
        self.tag=0#indentifier for a new field
        self.tagobject=None#identifier tag for a selected or new field
        self.tags={}#a tag for each field
        self.appfile=None#configuration file
        self.fields={}#fields or questions in a sheet
        self.field={}#temp dict with informations about a field in a sheet
        self.top=None#field configuration dialog
        self.image=None#background image
        self.imageid=None#identifier of the background image in canvas object
        self.root= Tix.Tk()#main windows
        self.imidvar=Tix.IntVar(self.root) #the field is part of the sheet identifier number
        self.root.title("Configurer 1.0")
        try:
            self.root.iconbitmap('icon.ico')
	except TclError:
            print 'No icon file found'
        self.root.bind_all("<Control-q>", lambda(event): self.root.quit())
        self.root.bind_all("<Control-a>", lambda(event): self.load_app())
        self.root.bind_all("<Control-i>", lambda(event): self.set_photo())
        self.root.bind_all("<Control-s>", lambda(event): self.save_app())
        self.root.bind_all("<Control-n>", lambda(event): self.new_app())
        self.make_menu()
        self.make_canvas()
        self.lastx, self.lasty, self.objeto=0,0,None

    def make_canvas(self):
        """
        Canvas to delimit graphically the dimensions of a field
        """
        h = Scrollbar(self.root, orient=HORIZONTAL)
        v = Scrollbar(self.root, orient=VERTICAL)
        self.canvas = Canvas(self.root, scrollregion=(0, 0, 1000, 1000), yscrollcommand=v.set, xscrollcommand=h.set)
        
        h['command'] = self.canvas.xview
        v['command'] = self.canvas.yview

        self.canvas.grid(column=0, row=0, sticky=(N,W,E,S))
        h.grid(column=0, row=1, sticky=(W,E))
        v.grid(column=1, row=0, sticky=(N,S))
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        if self.image:
            imgtk = PhotoImage(image=Image.open(self.image))                 # not file=imgpath
            imgwide  = imgtk.width()                         # size in pixels
            imghigh  = imgtk.height()                        # same as imgpil.size
            fullsize = (0, 0, imgwide, imghigh)              # scrollable
            self.canvas.delete('all')                             # clear prior photo
            self.canvas.config(height=imgwide, width=imghigh)   # viewable window size
            self.canvas.config(scrollregion=fullsize)             # scrollable area size
            self.imageid=self.canvas.create_image(0, 0, image=imgtk, anchor=NW)
            self.images.append(imgtk)
            self.canvas.bind("<Button-1>", self.xy)
            self.canvas.bind("<B1-Motion>", self.add_rectangle)
            self.canvas.bind("<B1-ButtonRelease>", self.done_stroke)
            self.canvas.bind_all('<Button-2>', self.select)
            self.canvas.bind_all('<B2-Motion>', self.on_drag)
            self.canvas.bind_all("<B2-ButtonRelease>", self.update_item)
            self.canvas.bind('<Button-3>', self.config_item)
            self.canvas.bind_all('<Delete>',self.delete_item)            
            self.canvas.focus()

    def main(self):
        """
        Main loop
        """
        self.root.mainloop()

    def make_menu(self):
        """
        Main windows menu
        """
        top=Menu(self.root)
        file = Menu(top,tearoff=False)
        file.add_command(label='New',  command=self.new_app,  underline=0,accelerator="Ctrl+n")
        file.add_command(label='Open Background Image', command=self.set_photo,  underline=6,accelerator="Ctrl+i")
        file.add_command(label='Open', command=self.load_app,  underline=0,accelerator="Ctrl+a")
        file.add_command(label='Save',  command=self.save_app,  underline=0,accelerator="Ctrl+s")
        file.add_separator()
        file.add_command(label='Quit',    command=self.root.quit, underline=0,accelerator="Ctrl+q")
        top.add_cascade(label='File',     menu=file,        underline=0)
        edit= Menu(top, tearoff=False)
        edit.add_command(label='New',     command=self.menu_edit_new,  underline=0)
        edit.add_command(label='Move',   command=self.menu_edit_move,  underline=0)
        top.add_cascade(label='Field',     menu=edit,        underline=1)
        help= Menu(top, tearoff=False)
        help.add_command(label='About',     command=self.about,  underline=0)
        top.add_cascade(label='Help',     menu=help,        underline=1)
        self.root.config(menu=top)

    def menu_edit_new(self):
        self.canvas.bind("<Button-1>", self.xy)
        self.canvas.bind("<B1-Motion>", self.add_rectangle)
        self.canvas.bind("<B1-ButtonRelease>", self.done_stroke)

    def menu_edit_move(self):
        self.canvas.bind("<Button-1>", self.select)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<B1-ButtonRelease>", self.update_item)

    def new_app(self):
        """
        Setup new file
        """
        self.field={}
        self.fields={}
        self.tag=0
        self.tags={}
        self.make_canvas()
        self.root.title("Configurer 1.0")

    def about(self):
        """
        Shows about dialog
        """
        tkMessageBox.showinfo("About", "Configurer 1.0\nLicenciado sobre a GPL v3")

    def select(self,event):
        """ 
        Selects a field in the sheet so you can delete or move the field
        @param event Event: mouse event
        """
        self.canvas.focus()
        self.canvas.itemconfigure('region', outline='black')
        self.canvas.itemconfigure('tag', fill='black')
        self.objeto = self.canvas.find_withtag(CURRENT)[0]   # tuple
        self.where=event
        if self.objeto!=self.imageid and 'tag' not in self.canvas.gettags(self.objeto):
            self.canvas.itemconfigure(self.objeto, outline='red',width=3)
            self.canvas.itemconfigure(self.tags[self.objeto]['id'], fill='red')

    def config_item(self,event):
        """
        Opens the field configuration dialog
        @param event Event: mouse event
        """
        self.canvas.itemconfigure('region', outline='black')
        self.canvas.itemconfigure('tag', fill='black')
        self.where  = event
        self.objeto = self.canvas.find_withtag(CURRENT)[0]   # tuple
        if self.objeto!=self.imageid and 'tag' not in self.canvas.gettags(self.objeto):
            self.canvas.itemconfigure(self.objeto, outline='blue',width=3)
            self.canvas.itemconfigure(self.tags[self.objeto]['id'], fill='blue')
            self.field=self.fields[self.objeto]
            self.imidvar.set(int( self.field['imid']))
            self.open_conf_dialog(self.field['num_cell'],self.field['direction'],self.field['type'],self.field['width'],self.field['height'],self.field['space'])

    def xy(self,event):
        """
        Sets x and y of a field
        @para event Event: evento do mouse
        """
        self.canvas.itemconfigure('region', outline='black')
        self.canvas.itemconfigure('tag', fill='black')
        self.lastx, self.lasty = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)        
        self.objeto=None
        
    def add_rectangle(self,event):
        """
        Creates a rectangle on the canvas to indicates a field
        @param event Event: evento do mouse
        """
        if self.objeto:
            self.canvas.delete(self.objeto)
            self.canvas.delete(self.tagobject)
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.objeto=self.canvas.create_rectangle((x, y, self.lastx, self.lasty),tags=('region'),width=3)
        self.tagobject=self.canvas.create_text((self.lastx-10, self.lasty-10),tags=('tag'),text=str(self.tag))

    def done_stroke(self,event):
        """
        Finalização da seleção da região ou campo da prova. Chama o diálogo para
        configurar os detalhes do campo.
        """
        self.canvas.itemconfigure('region', width=2)
        x, y = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        self.field['x'],self.field['y']=self.lastx,self.lasty
        self.open_conf_dialog()
        

    def on_drag(self, event):
        """
        Ação de mover a região selecionada.
        @param event Event: evento do mouse
        """
        if self.objeto!=self.imageid and 'tag' not in self.canvas.gettags(self.objeto):
            diffX = event.x - self.where.x                # OK if object in moving
            diffY = event.y - self.where.y                # throws it off course
            self.canvas.move(self.objeto, diffX, diffY)
            self.canvas.move(self.tags[self.objeto]['id'], diffX, diffY)
            self.where=event

    def set_photo(self):
        """
        Escolha da foto a ser carregada no plano de fundo do canvas e servir como orientação para a criação da máscara de correção de provas. A imagem deve estar em PNG.
        @todo permitir outros formatos de arquivos de imagens
        """
        filetypes=[('TIFF files', '.tif'),('JPG files', '.jpg'),('PNG files', '.png'), ('All files', '*')]
        self.image=tkFileDialog.askopenfilename( filetypes=filetypes)
        self.make_canvas()
        if self.appfile:
            if self.appfile.closed:
                with open(self.appfile.name) as self.appfile:
                    self.load_fields()
                    self.appfile.close()

    def load_fields(self):
        """
        Load fields from the file
        """
        reader = csv.DictReader(self.appfile)
        fields = [row for row in reader]
        for field in fields:
            if field['direction']=='vertical':
                objeto=self.canvas.create_rectangle((float(field['x']), float(field['y']), float(field['x'])+float(field['width']), float(field['y'])+float(field['space'])*float(field['num_cell'])+float(field['height'])*float(field['num_cell'])),tags=('region'),width=3)
            else:
                objeto=self.canvas.create_rectangle((float(field['x']), float(field['y']), float(field['x'])+float(field['width'])*float(field['num_cell'])+float(field['space'])*float(field['num_cell']), float(field['y'])+float(field['height'])),tags=('region'),width=3)
            tagobject=self.canvas.create_text((float(field['x'])-10, float(field['y'])-10),tags=('tag'),text=str(field['tag']))
            self.fields[objeto]=field
            self.tags[objeto]={'id': tagobject,'value':field['tag']}
            self.tag=self.tag+1

    def delete_item(self,event):
        """
        Apaga uma região ou campo selecionado.
        @param event Event: evento do teclado
        """
        if self.objeto and self.objeto!=self.imageid and 'tag' not in self.canvas.gettags(self.objeto):
            del self.fields[self.objeto]
            self.canvas.delete(self.objeto)
            self.canvas.delete(self.tags[self.objeto]['id'])
            del self.tags[self.objeto]
            self.tag=len(self.tags)
            if self.top :
                self.top.destroy()
            
    def load_app(self):
        """
        Carrega um arquivo com uma máscara de correções de provas. O arquivo deve ter a extensão .csv
        """
        self.tag=0
        self.tags={}
        if not self.image:
            tkMessageBox.showerror("Erro", "Nenhuma imagem de fundo carregada")
            return
        self.fields={}
        filetypes=[('CSV files', '.csv'), ('All files', '*')]
        appfilename=tkFileDialog.askopenfilename( filetypes=filetypes)
        if appfilename!=None and appfilename!='':
            self.appfile=open(appfilename, 'rb')
            self.root.title("Configurer 1.0 - "+appfilename)
            if self.canvas:
                self.make_canvas()
            self.load_fields()
            self.appfile.close()

    def save_app(self):
        """
        Salva os campos selecionados em um arquivo .csv para utilização pelo Arya
        """
        if len(self.fields)<1:
            tkMessageBox.showerror("Erro", "Nenhum campo configurado")
            return
        filetypes=[('CSV files', '.csv'), ('All files', '*')]
        appfilename=tkFileDialog.asksaveasfilename(filetypes=filetypes)
        if not appfilename:
            return
        with open(appfilename, 'wb') as self.appfile:
            self.root.title("Configurer 1.0 - "+appfilename)
            fieldnames= ['x','y','width','height','num_cell','type','direction','tag','imid','space']
            writer=csv.DictWriter(self.appfile,fieldnames=fieldnames)
            writer.writerow({'x':'x','y':'y','width':'width','height':'height','num_cell':'num_cell','type':'type','direction':'direction','tag':'tag','imid':'imid','space':'space'})
            ordered=sorted(self.fields.iteritems())
            for key,field in ordered:
                writer.writerow(field)
            self.appfile.close()

    def cancel_field(self):
        """
        Cancela a criação de um novo campo
        """
        if self.objeto!=self.imageid:
            self.canvas.itemconfigure('region', outline='black')
            self.canvas.delete(self.objeto)
            self.canvas.delete(self.tagobject)
            self.top.destroy()
            self.top=None

    def save_field(self):
        """
        Salva o campo a ser utilizado.
        """
        try:
            self.field['direction']=self.listdirection['value']
            self.field['type']=self.listtype['value']
            self.field['num_cell']=int(self.listnumber.get())
            self.field['width']=int(self.cellwidth.get())
            self.field['height']=int(self.cellheight.get())
            self.field['space']=int(self.space.get())
            self.field['imid']=int(self.imidvar.get())
            if self.field['direction']=='vertical':
                self.canvas.coords(self.objeto,(float(self.field['x']), float(self.field['y']), float(self.field['x'])+self.field['width'], float(self.field['y'])+self.field['space']*self.field['num_cell']+self.field['height']*self.field['num_cell']))
            else:
                self.canvas.coords(self.objeto,(float(self.field['x']), float(self.field['y']), float(self.field['x'])+self.field['width']*self.field['num_cell']+self.field['space']*self.field['num_cell'], float(self.field['y'])+self.field['height']))
            self.tags[self.objeto]={'id': self.tagobject,'value':self.tag}
            self.field['tag']=self.tags[self.objeto]['value']
            self.fields[self.objeto]=copy(self.field)
            self.tag=len(self.tags)
            self.top.destroy()
        except Exception as inst:
            print type(inst)     # the exception instance
            print inst.args      # arguments stored in .args
            print inst
            tkMessageBox.showerror("Erro", "Por favor, forneça dados válidos")

    def update_item(self,event):
        """
        Atualiza a localização do campo selecionado.
        @param event Event: evento do mouse
        """
        if self.objeto and self.objeto!=self.imageid and 'tag' not in self.canvas.gettags(self.objeto):
            self.fields[self.objeto]['x'],self.fields[self.objeto]['y']=self.canvas.coords(self.objeto)[0],self.canvas.coords(self.objeto)[1]

    def open_conf_dialog(self,num_cell=0,direction='vertical',type='num',cellwidth='0',cellheight='0',space='0'):
        """
        Abre o diálogo de configuração do campo selecionado
        @param num_cell int : quantidade de células do campo
        @param direction string: direção do campo (vertical ou horizontal)
        @param type string: tipo do campo (num ou char)
        @param cellwidth string: largura da célula do campo em pixels
        @param cellheight string: altura da célula do campo em pixels
        @param space string: espaçamento entre células em pixels
        """
        self.top=Toplevel(self.root)
        self.top.title('Configurar campo')
        self.top.protocol("WM_DELETE_WINDOW", self.cancel_field)

        self.imidbox= Checkbutton(self.top,text="Identificador",variable=self.imidvar)
        self.imidbox.pack()

        Label(self.top,text='Número de células:').pack()
        self.listnumber= Entry(self.top)
        self.listnumber.insert(0,num_cell)
        self.listnumber.pack()

        Label(self.top,text='Direção:').pack()
        self.listdirection=  Tix.ComboBox(self.top,selectmode=SINGLE)
        self.listdirection.pack()
        self.listdirection.insert(END,'horizontal')
        self.listdirection.insert(END,'vertical')
        self.listdirection['value']=direction

        Label(self.top,text='Tipo:').pack()
        self.listtype= Tix.ComboBox(self.top,selectmode=SINGLE)
        self.listtype.pack()
        self.listtype.insert(END,'num')
        self.listtype.insert(END,'char')
        self.listtype['value']=type

        Label(self.top,text='Largura da célula (px):').pack()
        self.cellwidth=Entry(self.top)
        self.cellwidth.pack()
        self.cellwidth.insert(0,cellwidth)        

        Label(self.top,text='Altura da célula (px):').pack()
        self.cellheight=Entry(self.top)
        self.cellheight.pack()
        self.cellheight.insert(0,cellheight)

        Label(self.top,text='Espaçamento (px):').pack()
        self.space=Entry(self.top)
        self.space.pack()
        self.space.insert(0,space)

        Button(self.top,text="OK",command=self.save_field).pack()
        if num_cell==0:
            Button(self.top,text="Cancelar",command=self.cancel_field).pack()
        else:
            Button(self.top,text="Cancelar",command=self.top.destroy).pack()

if __name__ == "__main__":
    conf=Configurer()
    conf.main()

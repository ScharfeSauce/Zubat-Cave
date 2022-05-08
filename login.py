import tkinter as tk
from tkinter import *

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.name = ""
        # Grid mit Ressourcen aufbauen
        Label(master, text="Please enter your playername, and klick the verify button.").grid(row=0, column=1)

        self.entryName = Entry(master)

        self.entryName.grid(row=2, column=1)

        # Initialisierung mit Texten
        self.entryName.insert(END, "")
        # Events/Methoden mit Buttons verbinden
        self.btnPlay = Button(master, text='Begin', command=root.destroy).grid(row=4, column=2, sticky=W, pady=4)
        self.btnEnter = Button(master, text='Verify', command=self.enter).grid(row=4, column=0, sticky=W, pady=4)

        
    def enter(self):
        self.name = self.entryName.get()
        print(self.name)
        self.entryName.delete(0,'end')

######################################################################



root = tk.Tk()
#app = Application(master=root)
#app.mainloop()
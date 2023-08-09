from tkinter import *
from objects.interface import Interface

window = Tk()
ui = Interface(window)
ui.mainloop()
ui.destroy()
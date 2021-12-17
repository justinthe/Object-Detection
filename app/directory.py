from tkinter import *
from tkinter import ttk
from tkinter import filedialog
win= Tk()
    #Define the geometry
win.geometry("250x250")
    #Create a label and a Button to Open the dialog
path= filedialog.askdirectory(title="Select a Folder")
# path2= filedialog.askdirectory(title="Select a Folder")
print(path)
win.destroy()
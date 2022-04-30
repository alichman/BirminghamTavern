from tkinter import *
import PyPDF2
from PIL import Image, ImageTk, ImageOps, ImageEnhance


window = Tk()
can = Canvas(window, width=600, height=300)
can.grid(columnspan = 3)

img = Image.open("images/college_1.png")
blackout = ImageEnhance.Color(img)

logo = ImageTk.PhotoImage(img)
label = Label(image=logo)
label.image = logo
label.grid(column=0,row=0)

stuff = Label(window, text="Ooga Booga")
stuff.grid(columnspan=3, column=0, row=1)

thing = StringVar()
btn = Button(window, textvariable=thing)

window.mainloop()
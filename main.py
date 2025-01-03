from tkinter import *
from tkinter.ttk import *
from temperature import *
from tkinter import messagebox

root = Tk()
root.title('temperature converter')
root.geometry('640x480')

source_temperature = Entry(root)
source_temperature.grid(row=1,column=1)
dest_temperature = Entry(root)
dest_temperature.grid(row=2,column=1)

temperature_units = [i.upper() for i in Temperature.units()]
combo_units_source = Combobox(values = temperature_units)
combo_units_source.set('C')
combo_units_source.grid(row=1,column=2)

combo_units_dest = Combobox(values = temperature_units)
combo_units_dest.set('F')
combo_units_dest.grid(row=2,column=2)

def converting():
    result = Temperature.convert(
                                  value = source_temperature.get(),
                                  source_unit = combo_units_source.get(),
                                  dest_unit = combo_units_dest.get()
                                )
    dest_temperature.delete(0,END)
    dest_temperature.insert(0,str(result))

btn = Button(root,text='converting',command=converting)
btn.grid(row=1,column=3)

root.mainloop()
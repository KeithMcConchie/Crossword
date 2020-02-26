import tkinter as tk
from cw20190520across import across_clues

master = tk.Tk()

listbox = tk.Listbox(master)
listbox.pack()
listbox.config(width=0,height=0)
#listbox.insert(tk.END, "a list entry")

for key, clue in across_clues.items():
    listbox.insert(tk.END, str(key) + ": " + clue)

master.mainloop()
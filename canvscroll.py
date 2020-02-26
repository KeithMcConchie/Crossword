import tkinter as tk
from tkinter.font import Font
from cw20190517across import across_clues
from cw20190517down import down_clues

root=tk.Tk()


list_frame=tk.Frame(root,width=300,height=300)
list_frame.grid(row=0,column=0)
list_label = tk.Label(list_frame, text="DOWN", fg="black", anchor="w")
list_label.pack(side=tk.TOP, fill=tk.X)

list_canvas=tk.Canvas(list_frame,bg='#FFFFFF',width=300,height=300,scrollregion=(0,0,500,500))
# hbar=tk.Scrollbar(list_frame,orient=tk.HORIZONTAL)
# hbar.pack(side=tk.BOTTOM,fill=tk.X)
# hbar.config(command=list_canvas.xview)
vbar=tk.Scrollbar(list_frame,orient=tk.VERTICAL)
vbar.pack(side=tk.RIGHT,fill=tk.Y)
vbar.config(command=list_canvas.yview)
list_canvas.config(width=240,height=300, yscrollcommand=vbar.set)
#list_canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
list_canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

# Arial
# Helvetica
# Courier New (Courier)
# Comic Sans MS
# Fixedsys-
# MS Sans Serif
# MS Serif
# Symbol
# System
# Times New Roman (Times)
# Verdana
# Purisa
bfont = Font(family="Arial", size=10, weight="bold")
rfont = Font(family="Arial", size=10)
keylist = sorted(list(down_clues.items()))
# keylist.sort()
# print(down_clues)
# print("*******")

# print(down_clues.items())

# Because our list is fixed in width
# the x coords are going to be constant
clue_rect_left_x = 0 
clue_rect_right_x = 240 # total width of the clue rectangle
# default clue rectangle height: this will change 
# after we figure out how tall the clue will actually be
# we will add the 
clue_rect_default_height = 75

x_pad = 20 # the amount to pad before starting the clue number
x_num_pad = 5 # the amount to pad between the clue number and the clue
y_pad = 5 # the amount to pad (top and bottom) between the end 
# of the clue box and the bounding box of the clue text

clue_rect_top_y = 0 # zero to start.  bottom_y + 1 in the loop
for key, value in down_clues.items():
    print(key, value)

    clue_number = key
    clue_text = value
    clue_text_length = rfont.measure(clue_text)
    clue_num_length = rfont.measure(clue_number)
    clue_text_height = rfont.metrics("linespace")
# print("clue_text_length:", clue_text_length)
# col_left_x, row_top_y, col_right_x, row_bot_y

# clue_rect_bottom_y = clue_rect_top_y + clue_rect_default_height 
# clue_text_line_len = clue_right_x - (clue_left_x + (x_pad*2) + clue_num_length + x_num_pad + clue_top_y + y_pad)

# cr = list_canvas.create_rectangle(clue_left_x, clue_top_y, clue_right_x, clue_bottom_y, fill="light grey")
# cn = list_canvas.create_text(clue_left_x + x_pad, clue_top_y + y_pad, text=clue_number, font=bfont, anchor = "nw")
# ct = list_canvas.create_text(clue_left_x + x_pad + clue_num_length + x_num_pad, clue_top_y + y_pad, text=clue_text, font=rfont, anchor = "nw", width=clue_text_line_len)
# bb = list_canvas.bbox(ct)
# x0, y0, x1, y1 = list_canvas.coords(cr)
# y1 = bb[3] + y_pad
# list_canvas.coords(cr, x0, y0, x1, y1)
# clue_rect_top_y = clue_rect_bottom_y + 1
# if key == 1: break

# print(bb)
root.mainloop()

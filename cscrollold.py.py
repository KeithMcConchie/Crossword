import tkinter as tk
from tkinter.font import Font
from cw20190517across import across_clues
from cw20190517down import down_clues

class ClueListBox(tk.Frame):
    def __init__(self, parent, clue_direction, clue_list, clue_list_box_height, **kwargs):
        super().__init__(parent, **kwargs)
        self.clue_direction = clue_direction

        self.list_label = tk.Label(self, text=self.clue_direction, fg="black", bg="white", anchor="w")
        self.list_label.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.list_canvas=tk.Canvas(self, bg='#FFFFFF', width=240, height=clue_list_box_height, scrollregion=(0,0,240,1500))
        #vbar=tk.Scrollbar(self, orient=tk.VERTICAL)
        vbar=tk.Scrollbar(self, orient=tk.VERTICAL, bg="white")
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=self.list_canvas.yview)
        self.list_canvas.config(yscrollcommand=vbar.set)
        # list_canvas.config(width=240,height=300, yscrollcommand=vbar.set)
        self.list_canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        ##yscrollincrement - increment for vertical scrolling, in pixels,
        ##millimeters '2m', centimeters '2c', or inches '2i'

        bfont = Font(family="Arial", size=10, weight="bold")
        rfont = Font(family="Arial", size=10)

        # Because our list is fixed in width
        # the x coords are going to be constant
        clue_rect_left_x = 0 
        clue_rect_right_x = 240 # total width of the clue rectangle

        # default clue rectangle height: this will change 
        # after we figure out how tall the clue will actually be.
        clue_rect_default_height = 75

        x_pad = 30 # the amount to pad before starting the clue number
        x_num_pad = 5 # the amount to pad between the clue number and the clue
        y_pad = 5 # the amount to pad (top and bottom) between the end 
        # of the clue box and the bounding box of the clue text

        clue_rect_top_y = 0 # zero to start.  bottom_y + 1 in the loop


        for clue_number, clue_text in clue_list:

            clue_num_length = rfont.measure(clue_number)

            clue_rect_bottom_y = clue_rect_top_y + clue_rect_default_height 
            clue_text_line_len = clue_rect_right_x - ((x_pad*2) + clue_num_length + x_num_pad)

            clue_num_left_x = clue_rect_left_x + (x_pad - clue_num_length)
            clue_num_top_y = clue_rect_top_y + y_pad
            clue_text_left_x = clue_num_left_x + clue_num_length + x_num_pad
            clue_text_top_y = clue_rect_top_y + y_pad
            clue_tag = self.clue_direction[0] + str(clue_number).zfill(3)
            cr = self.list_canvas.create_rectangle(clue_rect_left_x, clue_rect_top_y, 
                    clue_rect_right_x, clue_rect_bottom_y, fill="white", tags=clue_tag)
            cn = self.list_canvas.create_text(clue_num_left_x, clue_num_top_y, text=clue_number, 
                    font=bfont, anchor = "nw", tags=clue_tag)
            ct = self.list_canvas.create_text(clue_text_left_x, clue_text_top_y, 
                    text=clue_text, font=rfont, anchor = "nw", width=clue_text_line_len, tags=clue_tag)
            bb = self.list_canvas.bbox(ct)
            x0, y0, x1, y1 = self.list_canvas.coords(cr)
            y1 = bb[3] + y_pad
            self.list_canvas.coords(cr, x0, y0, x1, y1)
            clue_rect_top_y = y1
            self.list_canvas.itemconfig(cr, outline="white")

        self.list_canvas.configure(scrollregion = self.list_canvas.bbox("all"), yscrollincrement=0)
        # clue_tag = self.clue_direction[0] + str(last_selected_item).zfill(3)
        self.last_clue_tag = clue_tag
        self.set_clue_bg(clue_tag, "grey")

        ##yscrollincrement - increment for vertical scrolling, in pixels,
        ##millimeters '2m', centimeters '2c', or inches '2i'
        # list_canvas.yview_scroll(500, "units")
        #list_canvas.yview_moveto(1)
        self.list_canvas.bind('<Button-1>', self.on_click)

    def on_click(self, event=None):
        can_x = self.list_canvas.canvasx(event.x)
        can_y = self.list_canvas.canvasy(event.y)
        clicked_item = self.list_canvas.find_closest(can_x, can_y)[0]
        tags = self.list_canvas.gettags(clicked_item)
        for tag in tags:
            if tag[0] == self.clue_direction[0]:
                clue_tag = tag
                break
        self.set_clue_bg(self.last_clue_tag, "white")
        self.set_clue_bg(clue_tag, "grey")
        print(self.clue_direction, can_x, can_y, clicked_item, 
            tags)

    def set_clue_bg(self, clue_tag, clue_bg):
        
        clue_canvas_items = self.list_canvas.find_withtag(clue_tag)
        for item in clue_canvas_items:
            if self.list_canvas.type(item) == 'rectangle':
                rect_item = item
                break
        self.list_canvas.itemconfig(rect_item, fill=clue_bg)
        # rect_item



root=tk.Tk()
root.geometry("800x480")
root.config(bg="blue")
across_clue_list = list(sorted(across_clues.items()))
acl = ClueListBox(root, "ACROSS", across_clue_list, 300)
acl.pack(side=tk.LEFT, anchor="nw")

down_clue_list = list(sorted(down_clues.items()))
dcl = ClueListBox(root, "DOWN", down_clue_list, 300)
dcl.pack(side=tk.LEFT, anchor="nw")
# list_frame=tk.Frame(root, bg="yellow", width=240, height=300)

root.mainloop()


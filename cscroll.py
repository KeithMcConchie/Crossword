import tkinter as tk
from tkinter.font import Font
from cw20190517across import across_clues
from cw20190517down import down_clues

class ClueListBox(tk.Frame):
    def __init__(self, parent, clue_direction, clue_list, clue_list_box_height, **kwargs):
        super().__init__(parent, **kwargs)
        self.clue_direction = clue_direction

        self.list_label = tk.Label(self, text=self.clue_direction, fg="black", bg="white", anchor="w")
        self.list_canvas=tk.Canvas(self, bg='#FFFFFF', width=240, height=clue_list_box_height, scrollregion=(0,0,240,1500))

        self.vbar=tk.Scrollbar(self, orient=tk.VERTICAL, bg="white")
        self.vbar.config(command=self.list_canvas.yview)
        self.list_canvas.config(yscrollcommand=self.vbar.set)

        self.list_label.pack(side=tk.TOP, fill=tk.X, expand=1)
        self.vbar.pack(side=tk.RIGHT,fill=tk.Y)
        self.list_canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

        # These might be constants but they could be configurable in the 
        # future. It seems like that might be a big pain for little benefit.
        self.bfont = Font(family="Arial", size=10, weight="bold")
        self.rfont = Font(family="Arial", size=10)
        self.clue_rect_width = 240 # total width of the clue rectangle
        self.x_pad = 30 # the amount to pad before starting the clue number
        self.x_num_pad = 5 # the amount to pad between the clue number and the clue
        self.y_pad = 5 # the amount to pad (top and bottom) between the end 
        # of the clue box and the bounding box of the clue text

        # Because our list is fixed in width
        # the x coords are going to be constant
        clue_rect_left_x = 0 
        clue_rect_right_x = self.clue_rect_width 

        # default clue rectangle height: this will change 
        # after we figure out how tall the clue will actually be.
        self.clue_rect_default_height = 75

        clue_rect_top_y = 0 
        for clue_number, clue_text in clue_list:
            clue_num_length = self.rfont.measure(clue_number)

            clue_rect_bottom_y = clue_rect_top_y + self.clue_rect_default_height 
            clue_text_line_len = clue_rect_right_x - ((self.x_pad*2) + clue_num_length + self.x_num_pad)

            clue_num_left_x = clue_rect_left_x + (self.x_pad - clue_num_length)
            clue_num_top_y = clue_rect_top_y + self.y_pad
            clue_text_left_x = clue_num_left_x + clue_num_length + self.x_num_pad
            clue_text_top_y = clue_rect_top_y + self.y_pad
            clue_tag = self.clue_direction[0] + str(clue_number).zfill(3)
            cr = self.list_canvas.create_rectangle(clue_rect_left_x, clue_rect_top_y, 
                    clue_rect_right_x, clue_rect_bottom_y, fill="white", tags=clue_tag)
            cn = self.list_canvas.create_text(clue_num_left_x, clue_num_top_y, text=clue_number, 
                    font=self.bfont, anchor = "nw", tags=clue_tag)
            ct = self.list_canvas.create_text(clue_text_left_x, clue_text_top_y, 
                    text=clue_text, font=self.rfont, anchor = "nw", width=clue_text_line_len, tags=clue_tag)
            bb = self.list_canvas.bbox(ct)
            x0, y0, x1, y1 = self.list_canvas.coords(cr)
            y1 = bb[3] + self.y_pad
            self.list_canvas.coords(cr, x0, y0, x1, y1)
            clue_rect_top_y = y1
            self.list_canvas.itemconfig(cr, outline="white")

        self.list_canvas.configure(scrollregion = self.list_canvas.bbox("all"), yscrollincrement=0)
        self.current_clue_tag = self.clue_direction[0] + str(1).zfill(3)
        self.last_clue_tag = self.current_clue_tag
        self.set_clue_bg(self.current_clue_tag, "grey")

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
                self.last_clue_tag = self.current_clue_tag
                self.current_clue_tag = tag
                break
        self.set_clue_bg(self.last_clue_tag, "white")
        self.set_clue_bg(self.current_clue_tag, "grey")
        print(self.clue_direction, can_x, can_y, clicked_item, 
            tags)

    def set_clue_bg(self, clue_tag, clue_bg):
        
        clue_canvas_items = self.list_canvas.find_withtag(clue_tag)
        for item in clue_canvas_items:
            if self.list_canvas.type(item) == 'rectangle':
                rect_item = item
                break
        self.list_canvas.itemconfig(rect_item, fill=clue_bg)



if __name__ == '__main__':
    root=tk.Tk()
    root.geometry("800x480")
    root.config(bg="blue")
    
    across_clue_list = list(sorted(across_clues.items()))
    acl = ClueListBox(root, "ACROSS", across_clue_list, 300)
    acl.pack(side=tk.LEFT, anchor="nw")

    down_clue_list = list(sorted(down_clues.items()))
    dcl = ClueListBox(root, "DOWN", down_clue_list, 300)
    dcl.pack(side=tk.LEFT, anchor="nw")
 
    root.mainloop()


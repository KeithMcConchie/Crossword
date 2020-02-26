import tkinter as tk 
from enum import Enum
# from cw20190516gridl import gridLO
# from cw20190516gridl2 import gridLO2
# from cw20190516across import across_clues
# from cw20190516down import down_clues
# from cw20190517gridl import gridLO
# from cw20190517gridl2 import gridLO2
# from cw20190518gridl import gridLO
# from cw20190518gridl2 import gridLO2
from cw20190520gridl import gridLO
from cw20190520gridl2 import gridLO2
# from cw20190523gridl import gridLO
# from cw20190523gridl2 import gridLO2
# from cw20190525gridl import gridLO
# from cw20190525gridl2 import gridLO2

win = tk.Tk()
class Direction(Enum):
    ACROSS = 1
    DOWN = 2
class Mode(Enum):
    USER = 1
    SOLUTION = 2
class GridIndex:
    def __init__(self, row=0, col=0):
        self.row = row
        self.col = col
    def __eq__(self, other): 
        if not isinstance(other, GridIndex):
            # don't attempt to compare against unrelated types
            return NotImplemented
        return self.row == other.row and self.col == other.col
class CanvasGridSquareCoordinates:
    def __init__(self, col_left_x, row_top_y, col_right_x, row_bot_y):
        self.col_left_x = col_left_x
        self.row_top_y = row_top_y
        self.col_right_x = col_right_x
        self.row_bot_y = row_bot_y
class CanvasGridSquare:
    def __init__(self, canvas_item, canvas_coords):
        self.blackout = False
        self.number = None
        self.letter = None
        self.user_letter = None
        self.canvas_item = canvas_item
        self.canvas_coords = canvas_coords
        self.canvas_letter = None
        self.across_key = None
        self.down_key = None
def fonts():
    pass
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

class DisplayPuzzle:
    def __init__(self, square_size=30, start_x=5, start_y=5, num_row_squares=5, num_col_squares=5):
        # need to look at global win (should there be local ref?)

        # These member vars describe the grid: size of squares; how many rows, cols;
        # starting point on the canvas.  
        # kdm: think about adding canvas width & height
        self.square_size = square_size
        self.start_x = start_x
        self.start_y = start_y
        self.num_row_squares = num_row_squares
        self.num_col_squares = num_col_squares

        # These are square and grid colors
        # kdm: probably will want to add writing colors.  Write now everything is
        # written in black.
        self.select_color = "blue"
        self.select_word_color = "yellow"
        self.blackout_square_color = "black"
        self.grid_color = "white"

        # these determine how letter and number font size and placement within square            
        self.letter_x_offset = 15
        self.letter_y_offset = 20
        #n, ne, e, se, s, sw, w, nw, or center
        self.letter_anchor = "center"
        self.letter_font =  ('Fixedsys', 16)
        self.number_x_offset = 2
        self.number_y_offset = 2
        self.number_anchor = "nw"
        self.number_font =  ('Fixedsys', 5)

        self.grid_canvas = tk.Canvas(win, width=1000, height=600, bg=self.grid_color)
        self.grid_canvas.pack()
        
        # we will be getting rid of this eventually.  Its 
        # purpose is to display data about keypresses and 
        # mouse clicks. For now it needs to be member vars
        self.sv = tk.StringVar()
        self.lab = tk.Label(win, textvar=self.sv)
        self.sv.set("Press a key")
        self.lab.pack(side=tk.BOTTOM)

        # self.grid is a two-dimensional list that holds a collection of
        # CanvasGridSquares that hold all the inforrmation aboutt what is 
        # drawn on the canvas.  
        self.grid = []
        # build self.grid based on puzzle dimensions 
        self.build_grid()
        # load it with puzzle data.  This will be converted to a 
        # DB load
        self.load_data()

        # Navigation Data
        # this will hold a dictionary with clue keys (A001 for one across)
        # and grid indexes and grid letters of the words as data
        # kdm this only really needs to be generated at puzzle creation time
        # so it could be held as data
        self.word_dict = {}
        # This is a specialized word list used only for navigation by the
        # up and down arrows.  Rather than going to the next/prev clue in 
        # the down clue list they move to the prev/next word above/below 
        # and wrap first/last last/first columns.  The way I populate
        # the word_dict gives us the down clues in the correct order so
        # I use it to populate the arrow_word_list
        self.arrow_word_list = []
        self.build_word_dict()
        # this will hold a list of clue keys in tab order.  Tabbing simply 
        # involves moving to the next prev item in the list and using the
        # dictionary to get the squares involved.
        self.word_list = []
        self.build_word_list()        

        # Navigation bindings
        self.grid_canvas.bind('<Button-1>', self.on_click)
        win.bind('<Key>', self.on_key)
        self.curr_square = None
        self.direction = Direction.ACROSS
        self.curr_ti = 0
        self.curr_key = self.word_list[self.curr_ti]
        self.curr_gi_list = self.word_dict[self.curr_key][0]
        self.curr_letter_list = self.word_dict[self.curr_key][1]
        self.curr_letter_index = 0

        print(self.curr_ti)
        print(self.curr_key)
        for gi in self.curr_gi_list:
            print(gi.row, gi.col)
        print(self.curr_letter_list)

        old_key = self.word_list[0]
        new_key = self.word_list[1]

        # print(self.word_dict[old_key][0][0].row, self.word_dict[old_key][0][0].col)
        #self.change_active_word(None, old_key)
        self.change_active_word(self.curr_key)
        self.change_active_square(self.curr_letter_index)
        #self.change_active_word(old_key, new_key)
        #self.display_mode = Mode.USER
        self.display_mode = Mode.SOLUTION

    def build_grid_square(self, gi):
        cgs = self.grid[gi.row][gi.col]
        if cgs.blackout:
            self.display_bg(cgs, self.blackout_square_color)
        else:
            self.display_bg(cgs, self.grid_color)
        if cgs.number:
            self.display_number(cgs)

    def build_grid(self):
        #build the physical grid based on canvas size, number of squares, square size, starting x/y on canvas    
        row_top_y = self.start_y
        row_bot_y = self.start_y + self.square_size
        # using indexes (ri, ci) and insert gets rid of linting problem
    
        for ri in range(self.num_row_squares):
            row = []
            col_left_x = self.start_x
            col_right_x = col_left_x + self.square_size
            for ci in range(self.num_col_squares):
                canvas_item = self.grid_canvas.create_rectangle(col_left_x, row_top_y, col_right_x, row_bot_y)
                canvas_coords = CanvasGridSquareCoordinates(col_left_x, row_top_y, col_right_x, row_bot_y) 
                cgs = CanvasGridSquare(canvas_item, canvas_coords)
                row.insert(ci, cgs)
                col_left_x = col_right_x
                col_right_x += self.square_size
            self.grid.insert(ri, row)
            row_top_y = row_bot_y
            row_bot_y += self.square_size

    def load_data(self):
        #load numbers and blackout squares based on test data
        #this will be replaced by a database load
        #don't currently have letter data for this test puzzle.
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                cgs = self.grid[row][col]
                if gridLO[row][col] == "@":
                    cgs.blackout = True
                    self.display_bg(cgs, self.blackout_square_color)
                elif gridLO[row][col] == "":
                    pass
                else:
                    cgs.number = int(gridLO[row][col])
                    self.display_number(cgs)
                if gridLO2[row][col] != "@":
                    cgs.letter = gridLO2[row][col]



    def display_number(self, cgs):
        self.grid_canvas.create_text(cgs.canvas_coords.col_left_x + self.number_x_offset, 
                                    cgs.canvas_coords.row_top_y + self.number_y_offset, 
                                    text=cgs.number, anchor=self.number_anchor, 
                                    font=self.number_font)
    def display_letter(self, cgs):
        if cgs.canvas_letter is not None:
            self.grid_canvas.delete(cgs.canvas_letter)
            cgs.canvas_letter = None
        cgs.canvas_letter = self.grid_canvas.create_text(cgs.canvas_coords.col_left_x + self.letter_x_offset, 
                                    cgs.canvas_coords.row_top_y + self.letter_y_offset, 
                                    text=cgs.letter, anchor=self.letter_anchor, 
                                    font=self.letter_font)
    def display_user_letter(self, cgs):
        if cgs.canvas_letter is not None:
            self.grid_canvas.delete(cgs.canvas_letter)
            cgs.canvas_letter = None
        cgs.canvas_letter = self.grid_canvas.create_text(cgs.canvas_coords.col_left_x + self.letter_x_offset, 
                                    cgs.canvas_coords.row_top_y + self.letter_y_offset, 
                                    text=cgs.user_letter, anchor=self.letter_anchor, 
                                    font=self.letter_font)
    def display_bg(self, cgs, bg_color):
        self.grid_canvas.itemconfig(cgs.canvas_item, fill=bg_color)
    
    def build_word_dict(self):
        for row in range(self.num_row_squares):
            in_word = False
            for col in range(self.num_col_squares):
                if self.grid[row][col].blackout:
                    if in_word: # (we already have a word)
                    #   store it
                        #print(key, word_letters, word_indexes) 
                        self.word_dict[key] = [word_indexes, word_letters]       
                        
                        in_word = False
                else: #(not blackout)
                    if not in_word:
                #        start a new word
                #           (get the key and instantiate a new list)
                        key = "A" + str(self.grid[row][col].number).zfill(3)
                        word_letters = []
                        word_indexes = []
                        in_word = True
                #       
                #   append letter
                    self.grid[row][col].across_key = key
                    word_letters.append(self.grid[row][col].letter)
                    word_indexes.append(GridIndex(row, col))
                    
                #
            else: # this is for the col for loop
                #store the last word
                #print(key, word_letters, word_indexes)
                self.word_dict[key] = [word_indexes, word_letters]

        self.arrow_word_list_start = 0
        self.arrow_word_list_end = 0
        for col in range(self.num_col_squares):
            in_word = False
            for row in range(self.num_row_squares):
                if self.grid[row][col].blackout:
                    if in_word: # (we already have a word)
                    #   store it
                        #print(key, word_letters, word_indexes) 
                        self.word_dict[key] = [word_indexes, word_letters]       
                        self.arrow_word_list.append(key)
                        self.arrow_word_list_end += 1                        
                        in_word = False
                else: #(not blackout)
                    if not in_word:
                #        start a new word
                #           (get the key and instantiate a new list)
                        key = "D" + str(self.grid[row][col].number).zfill(3)
                        word_letters = []
                        word_indexes = []
                        in_word = True
                #       
                #   append letter
                    self.grid[row][col].down_key = key
                    word_letters.append(self.grid[row][col].letter)
                    word_indexes.append(GridIndex(row, col))
                #
            else: # this is for the row for loop
                #store the last word
                #print(key, word_letters, word_indexes)
                self.word_dict[key] = [word_indexes, word_letters]
                self.arrow_word_list.append(key)
                self.arrow_word_list_end += 1
        for a in self.arrow_word_list:
            print(a)                        
        # for k, v in word_dict.items():
        #     print(k, v[1])
        #
    def build_word_list(self):
        ti = 0
        self.across_list_start = ti
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                key = "A" + str(self.grid[row][col].number).zfill(3)
                if key in self.word_dict:
                    self.word_list.append(key)
                    ti +=1

        self.across_list_end = ti - 1
        self.down_list_start = ti
        
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                key = "D" + str(self.grid[row][col].number).zfill(3)
                if key in self.word_dict:
                    self.word_list.append(key)
                    ti += 1
        self.down_list_end = ti - 1

    
        #kdm
    def change_active_square(self, new_li):
        old_gi = self.curr_gi_list[self.curr_letter_index]
        self.display_bg(self.grid[old_gi.row][old_gi.col], self.select_word_color)
        new_gi = self.curr_gi_list[new_li]
        self.display_bg(self.grid[new_gi.row][new_gi.col], self.select_color)

        # if old_gi is not None:
        #     if old_gi in self.word_dict[self.word_list[self.curr_ti]][0]:
        #         self.display_bg(self.grid[old_gi.row][old_gi.col], self.select_word_color)
        #     else:
        #         self.display_bg(self.grid[old_gi.row][old_gi.col], self.grid_color)
        # self.display_bg(self.grid[new_gi.row][new_gi.col], self.select_color)
    def change_active_word(self, new_key):
        # assumes self.curr_ti has been updated but curr_key, curr_gi_list, and 
        # curr_letter_list has not. Those will have the prev values and we can use
        # them to reset the old word.  In the case of the first time it will be the 
        # same value, before and after update.
        for gi in self.curr_gi_list:
            self.display_bg(self.grid[gi.row][gi.col], self.grid_color)
        self.curr_key = self.word_list[self.curr_ti]
        self.curr_gi_list = self.word_dict[self.curr_key][0]
        self.curr_letter_list = self.word_dict[self.curr_key][1]
        for gi in self.curr_gi_list:
            self.display_bg(self.grid[gi.row][gi.col], self.select_word_color)
    def on_click(self, event=None):
        # find the square we clicked on by iterating through the 
        # grid, comparing to see if the x/y coordinates fall within
        # that of a particular square
        # need to use indexes because ultimately when we find the
        # square we clicked on we will want to create a GridIndex object

        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                cgs = self.grid[row][col]
                if ((cgs.canvas_coords.col_left_x < event.x < cgs.canvas_coords.col_right_x) 
                    and (cgs.canvas_coords.row_top_y < event.y < cgs.canvas_coords.row_bot_y)):
                    sel_gi = GridIndex(row, col)
                    if cgs.blackout:
                        # if we clicked a blackout square ignore it
                        break
                    elif sel_gi == self.curr_gi:
                        # are we clicking on the active square?
                        # if so swap direction - is there a more elegant way??
                        # this should work need to swap and test
                        ## self.direction = Direction.ACROSS if self.direction == Direction.DOWN else direction.DOWN
                        if self.direction == Direction.ACROSS:
                            self.direction = Direction.DOWN
                        else:
                            self.direction = Direction.ACROSS
                        # need to change this to the new change_active_word
                        #self.set_active_word()
                    else:
                        # need to change curr_gi
                        # and curr word            
                        old_gi = self.curr_gi
                        self.curr_gi = GridIndex(row, col)
                        #self.refresh_grid_square(old_gi)
                        #self.refresh_grid_square(self.curr_gi)
                        if self.curr_gi not in self.curr_word:
                            pass
                            #self.set_active_word()
        #self.sv.set(str(event.x) + " " + str(event.y))
    def on_key(self, event=None):
        letter = event.char.upper()
        # print("letter=",letter)
        # print("keysym=", event.keysym)
        # #print("key", event.key)
        
        # gi = self.curr_gi
        if letter in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
            pass
            # self.grid[gi.row][gi.col].user_letter = letter
            #self.refresh_grid_square(gi)
            # self.display_user_letter(self.grid[gi.row][gi.col])
        elif (event.keysym == "ISO_Left_Tab"):
            #print("keysym=", event.keysym)
            self.prev_word(True)
            self.curr_letter_index = 0
            self.change_active_square(self.curr_letter_index)
        elif (event.keysym == "Tab"):
            #print("keysym=", event.keysym)
            self.next_word(True)
            self.curr_letter_index = 0
            self.change_active_square(self.curr_letter_index)
        elif (event.keysym == "Left") or (event.keysym == "KP_Left"):
            #print("keysym=", event.keysym)
            self.go_left()
        elif (event.keysym == "Right") or (event.keysym == "KP_Right"):
            #print("keysym=", event.keysym)
            self.go_right()
        elif (event.keysym == "Up") or (event.keysym == "KP_Up"):
            #print("keysym=", event.keysym)
            self.go_up()
        elif (event.keysym == "Down") or (event.keysym == "KP_Down"):       
            #print("keysym=", event.keysym)
            self.go_down()

        if self.direction == Direction.ACROSS:
            pass
        #self.sv.set(event.keysym)
        self.sv.set(self.direction)

    def prev_word(self, change_direction = True):
        self.curr_ti -= 1
        if change_direction:
            if self.direction == Direction.ACROSS:
                if self.curr_ti < self.across_list_start:
                    self.direction = Direction.DOWN
                    self.curr_ti = self.down_list_end 
            elif self.direction == Direction.DOWN:
                if self.curr_ti < self.down_list_start:
                    self.direction = Direction.ACROSS
                    self.curr_ti = self.across_list_end 
        else:
            if self.direction == Direction.ACROSS:
                if self.curr_ti < self.across_list_start:
                    self.curr_ti = self.across_list_end
            elif self.direction == Direction.DOWN:
                if self.curr_ti < self.down_list_start:
                    self.curr_ti = self.down_list_end
        new_key = self.word_list[self.curr_ti]
        self.change_active_word(new_key)
    def next_word(self, change_direction = True):
        self.curr_ti += 1
        if change_direction:
            if self.direction == Direction.ACROSS:
                if self.curr_ti > self.across_list_end:
                    self.direction = Direction.DOWN
                    self.curr_ti = self.down_list_start 
            elif self.direction == Direction.DOWN:
                if self.curr_ti > self.down_list_end:
                    self.direction = Direction.ACROSS
                    self.curr_ti = self.across_list_start 
        else:
            if self.direction == Direction.ACROSS:
                if self.curr_ti > self.across_list_end:
                    self.curr_ti = self.across_list_start 
            elif self.direction == Direction.DOWN:
                if self.curr_ti > self.down_list_end:
                    self.curr_ti = self.down_list_start 
        new_key = self.word_list[self.curr_ti]
        self.change_active_word(new_key)
    def next_down_arrow_word(self):
        curr_arrow_ti = self.arrow_word_list.index(self.curr_key)
        curr_arrow_ti += 1
        if self.curr_ti > self.arrow_word_list_end:
            self.curr_ti = self.arrow_word_list_start 
        new_key = self.word_list[curr_arrow_ti]
        self.change_active_word(new_key)
    def go_left(self):
        print("go_left")
        if self.direction == Direction.ACROSS:
            new_li = self.curr_letter_index - 1
            if new_li < 0:
                self.prev_word(False)
                self.curr_letter_index = len(self.curr_gi_list) - 1
                self.change_active_square(self.curr_letter_index)
            else:                
                self.change_active_square(new_li)
                self.curr_letter_index -= 1
    def go_right(self):
        print("go_right")
        if self.direction == Direction.ACROSS:
            new_li = self.curr_letter_index + 1
            if new_li >= len(self.curr_gi_list):
                self.next_word(False)
                self.curr_letter_index = 0
                self.change_active_square(self.curr_letter_index)
            else:                
                self.change_active_square(new_li)
                self.curr_letter_index += 1
    def go_up(self):
        print("go_up")
        if self.direction == Direction.DOWN:
            new_li = self.curr_letter_index - 1
            if new_li < 0:
                self.prev_word(False)
                self.curr_letter_index = len(self.curr_gi_list) - 1
                self.change_active_square(self.curr_letter_index)
            else:                
                self.change_active_square(new_li)
                self.curr_letter_index -= 1
    def go_down(self):
        print("go_down")
        if self.direction == Direction.DOWN:
            new_li = self.curr_letter_index + 1
            if new_li >= len(self.curr_gi_list):
                #self.next_down_arrow_word()
                self.next_word(False)
                self.curr_letter_index = 0
                self.change_active_square(self.curr_letter_index)
            else:                
                self.change_active_square(new_li)
                self.curr_letter_index += 1




puzzle = DisplayPuzzle(num_row_squares = 15, num_col_squares = 15)
win.mainloop()
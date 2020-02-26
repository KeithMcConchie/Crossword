import tkinter as tk 
from enum import Enum
from cscroll import ClueListBox

foo = 1

if foo == 1:
    from cw20190516gridl import gridLO
    from cw20190516gridl2 import gridLO2
    from cw20190516across import across_clues
    from cw20190516down import down_clues

if foo == 2:
    from cw20190517gridl import gridLO
    from cw20190517gridl2 import gridLO2
    from cw20190517across import across_clues
    from cw20190517down import down_clues

if foo == 3:
    from cw20190518gridl import gridLO
    from cw20190518gridl2 import gridLO2
    from cw20190518across import across_clues
    from cw20190518down import down_clues

if foo == 4:
    from cw20190520gridl import gridLO
    from cw20190520gridl2 import gridLO2
    from cw20190520across import across_clues
    from cw20190520down import down_clues

if foo == 5:
    from cw20190523gridl import gridLO
    from cw20190523gridl2 import gridLO2
    from cw20190523across import across_clues
    from cw20190523down import down_clues

if foo == 6:
    from cw20190525gridl import gridLO
    from cw20190525gridl2 import gridLO2
    from cw20190525across import across_clues
    from cw20190525down import down_clues

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

        cw_frame = tk.Frame(win)
        clue_frame = tk.Frame(win)
        across_frame = tk.Frame(clue_frame)
        down_frame = tk.Frame(clue_frame)
        cw_frame.pack(side=tk.LEFT, fill=tk.Y)
        across_frame.pack(side=tk.LEFT)
        down_frame.pack(side=tk.LEFT)
        clue_frame.pack(side=tk.LEFT, fill=tk.Y)
        canvas_width = (self.num_row_squares * self.square_size) + (self.start_x * 2)
        canvas_height = (self.num_col_squares * self.square_size) + (self.start_x * 2)
        self.grid_canvas = tk.Canvas(cw_frame, width=canvas_width, height=canvas_height, bg=self.grid_color)
        self.grid_canvas.pack(side=tk.TOP)
 
        across_clue_list = list(sorted(across_clues.items()))
        acl = ClueListBox(win, "ACROSS", across_clue_list, 300)
        acl.pack(side=tk.LEFT, anchor="nw")

        down_clue_list = list(sorted(down_clues.items()))
        dcl = ClueListBox(win, "DOWN", down_clue_list, 300)
        dcl.pack(side=tk.LEFT, anchor="nw")
 
        # self.grid is a two-dimensional list that holds a collection of
        # CanvasGridSquares that hold all the information aboutt what is 
        # drawn on the canvas.  
        self.grid = []
        # build self.grid based on puzzle dimensions 
        self.build_grid()
        # load it with puzzle data.  This will be converted to a 
        # DB load
        self.load_data()

        # Navigation Data
        # this will hold a dictionary with clue keys(A001 for one across)
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
        # across_lb.bind("<Up>", lambda e: "break")
        # across_lb.bind("<Down>", lambda e: "break")
        # down_lb.bind("<Up>", lambda e: "break")
        # down_lb.bind("<Down>", lambda e: "break")
        win.bind('<Key>', self.on_key)
   
        # with these for memvars I should be able to 
        # keep track of where I am at all times
        # The curr_key will tell me what word I'm in and allow
        # me access to the word_dict, word_list, and
        # arrow_word_list 
        self.direction = Direction.ACROSS
        self.curr_key = self.word_list[0]
        self.curr_word = self.word_dict[self.curr_key][0]
        self.curr_word_index = 0
        # create a toplevel menu
        menubar = tk.Menu(win)

        # think I need to initialize the above vars earlier so I can create this menu
        # when I create the rest of the screen.  Maybe I can use something like filemenu.config
        # so I can add the command= parameter later in the code

        # damn it! I ran into this problem before in another project.  It seems to be executing
        # the reveal_letter, reveal_word (the ones with parameters) on instantiation
        # maybe I need to create an object inheriting from the window, bind these to it it and 
        # send messages.  That seems like a path fraught with peril.  It's got potential to break
        # a lot of things.  Hope I remember what I'm talking about tomorrow, because I'm not inclined
        # to work on it right now.

        # Got it working.  It seems like you can't pass any parms.  I think it is simply a function
        # identifier, so it thinks the string following command= is the name of the function - parms 
        # and all.  At least that's my working theory.  For now that's how I'll treat it.  Probably 
        # need to clean up the functions, but I'll look at that tomorrow. 

        filemenu = tk.Menu(menubar, tearoff=0)
        # filemenu.add_command(label="Reveal Letter", command=self.reveal_letter(self.curr_word, self.curr_word_index))
        # filemenu.add_command(label="Reveal Word", command=self.reveal_word(self.curr_word))
        # filemenu.add_command(label="Reveal Puzzle", command=self.reveal_puzzle)
        filemenu.add_command(label="Reveal Letter", command=self.reveal_letter)
        filemenu.add_command(label="Reveal Word", command=self.reveal_word)
        filemenu.add_command(label="Reveal Puzzle", command=self.reveal_puzzle)
        menubar.add_cascade(label="Reveal", menu=filemenu)
        win.config(menu=menubar)

        # print(self.curr_key)
        # for gi in self.curr_word:
        #     print(gi.row, gi.col)

        
        self.change_word_color(self.curr_word, self.select_word_color)
        self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
    
    def reveal_letter(self):
        gi = self.curr_word[self.curr_word_index]
        cgs = self.grid[gi.row][gi.col]
        cgs.user_letter = cgs.letter
        self.display_user_letter(cgs)
    def reveal_word(self):
        for gi in self.curr_word:
            cgs = self.grid[gi.row][gi.col]
            cgs.user_letter = cgs.letter
            self.display_user_letter(cgs)
    def reveal_puzzle(self):
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                cgs = self.grid[row][col]
                cgs.user_letter = cgs.letter
                self.display_user_letter(cgs)

    def change_word_color(self, word, new_color):
        for gi in word:
            self.display_bg(self.grid[gi.row][gi.col], new_color)
    def change_word_square_color(self, word, word_index, new_color):
        gi = word[word_index]
        self.display_bg(self.grid[gi.row][gi.col], new_color)
        
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

    def delete_user_letter(self, cgs):
        cgs.user_letter = None
        if cgs.canvas_letter is not None:
            self.grid_canvas.delete(cgs.canvas_letter)
            cgs.canvas_letter = None
    
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
                        # print(key) 
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
                if in_word:
                    self.word_dict[key] = [word_indexes, word_letters]
                    self.arrow_word_list.append(key)
                    self.arrow_word_list_end += 1
        # print(self.arrow_word_list)        
        self.arrow_word_list_end -= 1    
        # for a in self.arrow_word_list:
        #     print(a)                        
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
                    elif sel_gi == self.curr_word[self.curr_word_index]:
                        # are we clicking on the active square?
                        self.change_word_color(self.curr_word, self.grid_color)
                        if self.direction == Direction.ACROSS:
                            self.direction = Direction.DOWN
                            self.curr_key = cgs.down_key
                        else:
                            self.direction = Direction.ACROSS
                            self.curr_key = cgs.across_key
                        self.curr_word = self.word_dict[self.curr_key][0]
                        self.curr_word_index = self.curr_word.index(sel_gi)
                        self.change_word_color(self.curr_word, self.select_word_color)
                        self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
                    elif sel_gi in (self.curr_word):
                        self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_word_color)
                        self.curr_word_index = self.curr_word.index(sel_gi)
                        self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
                    elif sel_gi not in (self.curr_word):
                        self.change_word_color(self.curr_word, self.grid_color)
                        if self.direction == Direction.ACROSS:
                            self.curr_key = cgs.across_key
                        elif self.direction == Direction.DOWN:
                            self.curr_key = cgs.down_key
                        self.curr_word = self.word_dict[self.curr_key][0]
                        self.curr_word_index = self.curr_word.index(sel_gi)
                        self.change_word_color(self.curr_word, self.select_word_color)
                        self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)

        #self.sv.set(str(event.x) + " " + str(event.y))
    def on_key(self, event=None):
        letter = event.char.upper()
        # print("letter=",letter)
        # print("keysym=", event.keysym)
        gi = self.curr_word[self.curr_word_index]
        # print(gi.row, gi.col)
        if letter in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
            # pass
            self.grid[gi.row][gi.col].user_letter = letter
            self.display_user_letter(self.grid[gi.row][gi.col])
            # print("curr_word_index", self.curr_word_index)
            ind = list(range(len(self.curr_word)))
            # print("ind", ind)
            for cwi in ind[self.curr_word_index+1:] + ind[:self.curr_word_index]:
                gi = self.curr_word[cwi]
                if self.grid[gi.row][gi.col].user_letter is None:
                    self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_word_color)
                    self.curr_word_index = cwi
                    self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
                    break

                # print("cwi", cwi)
        elif (event.keysym == "ISO_Left_Tab"):
            #print("keysym=", event.keysym)
            self.change_word_color(self.curr_word, self.grid_color)
            self.curr_key = self.prev_word(self.curr_key, True)
            self.curr_word = self.word_dict[self.curr_key][0]
            self.curr_word_index = 0
            self.change_word_color(self.curr_word, self.select_word_color)
            self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
        elif (event.keysym == "Tab"):
            #print("keysym=", event.keysym)
            self.change_word_color(self.curr_word, self.grid_color)
            self.curr_key = self.next_word(self.curr_key, True)
            self.curr_word = self.word_dict[self.curr_key][0]
            self.curr_word_index = 0
            self.change_word_color(self.curr_word, self.select_word_color)
            self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
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
        elif (event.keysym == "Delete"):       
            # print("keysym=", event.keysym)
            self.delete_user_letter(self.grid[gi.row][gi.col])
        elif (event.keysym == "BackSpace"):       
            # print("keysym=", event.keysym)
            self.delete_user_letter(self.grid[gi.row][gi.col])
            if self.curr_word_index > 0:
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_word_color)
                self.curr_word_index -= 1 
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
        if self.direction == Direction.ACROSS:
            pass
        #self.sv.set(event.keysym)
        #self.sv.set(self.direction)

    def prev_word(self, key, change_direction = True):
        curr_ti = self.word_list.index(key)
        curr_ti -= 1
        if change_direction:
            if self.direction == Direction.ACROSS:
                if curr_ti < self.across_list_start:
                    self.direction = Direction.DOWN
                    curr_ti = self.down_list_end 
            elif self.direction == Direction.DOWN:
                if curr_ti < self.down_list_start:
                    self.direction = Direction.ACROSS
                    curr_ti = self.across_list_end 
        else:
            if self.direction == Direction.ACROSS:
                if curr_ti < self.across_list_start:
                    curr_ti = self.across_list_end
            elif self.direction == Direction.DOWN:
                if curr_ti < self.down_list_start:
                    curr_ti = self.down_list_end
        return self.word_list[curr_ti]
    def next_word(self, key, change_direction = True):
        curr_ti = self.word_list.index(key)
        curr_ti += 1
        if change_direction:
            if self.direction == Direction.ACROSS:
                if curr_ti > self.across_list_end:
                    self.direction = Direction.DOWN
                    curr_ti = self.down_list_start 
            elif self.direction == Direction.DOWN:
                if curr_ti > self.down_list_end:
                    self.direction = Direction.ACROSS
                    curr_ti = self.across_list_start 
        else:
            if self.direction == Direction.ACROSS:
                if curr_ti > self.across_list_end:
                    curr_ti = self.across_list_start 
            elif self.direction == Direction.DOWN:
                if curr_ti > self.down_list_end:
                    curr_ti = self.down_list_start 
        return self.word_list[curr_ti]

    def prev_up_down_arrow_word(self, key):
        curr_arrow_ti = self.arrow_word_list.index(key)
        curr_arrow_ti -= 1
        if curr_arrow_ti < self.arrow_word_list_start:
            curr_arrow_ti = self.arrow_word_list_end 
        return self.arrow_word_list[curr_arrow_ti]
    def next_up_down_arrow_word(self, key):
        curr_arrow_ti = self.arrow_word_list.index(key)
        curr_arrow_ti += 1
        if curr_arrow_ti > self.arrow_word_list_end:
            curr_arrow_ti = self.arrow_word_list_start 
        return self.arrow_word_list[curr_arrow_ti]

    def go_left(self):
        # print("go_left")
        if self.direction == Direction.ACROSS:
            if self.curr_word_index == 0:    
                self.change_word_color(self.curr_word, self.grid_color)
                self.curr_key = self.prev_word(self.curr_key, False)
                self.curr_word = self.word_dict[self.curr_key][0]
                self.curr_word_index = len(self.curr_word) - 1
                self.change_word_color(self.curr_word, self.select_word_color)
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
            else:
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_word_color)
                self.curr_word_index -= 1
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
                
        elif self.direction == Direction.DOWN:
            sel_gi = self.curr_word[self.curr_word_index]
            cgs = self.grid[sel_gi.row][sel_gi.col]
            self.change_word_color(self.curr_word, self.grid_color)
            self.direction = Direction.ACROSS
            self.curr_key = cgs.across_key
            self.curr_word = self.word_dict[self.curr_key][0]
            self.curr_word_index = self.curr_word.index(sel_gi)
            self.change_word_color(self.curr_word, self.select_word_color)
            self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
    def go_right(self):
        # print("go_right")
        if self.direction == Direction.ACROSS:
            if self.curr_word_index == len(self.curr_word) - 1:    
                self.change_word_color(self.curr_word, self.grid_color)
                self.curr_key = self.next_word(self.curr_key, False)
                self.curr_word = self.word_dict[self.curr_key][0]
                self.curr_word_index = 0
                self.change_word_color(self.curr_word, self.select_word_color)
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
            else:
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_word_color)
                self.curr_word_index += 1
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
                
        elif self.direction == Direction.DOWN:
            sel_gi = self.curr_word[self.curr_word_index]
            cgs = self.grid[sel_gi.row][sel_gi.col]
            self.change_word_color(self.curr_word, self.grid_color)
            self.direction = Direction.ACROSS
            self.curr_key = cgs.across_key
            self.curr_word = self.word_dict[self.curr_key][0]
            self.curr_word_index = self.curr_word.index(sel_gi)
            self.change_word_color(self.curr_word, self.select_word_color)
            self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
    def go_up(self):
        # print("go_up")
        if self.direction == Direction.DOWN:
            if self.curr_word_index == 0:    
                self.change_word_color(self.curr_word, self.grid_color)
                self.curr_key = self.prev_up_down_arrow_word(self.curr_key)
                self.curr_word = self.word_dict[self.curr_key][0]
                self.curr_word_index = len(self.curr_word) - 1
                self.change_word_color(self.curr_word, self.select_word_color)
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
            else:
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_word_color)
                self.curr_word_index -= 1
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
                
        elif self.direction == Direction.ACROSS:
            sel_gi = self.curr_word[self.curr_word_index]
            cgs = self.grid[sel_gi.row][sel_gi.col]
            self.change_word_color(self.curr_word, self.grid_color)
            self.direction = Direction.DOWN
            self.curr_key = cgs.down_key
            self.curr_word = self.word_dict[self.curr_key][0]
            self.curr_word_index = self.curr_word.index(sel_gi)
            self.change_word_color(self.curr_word, self.select_word_color)
            self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
    def go_down(self):
        # print("go_down")
        if self.direction == Direction.DOWN:
            if self.curr_word_index == len(self.curr_word) - 1:    
                self.change_word_color(self.curr_word, self.grid_color)
                self.curr_key = self.next_up_down_arrow_word(self.curr_key)
                self.curr_word = self.word_dict[self.curr_key][0]
                self.curr_word_index = 0
                self.change_word_color(self.curr_word, self.select_word_color)
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
            else:
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_word_color)
                self.curr_word_index += 1
                self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)
                
        elif self.direction == Direction.ACROSS:
            sel_gi = self.curr_word[self.curr_word_index]
            cgs = self.grid[sel_gi.row][sel_gi.col]
            self.change_word_color(self.curr_word, self.grid_color)
            self.direction = Direction.DOWN
            self.curr_key = cgs.down_key
            self.curr_word = self.word_dict[self.curr_key][0]
            self.curr_word_index = self.curr_word.index(sel_gi)
            self.change_word_color(self.curr_word, self.select_word_color)
            self.change_word_square_color(self.curr_word, self.curr_word_index, self.select_color)

puzzle = DisplayPuzzle(num_row_squares = 15, num_col_squares = 15)
win.mainloop()
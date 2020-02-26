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
        self.square_size = square_size
        self.start_x = start_x
        self.start_y = start_y
        self.num_row_squares = num_row_squares
        self.num_col_squares = num_col_squares

        # need to look at global win (should there be local ref?)
        self.grid = []
        self.select_color = "blue"
        self.select_word_color = "yellow"
        self.null_square_color = "black"
        self.grid_color = "white"
                    
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
        self.current_active_square = None

        # we will be getting rid of this eventually but for now
        # it needs to be member vars
        self.sv = tk.StringVar()
        self.lab = tk.Label(win, textvar=self.sv)
        self.sv.set("Press a key")
        self.lab.pack(side=tk.BOTTOM)

        self.grid_canvas.bind('<Button-1>', self.on_click)
        win.bind('<Key>', self.on_key)

        self.build_grid()
        self.build_test2()
        self.direction = Direction.ACROSS
        self.display_mode = Mode.USER
        
        self.word_dict = {}
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
                    word_letters.append(self.grid[row][col].letter)
                    word_indexes.append(GridIndex(row, col))
                    
                #
            else: # this is for the col for loop
                #store the last word
                #print(key, word_letters, word_indexes)
                self.word_dict[key] = [word_indexes, word_letters]
        for col in range(self.num_col_squares):
            in_word = False
            for row in range(self.num_row_squares):
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
                        key = "D" + str(self.grid[row][col].number).zfill(3)
                        word_letters = []
                        word_indexes = []
                        in_word = True
                #       
                #   append letter
                    word_letters.append(self.grid[row][col].letter)
                    word_indexes.append(GridIndex(row, col))
                    
                #
            else: # this is for the col for loop
                #store the last word
                #print(key, word_letters, word_indexes)
                self.word_dict[key] = [word_indexes, word_letters]
        # for k, v in word_dict.items():
        #     print(k, v[1])
        #
        #kdm
        #kdm
        # need to look at swapping variables e.g. x,y = y,x
        # I will most likely need to implement assignment operator
        # in the concerned classes (I think maybe just GridIndex to start)

        #kdm
        #if I store the clue key e.g. "A001" in the grid it greatly 
        #simplifies updating the current word (reset background on 
        # old word, set background on new word)
        
        #if I store the index into the tab array I can link back into
        #the clue lists, either using an offset to get to the down 
        #clues or separating them into two lists
        
        # a single list keeps tabbing really simple 
    
        # next tab
        # store old key
        # increment key index
        # if >= length then 0
        # store new key
        # call change current word (old key, new key)
        # set active square (and background) to first index in word

        # prev tab
        # store old key
        # decrement key index
        # if < 0 then len - 1
        # store new key
        # call change current word (old key, new key)
        # set active square (and background) to first index in word

        # need next and prev grid squares 
        # needs to advance or reverse and wrap around based on the direction
        # traveling. Word does not change direction when it reaches the end or the
        # beginning of the gsrid so if word direction is down and current word is in
        # the last grid square and last down word, right arrow will take it to the
        # first grid square and the first down word, this might be an argument for
        # separating the across and down key lists but I think it might be more 
        # easily managed by just tracking the down list starting offset
        # now that I think of it, this isn't necessary, just wrap around from the last
        # grid square to the first.  self.directions value won't change, and we will 
        # move from an old word to a new word, just like when we tab/backtab or click
        # on a new square        
        # change current word (old key, new key)
        #   unset backgrounds to old key
        #   set backgrounds to to new key
        
        self.word_list = []
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                key = "A" + str(self.grid[row][col].number).zfill(3)
                if key in self.word_dict:
                    self.word_list.append(key)

        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                key = "D" + str(self.grid[row][col].number).zfill(3)
                if key in self.word_dict:
                    self.word_list.append(key)

        for e in self.word_list:
            print(e)
        
        self.current_active_gi = GridIndex(0, 1)
        self.current_active_word = []

        #self.set_active_word()
        # for e in self.current_active_word:
        #     print(e.row, e.col)       
        #self.current_active_word = [GridIndex(0, 0), GridIndex(0, 1), GridIndex(0, 2)]
        self.display_mode = Mode.SOLUTION
        self.reset_puzzle()


    def reset_puzzle(self):
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                self.refresh_grid_square(GridIndex(row, col))
                # if self.grid[row][col].blackout == True:
                #     self.display_bg(self.grid[row][col], "black")
                # else:
                #     self.display_number(self.grid[row][col])
    def refresh_grid_square(self, gi):
        cgs = self.grid[gi.row][gi.col]
        if cgs.canvas_letter is not None:
            self.grid_canvas.delete(cgs.canvas_letter)
        if cgs.blackout:
            self.display_bg(cgs, self.null_square_color)
        elif gi == self.current_active_gi:
            self.display_bg(cgs, self.select_color)
        elif gi in self.current_active_word:
            self.display_bg(cgs, self.select_word_color)
        else:
            self.display_bg(cgs, self.grid_color)
        
        if cgs.number:
            self.display_number(cgs)

        if self.display_mode == Mode.SOLUTION:
            self.display_letter(cgs)
        else:
            self.display_user_letter(cgs)
        
    def build_test(self):
        #generic test data that puts a square and a number in 
        #every square with blackout squares every 10th square
        #to be removed and not replaced
        number = 0
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                letter = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[number%26]
                number += 1
                if number % 10 == 0:
                    self.grid[row][col].blackout = True
                else:
                    self.grid[row][col].letter = letter
                    self.grid[row][col].number = number
                
    def build_test2(self):
        #load numbers and blackout squares based on test data
        #this will be replaced by a database load
        #don't currently have letter data for this test puzzle.
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                if gridLO[row][col] == "@":
                    self.grid[row][col].blackout = True
                elif gridLO[row][col] == "":
                    pass
                else:
                    self.grid[row][col].number = int(gridLO[row][col])

        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                if gridLO2[row][col] != "@":
                    self.grid[row][col].letter = gridLO2[row][col]

    def build_grid(self):
        #build the physical grid based on canvas size, number of squares, square size, starting x/y on canvas    
        row_top_y = self.start_y
        row_bot_y = self.start_y + self.square_size
        for row in range(self.num_row_squares):
            row = []
            col_left_x = self.start_x
            col_right_x = col_left_x + self.square_size
            for col in range(self.num_col_squares):
                #need to figure out how to iterate without tripping the linter
                #using col in range to count iterations lint doesn't like it cause
                #I'm not using the variable
                a = col 

                canvas_item = self.grid_canvas.create_rectangle(col_left_x, row_top_y, col_right_x, row_bot_y)
                canvas_coords = CanvasGridSquareCoordinates(col_left_x, row_top_y, col_right_x, row_bot_y) 
                cgs = CanvasGridSquare(canvas_item, canvas_coords)
                row.append((cgs))
                col_left_x = col_right_x
                col_right_x += self.square_size
            self.grid.append(row)
            row_top_y = row_bot_y
            row_bot_y += self.square_size

    def display_number(self, cgs):
        self.grid_canvas.create_text(cgs.canvas_coords.col_left_x + self.number_x_offset, 
                                    cgs.canvas_coords.row_top_y + self.number_y_offset, 
                                    text=cgs.number, anchor=self.number_anchor, 
                                    font=self.number_font)
    def display_letter(self, cgs):
        cgs.canvas_letter = self.grid_canvas.create_text(cgs.canvas_coords.col_left_x + self.letter_x_offset, 
                                    cgs.canvas_coords.row_top_y + self.letter_y_offset, 
                                    text=cgs.letter, anchor=self.letter_anchor, 
                                    font=self.letter_font)
    def display_user_letter(self, cgs):
        cgs.canvas_letter = self.grid_canvas.create_text(cgs.canvas_coords.col_left_x + self.letter_x_offset, 
                                    cgs.canvas_coords.row_top_y + self.letter_y_offset, 
                                    text=cgs.user_letter, anchor=self.letter_anchor, 
                                    font=self.letter_font)
    def display_bg(self, cgs, bg_color):
        self.grid_canvas.itemconfig(cgs.canvas_item, fill=bg_color)
    #kdm
    def on_click(self, event=None):
        # find the square we clicked on by iterating through the 
        # grid, comparing to see if the x/y coordinates fall within
        # that of a particular square
        for row in range(self.num_row_squares):
            for col in range(self.num_col_squares):
                cgs = self.grid[row][col]
                if ((cgs.canvas_coords.col_left_x < event.x < cgs.canvas_coords.col_right_x) 
                    and (cgs.canvas_coords.row_top_y < event.y < cgs.canvas_coords.row_bot_y)):
                    sel_gi = GridIndex(row, col)
                    if cgs.blackout:
                        # if we clicked a blackout square ignore it
                        break
                    elif sel_gi == self.current_active_gi:
                        # are we clicking on the active square?
                        # if so swap direction - is there a more elegant way??
                        # this should work need to swap and test
                        ## self.direction = Direction.ACROSS if self.direction == Direction.DOWN else direction.DOWN
                        if self.direction == Direction.ACROSS:
                            self.direction = Direction.DOWN
                        else:
                            self.direction = Direction.ACROSS
                        # need to change this to the new change_active_word
                        self.set_active_word()
                    else:
                        # need to change current_active_gi
                        # and current_active word            
                        old_gi = self.current_active_gi
                        self.current_active_gi = GridIndex(row, col)
                        self.refresh_grid_square(old_gi)
                        self.refresh_grid_square(self.current_active_gi)
                        if self.current_active_gi not in self.current_active_word:
                            self.set_active_word()

        self.sv.set(str(event.x) + " " + str(event.y))


    def on_key(self, event=None):
        letter = event.char.upper()
        # print("letter=",letter)
        # print("keysym=", event.keysym)
        # #print("key", event.key)
        
        gi = self.current_active_gi
        if letter in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
            self.grid[gi.row][gi.col].user_letter = letter
            self.refresh_grid_square(gi)
        elif (event.keysym == "ISO_Left_Tab"):
            #print("keysym=", event.keysym)
            self.prev_word()
        elif (event.keysym == "Tab"):
            #print("keysym=", event.keysym)
            self.next_word()
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
        self.sv.set(event.keysym)
    def prev_word(self):
        print("prev_word")
    def next_word(self):
        print("next_word")
    def go_left(self):
        print("go_left")
    def go_right(self):
        print("go_right")
    def go_up(self):
        print("go_up")
    def go_down(self):
        print("go_down")

    def set_active_word(self):

        old_active_word = []
        for e in self.current_active_word:
            old_active_word.append(e)
        self.current_active_word = []
        self.refresh_word(old_active_word)

        row = self.current_active_gi.row
        col = self.current_active_gi.col
        #find start of word
        if self.direction == Direction.ACROSS:

            #reset the word
            #find the first column that is not less than zero
            #or a blackout square           
            while col > 0:
                if self.grid[row][col].blackout:
                    #we've overshot the first square, go forward 1
                    col += 1
                    break
                col -= 1
            #now find the end: blackout or end column
            while col <= self.num_col_squares:
                if self.grid[row][col].blackout:
                    col -= 1
                    break
                self.current_active_word.append(GridIndex(row, col))
                col += 1
        else:
            #reset the word
            #self.current_active_word = []
            #find the first row that is not less than zero
            #or a blackout square           
            #row = self.current_active_gi.row
            #col = self.current_active_gi.col
            while row > 0:
                if self.grid[row][col].blackout:
                    #we've overshot the first square, go forward 1
                    row += 1
                    break
                row -= 1
            #now find the end: blackout or end column
            while row <= self.num_row_squares:
                if self.grid[row][col].blackout:
                    row -= 1
                    break
                self.current_active_word.append(GridIndex(row, col))
                row += 1
        self.refresh_word(self.current_active_word)

    def refresh_word(self, active_word):
        for s in active_word:
            self.refresh_grid_square(s)

puzzle = DisplayPuzzle(num_row_squares = 15, num_col_squares = 15)
win.mainloop()
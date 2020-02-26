       # set tab index to 0
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
    
        # need next and prev grid squares 
        # needs to advance or reverse and wrap around based on the direction
        # traveling. Word does not change direction when it reaches the end or the
        # beginning of the grid so if word direction is down and current word is in
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
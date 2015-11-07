"""
Loyd's Fifteen puzzle - solver and visualizer
Note that solved configuration has the blank (zero) tile in upper left
Use the arrows key to swap this tile with its neighbors

Author: Weikang Sun
Date: 11/5/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_bZhtc0W2ny_40.py
"""

import poc_fifteen_gui

class Puzzle:
    """
    Class representation for the Fifteen puzzle
    """

    def __init__(self, puzzle_height, puzzle_width, initial_grid=None):
        """
        Initialize puzzle with default height and width
        Returns a Puzzle object
        """
        self._height = puzzle_height
        self._width = puzzle_width
        self._grid = [[col + puzzle_width * row
                       for col in range(self._width)]
                      for row in range(self._height)]

        if initial_grid != None:
            for row in range(puzzle_height):
                for col in range(puzzle_width):
                    self._grid[row][col] = initial_grid[row][col]

    def __str__(self):
        """
        Generate string representaion for puzzle
        Returns a string
        """
        ans = ""
        for row in range(self._height):
            ans += str(self._grid[row])
            ans += "\n"
        return ans

    #####################################
    # GUI methods

    def get_height(self):
        """
        Getter for puzzle height
        Returns an integer
        """
        return self._height

    def get_width(self):
        """
        Getter for puzzle width
        Returns an integer
        """
        return self._width

    def get_number(self, row, col):
        """
        Getter for the number at tile position pos
        Returns an integer
        """
        return self._grid[row][col]

    def set_number(self, row, col, value):
        """
        Setter for the number at tile position pos
        """
        self._grid[row][col] = value

    def clone(self):
        """
        Make a copy of the puzzle to update during solving
        Returns a Puzzle object
        """
        new_puzzle = Puzzle(self._height, self._width, self._grid)
        return new_puzzle

    ########################################################
    # Core puzzle methods

    def current_position(self, solved_row, solved_col):
        """
        Locate the current position of the tile that will be at
        position (solved_row, solved_col) when the puzzle is solved
        Returns a tuple of two integers        
        """
        solved_value = (solved_col + self._width * solved_row)

        for row in range(self._height):
            for col in range(self._width):
                if self._grid[row][col] == solved_value:
                    return (row, col)
        assert False, "Value " + str(solved_value) + " not found"

    def update_puzzle(self, move_string):
        """
        Updates the puzzle state based on the provided move string
        """
        zero_row, zero_col = self.current_position(0, 0)
        for direction in move_string:
            if direction == "l":
                assert zero_col > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col - 1]
                self._grid[zero_row][zero_col - 1] = 0
                zero_col -= 1
            elif direction == "r":
                assert zero_col < self._width - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row][zero_col + 1]
                self._grid[zero_row][zero_col + 1] = 0
                zero_col += 1
            elif direction == "u":
                assert zero_row > 0, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row - 1][zero_col]
                self._grid[zero_row - 1][zero_col] = 0
                zero_row -= 1
            elif direction == "d":
                assert zero_row < self._height - 1, "move off grid: " + direction
                self._grid[zero_row][zero_col] = self._grid[zero_row + 1][zero_col]
                self._grid[zero_row + 1][zero_col] = 0
                zero_row += 1
            else:
                assert False, "invalid direction: " + direction

    ##################################################################
    # Phase one methods

    def lower_row_invariant(self, target_row, target_col):
        """
        Check whether the puzzle satisfies the specified invariant
        at the given position in the bottom rows of the puzzle (target_row > 1)
        Returns a boolean
        """
        
        # check if 0 tile is at target position
        if self.get_number(target_row, target_col) != 0:
            return False
        
        # check solved for all tile rows below target row
        if target_row != self.get_height() - 1:
            for row in range(target_row + 1, self.get_height()):
                for col in range(self.get_width()):
                    if not self.compare_actual_position(row, col):
                        return False
                    
        # check solved for all tiles to the right of target
        if target_col != self.get_width() - 1:
            for col in range(target_col + 1, self.get_width()):
                if not self.compare_actual_position(target_row, col):
                    return False
        
        return True

    def compare_actual_position(self, solved_row, solved_col):
        """
        Helper function to check if the target tile is actually in the 
        solved position.  Uses current_position().
        Returns True or False.
        """
        
        actual_row, actual_col = self.current_position(solved_row, solved_col)
        if actual_row != solved_row or actual_col != solved_col:
            return False
        return True
    
    def solve_interior_tile(self, target_row, target_col, override = False, o_row = -1, o_col = -1):
        """
        Place correct tile at target position
        Updates puzzle and returns a move string
        
        Added override code to be able to reuse code for solving col0 method below
        """
        
        zero_row = target_row
        zero_col = target_col

        if override:
            # this override provides pseudo target tile coordinates passed from col0
            actual_row = o_row
            actual_col = o_col
        else:
            # find actual location of target tile
            actual_row, actual_col = self.current_position(target_row, target_col)
        
        move_string = ""
        
        # case 1: not in same row
        if actual_row < zero_row:
            
            move_string += self.solve_interior_tile_higher((zero_row, zero_col), (actual_row, actual_col), (target_row, target_col), move_string)
        
        # case 2: target in same row to the left
        elif actual_col < zero_col:
            while zero_col > actual_col:
                move_string += "l"
                zero_col -= 1
            actual_col += 1
            
            while actual_col < target_col:
                move_string += "urrdl"
                actual_col += 1
        
        # override conditions only when target in same row to the right
        else:
            while zero_col < actual_col:
                move_string += "r"
                zero_col += 1
            
            while actual_col > target_col:
                move_string += "ulldr"
                actual_col -= 1
            move_string += "l"
       
        self.update_puzzle(move_string)
        return move_string
    
    def solve_interior_tile_higher(self, zero, actual, target, move_string):
        """
        Helper function for above row inner tile solve. Delegated part of duty because of
        pylint's "too many branches" complaints. Also must limit number of inputs
        due to pylint's "too many arguments" complaints.
        """
        
        zero_row, zero_col = zero
        actual_row, actual_col = actual
        target_row, target_col = target
        
        # move up to the same row
        while zero_row > actual_row:
                move_string += "u"
                zero_row -= 1

        # case 1a: target is now to the left
        if actual_col < zero_col:
            # move 0 left to target
            while zero_col > actual_col:
                move_string += "l"
                zero_col -= 1
            actual_col += 1
            # at this point target tile is directly to right of 0
            # iterate until target tile directly above target position
            while actual_col < target_col:
                move_string += "drrul"
                actual_col += 1
            # position 0 tile accordingly
            move_string += "dru"


        # case 1b: target is now to the right
        elif actual_col > target_col:
            while zero_col < actual_col:
                move_string += "r"
                zero_col += 1
            actual_col -= 1
            # at this point target tile is directly to the left of 0
            # iterate until target tile directly above target position
            # this move is tricky if the target tile was above completed tiles
            while actual_col > target_col:
                move_string += "dllurdrul"
                actual_col -= 1
            # position 0 tile accordingly, also tricky if target tile is above completed tiles
            move_string += "dluldrruldlur"

        # at this point target tile should be directly below 0 tile
        actual_row += 1    
        # target tile now directly above target position, iterate moves downward
        while actual_row < target_row:
            move_string += "lddru"
            actual_row += 1

        # finally move 0 tile to invariant position
        move_string += "ld"
        
        return move_string
        
    def solve_col0_tile(self, target_row):
        """
        Solve tile in column zero on specified row (> 1)
        Updates puzzle and returns a move string
        """
        
        move_string = "ur"
        self.update_puzzle("ur")
        
        actual_row, actual_col = self.current_position(target_row, 0)
        
        # if tile is already positioned, then simple answer
        # otherwise perform moves to position target tile
        if actual_row != target_row or actual_col != 0:
            move_string += self.solve_interior_tile(target_row - 1, 1, True, actual_row, actual_col)
            
            # now position target tile in col 0 using 3x2 puzzle solution
            move_string += "ruldrdlurdluurddlur"
            self.update_puzzle("ruldrdlurdluurddlur")
        
        # finally move 0 tile to far right
        for dummy_var in range(self.get_width() - 2):
            move_string += "r"
            self.update_puzzle("r")
        
        return move_string

    #############################################################
    # Phase two methods

    def row0_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row zero invariant
        at the given column (col > 1)
        Returns a boolean
        """
        
        # check if 0 tile is at target position
        if self.get_number(0, target_col) != 0:
            return False
        
        # check solved for the tile below target tile
        if not self.compare_actual_position(1, target_col):
            return False
        
        # modify a copy of the puzzle to satisfy row1_invariant
        puzzle_copy = self.clone()
        puzzle_copy.update_puzzle("d")
        return puzzle_copy.row1_invariant(target_col)

    def row1_invariant(self, target_col):
        """
        Check whether the puzzle satisfies the row one invariant
        at the given column (col > 1)
        Returns a boolean
        """
        
        # check solved for all tile cols to the right of target col
        if target_col != self.get_width() - 1:
            for row in range(2):
                for col in range(target_col + 1, self.get_width()):
                    if not self.compare_actual_position(row, col):
                        return False
                    
        # must satisty the lower row invariant as well
        return self.lower_row_invariant(1, target_col)

    def solve_row0_tile(self, target_col):
        """
        Solve the tile in row zero at the specified column
        Updates puzzle and returns a move string
        """
        
        move_string = "ld"
        self.update_puzzle("ld")
        
        actual_row, actual_col = self.current_position(0, target_col)
        
        # if tile is already positioned, then simple answer
        # otherwise perform moves to position target tile
        if actual_row != 0 or actual_col != target_col:
            zero_col = target_col - 1
            
            # condition if target tile is directly above
            if actual_col == target_col - 1:
                move_string += "uldrl"
                self.update_puzzle("uldrl")
                actual_row += 1
            
            # move 0 tile to same column as target tile
            while zero_col > actual_col:
                move_string += "l"
                self.update_puzzle("l")
                zero_col -= 1
            
            # if the target tile is above the 0 tile
            if actual_row == 0:
                move_string += "urdl"
                self.update_puzzle("urdl")
            
            actual_col += 1            
            # iteratively move target tile to position (1, j-1)
            while actual_col < target_col - 1:
                move_string += "urrdl"
                self.update_puzzle("urrdl")
                actual_col += 1
        
            # now perform final move string to move tile into position
            move_string += "urdlurrdluldrruld"
            self.update_puzzle("urdlurrdluldrruld")
        
        return move_string

    def solve_row1_tile(self, target_col):
        """
        Solve the tile in row one at the specified column
        Updates puzzle and returns a move string
        """
        
        # can use exact same method for solving this tile
        move_string = self.solve_interior_tile(1, target_col)
        
        # prepare 0 tile for row0 invariant
        self.update_puzzle("ur")
        
        return move_string + "ur"

    ###########################################################
    # Phase 3 methods

    def solve_2x2(self):
        """
        Solve the upper left 2x2 part of the puzzle
        Updates the puzzle and returns a move string
        """
        
        # begin by moving 0 tile to 0 spot
        move_string = "ul"
        self.update_puzzle("ul")
        
        # now iteratively check until whole puzzle is solved
        while not self.row0_invariant(0):
            move_string += "drul"
            self.update_puzzle("drul")
            
        return move_string

    def solve_puzzle(self):
        """
        Generate a solution string for a puzzle
        Updates the puzzle and returns a move string
        """
        
        move_string = ""
        
        # start by moving 0 tile to bottom right
        zero_row, zero_col = self.current_position(0, 0)
        while zero_row < self.get_height() - 1:
            zero_row += 1
            move_string += "d"
            self.update_puzzle("d")
            
        while zero_col < self.get_width() - 1:
            zero_col += 1
            move_string += "r"
            self.update_puzzle("r")
        
        print self.__str__()
        
        # now iterate solve_interior_tile until two rows remain
        for row in range(self.get_height() - 1, 1, -1):
            for col in range(self.get_width() - 1, 0, -1):
                move_string += self.solve_interior_tile(row, col)
            move_string += self.solve_col0_tile(row)
                
        # now iterate solve_col1 and solve_col0 until 2x2 remains
        for col in range(self.get_width() - 1, 1, -1):
            move_string += self.solve_row1_tile(col)
            move_string += self.solve_row0_tile(col)
            
        # finally solve 2x2
        move_string += self.solve_2x2()
            
        return move_string

# Start interactive simulation
poc_fifteen_gui.FifteenGUI(Puzzle(4, 4))

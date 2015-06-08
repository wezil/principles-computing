"""
Clone of 2048 game.

Author: Weikang Sun
Date: 6/3/15

Codeskulptor source:
http://www.codeskulptor.org/#user40_L4PvWLchQ4_7.py

"""

import random
import poc_2048_gui


# Directions, DO NOT MODIFY
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

# Offsets for computing tile indices in each direction.
# DO NOT MODIFY this dictionary.
OFFSETS = {UP: (1, 0),
           DOWN: (-1, 0),
           LEFT: (0, 1),
           RIGHT: (0, -1)}

def merge(line):
    """
    Helper function that merges a single row or column in 2048
    """
    result = [0] * len(line)
    
    result_position = 0
    
    # iterate over all line values
    for line_value in line:
        if line_value != 0:
            # merge two tiles
            if result[result_position] == line_value:
                result[result_position] = 2 * line_value
                result_position += 1
            # put in blank spot
            elif result[result_position] == 0:
                result[result_position] = line_value               
            # add to next position for a non-matching, occupied spot
            else:
                result_position += 1
                result[result_position] = line_value
        
    return result

class TwentyFortyEight:
    """
    Class to run the game logic.
    """

    def __init__(self, grid_height, grid_width):
        """
        Initializes the game given the grid dimensions
        """
        
        self._grid_height = grid_height
        self._grid_width = grid_width
        self.reset()
        
        # pre-computation for "initial" tiles for move()
        # determines the first row or column affected by 
        # the direction (i.e. UP results in the top row)
        self._initial_tiles = {UP: self.traverse_grid((0, 0), LEFT),
                               DOWN: self.traverse_grid((grid_height - 1, 0), LEFT),
                               LEFT: self.traverse_grid((0, 0), UP),
                               RIGHT: self.traverse_grid((0, grid_width - 1), UP)}
            
    
        
    def reset(self):
        """
        Reset the game so the grid is empty except for two
        initial tiles.
        """
       
        self._game_board = [[0 for dummy_col in range(self._grid_width)] 
         for dummy_row in range(self._grid_height)]
        
        self._game_over = False
        self._user_score = 0
        
        self.new_tile()
        self.new_tile() 

    def __str__(self):
        """
        Return a string representation of the grid for debugging.
        """
        
        return str(self._game_board)
    
    def print_grid(self):
        """
        prints the grid for debug purposes
        """
        
        for counter in range(self._grid_height):
            print self._game_board[counter]

    def get_grid_height(self):
        """
        Get the height of the board.
        """

        return self._grid_height

    def get_grid_width(self):
        """
        Get the width of the board.
        """

        return self._grid_width

    def move(self, direction):
        """
        Move all tiles in the given direction and add
        a new tile if any tiles moved.
        """
        
        if not self._game_over:    
            _is_board_changed = False

            # get the list of tuple coordinates for the initial tiles
            # and iterate over each of these headers to merge the lines
            for start_cell in self._initial_tiles[direction]:
                # get the coordinates of row/col to be merged (list of tuples)
                line_coords = self.traverse_grid(start_cell, direction)

                # get the values of that row/col to be merged (list of ints)
                line = [self._game_board[tile_coord[0]][tile_coord[1]]
                                         for tile_coord in line_coords]

                merged_line = merge(line)
                self._user_score += self.compute_score(line)

                if merged_line != line:
                    _is_board_changed = True
                    # zips the tile coordinates and tile values
                    # and iterates to set_tile() for that line
                    # tile[0] is the coord tuple, tile[1] is the value
                    for tile in zip(line_coords, merged_line):
                        self.set_tile(tile[0][0], tile[0][1], tile[1])
                    
            if _is_board_changed:
                self.new_tile()
            
            self.is_game_over()

    def traverse_grid(self, start_cell, direction):
        """
        Returns a list of tuples of the coordinates of
        a row/col in the grid in a particular direction.
        This is useful for obtaining initial tiles and 
        indiviual row/col to be passed onto merge.
        """
        
        _result_list = []
        
        # determines the proper steps in direction to traverse
        _num_steps = self._grid_width
        
        # gets the tuple for the direction from the dictionary
        _dir_index = OFFSETS[direction]
        
        # changes steps depending on which direction specified
        if _dir_index[0] != 0:
            _num_steps = self._grid_height
        
        for steps in range(_num_steps):
            _result_list.append((start_cell[0] + _dir_index[0] * steps, 
                                 start_cell[1] + _dir_index[1] * steps))
        
        return _result_list
    
    def compute_score(self, line):
        """
        Helper method to compute the score change when tiles are merged
        Score is added by the value of the new tile after merging
        i.e. when two 4 tiles merge, a score of 8 is incremented.
        This is basically the merge() method, but since the grader checks
        the return result I had to make a new method just for scoring
        """
       
        _score = 0
        _result = [0] * len(line)
        _result_position = 0
        
        for line_value in line:
            if line_value != 0:
                # merge two tiles, this is where score actually changes
                if _result[_result_position] == line_value:
                    _result[_result_position] = 2 * line_value
                    _score += 2 * line_value
                    _result_position += 1
                # put in blank spot
                elif _result[_result_position] == 0:
                    _result[_result_position] = line_value               
                # add to next position for a non-matching, occupied spot
                else:
                    _result_position += 1
                    _result[_result_position] = line_value
        
        return _score
        
    def new_tile(self):
        """
        Create a new tile in a randomly selected empty
        square.  The tile should be 2 90% of the time and
        4 10% of the time.
        """
        
        _new_tile = 2
        
        # 10% chance random generator for 4 tile
        if random.randrange(10) == 0:
            _new_tile = 4
        
        # place new tile in a random empty spot
        _rand_row = random.randrange(self._grid_height)
        _rand_col = random.randrange(self._grid_width)
        
        while self._game_board[_rand_row][_rand_col] != 0 and not self.is_game_over():
            _rand_row = random.randrange(self._grid_height)
            _rand_col = random.randrange(self._grid_width)
        
        self.set_tile(_rand_row, _rand_col, _new_tile)

    def set_tile(self, row, col, value):
        """
        Set the tile at position row, col to have the given value.
        """
        
        # attempts to place value in position, 
        # except when referencing an invalid index
        try:
            self._game_board[row][col] = value
        except IndexError:
            print "Error: invalid index"

    def get_tile(self, row, col):
        """
        Return the value of the tile at position row, col.
        """
        
        # attempts to get the value of the tile at position,
        # except for index errors
        try:
            return self._game_board[row][col]
        except IndexError:
            print "Error: invalid index"
            
    def is_game_over(self):
        """
        Checks whether any legal moves are possible
        if not, then prints game over and final score
        """
        
        # check legal moves across all rows
        for row in range(self._grid_height):
            value = self._game_board[row][0]
            
            # empty space
            if value == 0:
                return False
            # iteratively check next value in this row
            for col in range(1, self._grid_width):
                new_value = self._game_board[row][col]
                if new_value == value or new_value == 0:
                    return False
                value = new_value
        
        # check legal moves down all columns
        for col in range(self._grid_width):
            value = self._game_board[0][col]
            if value == 0:
                return False
            for row in range(1, self._grid_height):
                new_value = self._game_board[row][col]
                if new_value == value or new_value == 0:
                    return False
                value = new_value
                
        # at this point no legal moves are allowed       
        print "Game Over!"
        print "Final score: ", self._user_score
        print "~~~~~~~~~~"
        
        self._game_over = True
                                    
    
poc_2048_gui.run_gui(TwentyFortyEight(4, 4))

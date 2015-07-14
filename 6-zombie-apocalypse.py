"""
Zombie Apocalypse mini-project
Using Breadth-First 2D Search
Principles of Computing Part 2

Author: Weikang Sun
Date: 7/14/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_iQQZl747fQ_13.py
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        # replace with an actual generator
        for zombie in self._zombie_list:
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        # replace with an actual generator
        for human in self._human_list:
            yield human
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        
        height = poc_grid.Grid.get_grid_height(self)
        width = poc_grid.Grid.get_grid_width(self)
        
        # create a visited grid of same dimensions that is empty        
        visited = poc_grid.Grid(height, width)
        # create a distance list of same dimensions that contains large value
        distance_field = [[height * width for dummy_width in range(width)] \
                          for dummy_height in range(height)]
        
        # queue of entity_type list
        boundary = poc_queue.Queue()
        
        # enqueue all instances of entity_type
        if entity_type is HUMAN:
            for human in self._human_list:
                boundary.enqueue(human)
        else:
            for zombie in self._zombie_list:
                boundary.enqueue(zombie)
        
        # update distance_field to 0 and visited to FULL for entities
        for entity in boundary:
            visited.set_full(entity[0], entity[1])
            distance_field[entity[0]][entity[1]] = 0
            
        # implementation of breadth-first search on these entities
        while len(boundary) is not 0:
            current_cell = boundary.dequeue()
            
            for neighbor_cell in poc_grid.Grid.four_neighbors(self, current_cell[0], current_cell[1]):
                # first check if this neighbor cell is a wall
                if not poc_grid.Grid.is_empty(self, neighbor_cell[0], neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                # otherwise check empty cell as usual
                elif visited.is_empty(neighbor_cell[0], neighbor_cell[1]):
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                    boundary.enqueue(neighbor_cell)
                    # also update distance of each neighbor cell
                    new_distance = distance_field[current_cell[0]][current_cell[1]] + 1
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = new_distance
                        
        return distance_field
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        
        # first create an empty list
        human_list_copy = []
        # iterate over all human in list
        for human in self._human_list:
            max_distance = zombie_distance_field[human[0]][human[1]]
            # a list of possible choices
            best_moves = [human]
            
            for neighbor in poc_grid.Grid.eight_neighbors(self, human[0], human[1]):
                # neighbor should not be a wall 
                if poc_grid.Grid.is_empty(self, neighbor[0], neighbor[1]):
                    distance = zombie_distance_field[neighbor[0]][neighbor[1]]
                    # if distance is better (but not a wall), wipe old list
                    if distance > max_distance:
                        max_distance = distance
                        best_moves = [neighbor]
                    # if distance is same, append to same list    
                    elif distance == max_distance:
                        best_moves.append(neighbor)

            # add the new coordinate by choosing randomly from best_moves
            human_list_copy.append(random.choice(best_moves))
        
        # update self list with copy
        self._human_list = human_list_copy
    
    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        
        zombie_list_copy = []
        
        for zombie in self._zombie_list:
            min_distance = human_distance_field[zombie[0]][zombie[1]]
            best_moves = [zombie]
            
            for neighbor in poc_grid.Grid.four_neighbors(self, zombie[0], zombie[1]):             
                if poc_grid.Grid.is_empty(self, neighbor[0], neighbor[1]):
                    distance = human_distance_field[neighbor[0]][neighbor[1]]
                    if distance < min_distance:
                        min_distance = distance
                        best_moves = [neighbor]
                    elif distance == min_distance:
                        best_moves.append(neighbor)
                    
            zombie_list_copy.append(random.choice(best_moves))
            
        self._zombie_list = zombie_list_copy

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))

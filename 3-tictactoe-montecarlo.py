"""
Monte Carlo Tic-Tac-Toe Player

Machine chooses next move based
on Monte Carlo simulation of 
the board state.

Author: Weikang Sun
Date: 6/10/15

codeskulptor source:
http://www.codeskulptor.org/#user40_K06ExlihP2_6.py
"""

import random
import poc_ttt_gui
import poc_ttt_provided as provided

# Constants for Monte Carlo simulator
# You may change the values of these constants as desired, but
#  do not change their names.
NTRIALS = 100       # Number of trials to run
SCORE_CURRENT = 1.0 # Score for squares played by the current player
SCORE_OTHER = 1.0   # Score for squares played by the other player
    
def mc_trial(board, player):
    """
    Monte Carlo single trial to run on an active board
    with the given current player to move
    
    Returns the finished game board
    """
    
    # play random game until board is finished
    while board.check_win() is None:
        # choose randomly from list of empty squares
        next_move = random.choice(board.get_empty_squares())
        board.move(next_move[0], next_move[1], player)
        
        # switch sides
        player = provided.switch_player(player)
        
    return board

def mc_update_scores(scores, board, player):
    """
    Function that takes the finished board and updates
    the scores for each cell given the winner
    """
    
    # no score update if the game is a draw
    if board.check_win() is provided.DRAW:
        return
    
    # iterate over all cells to update scores
    dim = board.get_dim()
    for row in range(dim):
        for col in range(dim):
            
            score = 0
            # get the player who marked at the cell
            marker = board.square(row, col)
            
            if marker is not provided.EMPTY:    
                # determine whether to add/subtract respective scores
                mult_const = 1
                if board.check_win() is not player:
                    mult_const = -1
                
                if marker is player:
                    score += mult_const * SCORE_CURRENT
                else:
                    score -= mult_const * SCORE_OTHER
            
            scores[row][col] += score

def get_best_move(board, scores):
    """
    Function that finds the best move(s) for the computer
    given the sum scores for many MC trials of each cell
    on the current, active board
    
    Returns the cell to play (randomly chosen if multiple high score)
    """
      
    max_score = float("-inf")
    
    # potential candidate choices, initially empty
    top_score_cells = []
    
    for (row, col) in board.get_empty_squares():
        cell_score = scores[row][col]
        # if new max score, dump out potential choices and put it this one
        if cell_score > max_score:
            top_score_cells = [(row, col)]
            max_score = cell_score
        # if matches max score, add it to potential choices
        elif cell_score is max_score:
            top_score_cells.append((row, col))
    
    # return a random choice amongst the potential candidates
    return random.choice(top_score_cells)

def mc_move(board, player, trials):
    """
    Function that analyzes the current board using MC trials
    
    Returns the best move for the computer (player)
    """
    
    # generate a blank score table
    scores = [[0 for dummy_col in range(board.get_dim())] 
              for dummy_row in range(board.get_dim())]
    
    # run trials for clone boards and update scores
    for _ in range(trials):
        clone = board.clone()
        mc_trial(clone, player)
        mc_update_scores(scores, clone, player)

    return get_best_move(board, scores)

def print_score(scores):
    """
    Helper function to print the score nicely for debug
    """
    for row in range(len(scores)):
        print scores[row]

    print
    
# Test game with the console or the GUI.  Uncomment whichever 
# you prefer.  Both should be commented out when you submit 
# for testing to save time.

# provided.play_game(mc_move, NTRIALS, False)        
poc_ttt_gui.run_gui(3, provided.PLAYERX, mc_move, NTRIALS, False)

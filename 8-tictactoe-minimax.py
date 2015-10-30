"""
Mini-max Tic-Tac-Toe Player

Author: Weikang Sun
Date: 10/29/15

CodeSkultpor source:
http://www.codeskulptor.org/#user40_nOKLY8YOrB_15.py
"""

import poc_ttt_gui
import poc_ttt_provided as provided

# Set timeout, as mini-max can take a long time
import codeskulptor
codeskulptor.set_timeout(60)

# SCORING VALUES - DO NOT MODIFY
SCORES = {provided.PLAYERX: 1,
          provided.DRAW: 0,
          provided.PLAYERO: -1}

def mm_move(board, player):
    """
    Make a move on the board.
    
    Returns a tuple with two elements.  The first element is the score
    of the given board and the second element is the desired move as a
    tuple, (row, col).
    """
    
    # check status of game
    status = board.check_win()
    
    # recursive case, when game is not yet finished
    if status is None:
        avail_moves = board.get_empty_squares()
        
        # set a score impossibly low with invalid move
        max_score = -2
        best_move = (-1, -1)
        
        for move in avail_moves:
            # remember to iterate on a clone of the board
            game = board.clone()
            game.move(move[0], move[1], player)
            # get the best score from the new board based on player
            mm_result, dummy_var = mm_move(game, provided.switch_player(player))
            mm_result *= SCORES[player]
            
            # short circuit in event of winning move
            if mm_result == 1:
                return SCORES[player], move

            elif mm_result > max_score:
                max_score = mm_result
                best_move = move
        # return the best move available    
        return SCORES[player]*max_score, best_move  
    
    # base cases, when game is already finished
    else:
        return SCORES[status], (-1, -1)
    

def move_wrapper(board, player, trials):
    """
    Wrapper to allow the use of the same infrastructure that was used
    for Monte Carlo Tic-Tac-Toe.
    """
    move = mm_move(board, player)
    assert move[1] != (-1, -1), "returned illegal move (-1, -1)"
    return move[1]

# Test game with the console or the GUI.
# Uncomment whichever you prefer.
# Both should be commented out when you submit for
# testing to save time.

# provided.play_game(move_wrapper, 1, False)        
# poc_ttt_gui.run_gui(3, provided.PLAYERO, move_wrapper, 1, False)




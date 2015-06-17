"""
Planner for Yahtzee
Simplifications:  only allow discard and roll, 
only score against upper level

Author: Weikang Sun
Date: 6/16/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_wmPIY4na8x_8.py
"""

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length.
    """
    
    answer_set = set([()])
    for dummy_idx in range(length):
        temp_set = set()
        for partial_sequence in answer_set:
            for item in outcomes:
                new_sequence = list(partial_sequence)
                new_sequence.append(item)
                temp_set.add(tuple(new_sequence))
        answer_set = temp_set
    return answer_set


def score(hand):
    """
    Compute the maximal score for a Yahtzee hand according to the
    upper section of the Yahtzee score card.

    hand: full yahtzee hand

    Returns an integer score 
    """
    
    max_score = 0
    
    for idx in range(max(hand) + 1):
        idx_score = hand.count(idx) * idx

        max_score = max(idx_score, max_score)
            
    return max_score


def expected_value(held_dice, num_die_sides, num_free_dice):
    """
    Compute the expected value based on held_dice given that there
    are num_free_dice to be rolled, each with num_die_sides.

    held_dice: dice that you will hold
    num_die_sides: number of sides on each die
    num_free_dice: number of dice to be rolled

    Returns a floating point expected value
    """
    
    free_dice_set = gen_all_sequences(range(1, num_die_sides + 1), num_free_dice)
    total_score = 0.0

    for item in free_dice_set:
        total_score += score(held_dice + item)
    
    return total_score / len(free_dice_set)


def gen_all_holds(hand):
    """
    Generate all possible choices of dice from hand to hold.

    hand: sorted full yahtzee hand

    Returns a set of tuples, where each tuple is sorted dice to hold
    """
    
    # start off with the original hand in set
    set_holds = set([(hand)])
    
    # now iterate with all sub hands with one element removed
    for item in hand:
        list_hand = list(hand)
        list_hand.remove(item)
        # add to set_holds this sub hand
        set_holds.add(tuple(list_hand))
        # also add to set_holds the recursion of this sub hand
        # set functionality also takes care of repeated sub hands
        set_holds.update(gen_all_holds(tuple(list_hand)))
    
    return set_holds


def strategy(hand, num_die_sides):
    """
    Compute the hold that maximizes the expected value when the
    discarded dice are rolled.

    hand: full yahtzee hand
    num_die_sides: number of sides on each die

    Returns a tuple where the first element is the expected score and
    the second element is a tuple of the dice to hold
    """
    
    set_all_holds = gen_all_holds(hand)
    
    max_expect_score = 0.0
    
    best_hold = ()
    
    for item in set_all_holds:
        expect_score = expected_value(item, num_die_sides, len(hand) - len(item))
        if expect_score > max_expect_score:
            max_expect_score = expect_score
            best_hold = item
    
    return (max_expect_score, best_hold)


def run_example():
    """
    Compute the dice to hold and expected score for an example hand
    """
    num_die_sides = 6
    hand = (2, 2, 2, 1, 1)
    hand_score, hold = strategy(hand, num_die_sides)
    print "Best strategy for hand", hand
    print "is to hold", hold, "with expected score", hand_score
    

def print_set(input_set):
    """ prints the set for debug purposes """
    for item in input_set:
        print item
    
run_example()

#import poc_holds_testsuite
#poc_holds_testsuite.run_suite(gen_all_holds)

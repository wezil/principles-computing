"""
Student code for Word Wrangler game
Note: some built-in functions are barred
in order to demonstrate recursion functions

Author: Weikang Sun
Date: 7/22/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_ODhJ8huYCA_9.py
"""

import urllib2
import codeskulptor
import poc_wrangler_provided as provided

WORDFILE = "assets_scrabble_words3.txt"

codeskulptor.set_timeout(20)


# Functions to manipulate ordered word lists

def remove_duplicates(list1):
    """
    Eliminate duplicates in a sorted list.

    Returns a new sorted list with the same elements in list1, but
    with no duplicates.

    This function can be iterative.
    """
    
    list_unique = []
    append = list_unique.append
    
    for element in list1:
        if element not in list_unique:
            append(element)
    
    return list_unique


def intersect(list1, list2):
    """
    Compute the intersection of two sorted lists.

    Returns a new sorted list containing only elements that are in
    both list1 and list2.

    This function can be iterative.
    """
    
    intersection = []
    append = intersection.append
    idx1 = 0
    idx2 = 0
    
    while idx1 < len(list1) and idx2 < len(list2):
        if list1[idx1] < list2[idx2]:
            idx1 += 1
        elif list1[idx1] > list2[idx2]:
            idx2 += 1
        else:
            append(list1[idx1])
            idx1 += 1
            idx2 += 1
    
    return intersection


# Functions to perform merge sort

def merge(list1, list2):
    """
    Merge two sorted lists.

    Returns a new sorted list containing all of the elements that
    are in either list1 and list2.

    This function can be iterative.
    """   
    
    merged = []
    idx1 = 0
    idx2 = 0
    
    while idx1 < len(list1) and idx2 < len(list2):
        if list1[idx1] <= list2[idx2]:
            merged.append(list1[idx1])
            idx1 += 1
        else:
            merged.append(list2[idx2])
            idx2 += 1
        
    if idx1 == len(list1):
        merged.extend(list2[idx2: ])
    else:
        merged.extend(list1[idx1: ])
        
    return merged

                
def merge_sort(list1):
    """
    Sort the elements of list1.

    Return a new sorted list with the same elements as list1.

    This function should be recursive.
    """
    
    new_list = list(list1)
    
    if len(list1) > 1:
        midpoint = len(list1) // 2
        left = list(list1[0: midpoint])
        right = list(list1[midpoint: ])
        left = merge_sort(left)
        right = merge_sort(right)
        new_list = merge(left, right)
    
    return new_list


# Function to generate all strings for the word wrangler game

def gen_all_strings(word):
    """
    Generate all strings that can be composed from the letters in word
    in any order.

    Returns a list of all strings that can be formed from the letters
    in word.

    This function should be recursive.
    """
    
    # base case with no length word
    if len(word) == 0:
        return [""]
    
    # recursive case
    head = word[0]
    tail = word[1: ]
    # keep track of a master list while generating sub list
    master_list = []
    sub_list = gen_all_strings(tail)
    # add sub list to master list
    master_list.extend(sub_list)
    # for each sub list word add to master list a combination of all
    # head character positions in sub word
    for sub_word in sub_list:
        for index in range(len(sub_word) + 1):
            master_list.append(sub_word[:index] + head + sub_word[index: ])
    
    return master_list


# Function to load words from a file

def load_words(filename):
    """
    Load word list from the file named filename.

    Returns a list of strings.
    """
    
    url = codeskulptor.file2url(filename)
    netfile = urllib2.urlopen(url)
    
    return [line[:-1] for line in netfile.readlines()]

def run():
    """
    Run game.
    """
    words = load_words(WORDFILE)
    wrangler = provided.WordWrangler(words, remove_duplicates, 
                                     intersect, merge_sort, 
                                     gen_all_strings)
    provided.run_game(wrangler)

# Uncomment when you are ready to try the game
run()


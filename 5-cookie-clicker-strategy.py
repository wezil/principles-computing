"""
Cookie Clicker Simulator

Non-graphical simulation of the popular game
Attempts a few strategies to maximize cookiez

Author: Weikang Sun
Date: 6/28/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_K2M2Do5WmM_9.py
"""

import simpleplot
import math
import random

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies = 0.0
        self._cookies = 0.0
        self._time = 0.0
        self._cps = 1.0
        # history = [time bought, item, item cost, total cookies produced]
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        state = "###STATE###"
        state += "\nTotal Cookies: " + str(self._total_cookies)
        state += "\nCurrent Cookies: " + str(self._cookies)
        state += "\nCurrent Time: " + str(self._time)
        state += "\nCurrent CPS: " + str(self._cps)
#        state += "\nHistory:"
#        
#        for item in self.get_history():
#            state += "\n " + str(item)
        
        return state
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._cookies
    
    def get_total_cookies(self):
        """
        Returns the total number of cookies
        """
        
        return self._total_cookies
    
    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._cps
    
    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._time
    
    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return list(self._history)

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        
        if self._cookies >= cookies:
            return 0.0
        else:
            return math.ceil((cookies - self._cookies) / self._cps)
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._time += time
            self._cookies += time * self._cps
            self._total_cookies += time * self._cps
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._cookies >= cost:
            self._cookies -= cost
            self._cps += additional_cps
            self._history.append((self._time, item_name, cost, self._total_cookies))
   
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    build_copy = build_info.clone()
    clicker = ClickerState()
    
    # iterate simulation over the duration time
    while clicker.get_time() <= duration:
        # get the item to buy from the strategy function
        item_to_get = strategy(clicker.get_cookies(), clicker.get_cps(),
                               clicker.get_history(), duration - clicker.get_time(), 
                               build_copy)
        # if no item, end simulation
        if item_to_get == None:
            break
        
        # retrieve item cost from build
        item_cost = build_copy.get_cost(item_to_get)
        # retrieve time needed to buy item from clicker
        time_needed = clicker.time_until(item_cost)
        
        # break if time needed will exceed sim duration
        if clicker.get_time() + time_needed > duration:
            break
        
        # wait for that time and buy the item
        clicker.wait(time_needed)
        clicker.buy_item(item_to_get, item_cost, 
                         build_copy.get_cps(item_to_get))
        
        # update the build copy for the item just bought
        build_copy.update_item(item_to_get) 
    
    # allow clicker to finish simulation duration if there is extra time
    clicker.wait(duration - clicker.get_time())
    
    return clicker

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    
    # maximum cookies to be able to get in the time left
    max_cookies = cookies + cps * time_left
    
    cheap_item = None
    cheap_item_cost = float("inf")
    
    #iterate over all items
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        
        if item_cost <= cheap_item_cost and item_cost <= max_cookies:
            cheap_item = item
            cheap_item_cost = item_cost
    
    return cheap_item

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    
    #maximum cookies to be able to get in the time left
    max_cookies = cookies + cps * time_left
    
    expensive_item = None
    expensive_item_cost = float("-inf")
    
    #iterate over all items
    for item in build_info.build_items():
        item_cost = build_info.get_cost(item)
        
        if item_cost > expensive_item_cost and item_cost <= max_cookies:
            expensive_item = item
            expensive_item_cost = item_cost
    
    return expensive_item

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    
    # get a sorted list of default items in build
    build_copy = provided.BuildInfo()
    default_order = [(build_copy.get_cost(item), item) 
                     for item in build_copy.build_items()]
    default_order.sort()
    
    # make a dictionary out of this ordered list
    default_dic = {}
    for cost, item in default_order:
        default_dic[item] = cost
    
    # get maximum cookies able to be generated in time left
    max_cookies = cookies + cps * time_left
    
    # generate a shopping list of all purchaseable items
    shopping_list = []
    for item in build_copy.build_items():
        item_cost = build_info.get_cost(item)
        if item_cost < max_cookies:
            shopping_list.append((item_cost, item))
    shopping_list.sort()
    
    if shopping_list == []:
        return None
    
    # immediately return the first item which is below the 
    # default price multipled by a cost incrase constant
    for cost, item in shopping_list:
        if cost <= default_dic[item] * 1.15 ** 124:
            return item
            
    # if nothing else, return the most expensive available item        
    return strategy_expensive(cookies, cps, history, time_left, build_info)  
        
def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

#    history = state.get_history()
#    history = [(item[0], item[3]) for item in history]
#    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run(strategy):
    """
    Run the simulator.
    """    
    run_strategy("Cursor", SIM_TIME, strategy)

    # Add calls to run_strategy to run additional strategies
    # run_strategy("Cheap", SIM_TIME, strategy_cheap)
    # run_strategy("Expensive", SIM_TIME, strategy_expensive)
    # run_strategy("Best", SIM_TIME, strategy_best)
    
# run(strategy_best)

# print
# print strategy_best(0, 10000.0, [(1, "Clicker")], 1000000, provided.BuildInfo())

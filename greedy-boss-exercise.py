"""
Simulator for greedy boss scenario

Author: Weikang Sun
Date: 6/28/15

CodeSkulptor source:
http://www.codeskulptor.org/#user40_1UUwuZGPrH_1.py
"""

import simpleplot
import math
import codeskulptor
codeskulptor.set_timeout(20)

STANDARD = True
LOGLOG = False

# constants for simulation
INITIAL_SALARY = 100
SALARY_INCREMENT = 100
INITIAL_BRIBE_COST = 1000


def greedy_boss(days_in_simulation, bribe_cost_increment, plot_type = STANDARD):
    """
    Simulation of greedy boss
    """
    
    # initialize necessary local variables
    total = 0
    earnings = 0
    salary = INITIAL_SALARY
    bribe_cost = INITIAL_BRIBE_COST
    current_day = 0
    
    # initialize list consisting of days vs. total salary earned for analysis
    days_vs_earnings = [(0, 0)]

    # Each iteration of this while loop simulates one bribe
    while current_day <= days_in_simulation:
        
        # check whether we have enough savings to bribe without waiting
        if earnings < bribe_cost:
        # advance current_day to day of next bribe (DO NOT INCREMENT BY ONE DAY)
            days = int(math.ceil((bribe_cost - earnings) / float(salary)))
            current_day += days
            earnings += salary * days
            total += salary * days    
            
        # update state of simulation to reflect bribe
        earnings -= bribe_cost
        salary += SALARY_INCREMENT
        bribe_cost += bribe_cost_increment
            
        # update list with days vs total salary earned for most recent bribe
        # use plot_type to control whether regular or log/log plot
        if plot_type is STANDARD:
            days_vs_earnings.append((current_day, total))
        else:
            days_vs_earnings.append((math.log(current_day), math.log(total)))

    return days_vs_earnings


def run_simulations():
    """
    Run simulations for several possible bribe increments
    """
    plot_type = STANDARD
    days = 70
    inc_0 = greedy_boss(days, 0, plot_type)
    inc_500 = greedy_boss(days, 500, plot_type)
    inc_1000 = greedy_boss(days, 1000, plot_type)
    inc_2000 = greedy_boss(days, 2000, plot_type)
    simpleplot.plot_lines("Greedy boss", 600, 600, "days", "total earnings", 
                          [inc_0, inc_500, inc_1000, inc_2000], False,
                         ["Bribe increment = 0", "Bribe increment = 500",
                          "Bribe increment = 1000", "Bribe increment = 2000"])

run_simulations()

print greedy_boss(35, 100)
print "should get:"
print [(0, 0), (10, 1000), (16, 2200), (20, 3400), (23, 4600), (26, 6100), (29, 7900), (31, 9300), (33, 10900), (35, 12700), (37, 14700)]

print
print greedy_boss(35, 0)
print "should get:"
print [(0, 0), (10, 1000), (15, 2000), (19, 3200), (21, 4000), (23, 5000), (25, 6200), (27, 7600), (28, 8400), (29, 9300), (30, 10300), (31, 11400), (32, 12600), (33, 13900), (34, 15300), (34, 15300), (35, 16900), (36, 18600)]
    

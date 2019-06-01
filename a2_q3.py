# START of a2_q3.py

#+----------------------------------------------------------------------------------------------+
#| QUESTION 3: Exact sloution																	|
#|		
#|
#|
#|
#+----------------------------------------------------------------------------------------------+

from csp import * 		# Import code from csp.py
from a2_q1 import *		# Import code from a2_q1.py. Effectively import rand_graph() sub-routine
from a2_q2 import *		# Import code from a2_q1.py. Effectively import check_teams() sub-routine

def generate_graphs():
	"""generate the 5 graphs as requested by the
	assignment description for this question"""
	graphs = [rand_graph(30, 0.1), rand_graph(30, 0.2), rand_graph(30, 0.3), rand_graph(30, 0.4), rand_graph(30, 0.5)]
	return graphs

# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def my_MapColoringCSP(colors, neighbors):
    """Make a CSP for the problem of coloring a map with different colors
    for any two adjacent regions. Arguments are a list of colors, and a
    dict of {region: [neighbor,...]} entries. This dict may also be
    specified as a string of the form defined by parse_neighbors."""

# !!!! Start of modification 1 by Siddharth
    # if isinstance(neighbors, str):
    #     neighbors = parse_neighbors(neighbors)
# End of modification 1 by Siddharth !!!!
    return CSP(list(neighbors.keys()), UniversalDict(colors), neighbors,
               different_values_constraint)

p = my_MapColoringCSP(range(5),rand_graph(5,0.5))
print(p.variables)
print(p.neighbors)
print(p.domains)
# END of a2_q3.py

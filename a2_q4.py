# START of a2_q4.py

#+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
#| QUESTION 4: Approximate solution 																																											|
#| 																																																		|
#| 	--> CITATIONS :-																																													|
#|		+ aima-code/aima-python : Textbook code in python from Github [ https://github.com/aimacode/aima-python]																						|
#|		+ python documentation : Genral usage and syntax for using python3 [ https://docs.python.org/3/ ]																								|
#|		+ Course website for CMPT310 : To get notes on CSP and Min-conflicts [ http://www.sfu.ca/~tjd/310summer2019/index.html ]																|
#|		+ Python library "openpyxl" : For making an Excel sheet using just python3  [ https://openpyxl.readthedocs.io/en/stable/ ]																		|
#|																																																		|
#| 	--> Implemented/Modified Fucntions:																																									|
#|		+ my_CSP class => created a child class from the CSP class in 'csp.py' to keep track of count of unassigned variables.																			|
#|		+ my_MapColoringCSP() => modified the code to not parse the neighbors argument as a string.																										|
#|		+ my_backtracking_search() => removed the assert statement.																																		|
#|		+ generate_graphs() => generate 5 graphs as instructed in the assignment description, with n=100 and p belonging to the set {0.1, 0.2, 0.3, 0.4, 0.5} and return them as a list.					|
#|		+ getChromaticNumber() => returns the number of colors used to color the given graph OR the number of teams the people in a friendship graph have been divided in to solve the Ice-Breaker Problem.	|
#|		+ run_q3() => runs the generate graph() function 5 times and solves the problems and prints out relevant data regarding the solutions.															|
#|		+ insert_into_cell() => writes data into the excel file at a specified cell location determined by row number and column number.																|
#|		+ q3_excel_sheet() => essentially the same thing as run_q3() but just writes raw data into an excel sheet named "a2_q3.xlsx" for each iterationa and solution.									|
#|																																																		|
#|	--> Usage:																																															|
#|		]=> running the 'run_q3()' subroutine will output data recorded/tracked for every graph for five iterations onto the console/terminal.															|
#|		]=> running the 'q3_excel_sheet' subroutine will output an excel file named "a2_q3.xlsx" in the same directory as this file with the data recorded/tracked.										|
#|																																																		|
#| 					!!!!!!!!!!! I generated the raw excel sheet and then syled/formatted it accordingly !!!!!!!!!!!																						|
#+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

from csp import * 		# Import code from csp.py
from a2_q1 import *		# Import code from a2_q1.py. Effectively import rand_graph() sub-routine
from a2_q2 import *		# Import code from a2_q2.py. Effectively import check_teams() sub-routine
import time 			# Import the time module to get running time for each instance of problem we solve
import openpyxl			# Import the library to automatically generate excel sheets for the recorded data


#__________________________TAKEN FROM csp.py and modified________________________________________

class my_CSP(CSP):
	def __init__(self, variables, domains, neighbors, constraints):
		CSP.__init__(self,variables,domains,neighbors,constraints)
		# MODIFIED to add a member variable to the class to get number of unassignments
		self.n_unassigns = 0

	def unassign(self, var, assignment):
		"""Remove {var: val} from assignment.
		DO NOT call this if you are changing a variable to a new value;
		just call assign for that."""
		if var in assignment:
			del assignment[var]
			self.n_unassigns += 1 # MODIFIED to increase the value of unassigned variables every time an unassignment takes place


# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def my_MapColoringCSP(colors, neighbors):
	"""Make a CSP for the problem of coloring a map with different colors
	for any two adjacent regions. Arguments are a list of colors, and a
	dict of {region: [neighbor,...]} entries. This dict may also be
	specified as a string of the form defined by parse_neighbors."""

# !!!! Start of modification 1 by Siddharth
	# if isinstance(neighbors, str):
	#	 neighbors = parse_neighbors(neighbors)
# End of modification 1 by Siddharth !!!!
	return my_CSP(list(neighbors.keys()), UniversalDict(colors), neighbors, different_values_constraint)

# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def my_min_conflicts(csp, max_steps=100000):
    """Solve a CSP by stochastic hillclimbing on the number of conflicts."""
    # Generate a complete assignment for all variables (probably with conflicts)
    csp.current = current = {}
    for var in csp.variables:
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    # Now repeatedly choose a random conflicted variable and change it
    for i in range(max_steps):
        conflicted = csp.conflicted_vars(current)
        if not conflicted:
            return current
        var = random.choice(conflicted)
        val = min_conflicts_value(csp, var, current)
        csp.assign(var, val, current)
    return None

# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def min_conflicts_value(csp, var, current):
    """Return the value that will give var the least number of conflicts.
    If there is a tie, choose at random."""
    return argmin_random_tie(csp.domains[var],
                             key=lambda val: csp.nconflicts(var, val, current))

#____________________________Implemented by Siddharth______________________________________________

def generate_graphs():
	"""generate the 5 graphs as requested by the
	assignment description for this question"""
	graphs = [rand_graph(100, 0.1), rand_graph(100, 0.2), rand_graph(100, 0.3), rand_graph(100, 0.4), rand_graph(100, 0.5)]
	return graphs

def getChromaticNumber(resDict):
	"""Gets the number of Colors in the result of backtracking search for the coloring problem CSP"""
	maxColor = 0
	for each in resDict.values():
		if each > maxColor:
			maxColor = each
	return (maxColor+1)

# END of a2_q4.py
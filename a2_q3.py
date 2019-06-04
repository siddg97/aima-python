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
	return my_CSP(list(neighbors.keys()), UniversalDict(colors), neighbors,
			   different_values_constraint)


# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def my_backtracking_search(csp,
						select_unassigned_variable,
						order_domain_values,
						inference):
	"""[Figure 6.5]"""

	def backtrack(assignment):
		if len(assignment) == len(csp.variables):
			return assignment
		var = select_unassigned_variable(assignment, csp)
		for value in order_domain_values(var, assignment, csp):
			if 0 == csp.nconflicts(var, value, assignment):
				csp.assign(var, value, assignment)
				removals = csp.suppose(var, value)
				if inference(csp, var, value, assignment, removals):
					result = backtrack(assignment)
					if result is not None:
						return result
				csp.restore(removals)
		csp.unassign(var, assignment)
		return None
	result = backtrack({})
	# assert result is None or csp.goal_test(result)
	return result
#_________________________________________________________________________________________________________________

#_______________________________________Implemented By SIDDHARTH__________________________________________________

def generate_graphs():
	"""generate the 5 graphs as requested by the
	assignment description for this question"""
	graphs = [rand_graph(30, 0.1), rand_graph(30, 0.2), rand_graph(30, 0.3), rand_graph(30, 0.4), rand_graph(30, 0.5)]
	return graphs

def getNumColors(resDict):
	"""Gets the number of Colors in the result of backtracking search for the coloring problem CSP"""
	maxColor = 0
	for each in resDict.values():
		if each > maxColor:
			maxColor = each
	return (maxColor+1)

def run_q3():
	for i in range(5):
		print('FOR ITERATION : '+ str(i+1))
		g = generate_graphs()
		gCount = 1
		for each in g:
			start_time = time.time()
			assigns = 0
			unassigns = 0
			for j in range(30):
				numColors = range(j)
				p = my_MapColoringCSP(numColors,each)
				res = my_backtracking_search(p,mrv,lcv,forward_checking)
				assigns+=p.nassigns
				unassigns+=p.n_unassigns
				if res != None and check_teams(each,res):
					elapsed_time = time.time() - start_time
					break
			print('For graph #'+str(gCount)+': \n===================================================================================================================')
			print(each)
			print('\nResults: \n===================================================================================================================')
			print(res)
			print('Time taken to find sloution: '+ str(elapsed_time))
			print('Number of varibales assigned: '+ str(assigns))
			print('Number of varibales unassigned: '+ str(unassigns))
			print('Is the result valid? ' + str(check_teams(each,res)))
			print('Number of teams(colors) required to solve the Ice-Breaker Problem for the given instance: ' + str(getNumColors(res)))
			print('===================================================================================================================\n')
			gCount+=1

wb = openpyxl.Workbook()	# Create a workbook in which an excel sheet will be created
sheet = wb.active			# create an active sheet in workbook
sheet.title = "Assignment2_Question3" # title of the sheet

def insert_into_cell(r,c,val):
	""" Inserts val in the cell at row r and column c """
	c = sheet.cell(row=r,column=c)
	c.value = val

def q3_excel_sheet():
	print('!!!!!! BUILDING EXCEL SHEET .............\n')
	sRow = 1	# sheet row index (global var)
	sCol = 1	# sheet column index (global var)
	insert_into_cell(sRow,sCol,'Assignment 2: Question 3 Data')
	sRow+= 2
	for i in range(5):
		insert_into_cell(sRow,sCol,'ITERATION #'+str(i+1))
		sRow+=1
		insert_into_cell(sRow,sCol,'Friendship graph #')
		sCol+=1
		insert_into_cell(sRow,sCol,'Number of People/Nodes [n]')
		sCol+=1
		insert_into_cell(sRow,sCol,'Probability of Friendship [p]')
		sCol+=1
		insert_into_cell(sRow,sCol,'Time taken to solve Ice-breaker Problem [seconds]')
		sCol+=1
		insert_into_cell(sRow,sCol,'Number of Variables Assigned')
		sCol+=1
		insert_into_cell(sRow,sCol,'Number of Variables Unassigned')
		sCol+=1
		insert_into_cell(sRow,sCol,'Number of Teams/Colors')
		sRow+=1
		graphs = generate_graphs()
		gNum = 1
		gProb = 0.1
		for each in graphs:
			start_time = time.time()
			steps = 1
			assigns=0
			unassigns=0
			sCol = 1
			for j in range(30):
				colors = range(j)
				p = my_MapColoringCSP(colors,each)
				res = my_backtracking_search(p,mrv,lcv,forward_checking)
				assigns+=p.nassigns
				unassigns+=p.n_unassigns
				if res != None and check_teams(each,res):
					elapsed_time = time.time() - start_time
					break
				else:
					steps += 1
			insert_into_cell(sRow,sCol,gNum)
			sCol+=1
			insert_into_cell(sRow,sCol,30)
			sCol+=1
			insert_into_cell(sRow,sCol,gProb)
			sCol+=1
			insert_into_cell(sRow,sCol,elapsed_time)
			sCol+=1
			insert_into_cell(sRow,sCol,assigns)
			sCol+=1
			insert_into_cell(sRow,sCol,unassigns)
			sCol+=1
			insert_into_cell(sRow,sCol,getNumColors(res))
			sCol=1
			sRow+=1
			gProb+=0.1
			gNum+=1
		sRow+=5
	wb.save('a2_q3.xlsx')
	print('DATA RECORDED IN "a2_q3.xlsx" IN THE ROOT DIRECTORY !!!!!!')



run_q3()

#q3_excel_sheet()

# END of a2_q3.py

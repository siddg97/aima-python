# START of a2_q3.py

#+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
#| QUESTION 3: Exact solution 																																											|
#| 																																																		|
#| 	--> CITATIONS :-																																													|
#|		+ aima-code/aima-python : Textbook code in python from Github [ https://github.com/aimacode/aima-python]																						|
#|		+ python documentation : Genral usage and syntax for using python3 [ https://docs.python.org/3/ ]																								|
#|		+ Course website for CMPT310 : To get notes on CSPs and backtracking search [ http://www.sfu.ca/~tjd/310summer2019/index.html ]																|
#|		+ Python library "openpyxl" : For making an Excel sheet using just python3  [ https://openpyxl.readthedocs.io/en/stable/ ]																		|
#|																																																		|
#| 	--> Implemented/Modified Fucntions:																																									|
#|		+ my_CSP class => created a child class from the CSP class in 'csp.py' to keep track of count of unassigned variables.																			|
#|		+ my_MapColoringCSP() => modified the code to not parse the neighbors argument as a string.																										|
#|		+ my_backtracking_search() => removed the assert statement.																																		|
#|		+ generate_graphs() => generate 5 graphs as instructed in the assignment description, with n=30 and p belonging to the set {0.1, 0.2, 0.3, 0.4, 0.5} and return them as a list.					|
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
def my_backtracking_search(csp, select_unassigned_variable, order_domain_values, inference):

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
	# MODIFICATION - START
	# assert result is None or csp.goal_test(result)
	# MODIFICATION - END
	return result
#_________________________________________________________________________________________________________________

#_______________________________________Implemented By SIDDHARTH__________________________________________________

def generate_graphs():
	"""generate the 5 graphs as requested by the
	assignment description for this question"""
	graphs = [rand_graph(30, 0.1), rand_graph(30, 0.2), rand_graph(30, 0.3), rand_graph(30, 0.4), rand_graph(30, 0.5)]
	return graphs

def getChromaticNumber(resDict):
	"""Gets the number of Colors in the result of backtracking search for the coloring problem CSP"""
	maxColor = 0
	for each in resDict.values():
		if each > maxColor:
			maxColor = each
	return (maxColor+1)

def run_q3():
	for i in range(5):
		print('+------------------+')
		print('| FOR ITERATION #'+ str(i+1)+' |')
		print('+------------------+\n')
		g = generate_graphs()
		gCount = 1
		for each in g:
			start_time = time.time()
			assigns = 0
			unassigns = 0
			for j in range(30):
				numColors = range(j+1)
				p = my_MapColoringCSP(numColors,each)
				res = my_backtracking_search(p,mrv,lcv,forward_checking)
				assigns+=p.nassigns
				unassigns+=p.n_unassigns
				if res != None and check_teams(each,res):
					elapsed_time = time.time() - start_time
					break
			print('For Graph #'+str(gCount))
			print('===================================================================================================================')
			print('Time taken to find sloution: '+ str(elapsed_time))
			print('Number of varibales assigned: '+ str(assigns))
			print('Number of varibales unassigned: '+ str(unassigns))
			print('Is the result valid? ' + str(check_teams(each,res)))
			print('Number of teams(chromatic number) required to solve the Ice-Breaker Problem for the given instance: ' + str(getChromaticNumber(res)))
			print('===================================================================================================================\n')
			gCount+=1

# Code to initialize hte excel workbook to write data into
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
		insert_into_cell(sRow,sCol,'Number of Teams or Chromatic Number')
		sRow+=1
		graphs = generate_graphs()
		gNum = 1
		gProb = 0.1
		for each in graphs:
			start_time = time.time()
			assigns=0
			unassigns=0
			sCol = 1
			for j in range(30):
				colors = range(j+1)
				p = my_MapColoringCSP(colors,each)
				res = my_backtracking_search(p,mrv,lcv,forward_checking)
				assigns+=p.nassigns
				unassigns+=p.n_unassigns
				if res != None and check_teams(each,res):
					elapsed_time = time.time() - start_time
					break
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
			insert_into_cell(sRow,sCol,getChromaticNumber(res))
			sCol=1
			sRow+=1
			gProb+=0.1
			gNum+=1
		sRow+=5
	wb.save('a2_q3.xlsx')
	print('DATA RECORDED IN "a2_q3.xlsx" IN THE ROOT DIRECTORY !!!!!!')



run_q3()
# q3_excel_sheet()


# END of a2_q3.py
#+--------------------------------------------------------------------------------------------------------------------------------------+
#| Assignment 1 : CMPT 310 - Summer 2019 - Toby Donaldson																				|
#| Author: Siddharth Gupta - SFU ID: 301327469																							|
#|																																		|
#|	CITATIONS :-																														|
#|		- aima-code/aima-python : Textbook code in python from Github [ https://github.com/aimacode/aima-python]						|
#|		- python documentation : Genral usage and syntax for using python3 [ https://docs.python.org/3/ ]								|
#|		- Course website for CMPT310 : To get notes on search methods and heuristics [ http://www.sfu.ca/~tjd/310summer2019/index.html ]|							|
#+--------------------------------------------------------------------------------------------------------------------------------------+

#	a1.py

from search import *
import numpy as np    	# used in aima-code/aima-python as a library
import time   		  	# importing time for timing heuristics
import random			# for generating random integers
import xlwt				# for generating outputs in the excel file directly from executing a1.py
wb = xlwt.Workbook()	# create a workbook from the xlwt module

style = xlwt.easyxf('font: bold 1;')
headstyle = xlwt.easyxf('font: bold 1, color red;')
qstyle = xlwt.easyxf('font: bold 1, color blue;')
# sheet.write(2,0,'MISSING TILE HEURISTIC')
# sheet.write(0,0,'Q2: EightPuzzle Problem Statistics')
# sheet.write(4,0,'Problem Number')
# sheet.write(4,1,'Time Taken to complete')
# sheet.write(4,2,'Number of Nodes Removed')
# sheet.write(4,3,'Length of Solution Path')

#+----------------------------------------------------------------------------------------------------------------------------------------------+
#| Q1 - Made 2 helper functions:																												|
#| 			(i)  make_rand_8puzzle() 	- returns an instance of the EightPuzzle class object with a random initial state that is solvable		|
#|			(ii) display(state)			- prints the array 'state' in the format of the eight puzzle on the console with 0 being the empty tile	|
#+----------------------------------------------------------------------------------------------------------------------------------------------+

# make_rand_8puzzle implementation :
def make_rand_8puzzle():
	goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)	# this is our final goal to be achieved for every instance of this problem
	while True:			# Keep generating random initial state till state is a solvable one
		state = tuple(np.random.choice(range(9), 9, replace=False))	# get the random initial state
		puzzle = EightPuzzle(state, goal)	# create an instance of the problem with the initial state and the end goal
		if puzzle.check_solvability(puzzle.initial):
			break
	return puzzle

# display(state) implemetation :
def display(state):
	row1 = " "		# string representing row 1
	row2 = " "		# string representing row 2
	row3 = " "		# string representing row 3
	for i in range(9):
		if i <= 2:
			if state[i] == 0:	# check if 0 => add * to row1
				row1 += "* "
			else:				# add the number
				row1 += str(state[i]) + " "
		elif i > 2 and i <= 5:
			if state[i] == 0:	# check if 0 => add * to row2
				row2 += "* "
			else:				# add the number
				row2 += str(state[i]) + " "
		else:
			if state[i] == 0:	# check if 0 => add * to row3
				row3 += "* "
			else:				# add the number
				row3 += str(state[i]) + " "
	print(row1 + "\n" + row2 + "\n" + row3 + "\n")

#+----------------------------------------------------------------------------------------------------------------------------------+
#| Q2 -	Created 20 instances of the 8puzzle problem and used the tree algorithms used to solve them and recorded the following data	| 
#|			- Algorithms used are :																									|
#|				(1) astar_search() using the h1() function [ h1() function is the misplaced tile heuristic ]						|
#|				(2) astar_search() using the h2() function [ h2() function is the Manhattan distance heuristic ]					|
#|				(3) astar_search() using the h3() function [ h3() function is simply the max(h1(),h2()) heuristic ]					|
#|			- Data recorded for every algortithm listed above:																		|
#|				i.   Total running time [ seconds ]																					|
#|				ii.  Length of solution [ path length of reaching from the root node to the gol node ]								|
#|				iii. Number of nodes removed from frontier 																			|
#|				iv.  Final state of node 																							|
#| 																																	|
#| *****Each algorithm was run on the exact same set of problems to make the comparision unbiassed*****								|
#+----------------------------------------------------------------------------------------------------------------------------------+


# MISSING TILE HEURISTIC
def h1(node):
	x = 0
	for i in range(9):
		if node.state[i] != i+1 and node.state[i] != 0:
			x += 1
	return x

# 	MANHATTAN HEURISTIC Helper Functions
def rowCoord(y):
	return int((y-1)/3)

def colCoord(x):
	if x % 3 != 0:
		return x % 3
	else:
		return 3

# MANHATTAN HEURISTIC FUNCTION
def h2(node):
	mDistances = [0, 0, 0, 0, 0, 0, 0, 0, 0]
	for i in range(9):
		if node.state[i] != i+1 and node.state[i] != 0:
			mDistances[i] = abs(rowCoord(node.state[i]) - rowCoord(i+1)) + abs(colCoord(node.state[i]) - colCoord(i+1))
	return sum(mDistances)

# Max of Missing tile and Manhattan heuristic FUNCTION
def h3(node):
	return max(h1(node),h2(node))

# Creates n instances of the 8puzzle then returns a tuple of them.
def listOfPuzzles(n):
	p = []
	for i in range(n):	# loop creates an instance of a puzzle and runs from i=0 to i=(n-1)
		instance = make_rand_8puzzle()
		p.append(instance) # add instance to tuple
	return p

# USED THESE FUNCTIONS TO GENERATE DATA FOR THE ALGORITHMS. THEY ARE MODIFIED VERSIONS OF astar_search() and best_fit_graph_search() from search.py
#		MODIFICATION ARE MARKED as the code marked b/w the "# !!! MODIFICATION(n) BY SIDDHARTH GUPTA: Start" and the "# MODIFICATION(n) BY SIDDHARTH GUPTA: End !!!" where n is the nth modification


# modified the original astar_search() function in search.py file -- !!! USE THIS INSTEAD OF THE search.py version !!!
def My_astar_search(problem, h=None):
	"""A* search is best-first graph search with f(n) = g(n)+h(n).
	You need to specify the h function when you call astar_search, or
	else in your Problem subclass."""
	h = memoize(h or problem.h, 'h')
	return My_best_first_graph_search(problem, lambda n: n.path_cost + h(n))

# modified the original best_fit_graph_search() function in search.py file -- !!! USE THIS INSTEAD OF THE search.py version !!!
def My_best_first_graph_search(problem, f):	
	# Modification made:
	#	recordes the number of nodes removed and the length of the solution and returns a tuple of the form ( nodesRemoved, length)
	f = memoize(f, 'f')
	node = Node(problem.initial)
	frontier = PriorityQueue('min', f)
	frontier.append(node)
	explored = set()
	#!!! MODIFICATION(1) BY SIDDHARTH GUPTA: Start
	nodesRemoved = 0
	# MODIFICATION(1) BY SIDDHARTH GUPTA: End !!!
	while frontier:
		node = frontier.pop()
		#!!! MODIFICATION(2) BY SIDDHARTH GUPTA: Start
		nodesRemoved += 1
		# MODIFICATION(2) BY SIDDHARTH GUPTA: End !!!
		if problem.goal_test(node.state):
		#!!! MODIFICATION(3) BY SIDDHARTH GUPTA: Start
			return (node,nodesRemoved,node.depth)
		# MODIFICATION(3) BY SIDDHARTH GUPTA: End !!!
		explored.add(node.state)
		for child in node.expand(problem):
			if child.state not in explored and child not in frontier:
				frontier.append(child)
			elif child in frontier:
				if f(child) < frontier[child]:
					del frontier[child]
					frontier.append(child)
	return None

# prints data for each of the n instances of the 8puzzle.
def getData(n):
	p = listOfPuzzles(n)
	# Data for MISSING TILE HEURISTICS
	i = 1
	print(" MISSING TILE HEURISTIC:\n")
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h1)
		elapsed_time = time.time() - start_time
		print("===========================================\n")
		print("For problem "+str(i)+" :\n")
		print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		print("   Nodes removed: " + str(d[1])+"\n")
		print("   Length of path: "+ str(d[2])+"\n")
		display(d[0].state)
		print("===========================================\n")
		i += 1
	print("\n")
	print(" MANHATTAN HEURISTIC:\n")
	i = 1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h2)
		elapsed_time = time.time() - start_time
		print("===========================================\n")
		print("For problem "+str(i)+" :\n")
		print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		print("   Nodes removed: " + str(d[1])+"\n")
		print("   Length of path: "+ str(d[2])+"\n")
		display(d[0].state)
		print("===========================================\n")
		i += 1
	print("\n")
	print(" max(MANHATTAN, MISSING TILE) HEURISTIC:\n")
	i = 1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h3)
		elapsed_time = time.time() - start_time
		print("===========================================\n")
		print("For problem "+str(i)+" :\n")
		print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		print("   Nodes removed: " + str(d[1])+"\n")
		print("   Length of path: "+ str(d[2])+"\n")
		display(d[0].state)
		print("===========================================\n")
		i += 1


#+----------------------------------------------------------------------------------------------------------------------------------+
#| Q3 -	Created 20 instances of the ypuzzle problem and used the three algorithms used to solve them and recorded the following data| 
#|			- Algorithms used are :																									|
#|				(1) astar_search() using the h1() function [ h1() function is the misplaced tile heuristic ]						|
#|				(2) astar_search() using the h2() function [ h2() function is the Manhattan distance heuristic ]					|
#|				(3) astar_search() using the h3() function [ h3() function is simply the max(h1(),h2()) heuristic ]					|
#|			- Data recorded for every algortithm listed above:																		|
#|				i.   Total running time [ seconds ]																					|
#|				ii.  Length of solution [ path length of reaching from the root node to the gol node ]								|
#|				iii. Number of nodes removed from frontier 																			|
#|				iv.  Final state of goal node 																						|
#| 																																	|
#| *****Each algorithm was run on the exact same set of problems to make the comparision unbiassed*****								|
#+----------------------------------------------------------------------------------------------------------------------------------+

class Ypuzzle(Problem):

	# Constructor
	def __init__(self, initial, goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)):
		self.goal = goal
		Problem.__init__(self, initial, goal)

	# get blank tile index
	def find_blank_square(self,state):
		return state.index(0)

	# get all possible actions for a given state
	def actions(self,state):
		potentialActions = []
		blankIndex = self.find_blank_square(state)

		if blankIndex == 0:
			potentialActions = ['DOWNX']
		elif blankIndex == 1:
			potentialActions = ['DOWN']
		elif blankIndex == 8:
			potentialActions = ['UPY']
		elif blankIndex == 5:
			potentialActions = ['UP','RIGHT']
		elif blankIndex == 2:
			potentialActions = ['UPY','DOWN','RIGHT']
		elif blankIndex == 3:
			potentialActions = ['DOWN','RIGHT','LEFT']
		elif blankIndex == 4:
			potentialActions = ['UP','DOWN','LEFT']
		elif blankIndex == 6:
			potentialActions = ['UP','DOWNX','LEFT','RIGHT']
		else:
			potentialActions = ['UP','LEFT']

		return potentialActions

	# check if solution is achieved
	def goal_test(self, state):
		return state == self.goal

	# takes current state and action => returns applied action state
	def result(self, state, action):
		blank = self.find_blank_square(state)
		nextState = list(state)

		delta = {'LEFT':-1, 'RIGHT':1, 'UPY':-2, 'UP':-3, 'DOWN':3, 'DOWNX':2}
		neighbor = blank + delta[action]
		nextState[blank], nextState[neighbor] = nextState[neighbor], nextState[blank]
		return tuple(nextState)
		

# makes an instance of the YPuzlle and gives it an initial solvable state.
def make_rand_ypuzzle():
	goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)	# this is our final goal to be achieved for every instance of this problem
	state = (1,2,3,4,5,6,0,8,7)			# a solvable state
	yp = Ypuzzle(state)
	randomNumberOfMoves = random.randint(0,100000) # perform 100000 random moves to a solvable state to get an initial state that is guaranteed to be solvable
	for i in range(randomNumberOfMoves):
		actions = yp.actions(yp.initial)
		actionNumber = random.randint(0,len(actions)-1)
		nState = yp.result(yp.initial,actions[actionNumber])
		yp = Ypuzzle(nState)
	return yp


# MANHATTAN HEURISTIC: Implemented for Ypuzzle with a 4x3 grid with (0,1), (3,0) and (3,2) are not being used.
def h4(node):
	state = node.state
	goalIndex = {0:[2,2], 1:[0,0], 2:[4,0], 3:[1,0], 4:[2,0], 5:[3,0], 6:[1,1], 7:[2,1], 8:[3,1]}
	stateIndex = {}
	index = [[0,0], [4,0], [1,0], [2,0], [3,0], [1,1], [2,1], [3,1], [2,2]]
	for i in range(len(state)):
		stateIndex[state[i]] = index[i]
	mDistance = 0
	for i in range(1,9):
		for j in range(2):
			mDistance += abs(goalIndex[i][j] - stateIndex[i][j])
	return mDistance

# YPUZZLE max(missing tile, manhattan)
def h5(node):
	return max(h1(node),h4(node))


# HELPER FUNCTIONS FOR Ypuzzle 


# Prints the state of the Ypuzzle to the console
def displayY(state):
	r1 = ""
	r2 = ""
	r3 = ""
	r4 = "  "
	for i in range(len(state)):
		num = str(state[i])
		if state[i] == 0:
			num = "*"
		if i == 0:
			r1 += num+"   "
		elif i == 1:
			r1 += num
		elif i >= 2 and i <= 4:
			r2 += num + " "
		elif i >= 5 and i <= 7:
			r3 += num + " "
		else:
			r4 += num
	print(r1 + "\n" + r2 + "\n" + r3 + "\n" + r4)


# Creates n instances of the Ypuzzle then returns a tuple of them.
def listOfYPuzzles(n):
	p = []
	for i in range(n):	# loop creates an instance of a puzzle and runs from i=0 to i=(n-1)
		instance = make_rand_ypuzzle()
		p.append(instance) # add instance to tuple
	return p

# prints data for each of the n instances of the Ypuzzle on the console
def getYData(n):
	p = listOfYPuzzles(n)
	# Data for MISSING TILE HEURISTICS
	i = 1
	print(" MISSING TILE HEURISTIC:\n")
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h1)
		elapsed_time = time.time() - start_time
		print("===========================================\n")
		print("For problem "+str(i)+" :\n")
		print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		print("   Nodes removed: " + str(d[1])+"\n")
		print("   Length of path: "+ str(d[2])+"\n")
		displayY(d[0].state)
		print("===========================================\n")
		i += 1
	print("\n")
	print(" MANHATTAN HEURISTIC:\n")
	i = 1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h4)
		elapsed_time = time.time() - start_time
		print("===========================================\n")
		print("For problem "+str(i)+" :\n")
		print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		print("   Nodes removed: " + str(d[1])+"\n")
		print("   Length of path: "+ str(d[2])+"\n")
		displayY(d[0].state)
		print("===========================================\n")
		i += 1
	print("\n")
	print(" max(MANHATTAN, MISSING TILE) HEURISTIC:\n")
	i = 1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h5)
		elapsed_time = time.time() - start_time
		print("===========================================\n")
		print("For problem "+str(i)+" :\n")
		print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		print("   Nodes removed: " + str(d[1])+"\n")
		print("   Length of path: "+ str(d[2])+"\n")
		displayY(d[0].state)
		print("===========================================\n")
		i += 1	



def makeExcelSheet(n):
	sheet = wb.add_sheet("CMPT310_Assignment_1")
	print('!!!!!	Starting to generate a1.xlsx file 	!!!!!\n')
	sheet.write(2,0,'MISSING TILE HEURISTIC',headstyle)
	sheet.write(0,0,'Q2: EightPuzzle Problem Statistics',qstyle)
	sheet.write(4,0,'Problem Number',style)
	sheet.write(4,1,'Time Taken to complete',style)
	sheet.write(4,2,'Number of Nodes Removed',style)
	sheet.write(4,3,'Length of Solution Path',style)
	p = listOfPuzzles(n)
	print('	Recording data for MISSING TILE HEURISTIC for the EightPuzzle Problem........')
	# Data for MISSING TILE HEURISTICS
	i = 1
	sIndex = 5
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h1)
		elapsed_time = time.time() - start_time
		sheet.write(sIndex,0,i)					# print("For problem "+str(i)+" :\n")
		sheet.write(sIndex,1,elapsed_time)		# print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		sheet.write(sIndex,2,d[1])				# print("   Nodes removed: " + str(d[1])+"\n")
		sheet.write(sIndex,3,d[2])				# print("   Length of path: "+ str(d[2])+"\n")
		sIndex += 1
		i += 1
	print('	Wrote data for MISSING TILE HEURISTIC for the EightPuzzle Problem!')
	print('	Recording data for MANHATTAN HEURISTIC for the EightPuzzle Problem........')
	# Data for MANHATTAN HEURISTIC
	sIndex +=2
	sheet.write(sIndex,0,'MANHATTAN HEURISTIC',headstyle)
	sIndex += 2
	sheet.write(sIndex,0,'Problem Number',style)
	sheet.write(sIndex,1,'Time Taken to complete',style)
	sheet.write(sIndex,2,'Number of Nodes Removed',style)
	sheet.write(sIndex,3,'Length of Solution Path',style)
	i = 1
	sIndex += 1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h2)
		elapsed_time = time.time() - start_time
		sheet.write(sIndex,0,i)					# print("For problem "+str(i)+" :\n")
		sheet.write(sIndex,1,elapsed_time)		# print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		sheet.write(sIndex,2,d[1])				# print("   Nodes removed: " + str(d[1])+"\n")
		sheet.write(sIndex,3,d[2])				# print("   Length of path: "+ str(d[2])+"\n")
		sIndex += 1
		i += 1
	print('	Wrote data for MANHATTAN HEURISTIC for the EightPuzzle Problem!')
	print('	Recording data for max(MANHATTAN, MISSING TILE) HEURISTIC for the EightPuzzle Problem........')
	i = 1
	sIndex +=2
	sheet.write(sIndex,0,'max(MANHATTAN, MISSING TILE) HEURISTIC',headstyle)
	sIndex += 2
	sheet.write(sIndex,0,'Problem Number',style)
	sheet.write(sIndex,1,'Time Taken to complete',style)
	sheet.write(sIndex,2,'Number of Nodes Removed',style)
	sheet.write(sIndex,3,'Length of Solution Path',style)
	sIndex +=1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h3)
		elapsed_time = time.time() - start_time
		sheet.write(sIndex,0,i)					# print("For problem "+str(i)+" :\n")
		sheet.write(sIndex,1,elapsed_time)		# print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		sheet.write(sIndex,2,d[1])				# print("   Nodes removed: " + str(d[1])+"\n")
		sheet.write(sIndex,3,d[2])				# print("   Length of path: "+ str(d[2])+"\n")
		sIndex += 1
		i += 1
	print('	Wrote data for max(MANHATTAN, MISSING TILE) HEURISTIC for the EightPuzzle Problem!')

	sIndex +=3
	sheet.write(sIndex,0,'Q3: YPuzzle Problem Statistics',qstyle)
	sIndex += 2
	sheet.write(sIndex,0,'MISSING TILE HEURISTIC',headstyle)
	sIndex += 2
	sheet.write(sIndex,0,'Problem Number')
	sheet.write(sIndex,1,'Time Taken to complete',style)
	sheet.write(sIndex,2,'Number of Nodes Removed',style)
	sheet.write(sIndex,3,'Length of Solution Path',style)
	p = listOfYPuzzles(n+10)
	print('	Recording data for MISSING TILE HEURISTIC for the YPuzzle Problem........')
	# Data for MISSING TILE HEURISTICS
	i = 1
	sIndex +=1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h1)
		elapsed_time = time.time() - start_time
		sheet.write(sIndex,0,i)					# print("For problem "+str(i)+" :\n")
		sheet.write(sIndex,1,elapsed_time)		# print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		sheet.write(sIndex,2,d[1])				# print("   Nodes removed: " + str(d[1])+"\n")
		sheet.write(sIndex,3,d[2])				# print("   Length of path: "+ str(d[2])+"\n")
		sIndex += 1
		i += 1
	print('	Wrote data for MISSING TILE HEURISTIC for the YPuzzle Problem!')
	print('	Recording data for MANHATTAN HEURISTIC for the YPuzzle Problem........')
	# Data for MANHATTAN HEURISTIC
	sIndex +=2
	sheet.write(sIndex,0,'MANHATTAN HEURISTIC',headstyle)
	sIndex += 2
	sheet.write(sIndex,0,'Problem Number',style)
	sheet.write(sIndex,1,'Time Taken to complete',style)
	sheet.write(sIndex,2,'Number of Nodes Removed',style)
	sheet.write(sIndex,3,'Length of Solution Path',style)
	i = 1
	sIndex += 1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h4)
		elapsed_time = time.time() - start_time
		sheet.write(sIndex,0,i)					# print("For problem "+str(i)+" :\n")
		sheet.write(sIndex,1,elapsed_time)		# print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		sheet.write(sIndex,2,d[1])				# print("   Nodes removed: " + str(d[1])+"\n")
		sheet.write(sIndex,3,d[2])				# print("   Length of path: "+ str(d[2])+"\n")
		sIndex += 1
		i += 1
	print('	Wrote data for MANHATTAN HEURISTIC for the YPuzzle Problem!')
	print('	Recording data for max(MANHATTAN, MISSING TILE) HEURISTIC for the YPuzzle Problem........')
	i = 1
	sIndex +=2
	sheet.write(sIndex,0,'max(MANHATTAN, MISSING TILE) HEURISTIC',headstyle)
	sIndex += 2
	sheet.write(sIndex,0,'Problem Number',style)
	sheet.write(sIndex,1,'Time Taken to complete',style)
	sheet.write(sIndex,2,'Number of Nodes Removed',style)
	sheet.write(sIndex,3,'Length of Solution Path',style)
	sIndex +=1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h5)
		elapsed_time = time.time() - start_time
		sheet.write(sIndex,0,i)					# print("For problem "+str(i)+" :\n")
		sheet.write(sIndex,1,elapsed_time)		# print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		sheet.write(sIndex,2,d[1])				# print("   Nodes removed: " + str(d[1])+"\n")
		sheet.write(sIndex,3,d[2])				# print("   Length of path: "+ str(d[2])+"\n")
		sIndex += 1
		i += 1
	print('	Wrote data for max(MANHATTAN, MISSING TILE) HEURISTIC for the YPuzzle Problem!')
	wb.save("a1.xlsx")
	print('!!!!!	EXCEL DATA WRITTEN FOR Q2	!!!!!\n')




makeExcelSheet(2)


#+------------------------------------------------------------------------------------------------------------------+
#| Assignment 1 : CMPT 310 - Summer 2019 - Toby Donaldson															|
#| Author: Siddharth Gupta - SFU ID: 301327469																		|
#|																													|
#|	CITATIONS :-																									|
#|		- aima-code/aima-python : Textbook code in python from Github [ https://github.com/aimacode/aima-python]	|
#|		- python documentation : Genral usage and syntax for using python3 [ https://docs.python.org/3/ ]			|
#|		- 																											|
#+------------------------------------------------------------------------------------------------------------------+

#	a1.py

from search import *
import numpy as np    	# used in aima-code/aima-python as a library
import time   		  	# importing time for timing heuristics



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
	# puzzle = EightPuzzle((5,1,6,2,0,3,7,4,8),goal)
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
			mDistances[i] = abs(rowCoord(node.state[i] - rowCoord(i+1)) + abs(colCoord(node.state[i]) - colCoord(i+1)))
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
			return (nodesRemoved,node.depth)
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
		print("   Nodes removed: " + str(d[0])+"\n")
		print("   Length of path: "+ str(d[1])+"\n")
		print("===========================================\n")
		i += 1
	print(" MANHATTAN HEURISTIC:\n")
	i = 1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h2)
		elapsed_time = time.time() - start_time
		print("===========================================\n")
		print("For problem "+str(i)+" :\n")
		print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		print("   Nodes removed: " + str(d[0])+"\n")
		print("   Length of path: "+ str(d[1])+"\n")
		print("===========================================\n")
		i += 1
	print(" max(MANHATTAN, MISSING TILE) HEURISTIC:\n")
	i = 1
	for each in p:
		start_time = time.time()
		d = My_astar_search(each,h3)
		elapsed_time = time.time() - start_time
		print("===========================================\n")
		print("For problem "+str(i)+" :\n")
		print("   Time [in seconds]: "+ str(elapsed_time)+"\n")
		print("   Nodes removed: " + str(d[0])+"\n")
		print("   Length of path: "+ str(d[1])+"\n")
		print("===========================================\n")
		i += 1


   	


# p = make_rand_8puzzle()
# display(p.initial)
# print('/n/nrunnning a*search....\n')
# astar_search(p)

getData(5)
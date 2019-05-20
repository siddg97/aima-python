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
#| Q1 - Make 2 helper functions:																												|
#| 			(i)  make_rand_8puzzle() 	- returns an instance of the EightPuzzle class object with a random initial state that is solvable		|
#|			(ii) display(state)			- prints the array 'state' in the format of the eight puzzle on the console with 0 being the empty tile	|
#+----------------------------------------------------------------------------------------------------------------------------------------------+

# make_rand_8puzzle implementation :
def make_rand_8puzzle():
	goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)	# this is our final goal to be achieved for every instance of this problem
	# while True:			# Keep generating random initial state till state is a solvable one
	# 	state = tuple(np.random.choice(range(9), 9, replace=False))	# get the random initial state
	# 	puzzle = EightPuzzle(state, goal)	# create an instance of the problem with the initial state and the end goal
	# 	if puzzle.check_solvability(puzzle.initial):
	# 		break
	puzzle = EightPuzzle((5,1,6,2,0,3,7,4,8),goal)
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

#+----------------------------------------------+
#| Q2 -											| 
#|												|
#|												|
#|												|
#+----------------------------------------------+

def h1(puzzle):
	x = 0
	for i in range(9):
		if puzzle.state[i] != i+1 and puzzle.state[i] != 0:
			x += 1
	return x

	


def myTiming():
   start_time = time.time()
   # goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)
   # p = EightPuzzle((5,1,6,2,0,3,7,4,8),goal)	# make an instance of problem
   p = make_rand_8puzzle()
   display(p.initial)
   astar_search(p, h1)
   print(p)
   elapsed_time = time.time() - start_time

   print('elapsed time (in seconds):'+ str(elapsed_time))


# p = make_rand_8puzzle()
# display(p.initial)
# print('/n/nrunnning a*search....\n')
# astar_search(p)

myTiming()
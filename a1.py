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
import numpy as np    # used in aima-code/aima-python as a library



#+----------------------------------------------------------------------------------------------------------------------------------------------+
#| Q1 - Make 2 helper functions:																												|
#| 			(i)  make_rand_8puzzle() 	- returns an instance of the EightPuzzle class object with a random initial state that is solvable		|
#|			(ii) display(state)			- prints the array 'state' in the format of the eight puzzle on the console with 0 being the empty tile	|
#+----------------------------------------------------------------------------------------------------------------------------------------------+

# make_rand_8puzzle implementation :
def make_rand_8puzzle():
	goal=(1, 2, 3, 4, 5, 6, 7, 8, 0)	# this is our final goal to be achieved for every instance of this problem
	while True:			# Keep generating random initial state till state is a solvable one
		state = np.random.choice(range(9), 9, replace=False)	# get the random initial state
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

#+----------------------------------------------+
#| Q2 -											| 
#|												|
#|												|
#|												|
#+----------------------------------------------+


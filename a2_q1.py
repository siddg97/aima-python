# START of a2_q1.py 

#+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
#| QUESTION 1: Erdos-Renyi random graphs:																																																							|
#|		- Implemented function rand_graph(n,p) which returns a new random graph with n nodes.																																										|
#|		- Each node is named from 0 to (n-1).																																																						|
#|		- every pair of nodes have an edge b/w them according to probability p.																																														|
#|		- Assumptions:																																																												|
#|			1. n > 1																																																												|
#|			2. 0 <= p <= 1																																																											|
#| 	--> CITATIONS :-																																																												|
#|		+ aima-code/aima-python : Textbook code in python from Github [ https://github.com/aimacode/aima-python]																																					|
#|		+ python documentation : Genral usage and syntax for using python3 [ https://docs.python.org/3/ ]																																							|
#|		+ Course website for CMPT310 : To get notes on CSPs and backtracking search [ http://www.sfu.ca/~tjd/310summer2019/index.html ]																																|
#|		+ Erdos-Renyi Graph Psuedo-code: ALgorithm to create an Erdos renyi graph [ https://stackoverflow.com/questions/54270647/create-an-erdos-renyi-graph-using-class-objects-in-python?fbclid=IwAR2nfpi1K35AIkXpx0Jbw3YGq0YyeJIRCNcmr_AmfUpsIzHKTz5vKZAdhxE ]	|
#| Libraries/Modules used:																																																											|
#|		1. random module - from the standard python library																																																			|
#+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

import random

def rand_graph(n,p):
	g = dict()	# empty dictionary
	for i in range(n):	# for every person (named as i) initialize an empty list
		g[i] = []		
	for person in range(n-1):	# for every single person in the graph
		for other_person in range(person+1,n): # for every other person
			a = random.random()
			if a <= p:
				g[person].append(other_person)
				g[other_person].append(person)
	return g
# END of a2_q1.py
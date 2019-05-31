# START of a2_q2.py

#+------------------------------------------------------------------------------+
#| QUESTION 2:																	|
#|		- Implemented function check_teams(graph,csp_sol) function.				|
#|		- Returns true if csp_sol satisfies all constraints. Else return false	|
#+------------------------------------------------------------------------------+


def check_teams(graph, csp_sol):
	n = len(graph)	# number of people
	for person in range(n-1):	# for every person in the friendship graph
		for other_person in range(person+1,n):	# for evry other person in the friendship graph
			if csp_sol[person] == csp_sol[other_person] and other_person in graph[person]:	# if both the person and other person are in the same group in csp_sol and are friends on the friendship graph
				return False
	return True


# END of a2_q2.py
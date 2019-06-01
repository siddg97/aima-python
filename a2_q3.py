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
import time 			# Import the time module to get running time for each instance of problem we solve

#__________________________TAKEN FROM csp.py and modified________________________________________

class my_CSP(search.Problem):
	def __init__(self, variables, domains, neighbors, constraints):
		"""Construct a CSP problem. If variables is empty, it becomes domains.keys()."""
		variables = variables or list(domains.keys())

		self.variables = variables
		self.domains = domains
		self.neighbors = neighbors
		self.constraints = constraints
		self.initial = ()
		self.curr_domains = None
		self.nassigns = 0
		# MODIFIED to add a member variable to the class to get number of unassignments
		self.n_unassigns = 0

	def assign(self, var, val, assignment):
		"""Add {var: val} to assignment; Discard the old value if any."""
		assignment[var] = val
		self.nassigns += 1

	def unassign(self, var, assignment):
		"""Remove {var: val} from assignment.
		DO NOT call this if you are changing a variable to a new value;
		just call assign for that."""
		if var in assignment:
			del assignment[var]
			# MODIFIED to increas the value of unassigned variables every time an unassignment takes place
			self.n_unassigns += 1

	def nconflicts(self, var, val, assignment):
		"""Return the number of conflicts var=val has with other variables."""
		# Subclasses may implement this more efficiently
		def conflict(var2):
			return (var2 in assignment and
					not self.constraints(var, val, var2, assignment[var2]))
		return count(conflict(v) for v in self.neighbors[var])

	def display(self, assignment):
		"""Show a human-readable representation of the CSP."""
		# Subclasses can print in a prettier way, or display with a GUI
		print('CSP:', self, 'with assignment:', assignment)

	# These methods are for the tree and graph-search interface:

	def actions(self, state):
		"""Return a list of applicable actions: nonconflicting
		assignments to an unassigned variable."""
		if len(state) == len(self.variables):
			return []
		else:
			assignment = dict(state)
			var = first([v for v in self.variables if v not in assignment])
			return [(var, val) for val in self.domains[var]
					if self.nconflicts(var, val, assignment) == 0]

	def result(self, state, action):
		"""Perform an action and return the new state."""
		(var, val) = action
		return state + ((var, val),)

	def goal_test(self, state):
		"""The goal is to assign all variables, with all constraints satisfied."""
		assignment = dict(state)
		return (len(assignment) == len(self.variables)
				and all(self.nconflicts(variables, assignment[variables], assignment) == 0
						for variables in self.variables))

	# These are for constraint propagation

	def support_pruning(self):
		"""Make sure we can prune values from domains. (We want to pay
		for this only if we use it.)"""
		if self.curr_domains is None:
			self.curr_domains = {v: list(self.domains[v]) for v in self.variables}

	def suppose(self, var, value):
		"""Start accumulating inferences from assuming var=value."""
		self.support_pruning()
		removals = [(var, a) for a in self.curr_domains[var] if a != value]
		self.curr_domains[var] = [value]
		return removals

	def prune(self, var, value, removals):
		"""Rule out var=value."""
		self.curr_domains[var].remove(value)
		if removals is not None:
			removals.append((var, value))

	def choices(self, var):
		"""Return all values for var that aren't currently ruled out."""
		return (self.curr_domains or self.domains)[var]

	def infer_assignment(self):
		"""Return the partial assignment implied by the current inferences."""
		self.support_pruning()
		return {v: self.curr_domains[v][0]
				for v in self.variables if 1 == len(self.curr_domains[v])}

	def restore(self, removals):
		"""Undo a supposition and all inferences from it."""
		for B, b in removals:
			self.curr_domains[B].append(b)

	# This is for min_conflicts search

	def conflicted_vars(self, current):
		"""Return a list of variables in current assignment that are in conflict"""
		return [var for var in self.variables
				if self.nconflicts(var, current[var], current) > 0]


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

# p = MapColoringCSP(range(5),rand_graph(5,0.5))
# print(p.variables)
# print(p.neighbors)
# print(p.domains)



# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def my_backtracking_search(csp,
						select_unassigned_variable=first_unassigned_variable,
						order_domain_values=unordered_domain_values,
						inference=no_inference):
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
	assert result is None or csp.goal_test(result)
	return result


# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def unordered_domain_values(var, assignment, csp):
	"""The default value order."""
	return csp.choices(var)


# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def first_unassigned_variable(assignment, csp):
	"""The default variable order."""
	return first([var for var in csp.variables if var not in assignment])


# !!! Taken from csp.py and modified !!! Modifications are marked with appropiate comments
def no_inference(csp, var, value, assignment, removals):
	return True

#_________________________________________________________________________________________________________________

def generate_graphs():
	"""generate the 5 graphs as requested by the
	assignment description for this question"""
	graphs = [rand_graph(30, 0.1), rand_graph(30, 0.2), rand_graph(30, 0.3), rand_graph(30, 0.4), rand_graph(30, 0.5)]
	return graphs

def run_q3():
	g = rand_graph(100,0.7)
	p = my_MapColoringCSP(range(30),g)
	start_time = time.time()
	# ... do something ...
	res = my_backtracking_search(p)
	elapsed_time = time.time() - start_time

	print(res)
	print(elapsed_time)
	print(p.nassigns)
	print(p.n_unassigns)



run_q3()



# END of a2_q3.py

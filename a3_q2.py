import math
import os
import time
import random
import subprocess

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

def get_nodes(g):
	""" returns a list of nodes for a friendship graph g """
	nodes = []
	for each in g.keys():
		nodes.append(each+1)
	return nodes

def is_in_edges(e,edges):
	""" checks if 'e' is already present in the set of edges 'edges' """
	if len(edges) == 0:
		return False

	for each in edges:
		if e == each or e == each[::-1]:
			return True
	return False


def get_edges(g):
	""" returns a list of edges for a friendship graph g """
	edges = []
	for each in g:
		for f in g[each]:
			l = [each+1,f+1]
			if is_in_edges(l,edges):
				continue
			else:
				edges.append(l)
	return edges

def map_to_var(n,c,k):
	""" maps a given node number 'n' of color 'c' to a given variable value """
	return ((n-1)*k + c)

def reduce_node(v,k):
	""" returns the node number represented by the given varaiable """
	return (math.floor(v/k) + 1)

def reduce_color(v,k):
	""" return the color of node represented by the given variable """
	return ((v%k) + 1)

def make_sat_vars(nodes,k):
	""" Takes in a set of nodes 'nodes' and 
	max possible colors 'k'. Returns
	a list of lists such that l[i] is 
	the list of vars associated with node i"""
	var_list = []
	for i in nodes:
		temp = []
		for c in range(1,k+1):
			temp.append(map_to_var(i,c,k))
		var_list.append(temp)
	return var_list

def list_edge_vars(l,k):
	""" l is list of the lists of 2 nodes that have an edge b/w them. 
	Returns a list of pairs such that they are corresponding variables 
	for each color of the the pair of vertices that make up the edges """
	l_constr = []
	for edge in l:
		for c in range(1,k+1):
			pair = []
			for node in edge:
				pair.append(-map_to_var(node,c,k))
			l_constr.append(pair)
	return l_constr


def make_constraints(l,k,type):
	""" make constraints according to the 'type' parameter:
		- type == 'atleast_one_color': pass in a list of lists such that, l[i] = list of variables associated with node i
		- type == 'atmost_one_color' : pass in a list of variables
		- type == 'diff_color'       : pass in a list of lists such that, l[i] = pair of nodes that have an edge in between
		- 'l' is the list of lists according tot he type of constraint to be generated
		- 'k' is the max number of colors possible
	 """	
	if type == 'atleast_one_color':
		constr = ''
		for each in l:
			for every in each:
				constr += str(every) + ' '
			constr += '0\n'
		return constr
	elif type == 'atmost_one_color':
		constr = ''
		for i in range(len(l)-1):
			constr += str(-l[i]) + '\n'
		constr += str(-l[len(l)-1]) + ' 0\n'
		return constr
	elif type == 'diff_color':
		constr = ''
		evars = list_edge_vars(l,k)
		for pair in evars:
			for each in pair:
				constr += str(each) + ' '
			constr += '0\n'
		return constr
	else:
		print('The "type" parameter passed is not correct')

def make_ice_breaker_sat(graph, k):
	""" Generates the CNF sentence to be passed to minisat to solve the given problem instance """
	edges = get_edges(graph)
	nodes = get_nodes(graph)
	var_l = make_sat_vars(nodes,k)
	N = len(graph)
	sentence = ''

	sentence += make_constraints(var_l,k,'atleast_one_color')
	for each in var_l:
		sentence += make_constraints(each,k,'atmost_one_color')
	sentence += make_constraints(edges,k,'diff_color')
	header = 'c k-coloring problem with '+str(N)+ ' nodes and k='+ str(k)+'\n' +'p cnf '+str(k*N)+' '+str(sentence.count(' 0'))+'\n'
	sentence = header + sentence
	return sentence

def num_teams(sol,k):
	""" returns the number of teams in the minisat solution 'sol' with a coloring of 'k' colors"""
	colors = []
	for each in sol:
		if each > 0:
			colors.append(reduce_color(each,k))
		else:
			continue
	return max(colors)

def make_minisat_file(cnf):
	""" Generates a file named 'sat2.txt' that contains the cnf 
	statement for the given cnf sentence as a python string"""
	f = open("sat2.txt","w+")
	f.write(cnf)
	f.close()

def read_sat_out():
	""" read the file 'out' and return a solution of the cnf given to minisat """
	f = open("out2","r")
	return f.read()

def convert_sol(str):
	""" Takes in the string in the output of minisat.
	Returns a list of integers of the solution"""

	sol_list_str = str.split()
	if sol_list_str[0] == 'UNSAT':
		return 'UNSAT'
	sol_list_int = list(map(int,sol_list_str[1:-1]))
	return sol_list_int

def run_minisat():
	""" run the command for running minisat to solve the cnf in 'sat.txt' """
	try:
		subprocess.run(['minisat','sat2.txt','out2'],timeout=5)
	except:
		return False
	return True
	#os.system('minisat sat2.txt out2')

def find_min_teams(graph):
	""" finds the min number of teams that are required 
	to solve the instance of the friendship graph given using minisat """
	n = len(graph)
	inc_k = range(1,n+1)
	for k in inc_k:
		cnf = make_ice_breaker_sat(graph,k)
		make_minisat_file(cnf)
		if(run_minisat()):
			sol = convert_sol(read_sat_out())
			if sol == 'UNSAT':
				print('k-coloring not possible for k='+ str(k))
				continue
			else:
				print('Optimal Solution Found k='+ str(num_teams(sol,k)))
				return num_teams(sol,k)
				break
		else:
			print('k=' + str(k) + ' runs minisat for too long and we consider that it is an UNSAT instance\n')
			continue
		
def run_experiment():
	g1 = [rand_graph(200,0.1)]*5
	g2 = [rand_graph(200,0.2)]*5
	g3 = [rand_graph(200,0.3)]*5
	g4 = [rand_graph(200,0.4)]*5
	g5 = [rand_graph(200,0.5)]*5
	g6 = [rand_graph(200,0.6)]*5
	g7 = [rand_graph(200,0.7)]*5
	g8 = [rand_graph(200,0.8)]*5
	g9 = [rand_graph(200,0.9)]*5
	all_graphs = []
	all_graphs.append(g1)
	all_graphs.append(g2)
	all_graphs.append(g3)
	all_graphs.append(g4)
	all_graphs.append(g5)
	all_graphs.append(g6)
	all_graphs.append(g7)
	all_graphs.append(g8)
	all_graphs.append(g9)

	times = []
	teams = []
	for each_list in all_graphs:
		sol_times = []
		min_teams = []
		for graph in each_list:
			s = time.time()
			t = find_min_teams(graph)
			e = time.time() - s
			sol_times.append(e)
			min_teams.append(t)
		times.append(sol_times)
		teams.append(min_teams)
	print(times)
	print(temas)

run_experiment()
# g = rand_graph(200,0.8)
# print(g)
# find_min_teams(g)




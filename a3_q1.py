import os
import time

def make_constraints(l,type='atmost_one'):
	"""	generate a string of constraints for the list l which can be a row or column or a diagonal of a n-queens problem.
		USAGE:
		- l = list of variables for which constraints are rto be generated
		- if type == 'exactly_one' is passed then makes constraints for a row or a column
		- if type is not passed OR if type == 'atmost_one' is passed then makes constraints for a diagonal
	"""
	n = len(l)
	constr = ''
	for i in range(n-1):
		for j in range(i+1,n):
			constr += str(-l[i]) + ' ' + str(-l[j]) + ' 0\n'
	
	if(type == 'exactly_one'):
		for each in l:
			constr += str(each) +' '
		constr += '0\n'
	return constr

def make_rows(n):
	"""returns a list of rows for the nxn chess board"""
	rows = []
	for i in range(1,n*n,n):
		r = [i]
		for j in range(i+1,i+n):
			r.append(j)
		rows.append(r)
	return rows

def make_cols(n):
	"""returns a list of columns for the nxn chess board"""
	cols = []
	for i in range(1,n+1):
		c = [i]
		for j in range(i+n,n*n + 1,n):
			c.append(j)
		cols.append(c)
	return cols 

def make_diagonals(n,board):
	"""returns a list of all diagonals for a nxn chess board"""
	diagonals = []
	d = []
	for p in range(2*n-1):
		d.append([board[p-q][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])
		d.append([board[n-p+q-1][q] for q in range(max(0, p - n + 1), min(p, n - 1) + 1)])

	for each in d:
		if len(each) == 1:
			continue
		else:
			diagonals.append(each)
	return diagonals

def make_queen_sat(N):
	"""generates a pyhton string which is a SAT sentence that can be passed to minisat"""
	rows  = make_rows(N)
	cols  = make_cols(N)
	diags = make_diagonals(N,rows)
	sentence = ''

	for each in rows:
		sentence += make_constraints(each,'exactly_one')

	for each in cols:
		sentence += make_constraints(each,'exactly_one')

	for each in diags:
		sentence += make_constraints(each,'atmost_one')

	header = 'c N='+str(N)+' queens problem\n'+'p cnf '+str(N*N)+' '+str(sentence.count('\n'))+'\n'
	final_sentence = header + sentence
	return final_sentence

def write_sat_file(N):
	"""create a file 'sat.txt' and write the SAT sentence in cnf form for minisat to use """
	f = open("sat.txt","w+")
	f.write(make_queen_sat(N))
	f.close()


# +---------------------[ ASSIGNMENT 3: Question 1 ]----------------------------------------------------+
# | Author: Siddharth Gupta																				|
# | SFUID: 301327469																					|
# | 																									|
# | - CITATIONS:																						|
# | 	+ Python3 Documentation: [ https://docs.python.org/3/ ]											|
# |     + Minisat Documentation: [ http://minisat.se/ ]													|
# |		+ Openpyxl Module for writing a raw excel sheet : [ https://openpyxl.readthedocs.io/en/stable/ ]|
# +-----------------------------------------------------------------------------------------------------+

import os
import time
import math
import openpyxl


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

def read_sat_out():
	""" read the file 'out' and return a solution of the cnf given to minisat """
	f = open("out","r")
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
	os.system('minisat sat.txt out')

def draw_queen_sat_sol(sol):
	""" Draws out a nxn chess board with the solution for the N-queens problem. OR 
	Returns a meesage '!!! NO solution found !!!' """
	if sol == 'UNSAT':
		print('!!! NO solution found !!!\n')
	else:
		n_sqr = sol[-2]
		if n_sqr < 0:
			n_sqr *= -1
		n = int(math.sqrt(n_sqr))
		if n >= 40:
			print('!!! SOLUTION TOO BIG TO PRINT !!!')
			return
		board = ''
		for i in range(n):
			row = ''
			for j in range(i*n,(i+1)*n):
				if sol[j] < 0:
					row += ' . '
				elif sol[j] > 0:
					row += ' Q '
				else:
					row += '\n'
			row += '\n'
			board += row
		print(board)
		

def run_experiment(t=20):
	""" Generates N-queens sat sentences and runs minisat.
	Stops running when a value of N takes more than 't' seconds. Default value for t is 20 [20 seconds]
	Returns the MAX_N values as described by assignment description"""
	i = 2
	while True:
		print('+++++++++++++++++++++++++++++++++')
		print('| Generating sat.txt for N='+str(i)+'\t|')
		write_sat_file(i)
		print('| Running mini sat now..... \t|')
		print('+++++++++++++++++++++++++++++++++')
		print('\n\n')
		t_s = time.time()
		run_minisat()
		t_e = time.time() - t_s
		print('\n\n+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		print('| Done Running minisat took time= ' + str(t_e) + ' seconds' + '\t|')
		print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
		print('SOLUTION :')
		sol = convert_sol(read_sat_out())
		draw_queen_sat_sol(sol)
		print('\n\n')
		if t_e > t:
			print('+=======================================================================================+')
			print('| MAX_N = ' + str(i-1) + ' for minisat to solve the N-queens problem in less than ' + str(t) + ' second(s) \t|') 
			print('+=======================================================================================+')
			break
		i += 1
	return i

def make_experiment_sheet(t=20):
	""" Generate excel sheet for experiment to find MAX_N for which 
	minisat can sole the N-queens problems in less than 't' seconds """
	wb = openpyxl.Workbook()				# Create a Workbook in which an excel sheet will be created
	sheet = wb.active						# Create an active sheet
	sheet.title = "Assignment3_Question1"	# Title of the active sheet

	def insert_into_cell(r,c,val):
		""" inserts val in the cell at row r and column c """
		c = sheet.cell(row=r,column=c)
		c.value = val
	
	print('RECORDING DATA NOW >>>')
	sRow = 1
	sCol = 1
	insert_into_cell(sRow,sCol,'N-Queens Experiment')
	sCol += 1
	insert_into_cell(sRow,sCol,'MAX_N for time (seconds) taken to run minisat for atmost :')
	sCol += 1
	insert_into_cell(sRow,sCol,t)
	sCol = 1
	sRow += 2
	insert_into_cell(sRow,sCol,'N')
	sCol += 1
	insert_into_cell(sRow,sCol,'Time taken by minisat')
	sCol = 1
	sRow += 1
	n = 2
	while True:
		write_sat_file(n)
		print('\n\n')
		t_s = time.time()
		run_minisat()
		t_e = time.time() - t_s
		print('\n\n')
		if t_e > t:
			insert_into_cell(sRow+2,1,'MAX_N:')
			insert_into_cell(sRow+2,2,n-1)
			break
		insert_into_cell(sRow,sCol,n)
		sCol += 1
		insert_into_cell(sRow,sCol,t_e)
		sCol = 1
		sRow += 1
		n += 1
	wb.save('a3_q1.xlsx')
	print('DATA RECORDED IN "a3_q1.xlsx" IN THE ROOT DIRECTORY <<<')


# make_experiment_sheet(20)
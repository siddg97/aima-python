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
	"""returns a list of rows for the n-queens problem"""
	rows = []
	for i in range(1,n*n,n):
		r = [i]
		for j in range(i+1,i+n):
			r.append(j)
		rows.append(r)
	return rows

def make_cols(n):
	"""returns a list of columns for the n-queens problem"""
	cols = []
	for i in range(1,n+1):
		c = [i]
		for j in range(i+n,n*n + 1,n):
			c.append(j)
		cols.append(c)
	return cols
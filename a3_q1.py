def make_constraints(l,type='atmost_one'):
	"""generate a string of constraints for the list l which can be a row or column or a diagonal of a n-queens problem."""
#	USAGE:
#		- l = list of variables for which constraints are rto be generated
#		- if type == 'exactly_one' is passed then makes constraints for a row or a column
#		- if type is not passed OR if type == 'atmost_one' is passed then makes constraints for a diagonal

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

class nQueens:
	def __init__(self,n):
		self.n = n
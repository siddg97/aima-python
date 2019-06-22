
class Contraint:
	def __init__(self,n):
		self.n = str(n)
		self.num_c = str(int(((5*n*n*n) - (6*n*n) + (7*n))/3))
		self.r_c = ''
		self.c_c = ''
		self.d_c = ''
		self.sat_str = 'c ' + self.n + '-queens problem (sat)' + '\n p cnf ' + self.n + ' ' + self.num_c + '\n'

	def make_sat_str(self):
		self.sat_str += self.r_c + '\n' + self.c_c + '\n' + self.d_c

t = Contraint(7)
print(t.num_c)
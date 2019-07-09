# a4.py - START

class Board:
	""" Board object for a 3x3 tic-tac-toe game
		 + state = a list of 'X', 'O', or '.' values. '.' signifies an empty tile
		 + moves = a list of all possible moves that can be performed on the given state of the board. A list of integers
	"""
	def __init__(self,state):
		self.state = state
		self.moves = self.getLegalMoves(state)

	def getLegalMoves(self,state):
		""" returns a list of all possible legal moves based on the given state """
		moves = []
		for i,each in enumerate(state):
			if each == '.':
				moves.append(i+1)
		return moves

	def applyMove(self,move,token):
		""" applies the move given to the given state for the token and returns a new state"""
		new_state = self.state
		new_state[move-1] = token
		self.state = new_state

	def didEnd(self):
		""" Returns a 'x' or 'Y' or 'D'
				+ 'X'     -> player who chose 'X' won
				+ 'O'     -> player who chose 'O' won
				+ 'D'     -> draw
				+ 'False' -> game not finished
		"""
		state = self.state
		if (state[0]==state[4] and state[4]==state[8] and state[0] != '.') or (state[2]==state[4] and state[4]==state[6] and state[2] != '.'):
			return state[4]
		else:
			# check for rows
			for i in range(0,9,3):
				if state[i]==state[i+1] and state[i+1]==state[i+2] and state[i] != '.':
					return state[i]
			# check for columns
			for i in range(0,3):
				if state[i]==state[i+3] and state[i+3]==state[i+6] and state[i] != '.':
					return state[i]
			if '.' not in self.state:
				return 'D'
			else:
				return False


class Tic_tac_toe:
	def __init__(self,board):
		self.board = board

	def display(self):
		state = self.board.state
		for i in range(9):
			if state[i] == '.':
				state[i]=' '
		r1 = '\x1b[4;30;43m'+ '| '+state[0]+' | '+state[1]+' | '+state[2]+' |'+'\x1b[0m' 
		r2 = '\x1b[4;30;43m'+ '| '+state[3]+' | '+state[4]+' | '+state[5]+' |'+'\x1b[0m' 
		r3 = '\x1b[6;30;43m'+ '| '+state[6]+' | '+state[7]+' | '+state[8]+' |'+'\x1b[0m' 
		print(r1+'\n'+r2+'\n'+r3)

def play_game():
	s = ['.']*9
	t =Tic_tac_toe(Board(s))
	human = input('What token would you like to be [X or O]? ')
	t.display()
	print('\x1b[6;30;41m'+'Player: '+human+' '+'\x1b[0m')

# if __name__ = '__main__':
# 	play_new_game()

play_game()
# print(b.didEnd())
# print(b.state)
# print(b.moves)

# print(b.didEnd())

# b.applyMove(1,'X')
# print(b.state)
# b.applyMove(4,'X')
# print(b.state)

# b.applyMove(7,'X')
# print(b.state)
# print(b.didEnd())



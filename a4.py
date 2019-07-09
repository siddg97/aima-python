def getLegalMoves(board):
	""" returns a list of all possible legal moves based on the given state """
	moves = []
	for i,each in enumerate(board):
		if each == ' ':
			moves.append(i+1)
	return moves

class tictactoe:
	def __init__(self):
		self.board = [' ']*9
		self.nextMoves = [1,2,3,4,5,6,7,8,9]

	def display(self):
		state = self.board
		for i in range(9):
			r1 = '\x1b[4;30;43m'+ ' '+state[0]+' | '+state[1]+' | '+state[2]+' '+'\x1b[0m' 
			r2 = '\x1b[4;30;43m'+ ' '+state[3]+' | '+state[4]+' | '+state[5]+' '+'\x1b[0m' 
			r3 = '\x1b[6;30;43m'+ ' '+state[6]+' | '+state[7]+' | '+state[8]+' '+'\x1b[0m' 
		print(r1+'\n'+r2+'\n'+r3)

	def applyMove(self,tile,player):
		self.board[tile-1]=player
		self.nextMoves = getLegalMoves(self.board)

	def playAsHuman(self,human):
		while True:
			h_move = int(input('\x1b[6;30;42m'+'Your next move at?'+'\x1b[0m'))
			if h_move in self.nextMoves:
				break
			else:
				print("Invalid move! try again!")
		self.applyMove(h_move,human)

	def playAsComputer(self,computer):
		c_move = int(input('\x1b[6;30;42m'+'computers next move at?'+'\x1b[0m'))
		self.applyMove(c_move,computer)

	def outcome(self):
		""" Returns a 'x' or 'o' or 'D'
				+ 'x'     -> player who chose 'X' won
				+ 'o'     -> player who chose 'O' won
				+ 'D'     -> draw
				+ 'False' -> game not finished
		"""
		state = self.board
		if (state[0]==state[4] and state[4]==state[8] and state[0] != ' ') or (state[2]==state[4] and state[4]==state[6] and state[2] != ' '):
			return state[4]
		else:
			# check for rows
			for i in range(0,9,3):
				if state[i]==state[i+1] and state[i+1]==state[i+2] and state[i] != ' ':
					return state[i]
			# check for columns
			for i in range(0,3):
				if state[i]==state[i+3] and state[i+3]==state[i+6] and state[i] != ' ':
					return state[i]
			if ' ' not in self.board:
				return 'D'
			else:
				return False

def play_game():
	s = ['.']*9
	t = tictactoe()
	human = input('What token would you like to be [X or O]? ').lower()
	print('\n')
	if human=='x':
		program = 'o'
	else:
		program = 'x'
	while t.outcome()==False:
		t.display()
		print('\x1b[6;30;41m'+'Player  : '+human+' '+'\x1b[0m')
		print('\x1b[6;30;44m'+'Computer: '+program+' '+'\x1b[0m\n')
		print('\x1b[6;30;47mYour next possible move can be one of the following tiles:\x1b[0m\n\x1b[1;31;40m'+str(t.nextMoves)+'\x1b[0m')
		t.playAsHuman(human)
		if len(t.nextMoves) == 0:
			break
		t.display()
		print('\x1b[6;30;41m'+'Player  : '+human+' '+'\x1b[0m')
		print('\x1b[6;30;44m'+'Computer: '+program+' '+'\x1b[0m\n')
		print('\n COMPUTERS TURN:')
		t.playAsComputer(program)
		if len(t.nextMoves) == 0:
			break
	finalstr = 'GAME OVER!'
	if t.outcome() == human:
		finalstr += ' HUMAN HAS WON!'
	elif t.outcome() == program:
		finalstr += ' COMPUTER HAS WON!'
	else:
		finalstr += ' IT IS A TIE!'
	t.display()
	print(finalstr)


play_game()
# t = tictactoe()
# t.display()
# print(t.board)
# t.applyMove(1,'x')
# print(t.board)
# print(t.nextMoves)

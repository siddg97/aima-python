import random
import time
from copy import deepcopy

def getLegalMoves(board):
	""" returns a list of all possible legal moves based on the given state """
	moves = []
	for i,each in enumerate(board):
		if each == ' ':
			moves.append(i+1)
	return moves

class Tictactoe:
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
			h_move = int(input('\x1b[6;30;42m'+'Your next move at?'+'\x1b[0m '))
			if h_move in self.nextMoves:
				break
			else:
				print("Invalid move! try again!")
		self.applyMove(h_move,human)

	def playAsComputer(self,computer,playouts=150):
		print("\x1b[6;30;44m I am calculating my next step to defeat you.....\x1b[0m\n")
		time.sleep(2)
		board = deepcopy(self.board)
		moves = deepcopy(self.nextMoves)
		human = 'o' if computer=='x' else 'x'
		scores = []
		for each in moves:
			w,l,d = 0,0,0
			for i in range(playouts):
				c=random_playout(board,each,computer,human)
				if c=='WIN':
					w+=1
				elif c=='LOSS':
					l+=1
				else:
					d+=1
			scores.append(w)
		nextMoveIndex = scores.index(max(scores))
		self.applyMove(moves[nextMoveIndex],computer)		


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

def random_move(moves):
	return random.choice(moves)

def random_playout(board,move,computer,human):
	""" takes in a board, next legal move, computers token and humans token.
			OUTPUT:
			 + 'WIN'  - computer won
			 + 'LOSS' - computer lost
			 + 'DRAW' - tie
	"""
	new = deepcopy(board)
	new[move-1] = computer
	t = Tictactoe()
	t.board = new
	t.nextMoves = getLegalMoves(t.board)
	turn = False 	# false -> simulated human turn; true -> computer turn
	while t.outcome() == False:
		nextmove = random_move(t.nextMoves)
		t.applyMove(nextmove,computer if turn else human)
		turn = not turn
	if t.outcome()==human:
		return 'LOSS'
	elif t.outcome()==computer:
		return 'WIN'
	else:
		return 'DRAW'

def play_game():
	s = ['.']*9
	t = Tictactoe()
	print('\x1b[7;30;44m WELCOME TO TIC-TAC-TOE!                                                         \x1b[0m')
	print('\x1b[2;30;45m This program is going to give you a run for your money!                         \x1b[0m')
	print('\x1b[6;30;41m It is IMPOSSIBLE to beat this program at tic-tac-toe. Best of luck (you need it)\x1b[0m')
	print('\x1b[0;30;43m Out of fairness you get the first move!                                         \x1b[0m')
	human = input('\x1b[6;30;47m What token would you like to be x or o?\x1b[0m'+' ').lower()
	if human=='x':
		program = 'o'
	else:
		program = 'x'
	while t.outcome()==False:
		print('\x1b[6;30;41m'+'Player  : '+human+' '+'\x1b[0m')
		print('\x1b[6;30;44m'+'Computer: '+program+' '+'\x1b[0m\n')
		print('\x1b[6;30;41m YOUR TURN HUMAN \x1b[0m')
		t.display()
		print('\x1b[6;30;42mYour next possible move can be one of the following tiles: \x1b[0m\n\x1b[1;31;40m  '+str(t.nextMoves)+'  \x1b[0m')
		t.playAsHuman(human)
		if len(t.nextMoves) == 0:
			break
		print('\x1b[6;30;41m'+'Player  : '+human+' '+'\x1b[0m')
		print('\x1b[6;30;44m'+'Computer: '+program+' '+'\x1b[0m\n')
		print('\x1b[6;30;44m IT IS MY TURN \x1b[0m')
		t.display()
		t.playAsComputer(program)
		if len(t.nextMoves) == 0:
			break
	finalstr = '\x1b[5;30;41m GAME OVER!'
	if t.outcome() == human:
		finalstr += ' YOU WIN!'
	elif t.outcome() == program:
		finalstr += ' I WIN! '
	else:
		finalstr += ' IT IS A TIE!'
	t.display()
	print(finalstr+'\x1b[0m')

if __name__=='__main__':
	while True:
		play_game()
		h = input('\x1b[1;31;40m Would like to challenge me again?? [y/n] \x1b[0m').lower()
		if h=='n':
			break
		else:
			print('\n\n')


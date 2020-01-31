# import numpy as np # this library is not used
import matplotlib.pyplot as plt
import csv

#run with python or pythonw (for MacOS)


# __all__ = ['Host', 'Player', 'Board']

class Player:
	# class variables, shared by all instances of this class
	numPlayers=0 
	maxNumPlayers:int  


	# class variable maxNumPlayers has to be set before calling __init__
	def __init__(self, host):
		"""initialize."""
		self.my_host = host
		print("anzahl gewünschte Spieler: ",self.maxNumPlayers)
		# variables local to each created object
		self.number=Player.numPlayers 
		self.highScore=0
		Player.numPlayers=Player.numPlayers+1
		if self.number == Player.maxNumPlayers-1:
			print("genügend Player vorhanden.")
		if self.number > Player.maxNumPlayers-1:
			print("zu viele Player. Oder Turniermodus. Oder losen, wer gegen wen spielt. Oder queueing for playing :-)")
		self.last_stone_accepted=True


	def propose_stone(self):
		"""asks a player to give two integers as coordinates where to put his/her stone.
		returns a position as a tuple or the string 'quit' """
		pos=[-1,-1]
		print("Type of pos " , type(pos))
		print("Du bist" , self.get_my_number())
		# get position from player - person
		for i in range(2):
			pos[i]=input(f"gib { i +1 } -te Koordinate der Position an: ")
			#print("whatever ...")
			accept=False
			while (not accept) and not (pos == 'quit'):
				try:
					int(pos[i])
					accept=True
					print("in try, prüfen auf int: accepted")
				except ValueError:
					pos[i]=input("gib eine Zahl (Integer) ein oder schreibe quit:")

			# exit while with pos[i] either an interger input or the string 'quit'.

			if pos[i]=='quit':
				print("exit input by typing quit. do something, interrupt whatever.")
				pos='quit'
		# end of for , both coordinates requested - or got input 'quit'

		pos=[int(pos[0]), int(pos[1])]
		print("return position", pos)
		return pos

	def negotiate_stone_position(self):
		"""A player-object gets a keyboard-input from the player-human. S/he can try three times. If not successful after the third input, no stone is set and the game continues (with the next player)."""
		count=0
		proposed_stone=self.propose_stone()
		while (not self.my_host.evaluate_stone(self.get_my_number(), proposed_stone) and count < 2):
			proposed_stone=self.propose_stone()
			count+=1
		if count == 2:
			self.last_stone_accepted=False
		else:
			self.last_stone_accepted=True

	def get_number_of_players(self):
		"""Returns the class-attribute number of players."""
		return Player.numPlayers

	def set_number_of_players(self, numPlayers):
		"Simple setter. Trust the name."
		self.numPlayers=numPlayers

	@classmethod
	def set_max_number_of_players(class_, a_number):
		"""Simple setter. Does what the name suggests."""
		class_.maxNumPlayers=a_number

	def get_my_number(self):
		"""returns the ID - number of a player."""
		return int(self.number)

	def get_other_player_number(self):
		"""works for 2 players only"""
		return int((1 + self.number)%2)


class Board:
	def __init__(self, host, size: int):
		"""init."""
		self.my_host=host
		self.size=size
		self.board={(k,l):-1 for k in range(self.size) for l in range(self.size)}
		self.score=[] # empty list 
		self.acceptedStone=(-1,-1)
		self.maxNumberStones=self.size*self.size
		self.stones_set=0

	def update_scores(self):
		"""To be called after a new stone has been set. Calculates from scratch."""
		self.score=[0,0]
		
		b=list(self.board.values())
		for i in range(2):
			self.score[i]=sum( 1 for j in range(len(b)) if b[j]==i)

	def get_scores(self):
		"""simple getter function. Returns the score of both (possibly more, later ...) players."""
		return self.score

	def update_board(self, id):
		"""When a player has put a new stone on the board newly includes / cought stones turn change color"""
		newStone=self.acceptedStone
		directions=self.get_directions(newStone)

		dir_touch_opponent=[]

		for direction in directions:
			if self.board[ tuple( x + y for x,y in zip( newStone, direction) ) ]==(1 + id)%2:
				dir_touch_opponent.append(direction)
		print("dir touch opponent ", dir_touch_opponent)

		dir_enclose_opponent = []

		for direction in dir_touch_opponent:
			pos = newStone
			print("initial position ", pos)
			enclose=False
			dicided=False
			while not dicided:
				try:
					nextField=self.board[ tuple( x + y for x,y in zip(pos , direction) ) ] 
				except KeyError:
					dicided=True

				if nextField==(1 + id)%2:
					pos = tuple( x+y for x,y in zip(pos , direction) )
					print("new position " , pos)
				elif nextField==id:
					dir_enclose_opponent.append(direction)
					enclose=True
					dicided=True 
				else:
					dicided=True
	
		for direction in dir_enclose_opponent:
			pos=newStone 
			done=False
			while not done:
				nextStoneInLine = tuple( x+y for x,y in zip(pos , direction) )
				if self.board[nextStoneInLine]==(1 + id)%2: 
					self.board[nextStoneInLine]=id
					pos=nextStoneInLine
				else:
					done=True

	def print_board(self):
		"""Outputs the board as a graph."""
		# it would be nice just to add one point innstead of printing all again from scratch
		k,v = zip(*self.board.items())
		a = [k for k,v in self.board.items() if v==0]
		b = [k for k,v in self.board.items() if v==1]
		plt.plot([0,self.size-1,0,self.size-1],[0,0,self.size-1,self.size-1], marker= 'x', ls='')
		plt.plot(*zip(*a), marker='o', color='r', ls='')
		plt.plot(*zip(*b), marker='o', color='b', ls='')

		plt.draw()
		plt.show(block=False)


	def check_stone(self, id, position):
		"""Calls three other check-functions."""
		print("in Brett : check Stone")		
#		code executes only until the first False
		return (self.check_position_exists(position) and self.check_position_free(position) and self.check_enclose_opponent( id , position))

	def check_position_exists(self, position):
		"""Returns True iff (position) is on the board."""
		print("in Brett : check position exists")		
		return ((position[0] in range(self.size)) and (position[1] in range(self.size)))

	def check_position_free(self, position):
		"""Check if a (position) is free. Returns True iff no stone is already placed on that position."""
		print("in Brett : check position free")
		return self.board[position]==-1

	def get_directions(self, position): 
		"""Given a (position) this function returns all other positions that are adjacent to this position and on the board."""
		allDirections = [(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(-1,1),(1,1),(1,-1)]
		
		d2 = [[ x+y for x,y in zip(position , direction) if x+y in range(self.size) ] for direction in allDirections ]
		# for a position and direction: if the go beyond the board it maybe only one coordinate is affected
		# first only this coordinate is removed. Resulting in tupels of length 0 or 1.
		# these shorter tupels are then removed
		mask = [len(d)==2 for d in d2]
		# Problem with masking: arrays can be masked, lists cannot

		validDirections = [allDirections[i] for i in range(8) if mask[i]==True]
		# print("directions d2: " , directions)

		return validDirections


	def check_enclose_opponent(self , id , position):
		"""For a player (id) to set a stone at a specified (position), this has to create an enclosing of the opponent's stones."""
		print("in Brett : check enclose opponent")
		directions = self.get_directions(position)
		dir_touch_opponent = []
		for direction in directions:
			if self.board[ tuple( x+y for x,y in zip(position , direction) ) ]==(1+id)%2:
				dir_touch_opponent.append(direction)
		print("dir touch opponent ", dir_touch_opponent)

		if len(dir_touch_opponent)==0:
			return False

		dir_enclose_opponent=[]
		for direction in dir_touch_opponent:
			pos=position 
			print("initial position ", pos)
			enclose=False
			dicided=False
			while not dicided:
				try:
					nextField = self.board[ tuple( x+y for x,y in zip(pos, direction) ) ] 
				except KeyError:
					dicided=True

				if nextField==(1+id)%2:
					pos=tuple( x+y for x,y in zip(pos, direction))
					print("new position ", pos)
				elif nextField==id:
					return True
				else:
					dicided=True
		return False

		# check that the set stone is adjacent to a stone of the opponent
		# check that there exists a direction such that in that direction 
		# at some point lies a stone of the same colour as the set stone 


	def set_stone(self, playerID, position):
		"""A stone is set on the board. Input: who (playerID) sets the stone where (position)."""
		if self.check_stone(playerID, position): 
			self.board[position]=playerID
			self.acceptedStone=position
			return True
		else:
			print("Stone rejected.")
			return False
		
class Host:

	def __init__(self):
		"""The host will have a board and players, to be created later. The host has a log file."""
		self.my_board:Board
		self.my_player:list
		self.my_logfile='./logs/log.csv'
		with open(self.my_logfile, 'w', newline='') as logfile:
			log_writer=csv.writer(logfile, delimiter=' ')
			log_writer.writerow( ['created host'] )

	def create_board(self, size):
		"""The host creates the board. For size n there will be n*n possible positions for the stones to set."""
		self.my_board=Board(self, size)
		return self.my_board

	def setup_board(self):
		"""soll man nicht machen: direkt auf die Daten zugreifen. Besser: Methode benutzen!"""
		# initial stones for player 0
		stones_0=[( int(self.my_board.size/2)-1, int(self.my_board.size/2)-1), (int(self.my_board.size/2)-1, int(self.my_board.size/2))]
		self.my_board.board[stones_0[0]]=0
		self.my_board.board[stones_0[1]]=0	
		# initial stones fpr player 1
		stones_1=[(int(self.my_board.size/2) , int(self.my_board.size/2)), (int(self.my_board.size/2), int(self.my_board.size/2)-1)]
		self.my_board.board[stones_1[0]]=1
		self.my_board.board[stones_1[1]]=1		

		self.my_board.stones_set=4

		# write set stones to logfile
		with open(self.my_logfile, 'a', newline='') as logfile:
			log_writer=csv.writer(logfile, delimiter=' ')
			log_writer.writerow(['### stones set by host in setup_board ###'])
			log_writer.writerow(['for player, 0 , '+str(stones_0)])
			log_writer.writerow(['for player, 1 , '+str(stones_1)])

	def create_players(self,some_number):
		"""The host creates the right amount of players. In this version there are always 2 players created."""
		# set class variable first
		Player.set_max_number_of_players(some_number)

		player_list=[]
		for _ in range(some_number):
			player_list.append(Player(self))

		self.my_player=player_list 

		return player_list	

	def evaluate_stone(self , playerID , position): 
		"""Check stone and set it , return True or False"""
		if self.my_board.set_stone(playerID, tuple(position)): 
			with open(self.my_logfile, 'a', newline='') as logfile:
				log_writer=csv.writer(logfile, delimiter=' ')
				log_writer.writerow( ['as player ,' + str(self.my_player[playerID].get_my_number()) + ',' + str(position)] )
			self.my_board.stones_set+=1
			return True
		else:
			return False
	
def next(i):
	"""get the id for the next player"""
	return ((1 + i)%2)

def main ():

	print("Starte das Spiel")

	host=Host()

	board=host.create_board(4)

	host.setup_board()

	player=host.create_players(2)

	print(board.print_board())

	board.update_scores()
	print("Punkte:" , board.get_scores())

	game_on=True

	current=0
	last = 0
	max_number_of_turns=board.maxNumberStones # define getter for max_number_of_stones 
	# better: move it all into Host or Board !!

	while game_on:
		
		player[current].negotiate_stone_position()

		if player[current].last_stone_accepted:
			board.update_board(player[current].get_my_number())
			board.print_board()
			board.update_scores()
			print("Punkte:", board.get_scores())

		last=current
		current=next(current)

		print("end of round. Next round?")	
		print("last_stone_accepted ", player[last].last_stone_accepted, player[current].last_stone_accepted)
		print("all stones set? " , board.stones_set , "< " , max_number_of_turns, "?")
		game_on=((player[last].last_stone_accepted or player[current].last_stone_accepted) and (board.stones_set<max_number_of_turns))

	print("game over")
	# should show a "game over" screen to each player

	scores_at_end=board.get_scores()
	print("Punktestand am Ende:", scores_at_end)
	if scores_at_end[0]>scores_at_end[1]: 
		print("Player 1 wins")
	elif scores_at_end[0]<scores_at_end[1]: 
		print("Player 2 wins")
	else:
		print("Both win.")	
	# the host should announce the winner


	# Funktioniert nicht, die Eingabe zu prüfen. 
	# Eingabe 9,9 produziert Keyvalue Error und wird nicht abgefangen

if __name__== "__main__":
  main()

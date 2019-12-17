import numpy as np
import matplotlib.pyplot as plt
#run with python or pythonw (for MacOS)


# __all__ = ['Host', 'Player', 'Board']

class Player:
	# class variables, shared by all instances of this class
	numPlayers = 0 
	maxNumPlayers : int  


	# class variable maxNumPlayers has to be set before calling __init__
	def __init__(self, host):
		self.my_host = host
		print("anzahl gewünschte Spieler: " , self.maxNumPlayers)
		# variables local to each created object
		self.number = Player.numPlayers 
		self.highScore = 0
		Player.numPlayers = Player.numPlayers + 1
		if self.number == Player.maxNumPlayers -1 :
			print("genügend Player vorhanden.")
		if self.number > Player.maxNumPlayers -1 :
			print("zu viele Player. Oder Turniermodus. Oder losen, wer gegen wen spielt. Oder queueing for playing :-)")
		self.lastStoneAccepted = True


	def propose_stone(self):
		"""asks a player to give two integers as coordinates where to put his/her stone.
		returns a position as a tuple or the string 'quit' """
		pos=[-1,-1]
		print("Type of pos " , type(pos))
		print("Du bist" , self.getMyNumber())
		# get position from player - person
		for i in range(2):
			pos[i] = input(f"gib { i +1 } -te Koordinate der Position an: ")
			#print("whatever ...")
			accept = False
			while (not accept) and not (pos == 'quit'):
				try:
					int(pos[i])
					accept = True
					print("in try, prüfen auf int: accepted")
				except ValueError:
					pos[i] = input("gib eine Zahl (Integer) ein oder schreibe quit:")

			# exit while with pos[i] either an interger input or the string 'quit'.

			if pos[i] == 'quit':
				print("exit input by typing quit. do something, interrupt whatever.")
				pos='quit'				
		# end of for , both coordinates requested - or got input 'quit'

		pos = [int(pos[0]), int(pos[1])]
		print("return position" , pos)
		return pos


	def negotiate_stone_position(self):

		while (not self.my_host.evaluate_stone(self.getMyNumber() , self.propose_stone() ) ):
			print("in while")

	def setColor(self, color):
		self.color = color
		print("I chose " + str(color))

	def getNumPlayer(self):
		return numPlayers

	def setNumPlayers(self, numPlayers):
		self.numPlayers = numPlayers

	@classmethod
	def set_max_number_of_players (class_ , a_number):
		class_.maxNumPlayers = a_number


	def getMyNumber (self):
		return int(self.number)

	def getOtherPlayerNumber(self):
		"""works for 2 players only"""
		return int((1 + self.number)%2)


class Brett:
	"""Brett soll das Model(l) sein, die Daten des Spieles enthalten. Von der Klasse soll es nur ein Objekt geben (Singleton?)."""
	# wenn es nur ein Objekt dieser Klasse gibt, wozu in Klassen- und Objektvariablen unterscheiden?
	#size = 6 
	# brett is a dictionary with key a tupel of integers. 
	# the value is 0 when empty, 1 when carrying a stone of player 1, 2 when carrying a stone of player 2
	# values are accessed or set through brett[(1,2)]

	def __init__(self, host, size: int):
		self.my_host = host
		self.size = size
		self.brett = {(k,l):-1 for k in range(self.size) for l in range(self.size)}
		self.score = [] # empty list 
		self.acceptedStone = (-1,-1)
		self.maxNumberStones = self.size * self.size

	#def setColor (self, color):	

	def update_scores(self):
		self.score = [0,0]
		
		b = list(self.brett.values())
		for i in range(2):
			self.score[i] = sum( 1 for j in range(len(b)) if b[j] == i )

	def get_scores(self):
		return self.score

	def updateBrett(self, id ):
		"""When a player has put a new stone on the board newly includes / cought stones turn change color"""
		newStone = self.acceptedStone
		directions = self.getDirections(newStone)

		dirTouchOpponent = []

		for direction in directions:
			if self.brett[ tuple( x + y for x,y in zip( newStone , direction) ) ] == (1 + id)%2 :
				dirTouchOpponent.append(direction)
		print("dir touch opponent " , dirTouchOpponent )

		dirEncloseOpponent = []

		for direction in dirTouchOpponent:
			pos = newStone
			print("initial position " , pos )
			enclose = False
			dicided = False
			while not dicided :
				try:
					nextField = self.brett[ tuple( x + y for x,y in zip(pos , direction) ) ] 
				except KeyError:
					dicided = True

				if nextField == (1 + id)%2 :
					pos = tuple( x + y for x,y in zip(pos , direction))
					print("new position " , pos)
				elif nextField == id :
					dirEncloseOpponent.append(direction)
					enclose = True
					dicided = True 
				else:
					dicided = True
	
		for direction in dirEncloseOpponent:
			pos = newStone 
			done = False
			while not done:
				nextStoneInLine = tuple( x + y for x,y in zip(pos , direction) )
				if self.brett[ nextStoneInLine ] == (1 + id)%2: 
					self.brett[ nextStoneInLine ] = id
					pos= nextStoneInLine
				else:
					done = True

	def printBrett(self):
		# it would be nice just to add one point innstead of printing all again from scratch
		k,v = zip(*self.brett.items())
		a = [k for k, v in self.brett.items() if v == 0]
		b = [k for k, v in self.brett.items() if v == 1]
		plt.plot([0,self.size-1,0,self.size-1],[0,0,self.size-1,self.size-1], marker= 'x', ls='')
		plt.plot(*zip(*a), marker='o', color='r', ls='')
		plt.plot(*zip(*b), marker='o', color='b', ls='')

		plt.draw()
		plt.show(block=False)


	def checkStone(self, id , position):
		print("in Brett : check Stone")
		# not catching the position outt of bounds, also zu groß
		# return brett.checkPositionExists(position) & brett.checkPositionFree(position) & brett.checkEncloseOpponent( id , position)
		if self.checkPositionExists(position):
			if self.checkPositionFree(position):
				if self.checkEncloseOpponent( id , position):
					print("checkStone: OK")
					return True
		
		return False


	def checkPositionExists(self, position):
		print("in Brett : check position exists")
		if (( position[0] in range(self.size)) & (position[1] in range(self.size))):
			return True
		else:
			return False	

	def checkPositionFree(self, position):
		print("in Brett : check position free")
		try:
			return self.brett[position] == -1
		except KeyError:
			return False

	def getDirections(self, position): 
		allDirections = [(1,0),(-1,0),(0,1),(0,-1),(-1,-1),(-1,1),(1,1),(1,-1)]
		
		d2 = [[ x + y for x,y in zip(position , direction) if x+y in range(self.size) ] for direction in allDirections ]
		# for a position and direction: if the go beyond the brett it maybe only one coordinate is affected
		# first only this coordinate is removed. Resulting in tupels of length 0 or 1.
		# these shorter tupels are then removed
		mask = [ len(d) == 2 for d in d2]
		# Problem with masking: arrays can be masked, lists cannot

		validDirections = [allDirections[i] for i in range(8) if mask[i]== True]
		# print("directions d2: " , directions)

		return validDirections


	def checkEncloseOpponent(self , id , position):
		
		print("in Brett : check enclose opponent")

		directions = self.getDirections(position)

		dirTouchOpponent = []

		for direction in directions:
			if self.brett[ tuple( x + y for x,y in zip(position , direction) ) ] == (1+id)%2  :
				dirTouchOpponent.append(direction)
		print("dir touch opponent " , dirTouchOpponent )


		if len(dirTouchOpponent) == 0:
			return False

		dirEncloseOpponent = []

		for direction in dirTouchOpponent:
			pos = position 
			print("initial position " , pos )
			enclose = False
			dicided = False
			while not dicided :
				try:
					nextField = self.brett[ tuple( x + y for x,y in zip(pos , direction) ) ] 
				except KeyError:
					dicided = True

				if nextField == (1+id)%2 :
					pos = tuple( x + y for x,y in zip(pos , direction))
					print("new position " , pos)
				elif nextField == id :
					return True
				else:
					dicided = True
		
		return False

		# check that the set stone is adjacent to a stone of the opponent
		# check that there exists a direction such that in that direction 
		# at some point lies a stone of the same colour as the set stone 


	def setStone(self, playerID , position):
		if self.checkStone(playerID , position): 
			self.brett[position] = playerID
			self.acceptedStone = position
			#player.lastStoneAccepted = True
			return True
		else:
			print("Stone rejected.")
			return False

	def controlNewPosition(self, id, position):
		pass
		
class Host:
	
	def __init__(self):
		self.my_board : Board
		self.my_player : list

	def createBoard(self, size):
		self.my_board = Brett(self, size)
		return self.my_board

	def setupBoard(self):
		"""soll man nicht machen: direkt auf die Daten zugreifen. Besser: Methode benutzen!"""
		self.my_board.brett[(1,1)] = 0
		self.my_board.brett[(1,2)] = 0	
		self.my_board.brett[(2,2)] = 1
		self.my_board.brett[(2,1)] = 1		
	# this should return something??	

	def invitePlayers(self):
		pass

	def create_players(self,some_number):
		# set class variable first
		Player.set_max_number_of_players(some_number)

		p=[]
		for i in range(some_number):
			p.append( Player(self) )	

		self.my_player = p 

		return p	

	def evaluate_stone(self , playerID , position): 
		"""Check stone and if OK set stone on board"""
		print("Übergebene Parameter ***") 
		print(list(self.my_board.brett.values()))
		#print(player.getMyNumber)
		print(position)
		print("in host : evaluate stone")
		if self.my_board.checkStone(playerID, tuple(position)) == True:
			if self.my_board.setStone(playerID , tuple(position)):
				self.my_player[playerID].lastStoneAccepted = True
				return True
		else:
			return False


	# def game_on(self):
	# return whether the game should go on.
	# is the next player allowed to continue ??
	# return True or False

	@staticmethod
	def next(i):
		return ((1 + i)%2)

def main ():

	print("Starte das Spiel")

	h = Host()

	b = h.createBoard(4)

	h.setupBoard()

	p = h.create_players(2)

	print(b.printBrett())

	b.update_scores()
	print("Punkte:" , b.get_scores())

	game_on = True
	stones_set = 4  # for stones initially set when setting up the board

	current = 0
	last = 0
	maxNumberOfTurns = b.maxNumberStones # define getter for max_number_of_stones 
	# better: move it all into Host or Board !!

	while game_on :
		
		p[current].negotiate_stone_position()

		# h.update_board()
		# the host updates the board. Information: Who was the last player and where was the stone put (if any WAS put)

		# in setStone the position of the last accepted stone is stored in Brett.acceptedStone
		# the same way you coud store the currently active player ...
		b.updateBrett(p[current].getMyNumber())

		b.printBrett()
		# with the subscriber pattern in a network setting (client / server)  this should change

		b.update_scores()
		print("Punkte:" , b.get_scores())

		last = current 
		current = h.next(current)

		game_on = ( p[last].lastStoneAccepted or p[current].lastStoneAccepted ) and (stones_set < maxNumberOfTurns)

	print("game over")
	# should show a "game over" screen to each player

	scores_at_end = b. get_scores()
	print("Punktestand am Ende:" , scores_at_end)
	if scores_at_end[0] > scores_at_end[1] : 
		print("Player 1 wins")
	elif scores_at_end[0] < scores_at_end[1] : 
		print("Player 2 wins")
	else:
		print("Both win.")	
	# the host should announce the winner


	# Funktioniert nicht, die Eingabe zu prüfen. 
	# Eingabe 9,9 produziert Keyvalue Error und wird nicht abgefangen

if __name__== "__main__":
  main()

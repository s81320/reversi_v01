# 10.2.2020
"""Should I have a docstring for the whole file?"""
# import numpy as np # this library is not used
import matplotlib.pyplot as plt

#run with python or pythonw (for MacOS)


# __all__  =  ['Host', 'Player', 'Board']

class Player:
    """The player class. What can I say??"""
    # class variables, shared by all instances of this class
    num_players_created = 0
    max_num_players = 2


    # class variable max_num_players has to be set before calling __init__
    def __init__(self, host):
        """initialize. Set the number. increase the number of created players."""
        # print("create Player")
        self.my_host = host
        self.number = Player.num_players_created
        self.last_stone_accepted = True
        Player.num_players_created = Player.num_players_created+1

    def propose_stone(self):
        """asks a player to give two integers as coordinates where to put his/her stone.
        returns a position as a tuple. No error handling."""
        pos = [-1, -1]
        #print("Type of pos " , type(pos))
        # here I used states and assignments
        #if self.get_my_number() == 0:
        #   col  =  'red'
        #else:
        #   col  =  'blue'
        #print("Set a " + col + " stone!")
        # this is now stateless. And it avoids an if else clause.
        colours = ['red', 'blue']
        print("Set a "+colours[self.get_my_number()]+" stone.")
        # get position from player - person
        for i in range(2):
            pos[i] = input(f"Input coordinate { i +1 } for your chosen position. Input an integer, range 0 to 7: ")
        return [int(pos[0]), int(pos[1])]


    def negotiate_stone(self):
        """A player-object gets a keyboard-input from the player-human. If not successful (out of bounds, not free), no stone is set and the game continues (with the next player)."""
        proposed_stone = self.propose_stone()
        self.last_stone_accepted = self.my_host.evaluate_stone(self.get_my_number(), proposed_stone)

    @classmethod
    def get_number_of_players(cls):
        """Returns the class-attribute number of players."""
        #return Player.num_players
        return cls.num_players_created

#   @classmethod
#   def set_max_number_of_players(class_, a_number):
#       """Simple setter. Does what the name suggests."""
#       class_.max_num_players = a_number

    def get_my_number(self):
        """returns the ID - number of a player."""
        return int(self.number)

    def get_other_player_number(self):
        """works for 2 players only"""
        return int((1+self.number)%2)

class Board:
    """Documenting the Board class."""
    def __init__(self, host):
        """init."""
        self.my_host = host
        self.size = 8
        self.max_number_stones = 64
        self.board = {(k, l):-1 for k in range(self.size) for l in range(self.size)}
        self.score = [] # empty list
        self.accepted_stone = (-1, -1)
        self.stones_set = 0

    def update_scores(self):
        """To be called after a new stone has been set. Calculates from scratch."""
        self.score = [0, 0]
        stones_on_board = list(self.board.values())
        for i in range(2):
            self.score[i] = sum(1 for j in range(len(stones_on_board)) if stones_on_board[j] == i)

    def get_scores(self):
        """simple getter function. Returns the score of both (possibly more, later ...) players."""
        return self.score

    def update_board(self, player_id):
        """When a player has put a new stone on the board newly includes / cought stones turn change color"""
        new_stone = self.accepted_stone
        directions = self.get_directions(new_stone)

        dir_touch_opponent = []

        for direction in directions:
            if self.board[tuple(x+y for x, y in zip(new_stone, direction))] == (1+player_id)%2:
                dir_touch_opponent.append(direction)
        print("dir touch opponent ", dir_touch_opponent)

        dir_enclose_opponent = []

        for direction in dir_touch_opponent:
            pos = new_stone
            #print("initial position ", pos)
            dicided = False
            while not dicided:
                try:
                    next_field = self.board[tuple(x+y for x, y in zip(pos, direction))]
                except KeyError:
                    dicided = True

                if next_field == (1+player_id)%2:
                    pos = tuple(x+y for x, y in zip(pos, direction))
                    #print("new position " , pos)
                elif next_field == player_id:
                    dir_enclose_opponent.append(direction)
                    dicided = True
                else:
                    dicided = True

        for direction in dir_enclose_opponent:
            pos = new_stone
            done = False
            while not done:
                next_stone_in_line = tuple(x+y for x, y in zip(pos, direction))
                if self.board[next_stone_in_line] == (1+player_id)%2:
                    self.board[next_stone_in_line] = player_id
                    pos = next_stone_in_line
                else:
                    done = True

    def print_board(self):
        """Outputs the board as a graph."""
        # it would be nice just to add one point instead of printing all again from scratch
        stones_player_0 = [k for k, v in self.board.items() if v == 0]
        stones_player_1 = [k for k, v in self.board.items() if v == 1]
        plt.plot([0, self.size-1, 0, self.size-1], [0, 0, self.size-1, self.size-1], marker='x', ls='')
        plt.plot(*zip(*stones_player_0), marker='o', color='r', ls='')
        plt.plot(*zip(*stones_player_1), marker='o', color='b', ls='')

        plt.draw()
        plt.show(block=False)


    def check_stone(self, player_id, position):
        """Calls three other check-functions."""
        #print("in Brett : check Stone")
        #code executes only until the first False
        return self.check_position_exists(position) and self.check_position_free(position) and self.check_enclose_opponent(player_id, position)

    def check_position_exists(self, position):
        """Returns True iff (position) is on the board."""
        #print("in Brett : check position exists")
        return (position[0] in range(self.size)) and (position[1] in range(self.size))

    def check_position_free(self, position):
        """Check if a (position) is free. Returns True iff no stone is already placed on that position."""
        #print("in Brett : check position free")
        return self.board[position] == -1

    def get_directions(self, position):
        """Given a (position) this function returns all other positions that are adjacent to this position and on the board."""
        all_directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1)]
        dont_remember_what_it_is = [[x+y for x, y in zip(position, direction) if x+y in range(self.size)] for direction in all_directions]
        mask = [len(d) == 2 for d in dont_remember_what_it_is]
        return [all_directions[i] for i in range(8) if mask[i]]

    def check_enclose_opponent(self, player_id, position):
        """For a player (player_id) to set a stone at a specified (position), this has to create an enclosing of the opponents' stones."""
        print("in Brett : check enclose opponent")
        directions = self.get_directions(position)
        dir_touch_opponent = []
        for direction in directions:
            if self.board[tuple(x+y for x, y in zip(position, direction))] == (1+player_id)%2:
                dir_touch_opponent.append(direction)
        print("dir touch opponent ", dir_touch_opponent)

        # this is a break statement - function can be exited at this point
        if len(dir_touch_opponent) == 0:
            return False

        print("is this ever reached? pylint thinks it's not.")
        dir_enclose_opponent = []
        for direction in dir_touch_opponent:
            pos = position
            #print("initial position ", pos)
            dicided = False
            while not dicided:
                try:
                    next_field = self.board[tuple(x+y for x, y in zip(pos, direction))]
                except KeyError:
                    dicided = True

                if next_field == (1+player_id)%2:
                    pos = tuple(x+y for x, y in zip(pos, direction))
                    #print("new position ", pos)
                elif next_field == player_id:
                    return True
                else:
                    dicided = True
        return False

        # check that the set stone is adjacent to a stone of the opponent
        # check that there exists a direction such that in that direction
        # at some point lies a stone of the same colour as the set stone

    def set_stone(self, player_id, position):
        """A stone is set on the board. Input: who (player_id_) sets the stone where (position)."""
        if self.check_stone(player_id, position):
            self.board[position] = player_id
            self.accepted_stone = position
            self.stones_set += 1
            return True
        else:
            print("Stone rejected.")
            return False

class Host:
    """The Host controlls the game. players communicate with the host, and s/he interacts with the board."""
    def __init__(self):
        """The host will have a board and players, to be created later. The host has a log file."""
        self.my_board: Board
        self.my_player: list

    def create_board(self):
        """The host creates the board. For size n there will be n*n possible positions for the stones to set."""
        self.my_board = Board(self)
        return self.my_board

    def setup_board(self):
        """soll man nicht machen: direkt auf die Daten zugreifen. Besser: Methode benutzen!"""
        # initial stones for player 0
        stones_0 = [(int(self.my_board.size/2)-1, int(self.my_board.size/2)-1), (int(self.my_board.size/2)-1, int(self.my_board.size/2))]
        self.my_board.board[stones_0[0]] = 0
        self.my_board.board[stones_0[1]] = 0
        # initial stones fpr player 1
        stones_1 = [(int(self.my_board.size/2), int(self.my_board.size/2)), (int(self.my_board.size/2), int(self.my_board.size/2)-1)]
        self.my_board.board[stones_1[0]] = 1
        self.my_board.board[stones_1[1]] = 1

        self.my_board.stones_set = 4

    def create_2_players(self):
        """The host creates 2 players."""
        return [Player(self), Player(self)]

    def evaluate_stone(self, player_id, position):
        """Check stone and set it , return True or False"""
        return self.my_board.set_stone(player_id, tuple(position))
        # avoid if then else statements
        #if self.my_board.set_stone(player_id, tuple(position)):
        #   return True
        #else:
        #   return False

def next_player(i):
    """get the id for the next player"""
    return (1+i)%2

def main():
    """D docstring for the main function."""
    print("***********************")
    print("*** Game starts now ***")
    print("***********************")
    print("*** Rules *************")
    print("***********************")
    print("*** Red and blue take turns in setting stones on the board. Players input positions where they want to set a stone of their colour.")
    print("*** A stone can only be set adjacent to a stone of the opponent and has to enclose stones of the opponent. Allenclosed stones will change colour and become the colour of the stone just set.")
    print("*** If a player sets a stone incorrectly, no stone is set. It is then the opponents turn to set a stone.")
    print("*** The game ends when the board is full or whenever the red player puts a stone incorrectly and the blue player immediately afterwards, too.")
    print("*** Game is interrupted at input ctrl+C followed by enter.")

    host = Host()
    board = host.create_board()
    host.setup_board()
    player = host.create_2_players()
    board.print_board()
    board.update_scores()
    print("Scores:", board.get_scores())

    game_on = True
    current = 0
    last = 0
    max_number_of_turns = board.max_number_stones # define getter for max_number_of_stones
    # better: move it all into Host or Board !!

    while game_on:
        player[current].negotiate_stone()
        if player[current].last_stone_accepted:
            board.update_board(player[current].get_my_number())
            board.print_board()
            board.update_scores()
            print("Punkte:", board.get_scores())

        last = current
        current = next_player(current)

        print("end of round. Next round?")
        print("last_stone_accepted ", player[0].last_stone_accepted, player[1].last_stone_accepted)
        print("all stones set? ", board.stones_set, " < ", max_number_of_turns, "?")
        game_on = ((player[last].last_stone_accepted or player[current].last_stone_accepted) and (board.stones_set < max_number_of_turns))
    print("*****************")
    print("*** game over ***")
    print("*****************")

    scores_at_end = board.get_scores()
    print("Scores for red and blue:", scores_at_end)
    if scores_at_end[0] > scores_at_end[1]:
        print("************************")
        print("*** red Player wins *** ")
        print("************************")
    elif scores_at_end[0] < scores_at_end[1]:
        print("************************")
        print("*** blue Player wins ***")
        print("************************")
    else:
        print("Both win.")

if __name__ == "__main__":
    main()

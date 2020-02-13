# 10.2.2020
"""Should I have a docstring for the whole file?"""
import numpy as np # this library is not used - not yet ... 11.2.2020
import matplotlib.pyplot as plt

#run with python or pythonw (for MacOS)

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
            pos[i] = input("input where you want to set the stone, one coordinate at a time. Range 0 to 7:")
      #      pos[i] = input(f"Input coordinate { i +1 } for your chosen position. Input an integer, range 0 to 7: ")
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

        directions = self.create_directions_ingoing(new_stone)
        dir_touch_opponent = self.select_directions_touching(player_id, new_stone, directions)
        dir_enclose_opponent = self.select_directions_enclosing(player_id, new_stone, dir_touch_opponent)

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
        """Calls three other check-functions.
        Check if the proposed position is within the boundries of the board,
        if the position is free / empty and if it creates an enclosing of the stones of the opponent.
        """
        #code executes only until the first False
        return self.check_position_exists(position) and self.check_position_free(position) and self.check_enclose_opponent(player_id, position)

    def check_position_exists(self, position):
        """Returns True iff (position) is on the board."""
        return (position[0] in range(self.size)) and (position[1] in range(self.size))

    def check_position_free(self, position):
        """Check if a (position) is free. Returns True iff no stone is already placed on that position."""
        return self.board[position] == -1

    def check_position_for_same_occupancy(self, position1, position2):
        """Returns True if on both positions there is the same colour or if both positions are empty."""
        return self.board[position1] == self.board[position2]

    def check_position_for_same_colour(self, position1, position2):
        """Returns True if both positions are occupied by the same player."""
        return (not self.check_position_free(position1)) and self.check_position_for_same_occupancy(position1, position2)

    def check_for_same_colour(self, arg1, arg2):
        """Should be called with arguments either of type tuple or the same as player.number, int (with values 0 or 1) at the moment.
        Where the argument is a player.number - what then??"""
        return_value = True
        if isinstance(arg1, tuple):
            if isinstance(arg2, tuple):
                return_value = self.check_position_for_same_colour(arg1, arg2)
            else:
                if isinstance(arg2, int):
                    return_value = (self.board[arg1] == arg2)
        else:
            if isinstance(arg1, int):
                if isinstance(arg2, tuple):
                    return_value = (arg1 == self.board[arg2])
                else:
                    if isinstance(arg2, int):
                        return_value = (arg1 == arg2)

        return return_value

    def create_directions_ingoing(self, position):
        """Given a (position) this function
        returns all directions that lead to a position that is adjacent to this position and on the board."""

        all_directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1))

        # filter returns an iterator, we have to materialize the filter and turn it into a tuple (or list or whatever...)
        return tuple(filter(lambda x: self.check_position_exists(np.array(position)+x), all_directions))
        # all directions used to be a list, now it is a tuple. Seems to work fine...
        # filter needs the data to be filtered as a iterable container

    def select_directions_touching(self, own_player_id, position, directions):
        """Of all ingoing directions / directions that from (position) in (directions) stay on the board
        select those where the current player (own_player_id) touches / is directly adjacent to a stone of the opponent.
        For player 1 it would be necessary to put a stone such that in (direction) we see 1 0 .
        Especially a stone cannot be placed on a (position) where it would be surrounded by empty positions only.

        input: a n-tuple of directions, n in {0,..,8}, with each direction a 2-tuple.
        output: a possibly reduced input tuple. """

        #print("in select directions touching")
        #print("args: " , position , directions)
        dir_touch_opponent = []
        for direction in directions:
            pos = position
            adjacent_pos = tuple(np.array(pos) + np.array(direction))
            if self.check_position_exists(adjacent_pos) and not self.check_position_free(adjacent_pos):
                #print("position exists and occupied: " , adjacent_pos)
                if not self.check_for_same_colour(own_player_id, adjacent_pos):
                    dir_touch_opponent.append(direction)
                    #print("not same colour, append" , dir_touch_opponent)
        return dir_touch_opponent

    def select_directions_enclosing(self, player_id, start_pos_on_beam, directions):
        """Of all (directions) in which the player (player_id) directly touches a stone of the opponent
        select those where at some time there comes a stone of the own colour again.
        that is for player 1 in that direction there is    1 0 1   or    1 0 0 0 1

        For a player (player_id) at a position (start_pos_on_beam) walking on the board in a direction (element of directions):
        What happens first:
        1) get to limit of the board,
        2) meet an empty position,
        3) meet your own colour again
        If it is no 3 then the player does enclose the opponent in this direction. 
        So, append the direction to the list that will later be returned.

        Requires (directions) to be ingoing and touching directions.
        The following methods of class Board should be called to get the correct (directions):
        select_ingoing_directions , select_touching_directions."""
        dir_enclose_opponent = []

        for direction in directions:
            walk_on_beam = True # starting at (start_pos_on_beam) walking on the board in (direction) we create a straight line path, i.e. a beam
            pos_on_beam = start_pos_on_beam
            while walk_on_beam:
                step_further_on_beam = tuple(np.array(pos_on_beam) + np.array(direction)) # a step further in (direction)
                if self.check_position_exists(step_further_on_beam) and not self.check_position_free(step_further_on_beam):
                    if self.check_for_same_colour(player_id, step_further_on_beam): # meet your own colour again! it's an enclosing!
                        dir_enclose_opponent.append(direction)
                        walk_on_beam = False
                    else:
                        pos_on_beam = step_further_on_beam # walk on and look for a stone of your own colour
                else:
                    walk_on_beam = False # stepped on empty field or out of bounds of the board
        return dir_enclose_opponent

    def check_enclose_opponent(self, player_id, position):
        """A player (player_id) canset a stone at a (position) if - along a line of stones on the board -
        an enclosing of the opponents stones is created.
        If player 1 sets a stone right next to a line like 0 0 1 so that it becomes 1 0 0 1,
        or 1 0 0 0 so that it becomes 1 0 0 0 1.
        Similarly for up - down directions or on other directions like south west to north east.
        
        Starting from all possible directions reduce to ingoing directions: 
            positions, such that position + direction stays on the board
        From all ingoing directions reduce to directions that touch an opponents stone: 
            that are directly adjacent to a stone of the opponent
        From these directions reduce to directions that enclose the opponents stones.
        """
        directions = self.create_directions_ingoing(position)
        dir_touch_opponent = self.select_directions_touching(player_id, position, directions)
        dir_enclose_opponent = self.select_directions_enclosing(player_id, position, dir_touch_opponent)
        return len(dir_enclose_opponent) > 0

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
        self.my_board.board[(3, 3)] = 0
        self.my_board.board[(3, 4)] = 0
        self.my_board.board[(4, 3)] = 1
        self.my_board.board[(4, 4)] = 1

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

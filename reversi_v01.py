# 27.2.2020
"""Board game reversi (aka othello) for 2 players (or 1 player impersonating both the player and his/her opponent).
Game is played at one terminal."""
import numpy as np
import matplotlib.pyplot as plt

#run with python or pythonw (for MacOS)

class Player:
    """Two players compete against each other.
    Players communicate through their mediator, the Host.
    Players are identified by their (number), either 0 or 1."""
    # class variables, shared by all instances of this class
    num_players_created = 0
    max_num_players = 2

    def __init__(self, host):
        """initialize. Set the number. increase the number of created players."""
        self.my_host = host
        self.number = Player.num_players_created
        self.last_stone_accepted = True
        Player.num_players_created = Player.num_players_created+1

    def input_stone_position(self):
        """asks a player to give two integers as coordinates where to put his/her stone.
        returns a position as a tuple. No error handling."""
        pos = [-1, -1]
        colours = ['red', 'blue']
        print("Set a "+colours[self.get_number()]+" stone.")
        # get position from player - person
        for i in range(2):
            pos[i] = input("one co-ordinate, range 0 to 7:")
        return [int(pos[0]), int(pos[1])]

    def propose_stone(self):
        """A player-object gets a keyboard-input from the player-human. If not successful (out of bounds, not free), no stone is set and the game continues (with the next player)."""
        proposed_stone = self.input_stone_position()
        self.last_stone_accepted = self.my_host.evaluate_stone(self.get_number(), proposed_stone)

    def get_number(self):
        """returns the ID - number of a player."""
        return int(self.number)

class Board:
    """The reversi board is an 8 x 8 squares board.
    The Host sets stones on the board.
    Players communicate to the Host where the stone should be set
    and the Host checks for compliance with reversi rules.

    Once a stone is accepted and set the board is updated according to reversi rules:
    Stones of the opponent that are enclosed (along a straight line: up/down-wards, left-to-right or in a diagonal fashion)
    by the new stone of the active player and an old stone (also belonging to the active player) change colour
    and become stones of the active player."""
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

    def check_for_different_colour(self, arg1_position, arg2):
        """Returns True if arg1_position is a position (type tuple) and
        occupied and with a different colour from arg2, which may be a position or a colour (type tuple or int).
        So the ordering is imortant here. There is flexibility only in the second argument."""
        return (not self.check_position_free(arg1_position)) and (not self.check_for_same_colour(arg1_position, arg2))

    def check_position_for_same_colour(self, position1, position2):
        """Returns True if both positions are occupied by the same player."""
        return (not self.check_position_free(position1)) and self.check_position_for_same_occupancy(position1, position2)

    def check_for_same_colour(self, arg1_position, arg2):
        """Should be called with arguments either of type tuple or the same as player.number: int (with values 0 or 1).
        If it is a tuple, it is a position on the board and the colour has to be looked up when comparing.
        If an argument is an int, it already denotes a colour / a players id and thus its colour."""
        return_value = True
        if isinstance(arg2, tuple):
            return_value = self.check_position_for_same_colour(arg1_position, arg2)
        else:
            return_value = (self.board[arg1_position] == arg2)
        return return_value

    def create_directions_ingoing(self, position):
        """Given a (position) this function
        returns all directions that lead to a position that is adjacent to this position and on the board."""

        all_directions = ((1, 0), (-1, 0), (0, 1), (0, -1), (-1, -1), (-1, 1), (1, 1), (1, -1))

        # filter returns an iterator, we have to materialize the filter and turn it into a tuple (or list or whatever...)
        return tuple(filter(lambda x: self.check_position_exists(np.array(position)+x), all_directions))
        # all directions used to be a list, now it is a tuple. Seems to work fine...
        # filter needs the data to be filtered as a iterable container

    def select_directions_touching(self, player_id, position, directions):
        """Filters directions such that (position) + (direction) is
        of different colour than the players own stone (player_id).
        Requires input (directions) to be of ingoing directions only."""
        return tuple(filter(lambda x: self.check_for_different_colour(tuple(np.array(position)+np.array(x)), player_id), directions))


    def walk_on_beam(self, colour, position, direction):
        """Recursion replacing a while loop.
        On the reversi board a beam is formed
        starting at the (position) a new stone may be [checking stone] or has been [update board] set
        in a given (direction).
        colour is the colour of the stone that may be or has been set. This is at (position).

        Walking on that beam we take one step at a time, only to the (next_pos).
        We return False if the beam of opponents stone ends in an empty field or at the boundary of the board.
        and True if we meet a stone of our initially set (colour)."""

        next_pos = tuple(np.array(position) + np.array(direction))

        if not self.check_position_exists(next_pos): # position is on the boundary, next_pos is off the board
            return False
        elif self.check_position_free(next_pos): # position exists, is on board -> but empty
            return False
        elif self.check_for_same_colour(next_pos, colour): # next_pos is on the board and occupied -> colours match
            return True
        else: # undecided -> walk to next position on the beam
            return self.walk_on_beam(colour, next_pos, direction)

    def select_directions_enclosing(self, player_id, start_pos, directions):
        """Filters directions d such that along the beam starting in start_pos and in direction d
        at some time another stone is met that has the colour belonging to (player_id).
        This means setting a stone at start_pos would create an enclosing of the opponent players stones. """
        return tuple(filter(lambda d: self.walk_on_beam(player_id, np.array(start_pos) + np.array(d), np.array(d)), directions))


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
        From these directions reduce to directions that enclose the opponents stones."""
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
            print("Your stone was rejected. Next player, please.")
            return False

class Host:
    """The Host controlls the game. players communicate with the host, and s/he interacts with the board."""
    def __init__(self):
        """The host is mediator between the boardt and two playerse."""
        self.my_board = Board(self)
        self.my_player = [Player(self), Player(self)]
        
    def setup_board(self):
        """Initially there are 4 stones at the center of the board, two in each players colour."""
        self.my_board.board[(3, 3)] = 0
        self.my_board.board[(3, 4)] = 0
        self.my_board.board[(4, 3)] = 1
        self.my_board.board[(4, 4)] = 1

        self.my_board.stones_set = 4

    def evaluate_stone(self, player_id, position):
        """Check stone and set it , return True or False"""
        return self.my_board.set_stone(player_id, tuple(position))

def opponent(i):
    """calculate the id for the other player, the opponent."""
    return (1+i)%2

def main():
    """Players act one at a time. Each time through the loop one player is allowed to set a stone.
    The other player is sometimes called the opponent.
    Roles change at the end of each loop."""
    print("***********************")
    print("*** Game starts now ***")
    print("***********************")
    print("*** Rules *************")
    print("***********************")
    print("*** Red and blue take turns in setting stones on the board. Players input positions where they want to set a stone of their colour.")
    print("*** A stone can only be set adjacent to a stone of the opponent and has to enclose stones of the opponent. All enclosed stones will change colour and become the colour of the stone just set.")
    print("*** If a player sets a stone incorrectly, no stone is set. It is then the opponents turn to set a stone.")
    print("*** The game ends when the board is full or whenever the red player puts a stone incorrectly and the blue player immediately afterwards, too.")
    print("*** Game is interrupted at input ctrl+C followed by enter.")
    print("***********************")

    host = Host()
    host.setup_board()

    host.my_board.print_board()
    host.my_board.update_scores()
    print("Scores for red and blue:", host.my_board.get_scores())

    game_on = True
    current = 0
    last = 0

    while game_on:
        host.my_player[current].propose_stone()
        if host.my_player[current].last_stone_accepted:
            host.my_board.update_board(host.my_player[current].get_number())
            host.my_board.print_board()
            host.my_board.update_scores()
            print("Scores for red and blue:", host.my_board.get_scores())

        game_on = ((host.my_player[last].last_stone_accepted or host.my_player[current].last_stone_accepted) and (host.my_board.stones_set < host.my_board.max_number_stones ))

        last = current
        current = opponent(current)

    print("*****************")
    print("*** game over ***")
    print("*****************")

    scores_at_end = host.my_board.get_scores()
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
        print("************************")
        print("*** Both player win. ***")
        print("************************")

if __name__ == "__main__":
    main()

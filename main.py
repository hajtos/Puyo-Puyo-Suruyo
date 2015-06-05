"""
authors: Pawel Chachaj, Krzysztof Hajto
version: 0.3

This is the main executable for running the puyo puyo game
"""

from puyo.game_ui import GameUI
from puyo.graphics.colors import COLORS as Colors
from puyo.player_controller import PlayerController
from puyo.graphics.board_frame import BoardFrame
from puyo.graphics.scoreboard_frame import ScoreBoardFrame
from puyo.system.game_map import GameMap
import pygame.locals as gamelocals
import argparse

TITLE = 'Puyo puyo'
#----window size
WINDOW_WIDTH = 860
WINDOW_HEIGHT = 480
#----window bg color
BACKGROUND_COLOR = Colors.DARKTURQUOISE
#----board size
MARGIN = 40
BOARD_WIDTH = 300
BOARD_HEIGHT = WINDOW_HEIGHT-2*MARGIN
SCOREBOARD_MARGIN = 20
SCOREBOARD_WIDTH = WINDOW_WIDTH-2*BOARD_WIDTH-2*MARGIN-2*SCOREBOARD_MARGIN
SCOREBOARD_HEIGHT = 100

class ArgParser(object):
    """
    A parser for command line arguments
    """
    def __init__(self):
        """
        initializes parser
        """
        self.parser = argparse.ArgumentParser()

    def load_options(self):
        """
        loads parser options
        """
        self.parser.add_argument("-c", "--colors", \
            help="The number of colors", type=int, default=4)
        self.parser.add_argument("-f", "--framerate", help="The frames per \
            second, affects game speed", type=int, default=25)
        self.parser.add_argument("-s", "--size", help="The size of the board, \
            rows and columns", nargs=2, type=int, default=(12, 6))
        self.parser.add_argument("--player1", help="The name of the first \
            player", default="player1")
        self.parser.add_argument("--player2", help="The name of the second \
            player", default="player2")
        self.parser.add_argument("-l", "--limit", help="The number of elements \
            before a group is deleted", type=int, default=3)
        self.parser.add_argument("-ps", "--player-speed", help="The number of \
            frames required for a block to fall by one", type=int, default=10)
        return self

    def get_args(self):
        """
        parses arguments
        """
        return self.parser.parse_args()


def start_game():
    """
    Starts the game
    """
    args = ArgParser().load_options().get_args()
    game = GameUI(TITLE, ((WINDOW_HEIGHT, WINDOW_WIDTH), \
        args.size), args.framerate, BACKGROUND_COLOR)
    # pylint: disable=E1103
    player_controller1 = PlayerController([gamelocals.K_a, gamelocals.K_d, \
        gamelocals.K_w, gamelocals.K_w, gamelocals.K_s])
    player_controller2 = PlayerController([gamelocals.K_LEFT, \
        gamelocals.K_RIGHT, gamelocals.K_UP, gamelocals.K_UP, gamelocals.K_DOWN])
    # pylint: enable=E1103
    game.set_players(player_controller1, player_controller2)
    board_1 = BoardFrame(game.display_surf, (MARGIN, MARGIN), \
                BOARD_WIDTH, BOARD_HEIGHT)
    board_2 = BoardFrame(game.display_surf, (WINDOW_WIDTH-BOARD_WIDTH-MARGIN, \
                MARGIN), BOARD_WIDTH, BOARD_HEIGHT)
    game.set_game_boards(board_1, board_2)
    scoreboard_1 = ScoreBoardFrame(args.player1, game.display_surf, \
                (MARGIN+BOARD_WIDTH+SCOREBOARD_MARGIN, MARGIN), \
                (SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT))
    scoreboard_2 = ScoreBoardFrame(args.player2, game.display_surf, \
                (MARGIN+BOARD_WIDTH+SCOREBOARD_MARGIN, \
                MARGIN+BOARD_HEIGHT-SCOREBOARD_HEIGHT), \
                (SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT))
    game.set_scoreboards(scoreboard_1, scoreboard_2)
    game_map1 = GameMap(game, size=args.size, \
        params=(args.limit, args.colors, args.player_speed))
    game_map2 = GameMap(game, size=args.size, \
        params=(args.limit, args.colors, args.player_speed))
    game.set_game_maps(game_map1, game_map2)
    game.start()

if __name__ == "__main__":
    start_game()

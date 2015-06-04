"""
authors: Pawel Chachaj, Krzysztof Hajto
version: 0.3

This is the main executable for running the puyo puyo game
"""

from puyo.GameUI import GameUI
from puyo.Graphics.Colors import COLORS as Colors
from puyo.PlayerController import PlayerController
from puyo.Graphics.BoardFrame import BoardFrame
from puyo.Graphics.ScoreBoardFrame import ScoreBoardFrame
from puyo.System.GameMap import GameMap
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

    def loadOptions(self):
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

    def getArgs(self):
        """
        parses arguments
        """
        return self.parser.parse_args()


def startGame():
    """
    Starts the game
    """
    args = ArgParser().loadOptions().getArgs()
    game = GameUI(TITLE, WINDOW_HEIGHT, WINDOW_WIDTH, \
        args.size, args.framerate, BACKGROUND_COLOR)
    # pylint: disable=E1103
    player_controller1 = PlayerController(gamelocals.K_a, gamelocals.K_d, \
        gamelocals.K_w, gamelocals.K_w, gamelocals.K_s)
    player_controller2 = PlayerController(gamelocals.K_LEFT, \
        gamelocals.K_RIGHT, gamelocals.K_UP, gamelocals.K_UP, gamelocals.K_DOWN)
    # pylint: enable=E1103
    game.setPlayers(player_controller1, player_controller2)
    board_1 = BoardFrame(game.display_surf, MARGIN, MARGIN, \
                BOARD_WIDTH, BOARD_HEIGHT)
    board_2 = BoardFrame(game.display_surf, WINDOW_WIDTH-BOARD_WIDTH-MARGIN, \
                MARGIN, BOARD_WIDTH, BOARD_HEIGHT)
    game.setGameBoards(board_1, board_2)
    scoreboard_1 = ScoreBoardFrame(args.player1, game.display_surf, \
                MARGIN+BOARD_WIDTH+SCOREBOARD_MARGIN, MARGIN, \
                SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
    scoreboard_2 = ScoreBoardFrame(args.player2, game.display_surf, \
                MARGIN+BOARD_WIDTH+SCOREBOARD_MARGIN, \
                MARGIN+BOARD_HEIGHT-SCOREBOARD_HEIGHT, \
                SCOREBOARD_WIDTH, SCOREBOARD_HEIGHT)
    game.setScoreboard(scoreboard_1, scoreboard_2)
    game_map1 = GameMap(game, colors=args.colors, size=args.size, \
        player_ticks=args.player_speed, limit=args.limit)
    game_map2 = GameMap(game, colors=args.colors, size=args.size, \
        player_ticks=args.player_speed, limit=args.limit)
    game.setGameMaps(game_map1, game_map2)
    game.start()

if __name__ == "__main__":
    startGame()

from GameUI import GameUI
from Graphics.Colors import Colors
from PlayerController import PlayerController
from Graphics.BoardFrame import BoardFrame
from Graphics.ScoreBoardFrame import ScoreBoardFrame
from Graphics.TextFrame import TextFrame
from pygame.locals import *
#main

#class main(object):
#    def __init__(self):
#print '2'
#----window title
TITLE = 'Puyo puyo'
#----window size
WINDOW_WIDTH = 860
WINDOW_HEIGHT = 480
#----game speed
FPS = 30
#----window bg color
BACKGROUND_COLOR = Colors.DARKTURQUOISE

game = GameUI(TITLE, WINDOW_HEIGHT, WINDOW_WIDTH, (12,6), FPS, BACKGROUND_COLOR)

#create players
playerController_1 = PlayerController(K_a, K_d, K_w, K_w, K_s)
playerController_2 = PlayerController(K_LEFT, K_RIGHT, K_UP, K_UP, K_DOWN)
game.setPlayers(playerController_1, playerController_2)

#----create boards
#----window margin
MARGIN = 40
#----board size
BOARD_WIDTH = 300
BOARD_HEIGHT = WINDOW_HEIGHT-2*MARGIN

board_1 = BoardFrame(
                game.DISPLAYSURF, 
                MARGIN, 
                MARGIN, 
                BOARD_WIDTH, 
                BOARD_HEIGHT)
board_2 = BoardFrame(
                game.DISPLAYSURF, 
                WINDOW_WIDTH-BOARD_WIDTH-MARGIN, 
                MARGIN, 
                BOARD_WIDTH, 
                BOARD_HEIGHT)

game.setGameBoards(board_1, board_2)

#----create scoreboards
#----scoreboard size
SCOREBOARD_MARGIN = 20
SCOREBOARD_WIDTH = WINDOW_WIDTH-2*BOARD_WIDTH-2*MARGIN-2*SCOREBOARD_MARGIN
SCOREBOARD_HEIGHT = 100

scoreboard_1 = ScoreBoardFrame(
                'Player 1', 
                game.DISPLAYSURF,
                MARGIN+BOARD_WIDTH+SCOREBOARD_MARGIN, 
                MARGIN, 
                SCOREBOARD_WIDTH, 
                SCOREBOARD_HEIGHT)
scoreboard_2 = ScoreBoardFrame(
                'Player 2', 
                game.DISPLAYSURF,
                MARGIN+BOARD_WIDTH+SCOREBOARD_MARGIN, 
                MARGIN+BOARD_HEIGHT-SCOREBOARD_HEIGHT, 
                SCOREBOARD_WIDTH, 
                SCOREBOARD_HEIGHT)

game.setScoreboard(scoreboard_1, scoreboard_2)
#print '1'
game.start()

#main()
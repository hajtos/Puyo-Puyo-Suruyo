"""
author: Pawel Chachaj
version: 0.2



"""
#from .Graphics import *
from .Graphics.Colors import COLORS as Colors
from .Graphics.TextFrame import TextFrame
import pygame, sys
import pygame.locals as gamelocals
from .System.GameMap import GameMap


class GameUI(object):
    '''main game handler'''
    #----game key values
    # pylint: disable=E1103
    KEY_PAUSE = gamelocals.K_p
    KEY_START = 13
    KEY_EXIT = gamelocals.K_ESCAPE
    KEY_RESTART = gamelocals.K_BACKSPACE
    # pylint: enable=E1103
    KEYS_TIP = 'Start = Enter, Pause = P, Restart Game = BACKSPACE, \
        Exit = Ecs '

    def __init__(self, title, height, width, size, fps, bg_color):
        '''initialize all variables'''
        self.fps = fps
        self.background_color = bg_color
        self.window_height = height
        self.window_width = width
        self.fps_clock = pygame.time.Clock()
        self.display_surf = \
            pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(title)
        self.size = size
        self.player_controller_1 = None
        self.player_controller_2 = None
        self.board_1 = None
        self.board_2 = None
        self.scoreboard_1 = None
        self.scoreboard_2 = None
        self.game_map1 = None
        self.game_map2 = None
        #----main loop
        self.exit = False
        self.pause = False
        self.start_stopper = True

    def setPlayers(self, player_1, player_2):
        '''set player controllers'''
        self.player_controller_1 = player_1
        self.player_controller_2 = player_2

    def setGameBoards(self, board_1, board_2):
        '''set game boards for players'''
        self.board_1 = board_1.setSize(self.size)#.setMap(GameMap(self.size))
        self.board_2 = board_2.setSize(self.size)#.setMap(GameMap(self.size))

    def setScoreboard(self, scoreboard_1, scoreboard_2):
        self.scoreboard_1 = scoreboard_1
        self.scoreboard_2 = scoreboard_2

    def setGameMaps(self, game_map1, game_map2):
        """
        set gameMap objects for handling board system
        """
        self.game_map1 = game_map1
        self.game_map2 = game_map2

    def start(self):
        '''start game, handle logic and graphic'''
        # pylint: disable=R0912
        self.drawNewGame()
        while True:
            #----main event handler
            events = self.eventHandler()
            #----logic
            for event in events:
                print event
                if event[0] == 'game':
                    if event[1] == 'quit':
                        self.terminate()
                        break
                    elif event[1] == 'pause':
                        self.pause = not self.pause
                        self.drawNewGame()
                        break
                    elif event[1] == 'start':
                        self.pause = False
                        self.start_stopper = False
                        self.drawNewGame()
                        break
                    elif event[1] == 'restart':
                        self.restartGame()
                        break
                elif not self.pause and event[0] == 'player':
                    the_map = None
                    if event[1] == 1:
                        the_map = self.game_map1
                    elif event[1] == 2:
                        the_map = self.game_map2
                    if event[2] == 'move':
                        if event[3] == 'left':
                            the_map.keyMove(-1)
                        elif event[3] == 'right':
                            the_map.keyMove(1)
                    elif event[2] == 'rotate':
                        the_map.rotate()
                    elif event[2] == 'speed':
                        if event[3] == 'up':
                            the_map.startSpeed()
                        elif event[3] == 'down':
                            the_map.stopSpeed()
            if self.exit: #exit game if terimnated
                break
            if self.start_stopper: #wait for key input to start the game
                self.drawStopper('START', Colors.WHITE, Colors.LIGHTGREEN)
                continue
            if self.pause: #do nothing if game paused
                self.drawStopper('PAUSE', Colors.WHITE, Colors.GREY)
                continue
            #test
            self.game_map1.tick()
            self.game_map2.tick()
            #----display
            #background
            self.drawGame()
            self.fps_clock.tick(self.fps)
        # pylint: enable=R0912

    def get_score(self, game_map, combo, cell_count):
        print 'score: ', combo, cell_count
        score = combo*cell_count
        if game_map == self.game_map1:
            self.scoreboard_1.addScore(score)
            self.game_map2.addColorless(float(score)/5)
        elif game_map == self.game_map2:
            self.scoreboard_2.addScore(score)
            self.game_map1.addColorless(float(score)/5)
        self.scoreboard_1.draw()
        self.scoreboard_2.draw()
        pygame.display.update()

    def drawNewGame(self):
        self.display_surf.fill(self.background_color)
        self.drawTips()
        self.board_1.drawMap(self.game_map1.getMap())
        self.board_2.drawMap(self.game_map2.getMap())
        self.scoreboard_1.draw()
        self.scoreboard_2.draw()
        pygame.display.update()

    def drawGame(self):
        self.board_1.drawMap(self.game_map1.getMap())
        self.board_2.drawMap(self.game_map2.getMap())
        pygame.display.update()

    def drawTips(self):
        self.drawText(self.KEYS_TIP, 15, Colors.BLACK, \
            Colors.WHITE, 0, self.window_height-20)

    def drawStopper(self, text, txt_color, bg_color):
        self.drawText('   '+text+'   ', 40, txt_color, bg_color, \
            self.window_width/2-100, self.window_height/2-35)

    def drawText(self, text, size, txt_color, bg_color, start_x, start_y):
        text_font = TextFrame(size)
        surf, rect = text_font.makeText(text, txt_color, \
            bg_color, start_x, start_y)
        self.display_surf.blit(surf, rect)
        pygame.display.update()

    def terminate(self):
        '''exit game & windown'''
        self.exit = True
        # pylint: disable=E1103
        # pylint: disable=W0104
        pygame.quit()
        sys.exit
        # pylint: enable=W0104
        # pylint: enable=E1103

    def restartGame(self):
        self.start_stopper = True
        self.scoreboard_1.setScore(0)
        self.scoreboard_2.setScore(0)
        self.game_map1 = GameMap(self).copyArgs(self.game_map1)
        self.game_map2 = GameMap(self).copyArgs(self.game_map2)

    def eventHandler(self):
        '''handle quit and key events'''
        # pylint: disable=E1103
        # pylint: disable=R0912
        # get all the QUIT events
        for event in pygame.event.get(gamelocals.QUIT):
            yield ['game', 'quit']
        # get all the KEYDOWN events
        for event in pygame.event.get(gamelocals.KEYDOWN):
            if self.player_controller_1.getByKeyDown(event.key, 1) \
                    is not None:
                yield self.player_controller_1.getByKeyDown(event.key, 1)
            elif self.player_controller_2.getByKeyDown(event.key, 2) \
                    is not None:
                yield self.player_controller_2.getByKeyDown(event.key, 2)
        # get all the KEYUP events
        for event in pygame.event.get(gamelocals.KEYUP):
            if event.key == self.KEY_EXIT:
                yield ['game', 'quit']
            elif event.key == self.KEY_PAUSE:
                yield ['game', 'pause']
            elif event.key == self.KEY_START:
                yield ['game', 'start']
            elif event.key == self.KEY_RESTART:
                yield ['game', 'restart']
            elif self.player_controller_1.getByKeyUp(event.key, 1) is not None:
                yield self.player_controller_1.getByKeyUp(event.key, 1)
            elif self.player_controller_2.getByKeyUp(event.key, 2) is not None:
                yield self.player_controller_2.getByKeyUp(event.key, 2)
        # pylint: enable=R0912
        # pylint: enable=E1103

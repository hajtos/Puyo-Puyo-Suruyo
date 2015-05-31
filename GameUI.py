from Graphics import *
import PlayerController
from Graphics.Colors import Colors
from PlayerController import PlayerController
from Graphics.TextFrame import TextFrame
import pygame, sys, random
from pygame.locals import *
from System.GameMap import GameMap


class GameUI(object):
    '''main game handler'''
    #----game key values
    KEY_PAUSE = K_p
    KEY_START = 13
    KEY_EXIT = K_ESCAPE
    KEY_RESTART = K_BACKSPACE
    KEYS_TIP = 'Start = Enter, Pause = P, Restart Game = BACKSPACE, Exit = Ecs '

    def __init__(self, title, height, width, size, fps, bg_color):
        '''initialize all variables'''
        self.FPS = fps
        self.BACKGROUND_COLOR = bg_color
        self.WINDOW_HEIGHT = height
        self.WINDOW_WIDTH = width
        self.FPSCLOCK = pygame.time.Clock()
        self.DISPLAYSURF = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption(title)
        self.size = size
        self.playerController_1 = None
        self.playerController_2 = None
        self.board_1 = None
        self.board_2 = None
        self.scoreboard_1 = None
        self.scoreboard_2 = None
        self.gameMap1 = GameMap(self, size=self.size)
        self.gameMap2 = GameMap(self, size=self.size)
        #----main loop
        self.exit = False
        self.pause = False
        self.start_stopper = True
    
    def setPlayers(self, player_1, player_2):
        '''set player controllers'''
        self.playerController_1 = player_1
        self.playerController_2 = player_2
    
    def setGameBoards(self, board_1, board_2):
        '''set game boards for players'''
        self.board_1 = board_1.setSize(self.size)#.setMap(GameMap(self.size))
        self.board_2 = board_2.setSize(self.size)#.setMap(GameMap(self.size))
    
    def setScoreboard(self, scoreboard_1, scoreboard_2):
        self.scoreboard_1 = scoreboard_1
        self.scoreboard_2 = scoreboard_2
        
    def start(self):
        '''start game, handle logic and graphic'''
        self.drawNewGame()
        time = 0
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
                        the_map = self.gameMap1
                    elif event[1] == 2:
                        the_map = self.gameMap2
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
            self.gameMap1.tick()
            self.gameMap2.tick()
            #----display
            #background
            self.drawGame()
            self.FPSCLOCK.tick(self.FPS)
    
    def get_score(self, gameMap, combo, cell_count):
        print 'score: ', combo, cell_count
        score = combo*cell_count
        if gameMap == self.gameMap1:
            self.scoreboard_1.addScore(score)
            self.gameMap2.addColorless(float(score)/10)
        elif gameMap == self.gameMap2:
            self.scoreboard_2.addScore(score)
            self.gameMap1.addColorless(float(score)/10)
        self.scoreboard_1.draw()
        self.scoreboard_2.draw()
        pygame.display.update()
    
    def drawNewGame(self):
            self.DISPLAYSURF.fill(self.BACKGROUND_COLOR)
            self.drawTips()
            self.board_1.draw(self.gameMap1.getMap())
            self.board_2.draw(self.gameMap2.getMap())
            self.scoreboard_1.draw()
            self.scoreboard_2.draw()
            pygame.display.update()
    
    def drawGame(self):
            self.board_1.draw(self.gameMap1.getMap())
            self.board_2.draw(self.gameMap2.getMap())
            pygame.display.update()
        
    def drawTips(self):
        self.drawText(self.KEYS_TIP, 15, Colors.BLACK, Colors.WHITE, 0, self.WINDOW_HEIGHT-20)
    
    def drawStopper(self, text, txt_color, bg_color):
        self.drawText('   '+text+'   ', 40, txt_color, bg_color, self.WINDOW_WIDTH/2-100, self.WINDOW_HEIGHT/2-35)
    
    def drawText(self, text, size, txt_color, bg_color, start_x, start_y):
        self.textFont = TextFrame(size)
        SURF, RECT = self.textFont.makeText(text, txt_color, bg_color, start_x, start_y)
        self.DISPLAYSURF.blit(SURF, RECT)
        pygame.display.update()
    
    def terminate(self):
        '''exit game & windown'''
        self.exit = True
        pygame.quit()
        sys.exit
    
    def restartGame(self):
        self.start_stopper = True
        self.scoreboard_1.setScore(0)
        self.scoreboard_2.setScore(0)
        self.gameMap1 = GameMap(self)
        self.gameMap2 = GameMap(self)

    def eventHandler(self):
        '''handle quit and key events'''
        for event in pygame.event.get(QUIT): # get all the QUIT events
            yield ['game', 'quit']
        
        for event in pygame.event.get(KEYDOWN): # get all the KEYDOWN events
            if event.key == self.playerController_1.SPEED:
                yield ['player', 1, 'speed', 'up']
            elif event.key == self.playerController_2.SPEED:
                yield ['player', 2, 'speed', 'up']
        
        for event in pygame.event.get(KEYUP): # get all the KEYUP events
            if event.key == self.KEY_EXIT:
                yield ['game', 'quit']
            elif event.key == self.KEY_PAUSE:
                yield ['game', 'pause']
            elif event.key == self.KEY_START:
                yield ['game', 'start']
            elif event.key == self.KEY_RESTART:
                yield ['game', 'restart']
            elif event.key == self.playerController_1.LEFT:
                yield ['player', 1, 'move', 'left']
            elif event.key == self.playerController_2.LEFT:
                yield ['player', 2, 'move', 'left']
            elif event.key == self.playerController_1.RIGHT:
                yield ['player', 1, 'move', 'right']
            elif event.key == self.playerController_2.RIGHT:
                yield ['player', 2, 'move', 'right']
            elif event.key == self.playerController_1.ROTATE_LEFT:
                yield ['player', 1, 'rotate', 'left']
            elif event.key == self.playerController_2.ROTATE_LEFT:
                yield ['player', 2, 'rotate', 'left']
            elif event.key == self.playerController_1.ROTATE_RIGHT:
                yield ['player', 1, 'rotate', 'right']
            elif event.key == self.playerController_2.ROTATE_RIGHT:
                yield ['player', 2, 'rotate', 'right']
            elif event.key == self.playerController_1.SPEED:
                yield ['player', 1, 'speed', 'down']
            elif event.key == self.playerController_2.SPEED:
                yield ['player', 2, 'speed', 'down']
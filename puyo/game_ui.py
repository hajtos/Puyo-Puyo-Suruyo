"""
author: Pawel Chachaj
version: 0.2



"""
#from .Graphics import *
from .graphics.colors import COLORS as Colors
from .graphics.text_frame import TextFrame
import pygame, sys
import pygame.locals as gamelocals
from .system.game_map import GameMap


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

    def __init__(self, title, sizes, fps, bg_color):
        '''initialize all variables'''
        self.params = {"fps": fps, "bg_color": bg_color, \
            "win_height": sizes[0][0], "win_width": sizes[0][1], \
            "game_size": sizes[1]}
        self.memory = {"clock": pygame.time.Clock(), "exit": False, \
            "pause": False, "stopper": True}
        self.display_surf = \
            pygame.display.set_mode((self.params["win_width"], \
            self.params["win_height"]))
        pygame.display.set_caption(title)
        self.player_controllers = (None, None)
        self.boards = (None, None)
        self.scoreboards = (None, None)
        self.game_maps = (None, None)
        #----main loop

    def set_players(self, player_1, player_2):
        '''set player controllers'''
        self.player_controllers = (player_1, player_2)

    def set_game_boards(self, board_1, board_2):
        '''set game boards for players'''
        self.boards = (board_1.set_size(self.params["game_size"]), \
            board_2.set_size(self.params["game_size"]))

    def set_scoreboards(self, scoreboard_1, scoreboard_2):
        self.scoreboards = (scoreboard_1, scoreboard_2)

    def set_game_maps(self, game_map1, game_map2):
        """
        set gameMap objects for handling board system
        """
        self.game_maps = (game_map1, game_map2)

    def start(self):
        '''start game, handle logic and graphic'''
        # pylint: disable=R0912
        self.draw_new_game()
        while True:
            #----main event handler
            events = self.event_handler()
            #----logic
            for event in events:
                print event
                if event[0] == 'game':
                    if event[1] == 'quit':
                        self.terminate()
                        break
                    elif event[1] == 'pause':
                        self.memory["pause"] = not self.memory["pause"]
                        self.draw_new_game()
                        break
                    elif event[1] == 'start':
                        self.memory["pause"] = False
                        self.memory["stopper"] = False
                        self.draw_new_game()
                        break
                    elif event[1] == 'restart':
                        self.restart_game()
                        break
                elif not self.memory["pause"] and event[0] == 'player':
                    the_map = None
                    if event[1] == 1:
                        the_map = self.game_maps[0]
                    elif event[1] == 2:
                        the_map = self.game_maps[1]
                    if event[2] == 'move':
                        if event[3] == 'left':
                            the_map.key_move(-1)
                        elif event[3] == 'right':
                            the_map.key_move(1)
                    elif event[2] == 'rotate':
                        the_map.rotate()
                    elif event[2] == 'speed':
                        if event[3] == 'up':
                            the_map.start_speed()
                        elif event[3] == 'down':
                            the_map.stop_speed()
            if self.memory["exit"]: #exit game if terimnated
                break
            if self.memory["stopper"]: #wait for key input to start the game
                self.draw_stopper('START', Colors.WHITE, Colors.LIGHTGREEN)
                continue
            if self.memory["pause"]: #do nothing if game paused
                self.draw_stopper('PAUSE', Colors.WHITE, Colors.GREY)
                continue
            #test
            self.game_maps[0].tick()
            self.game_maps[1].tick()
            #----display
            #background
            self.draw_game()
            self.memory["clock"].tick(self.params["fps"])
        # pylint: enable=R0912

    def get_score(self, game_map, combo, cell_count):
        print 'score: ', combo, cell_count
        score = combo*cell_count
        if game_map == self.game_maps[0]:
            self.scoreboards[0].add_score(score)
            self.game_maps[1].add_colorless(float(score)/5)
        elif game_map == self.game_maps[1]:
            self.scoreboards[1].add_score(score)
            self.game_maps[0].add_colorless(float(score)/5)
        self.scoreboards[0].draw()
        self.scoreboards[1].draw()
        pygame.display.update()

    def draw_new_game(self):
        self.display_surf.fill(self.params["bg_color"])
        self.draw_tips()
        self.boards[0].draw_map(self.game_maps[0].get_map())
        self.boards[1].draw_map(self.game_maps[1].get_map())
        self.scoreboards[0].draw()
        self.scoreboards[1].draw()
        pygame.display.update()

    def draw_game(self):
        self.boards[0].draw_map(self.game_maps[0].get_map())
        self.boards[1].draw_map(self.game_maps[1].get_map())
        pygame.display.update()

    def draw_tips(self):
        self.draw_text(self.KEYS_TIP, 15, (Colors.BLACK, \
            Colors.WHITE), (0, self.params["win_height"]-20))

    def draw_stopper(self, text, txt_color, bg_color):
        self.draw_text('   '+text+'   ', 40, (txt_color, bg_color), \
            (self.params["win_width"]/2-100, self.params["win_height"]/2-35))

    def draw_text(self, text, size, colors, start_pos):
        text_font = TextFrame(size)
        surf, rect = text_font.make_text(text, colors[0], \
            colors[1], start_pos)
        self.display_surf.blit(surf, rect)
        pygame.display.update()

    def terminate(self):
        '''exit game & windown'''
        self.memory["exit"] = True
        # pylint: disable=E1103
        # pylint: disable=W0104
        pygame.quit()
        sys.exit
        # pylint: enable=W0104
        # pylint: enable=E1103

    def restart_game(self):
        self.memory["stopper"] = True
        self.scoreboards[0].set_score(0)
        self.scoreboards[1].set_score(0)
        self.game_maps = (GameMap(self).copy_args(self.game_maps[0]), \
            GameMap(self).copy_args(self.game_maps[1]))

    def event_handler(self):
        '''handle quit and key events'''
        # pylint: disable=E1103
        # pylint: disable=R0912
        # get all the QUIT events
        for event in pygame.event.get(gamelocals.QUIT):
            yield ['game', 'quit']
        # get all the KEYDOWN events
        for event in pygame.event.get(gamelocals.KEYDOWN):
            if self.player_controllers[0].get_by_key_down(event.key, 1) \
                    is not None:
                yield self.player_controllers[0].get_by_key_down(event.key, 1)
            elif self.player_controllers[1].get_by_key_down(event.key, 2) \
                    is not None:
                yield self.player_controllers[1].get_by_key_down(event.key, 2)
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
            elif self.player_controllers[0].get_by_key_up(event.key, 1) is not None:
                yield self.player_controllers[0].get_by_key_up(event.key, 1)
            elif self.player_controllers[1].get_by_key_up(event.key, 2) is not None:
                yield self.player_controllers[1].get_by_key_up(event.key, 2)
        # pylint: enable=R0912
        # pylint: enable=E1103

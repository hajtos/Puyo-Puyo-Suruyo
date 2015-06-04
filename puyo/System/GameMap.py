"""
author: Krzysztof Hajto
version: 0.2

This file contains the class GameMap, responsible for
controlling the system of a player's board

"""
from .MapCell import MapCell
from .Group import Group
import random

import itertools
def tupleSum(tuple1, tuple2):
    """
    A utility function, adds 2 tuples element-wise
    """
    return [sum(pair) for pair in zip(tuple1, tuple2)]

def tupleDiff(tuple1, tuple2):
    """
    A utility function, subtracts 2 tuples element-wise
    """
    return [t1-t2 for t1, t2 in zip(tuple1, tuple2)]

class GameMap(object):
    """
    The main operating class of the board
    The attributes are:

    size - a tuple with the number of rows and columns of the board
    cells - a 2D array(as list of lists) of MapCell objects, the map
        of the board
    to_delete - a list of group that are scheduled to be deleted
    moving - a list of group that are not anchored to a cell yet
    limit - the number of elements in a group before it needs to be deleted
    game - the reference to the mother object(the GameUI)
    halted - False when the player can control a block, True when his control
        is witheld(for example, during a fall animation)
    sped_up - if the block falling is sped up(usually due to a player holding
        the down key)
    player_timer_ticks - how many ticks does it take for a block to fall down
        1 space when the player is in control and the sped_up is False
    player_tick - the counter for the above number of ticks
    combo - the number of groups that were deleted so far before
        the last score counting
    combo_cells - the summed number of elements that were deleted so far
        before the last score counting
    rows_to_add - the number of rows to be added the next time
        a block is to be generated
    color_count - the number of possible colors on
        the board(not counting colorless)
    """
    def __init__(self, game, size=(12, 6), limit=3, \
            colors=4, player_ticks=10):
        """
        the main constructor

        game - the reference to the mother object
        size - the size of the board
        limit - the number of elements in a group that
            would mark it for deletion
        colors - the number of colors for the board(not counting colorless)
        player_ticks - the number of ticks before a block is
            lowered when the player is in control
        """
        self.size = size
        self.cells = [[MapCell((i, j), self, None) for j in range(size[1])]\
            for i in range(size[0])]
        self.to_delete = []
        self.moving = []
        self.limit = limit
        self.game = game
        self.halted = False
        self.player_timer_ticks = player_ticks
        self.player_tick = 0
        self.combo = 0
        self.combo_cells = 0
        self.rows_to_add = 0.0
        self.color_count = colors
        self.sped_up = False

    def copyArgs(self, copy):
        """
        Copies the game parameters between instances
        """
        self.size = copy.size
        self.cells = [[MapCell((i, j), self, None) for j in \
            range(self.size[1])] for i in range(self.size[0])]
        self.limit = copy.limit
        self.player_timer_ticks = copy.player_timer_ticks
        self.color_count = copy.color_count
        return self

    def startSpeed(self):
        """
        starts speeding up, called externally
        """
        self.sped_up = True

    def stopSpeed(self):
        """
        stops speeding up, called externally
        """
        self.sped_up = False

    def addColorless(self, count):
        """
        adds a number of colorless elements to generate, called externally
        """
        self.rows_to_add += float(count)/self.size[1]

    def placeAt(self, color, pos):
        """
        anchores an element in a cell

        color - the color of the element
        pos - the position to be placed at
        """
        if color == 0:
            cell = self.cells[pos[0]][pos[1]]
            cell.setGroup(Group(0, pos, [], self))
            for neigh in cell.neighbours():
                neigh.getGroup().addColorless([pos])
            return
        cell = self.cells[pos[0]][pos[1]]
        added = set([matching.getGroup() for matching in \
            cell.neighbours() if matching.getGroup().color == color\
            and matching.getGroup() not in self.moving])
        self.to_delete = [group for group in self.to_delete \
            if group not in added]
        new_group = Group(color, pos, added, self)
        for item in new_group.cells():
            self.cells[item[0]][item[1]].setGroup(new_group)
        new_group.addColorless([matching.pos for matching in \
            cell.neighbours() if matching.getGroup().color == 0])
        if new_group.size() > self.limit:
            self.to_delete.append(new_group)
        self.halted = True

    def getMap(self):
        """
        returns the current state of the board as a list of lists of
            colors, with None meaning no element at that position
        """
        return [[None if cell.getGroup() is None else cell.getGroup().color \
            for cell in row] for row in self.cells]

    def keyMove(self, direction):
        """
        moves the block horizontally
        will do nothing if the player is halted or the move is invalid

        direction - 1 when moving right, -1 when moving left
        """
        if self.halted:
            return
        for group in self.moving:
            next_pos = group.cells()[0][1]+direction
            if next_pos < 0 or next_pos >= self.size[1]:
                return
            collision = self.cells[group.cells()[0][0]][next_pos].getGroup()
            if collision is not None and collision not in self.moving:
                return
        for group in self.moving:
            pos = group.cells()[0]
            group.cells()[0] = tupleSum(pos, (0, direction))
            self.cells[pos[0]][pos[1]].setGroup(None)
        for group in self.moving:
            group.updateMap()

    def rotate(self):
        """
        rotates the block clockwise
        will do nothing if the player is halted or the move is invalid
        """
        if self.halted:
            return
        pos1 = self.moving[0].cells()[0]
        pos2 = self.moving[1].cells()[0]
        self.cells[pos1[0]][pos1[1]].setGroup(None)
        self.cells[pos2[0]][pos2[1]].setGroup(None)
        diff = tupleDiff(pos1, pos2)
        self.moving[1].cells()[0] = tupleSum(pos2, diff)
        diff = (diff[1], -diff[0])
        self.moving[0].cells()[0] = tupleSum(pos1, diff)
        new_pos1 = self.moving[0].cells()[0]
        new_pos2 = self.moving[1].cells()[0]
        if new_pos1[1] < 0 or new_pos2[1] < 0\
                or new_pos1[1] >= self.size[1] or new_pos2[1] >= self.size[1]\
                or new_pos1[0] >= self.size[0] or new_pos2[0] >= self.size[0]\
                or self.cells[new_pos1[0]][new_pos1[1]].getGroup() is not None\
                or self.cells[new_pos2[0]][new_pos2[1]].getGroup() is not None:
            self.moving[0].cells()[0] = pos1
            self.moving[1].cells()[0] = pos2
        self.moving[0].updateMap()
        self.moving[1].updateMap()

    def deleteStored(self):
        """
        deletes the groups marked for deletion
        """
        for group in self.to_delete:
            self.deleteGroup(group)
        self.to_delete = []

    def makeMoving(self, color, pos):
        """
        create a new moving element as a new group

        color - the color of the element
        pos - the position for the element
        """
        new_group = Group(color, pos, [], self)
        self.cells[pos[0]][pos[1]].setGroup(new_group)
        self.moving.append(new_group)

    def makeBlock(self):
        """
        generates a new moving block for the player
        if there are enough colorless elements to add for a complete row
        generates as many colorless elements as possible instead

        if there is no space for the new block/colorless elements the
        game is considered over and a feedback to the mother object is sent
        """
        if int(self.rows_to_add) > 0:
            rows = int(self.rows_to_add)
            game_over = False
            for i in range(rows):
                for j in range(self.size[1]):
                    if self.cells[i][j].getGroup() is not None:
                        game_over = True
                    else:
                        self.makeMoving(0, (i, j))
            if game_over:
                self.game.restartGame()
            self.halted = True
            self.rows_to_add -= rows
            return
        random.seed()
        if self.cells[0][self.size[1]/2].getGroup() is not None or \
                self.cells[0][self.size[1]/2-1].getGroup() is not None:
            self.game.restartGame()
        self.makeMoving(random.randint(1, self.color_count), \
            (0, self.size[1]/2))
        self.makeMoving(random.randint(1, self.color_count), \
            (0, self.size[1]/2-1))
        self.halted = False

    def draw(self):
        """
        prints the current state of the board to console
        used for debugging and testing purpouses
        """
        for row in self.cells:
            print " ".join(['.' if cell.getGroup() is None \
                else str(cell.getGroup().color) for cell in row])

    def move(self):
        """
        moves the moving elements and anchores those that cannot move further
        """
        finished = []
        for group in sorted(self.moving, key=lambda gr: -gr.cells()[0][0]):
            pos = group.cells()[0]
            self.cells[pos[0]][pos[1]].setGroup(None)
            if pos[0] == self.size[0] -1 or \
                    (self.cells[pos[0]+1][pos[1]].getGroup() is not None and \
                    self.cells[pos[0]+1][pos[1]].getGroup() not in self.moving):
                self.placeAt(group.color, (pos[0], pos[1]))
                finished.append(group)
            else:
                group.cells()[0] = (pos[0]+1, pos[1])
        self.moving = [group for group in self.moving if group not in finished]
        for group in self.moving:
            group.updateMap()

    def tick(self):
        """
        passes a single tick of time in the game
        """
        if self.halted:
            self.move()
            if not self.moving:
                if self.to_delete:
                    self.deleteStored()
                else:
                    self.halted = False
                    if self.combo > 0:
                        self.game.get_score(self, self.combo, self.combo_cells)
                        self.combo = 0
                        self.combo_cells = 0
                    self.makeBlock()
        else:
            self.player_tick -= 1
            if self.player_tick <= 0 or self.sped_up:
                self.move()
                if not self.moving and self.to_delete:
                    self.deleteStored()
                self.player_tick = self.player_timer_ticks
                if not self.moving:
                    self.halted = True

    def deleteGroup(self, group):
        """
        deletes the selected group and handles its neighbours

        group - the group to delete
        """
        self.combo_cells += group.size()
        self.combo += 1
        deleted = sorted(group.cells()+group.colorless, key=lambda x: x[1])
        lowers = [(key, max([c[0] for c in column])) \
            for key, column in itertools.groupby(deleted, key=lambda x: x[1])]
        for xpos, low in lowers:
            low -= 1
            while low > 0:
                cell = self.cells[low][xpos]
                if cell.pos in deleted:
                    low -= 1
                    continue
                if cell.getGroup() is not None and cell.getGroup() != group \
                        and cell.getGroup() not in self.to_delete:
                    cell.getGroup().remove(cell.pos)
                    self.makeMoving(cell.getGroup().color, cell.pos)
                low -= 1
        for pos in deleted:
            self.cells[pos[0]][pos[1]].setGroup(None)


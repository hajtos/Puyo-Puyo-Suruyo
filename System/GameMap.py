from MapCell import MapCell
from Group import Group
import random

import itertools

def tupleSum(tuple1, tuple2):
    return [sum(pair) for pair in zip(tuple1, tuple2)]

def tupleDiff(tuple1, tuple2):
    return [t1-t2 for t1, t2 in zip(tuple1, tuple2)]

class GameMap(object):
    def __init__(self, game, size = (12, 6), limit = 3, \
            colors = 5, player_ticks = 10):
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
        self.colorCount = colors
        self.sped_up = False

    def startSpeed(self):
        self.sped_up = True
        
    def stopSpeed(self):
        self.sped_up = False
        
    def addColorless(self, count):
        self.rows_to_add += float(count)/self.size[1]

    def placeAt(self, color, pos):
        if color == 0:
            cell = self.cells[pos[0]][pos[1]]
            cell.group = Group(0, pos, [], self)
            for neigh in cell.neighbours():
                neigh.group.addColorless([pos])
            return
        cell = self.cells[pos[0]][pos[1]]
        added = set([matching.group for matching in \
            cell.neighbours() if matching.group.color == color\
            and matching.group not in self.moving])
        self.to_delete = [group for group in self.to_delete \
            if group not in added]
        newGroup = Group(color, pos, added, self)
        for item in newGroup.cells():
            self.cells[item[0]][item[1]].group = newGroup
        newGroup.addColorless([matching.pos for matching in \
            cell.neighbours() if matching.group.color == 0])
        if newGroup.size() > self.limit:
            self.to_delete.append(newGroup)
        self.halted = True

    def getMap(self):
        return [[None if cell.group is None else cell.group.color \
            for cell in row] for row in self.cells]

    def keyMove(self, direction):
        if self.halted:
            return
        for group in self.moving:
            nextPos = group.cells()[0][1]+direction
            if nextPos < 0 or nextPos >= self.size[1]:
                return
            collision = self.cells[group.cells()[0][0]][nextPos].group
            if collision is not None and collision not in self.moving:
                return
        for group in self.moving:
            pos = group.cells()[0]
            group.cells()[0] = tupleSum(pos, (0, direction))
            self.cells[pos[0]][pos[1]].group = None
        for group in self.moving:
            group.updateMap()

    def rotate(self):
        if self.halted:
            return
        pos1 = self.moving[0].cells()[0]
        pos2 = self.moving[1].cells()[0]
        self.cells[pos1[0]][pos1[1]].group = None
        self.cells[pos2[0]][pos2[1]].group = None
        diff = tupleDiff(pos1, pos2)
        self.moving[1].cells()[0] = tupleSum(pos2, diff)
        diff = (diff[1], -diff[0])
        self.moving[0].cells()[0] = tupleSum(pos1, diff)
        newPos1 = self.moving[0].cells()[0]
        newPos2 = self.moving[1].cells()[0]
        if newPos1[1] < 0 or newPos2[1] < 0\
                or newPos1[1] >= self.size[1] or newPos2[1] >= self.size[1]\
                or newPos1[0] >= self.size[0] or newPos2[0] >= self.size[0]\
                or self.cells[newPos1[0]][newPos1[1]].group is not None\
                or self.cells[newPos2[0]][newPos2[1]].group is not None:
            self.moving[0].cells()[0] = pos1
            self.moving[1].cells()[0] = pos2
        self.moving[0].updateMap()
        self.moving[1].updateMap()

    def deleteStored(self):
        for group in self.to_delete:
            self.deleteGroup(group)
        self.to_delete = []

    def makeMoving(self, color, pos):
        newGroup = Group(color, pos, [], self)
        self.cells[pos[0]][pos[1]].group = newGroup
        self.moving.append(newGroup)

    def makeBlock(self):
        if int(self.rows_to_add) > 0:
            rows = int(self.rows_to_add)
            game_over = False
            for i in range(rows):
                for j in range(self.size[1]):
                    if self.cells[i][j].group is not None:
                        game_over = True
                    else:
                        self.makeMoving(0, (i, j))
            if game_over:
                game.restartGame()
            self.halted = True
            self.rows_to_add -= rows
            return
        random.seed()
        if self.cells[0][self.size[1]/2].group is not None or \
                self.cells[0][self.size[1]/2-1].group is not None:
            self.game.restartGame()
        self.makeMoving(random.randint(1, self.colorCount), (0, self.size[1]/2))
        self.makeMoving(random.randint(1, self.colorCount), (0, self.size[1]/2-1))
        self.halted = False

    def draw(self):
        for row in self.cells:
            print " ".join(['.' if cell.group is None \
                else str(cell.group.color) for cell in row])

    def move(self):
        finished = []
        for group in sorted(self.moving, key=lambda gr: -gr.cells()[0][0]):
            pos = group.cells()[0]
            self.cells[pos[0]][pos[1]].group = None
            if pos[0] == self.size[0] -1 or \
                    (self.cells[pos[0]+1][pos[1]].group is not None and \
                    self.cells[pos[0]+1][pos[1]].group not in self.moving):
                self.placeAt(group.color, (pos[0], pos[1]))
                finished.append(group)
            else:
                group.cells()[0] = (pos[0]+1, pos[1])
        self.moving = [group for group in self.moving if group not in finished]
        for group in self.moving:
            group.updateMap()

    def tick(self):
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
        print group.size()
        self.combo_cells += group.size()
        self.combo += 1
        deleted = sorted(group.cells()+group.colorless, key=lambda x:x[1])
        lowers = [(key, max([c[0] for c in column])) \
            for key, column in itertools.groupby(deleted, key=lambda x:x[1])]
        for xpos, low in lowers:
            low -= 1
            while low > 0:
                cell = self.cells[low][xpos]
                if cell.pos in deleted:
                    low -= 1
                    continue
                if cell.group is not None and cell.group != group \
                        and cell.group not in self.to_delete:
                    cell.group.remove(cell.pos)
                    self.makeMoving(cell.group.color, cell.pos)
                low -= 1
        for pos in deleted:
            self.cells[pos[0]][pos[1]].group = None
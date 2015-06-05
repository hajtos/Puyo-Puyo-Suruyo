"""
author: Krzysztof Hajto
version: 0.2

This file contains the class GameMap, responsible for
controlling the system of a player's board

"""
from .map_cell import MapCell
from .group import Group
import random

import itertools
def tuple_sum(tuple1, tuple2):
    """
    A utility function, adds 2 tuples element-wise
    """
    return [sum(pair) for pair in zip(tuple1, tuple2)]

def tuple_diff(tuple1, tuple2):
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
    memory - a dictionary that holds multiple variables. The only reason many
        variables are stuck in one is pylint. The values of the dictionary are:
        to_delete - a list of group that are scheduled to be deleted
        moving - a list of group that are not anchored to a cell yet
        halted - False when the player can control a block, True when his control
            is witheld(for example, during a fall animation)
        speed - if the block falling is sped up(usually due to a player holding
            the down key)
        player_tick - the counter for the above number of ticks
        combo - a tuple of the number of groups and the summed number of
            elements that were deleted so far before the last score counting
        rows - the number of rows to be added the next time
            a block is to be generated
    limit - the number of elements in a group before it needs to be deleted
    game - the reference to the mother object(the GameUI)
    player_timer_ticks - how many ticks does it take for a block to fall down
        1 space when the player is in control and the sped_up is False
    color_count - the number of possible colors on
        the board(not counting colorless)
    """
    def __init__(self, game, size=(12, 6), params=(3, 4, 10)):
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
        self.memory = {"moving": [], "halted": False, "combo": [0, 0], \
            "rows": 0.0, "to_delete": [], "speed": False, "player_tick": 0}
        self.limit = params[0]
        self.game = game
        self.player_timer_ticks = params[2]
        self.color_count = params[1]

    def copy_args(self, copy):
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

    def start_speed(self):
        """
        starts speeding up, called externally
        """
        self.memory["speed"] = True

    def stop_speed(self):
        """
        stops speeding up, called externally
        """
        self.memory["speed"] = False

    def add_colorless(self, count):
        """
        adds a number of colorless elements to generate, called externally
        """
        self.memory["rows"] += float(count)/self.size[1]

    def place_at(self, color, pos):
        """
        anchores an element in a cell

        color - the color of the element
        pos - the position to be placed at
        """
        if color == 0:
            cell = self.cells[pos[0]][pos[1]]
            cell.set_group(Group(0, pos, [], self))
            for neigh in cell.neighbours():
                neigh.get_group().add_colorless([pos])
            return
        cell = self.cells[pos[0]][pos[1]]
        added = set([matching.get_group() for matching in \
            cell.neighbours() if matching.get_group().color == color\
            and matching.get_group() not in self.memory["moving"]])
        self.memory["to_delete"] = [group for group in self.memory["to_delete"] \
            if group not in added]
        new_group = Group(color, pos, added, self)
        for item in new_group.cells():
            self.cells[item[0]][item[1]].set_group(new_group)
        new_group.add_colorless([matching.pos for matching in \
            cell.neighbours() if matching.get_group().color == 0])
        if new_group.size() > self.limit:
            self.memory["to_delete"].append(new_group)
        self.memory["halted"] = True

    def get_map(self):
        """
        returns the current state of the board as a list of lists of
            colors, with None meaning no element at that position
        """
        return [[None if cell.get_group() is None else cell.get_group().color \
            for cell in row] for row in self.cells]

    def key_move(self, direction):
        """
        moves the block horizontally
        will do nothing if the player is halted or the move is invalid

        direction - 1 when moving right, -1 when moving left
        """
        if self.memory["halted"]:
            return
        for group in self.memory["moving"]:
            next_pos = group.cells()[0][1]+direction
            if next_pos < 0 or next_pos >= self.size[1]:
                return
            collision = self.cells[group.cells()[0][0]][next_pos].get_group()
            if collision is not None and collision not in self.memory["moving"]:
                return
        for group in self.memory["moving"]:
            pos = group.cells()[0]
            group.cells()[0] = tuple_sum(pos, (0, direction))
            self.cells[pos[0]][pos[1]].set_group(None)
        for group in self.memory["moving"]:
            group.update_map()

    def rotate(self):
        """
        rotates the block clockwise
        will do nothing if the player is halted or the move is invalid
        """
        if self.memory["halted"]:
            return
        pos1 = self.memory["moving"][0].cells()[0]
        pos2 = self.memory["moving"][1].cells()[0]
        self.cells[pos1[0]][pos1[1]].set_group(None)
        self.cells[pos2[0]][pos2[1]].set_group(None)
        diff = tuple_diff(pos1, pos2)
        self.memory["moving"][1].cells()[0] = tuple_sum(pos2, diff)
        diff = (diff[1], -diff[0])
        self.memory["moving"][0].cells()[0] = tuple_sum(pos1, diff)
        new_pos1 = self.memory["moving"][0].cells()[0]
        new_pos2 = self.memory["moving"][1].cells()[0]
        if new_pos1[1] < 0 or new_pos2[1] < 0\
                or new_pos1[1] >= self.size[1] or new_pos2[1] >= self.size[1]\
                or new_pos1[0] >= self.size[0] or new_pos2[0] >= self.size[0]\
                or self.cells[new_pos1[0]][new_pos1[1]].get_group() is not None\
                or self.cells[new_pos2[0]][new_pos2[1]].get_group() is not None:
            self.memory["moving"][0].cells()[0] = pos1
            self.memory["moving"][1].cells()[0] = pos2
        self.memory["moving"][0].update_map()
        self.memory["moving"][1].update_map()

    def delete_stored(self):
        """
        deletes the groups marked for deletion
        """
        for group in self.memory["to_delete"]:
            self.delete_group(group)
        self.memory["to_delete"] = []

    def make_moving(self, color, pos):
        """
        create a new moving element as a new group

        color - the color of the element
        pos - the position for the element
        """
        new_group = Group(color, pos, [], self)
        self.cells[pos[0]][pos[1]].set_group(new_group)
        self.memory["moving"].append(new_group)

    def make_block(self):
        """
        generates a new moving block for the player
        if there are enough colorless elements to add for a complete row
        generates as many colorless elements as possible instead

        if there is no space for the new block/colorless elements the
        game is considered over and a feedback to the mother object is sent
        """
        if int(self.memory["rows"]) > 0:
            rows = int(self.memory["rows"])
            game_over = False
            for i in range(rows):
                for j in range(self.size[1]):
                    if self.cells[i][j].get_group() is not None:
                        game_over = True
                    else:
                        self.make_moving(0, (i, j))
            if game_over:
                self.game.restart_game()
            self.memory["halted"] = True
            self.memory["rows"] -= rows
            return
        random.seed()
        if self.cells[0][self.size[1]/2].get_group() is not None or \
                self.cells[0][self.size[1]/2-1].get_group() is not None:
            self.game.restart_game()
        self.make_moving(random.randint(1, self.color_count), \
            (0, self.size[1]/2))
        self.make_moving(random.randint(1, self.color_count), \
            (0, self.size[1]/2-1))
        self.memory["halted"] = False

    def draw(self):
        """
        prints the current state of the board to console
        used for debugging and testing purpouses
        """
        for row in self.cells:
            print " ".join(['.' if cell.get_group() is None \
                else str(cell.get_group().color) for cell in row])

    def move(self):
        """
        moves the moving elements and anchores those that cannot move further
        """
        finished = []
        for group in sorted(self.memory["moving"], key=lambda gr: -gr.cells()[0][0]):
            pos = group.cells()[0]
            self.cells[pos[0]][pos[1]].set_group(None)
            if pos[0] == self.size[0] -1 or \
                    (self.cells[pos[0]+1][pos[1]].get_group() is not None and \
                    self.cells[pos[0]+1][pos[1]].get_group() not in self.memory["moving"]):
                self.place_at(group.color, (pos[0], pos[1]))
                finished.append(group)
            else:
                group.cells()[0] = (pos[0]+1, pos[1])
        self.memory["moving"] = [group for group in self.memory["moving"] if group not in finished]
        for group in self.memory["moving"]:
            group.update_map()

    def tick(self):
        """
        passes a single tick of time in the game
        """
        if self.memory["halted"]:
            self.move()
            if not self.memory["moving"]:
                if self.memory["to_delete"]:
                    self.delete_stored()
                else:
                    self.memory["halted"] = False
                    if self.memory["combo"][0] > 0:
                        self.game.get_score(self, self.memory["combo"][0], self.memory["combo"][1])
                        self.memory["combo"][0] = 0
                        self.memory["combo"][1] = 0
                    self.make_block()
        else:
            self.memory["player_tick"] -= 1
            if self.memory["player_tick"] <= 0 or self.memory["speed"]:
                self.move()
                if not self.memory["moving"] and self.memory["to_delete"]:
                    self.delete_stored()
                self.memory["player_tick"] = self.player_timer_ticks
                if not self.memory["moving"]:
                    self.memory["halted"] = True

    def delete_group(self, group):
        """
        deletes the selected group and handles its neighbours

        group - the group to delete
        """
        self.memory["combo"][1] += group.size()
        self.memory["combo"][0] += 1
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
                if cell.get_group() is not None and cell.get_group() != group \
                        and cell.get_group() not in self.memory["to_delete"]:
                    cell.get_group().remove(cell.pos)
                    self.make_moving(cell.get_group().color, cell.pos)
                low -= 1
        for pos in deleted:
            self.cells[pos[0]][pos[1]].set_group(None)


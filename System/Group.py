
import GameMap

class Group(object):
    def __init__(self, color, pos, merging, game_map):
        self.color = color
        self.positions = [pos]
        self.colorless = []
        self.game_map = game_map
        for group in merging:
            self.positions += group.positions
            self.colorless += group.colorless

    def cells(self):
        return self.positions

    def size(self):
        return len(self.positions)
        
    def remove(self, removed):
        self.positions = [pos for pos in self.positions if pos != removed]

    def addColorless(self, positions):
        self.colorless += positions

    def updateMap(self):
        for pos in self.positions:
            self.game_map.cells[pos[0]][pos[1]].group = self
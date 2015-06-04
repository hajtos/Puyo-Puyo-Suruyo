"""
author: Krzysztof Hajto
version: 0.2

This file contains the class for a group of elements
"""

class Group(object):
    """
    This class holds information on a group of
    connected elements of the same color

    Its atributes are:
    color - the color of the elements in the group
    positions - the position tuples of the elements
    colorless - the position tuples of neighbouring colorless elements
    game_map - the reference to the mother GameMap object
    """
    def __init__(self, color, pos, merging, game_map):
        """
        The constructor

        color - the color for the group
        pos - the position of the binding element(the new element
            that spurred the creation of this group)
        merging - the list of groups that will be merged into this group
        game_map - the reference to the mother GameMap object
        """
        self.color = color
        self.positions = [pos]
        self.colorless = []
        self.game_map = game_map
        for group in merging:
            self.positions += group.positions
            self.colorless += group.colorless

    def cells(self):
        """
        returns a list of the elements' positions
        """
        return self.positions

    def size(self):
        """
        returns the number of elements in the group
        """
        return len(self.positions)

    def remove(self, removed):
        """
        removes an element from the group

        removed - the position of the element to be removed
        """
        self.positions = [pos for pos in self.positions if pos != removed]

    def addColorless(self, positions):
        """
        adds a list of colorless elements to the colorless neigbours

        positions - the positions of the colorless elements
        """
        self.colorless += positions

    def updateMap(self):
        """
        update the map of the GameMap object, setting itself as the group
        in positions of its elements
        """
        for pos in self.positions:
            self.game_map.cells[pos[0]][pos[1]].group = self

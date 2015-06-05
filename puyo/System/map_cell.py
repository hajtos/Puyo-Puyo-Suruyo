"""
author: Krzysztof Hajto
version: 0.2

This file contains the class representing a single cell in the board
"""

class MapCell(object):
    """
    Represents a single cell of the board
    Attributes:

    pos - the position in the board
    cell_map - the reference to the mother object
    group - the reference to the group placed at this cell
    """
    def __init__(self, pos, cell_map, group):
        """
        the constructor, arguments are self-explanatory
        """
        self.pos = pos
        self.cell_map = cell_map
        self.group = group

    def neighbours(self):
        """
        returns a list of non-empty(i.e. with group not None) neighbouring cells
        """
        candidates = [(self.pos[0], self.pos[1]+1), \
            (self.pos[0], self.pos[1]-1), \
            (self.pos[0]+1, self.pos[1]), \
            (self.pos[0]-1, self.pos[1])]
        #print candidates
        candidates = [self.cell_map.cells[neig[0]][neig[1]] \
            for neig in candidates if neig[0] >= 0 \
            and neig[1] >= 0 and neig[0] < self.cell_map.size[0] \
            and neig[1] < self.cell_map.size[1]]
        #print candidates
        return [cell for cell in candidates if cell.group is not None]

    def set_group(self, group):
        """
        a setter for the group attribute
        """
        self.group = group

    def get_group(self):
        """
        a getter for the group attribute
        """
        return self.group

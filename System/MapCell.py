

class MapCell(object):
    def __init__(self, pos, cell_map, group):
        self.pos = pos
        self.cell_map = cell_map
        self.group = group

    def neighbours(self):
        candidates = [(self.pos[0], self.pos[1]+1), 
            (self.pos[0], self.pos[1]-1), 
            (self.pos[0]+1, self.pos[1]), 
            (self.pos[0]-1, self.pos[1])]
        #print candidates
        candidates = [self.cell_map.cells[neig[0]][neig[1]] \
            for neig in candidates if neig[0] >= 0 \
            and neig[1] >= 0 and neig[0] < self.cell_map.size[0] \
            and neig[1] < self.cell_map.size[1]]
        #print candidates
        return [cell for cell in candidates if cell.group is not None]
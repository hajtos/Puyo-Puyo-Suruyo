
class PlayerController(object):
    '''holder of player key controlls'''
    def __init__(self, left, right, rotate_left, rotate_right, speed):
        self.left = left
        self.right = right
        self.rotate_left = rotate_left
        self.rotate_right = rotate_right
        self.speed = speed

    def getByKeyUp(self, key, player_number):
        if key == self.left:
            return ['player', player_number, 'move', 'left']
        elif key == self.right:
            return ['player', player_number, 'move', 'right']
        elif key == self.rotate_left:
            return ['player', player_number, 'rotate', 'left']
        elif key == self.rotate_right:
            return ['player', player_number, 'rotate', 'right']
        elif key == self.speed:
            return ['player', player_number, 'speed', 'down']
        else:
            return None

    def getByKeyDown(self, key, player_number):
        if key == self.speed:
            return ['player', player_number, 'speed', 'up']
        else:
            return None


class PlayerController(object):
    '''holder of player key controlls'''
    def __init__(self, keys):
        self.left = keys[0]
        self.right = keys[1]
        self.rotate_left = keys[2]
        self.rotate_right = keys[3]
        self.speed = keys[4]

    def get_by_key_up(self, key, player_number):
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

    def get_by_key_down(self, key, player_number):
        if key == self.speed:
            return ['player', player_number, 'speed', 'up']
        else:
            return None

"""
This is a module for testing the System module of the game

the tests are not exhaustive, since any situation to check
would probably require 10-15 minutes of coding while replicating
that situation in the game itself would take 15-20 seconds

nevertheless, these tests can be performed as a
sanity check on any changes in the code
"""


import unittest
from puyo.System import GameMap

class DummyGame(object):
    """
    A dummy class whose only purpouse is to mock the mother object GameUI
    """
    def __init__(self):
        """
        just a dummy
        """
        self.score = 0

    def restartGame(self):
        """
        just a dummy
        """
        pass

    def getScore(self, combo, cells):
        """
        just a dummy
        """
        pass

class GameSystemTester(unittest.TestCase):
    """
    The unittest TestCase class for sanity checks
    """
    def setUp(self):
        """
        creating the new GameMap object before each test
        small size is easier to check
        """
        self.game = GameMap.GameMap(DummyGame(), size=(3, 4))

    def test_stacking(self):
        """
        tests whether the group stack correctly
        """
        self.game.placeAt(1, (2, 1))
        self.game.placeAt(1, (2, 2))
        self.game.placeAt(1, (1, 1))
        self.game.placeAt(2, (2, 3))
        self.game.placeAt(2, (2, 0))
        self.game.placeAt(2, (1, 2))
        self.game.placeAt(0, (1, 0))
        self.assertEquals(self.game.getMap(), [[None, None, None, None], \
            [0, 1, 2, None], [2, 1, 1, 2]])
        self.assertEquals(self.game.cells[2][0].group.size(), 1)
        self.assertEquals(self.game.cells[2][1].group.size(), 3)
        self.assertEquals(self.game.cells[2][3].group.size(), 1)
        self.assertEquals(self.game.cells[1][2].group.size(), 1)

    def test_deleting(self):
        """
        checks if group deletion works as it should
        """
        self.game.placeAt(1, (2, 0))
        self.game.placeAt(1, (2, 1))
        self.game.placeAt(1, (2, 2))
        self.game.placeAt(1, (2, 3))
        self.game.placeAt(2, (1, 2))
        self.game.placeAt(1, (1, 3))
        self.assertEquals(self.game.getMap(), [\
            [None, None, None, None], \
            [None, None, 2, 1], \
            [1, 1, 1, 1]])
        self.assertEquals(len(self.game.to_delete), 1)
        self.assertEquals(self.game.to_delete[0].size(), 5)
        self.game.deleteStored()
        self.assertEquals(self.game.getMap(), [\
            [None, None, None, None], \
            [None, None, 2, None], \
            [None, None, None, None]])
        self.assertEquals(len(self.game.moving), 1)
        self.assertEquals(self.game.moving[0].cells(), [(1, 2)])
        self.assertTrue(self.game.halted)
        self.game.tick()
        self.assertEquals(self.game.getMap(), [\
            [None, None, None, None], \
            [None, None, None, None], \
            [None, None, 2, None]])

    def test_moving(self):
        """
        tests if the game properly reacts to player commands
        """
        self.game.tick()
        self.game.tick()
        self.assertEquals(len(self.game.moving), 2)
        colors = (self.game.cells[0][1].getGroup().color, \
            self.game.cells[0][2].getGroup().color)
        self.assertEquals(self.game.getMap(), [\
            [None, colors[0], colors[1], None], \
            [None, None, None, None], \
            [None, None, None, None]])
        self.game.keyMove(1)
        self.assertEquals(self.game.getMap(), [\
            [None, None, colors[0], colors[1]], \
            [None, None, None, None], \
            [None, None, None, None]])
        self.game.keyMove(1)
        self.assertEquals(self.game.getMap(), [\
            [None, None, colors[0], colors[1]], \
            [None, None, None, None], \
            [None, None, None, None]])
        self.game.keyMove(-1)
        self.game.keyMove(-1)
        self.assertEquals(self.game.getMap(), [\
            [colors[0], colors[1], None, None], \
            [None, None, None, None], \
            [None, None, None, None]])
        self.game.rotate()
        self.assertEquals(self.game.getMap(), [\
            [None, colors[0], None, None], \
            [None, colors[1], None, None], \
            [None, None, None, None]])
        self.game.keyMove(-1)
        self.game.rotate()
        self.assertEquals(self.game.getMap(), [\
            [colors[0], None, None, None], \
            [colors[1], None, None, None], \
            [None, None, None, None]])

def test():
    """
    performs the tests
    """
    suite = unittest.TestLoader().loadTestsFromTestCase(GameSystemTester)
    print unittest.TextTestRunner(verbosity=3).run(suite)

if __name__ == "__main__":
    test()

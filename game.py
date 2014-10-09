import core
import pyglet
from pyglet.window import key
from core import GameElement
import sys

#### DO NOT TOUCH ####
GAME_BOARD = None
DEBUG = False
######################

GAME_WIDTH = 10
GAME_HEIGHT = 10

class Rock(GameElement):
    IMAGE = 'Rock'
    SOLID = True

class Gem(GameElement):
    IMAGE = 'BlueGem'
    SOLID = False

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class Tree(GameElement):
    IMAGE = 'TallTree'
    SOLID = True

class Character(GameElement):
    IMAGE = 'Cat'

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []

    def next_pos(self, direction):
        if direction == "up":
            return (self.x, self.y-1)
        elif direction == "down":
            return (self.x, self.y+1)
        elif direction == "left":
            return (self.x-1, self.y)
        elif direction == "right":
            return (self.x+1, self.y)
        return None


    def keyboard_handler(self, symbol, modifier):

        direction = None
        if symbol == key.UP:
            direction = "up"
        elif symbol == key.DOWN:
            direction = "down"
        elif symbol == key.LEFT:
            direction = "left"
        elif symbol == key.RIGHT:
            direction = "right"

        self.board.draw_msg('[%s] moves %s' % (self.IMAGE, direction))

        if direction:
            next_location = self.next_pos(direction)

            if next_location:
                next_x = next_location[0]
                next_y = next_location[1]

                if next_x > (GAME_WIDTH-1) or next_x < 0 or next_y > (GAME_HEIGHT -1) or next_y < 0:
                    self.board.draw_msg("You can't go there!")
                    self.board.del_el(self.x, self.y)
                    self.board.set_el(self.x, self.y, self)

                else:

                    existing_el = self.board.get_el(next_x, next_y)

                    if existing_el:
                        existing_el.interact(self)

                    if existing_el and existing_el.SOLID:
                        self.board.draw_msg("There's something in my way!")
                    elif existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        self.board.set_el(next_x, next_y, self)

def initialize():
    """Put game initialization code here"""
    rock_positions = [(2,1), (1,2), (3,2), (2,3)]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)
    rocks[-1].SOLID = False

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(2,2, player)

    GAME_BOARD.draw_msg('This game is wicked awesome.')

    gem = Gem()
    GAME_BOARD.register(gem)
    GAME_BOARD.set_el(3, 1, gem)

    tree = Tree()
    GAME_BOARD.register(tree)
    GAME_BOARD.set_el(5, 5, tree)
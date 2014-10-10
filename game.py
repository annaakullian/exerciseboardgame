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

class Object(GameElement):
    SOLID = True 
    def __init__(self):
        GameElement.__init__(self)

    

class Rock(Object):
    IMAGE = 'Rock'

class Door(Object):
    door_position = "closed"
    IMAGE = "DoorClosed"

    # if door_position == 'open':
    def interact(self, player):
        if self.door_position == "closed":
            if (len(player.inventory)) >= 5:
                self.door_position = "open"
                del player.inventory[-5:]
                GAME_BOARD.draw_msg("Congratulations! You just opened the door. Now, you only have %d Gems!" % (len(player.inventory)))
                self.change_image("DoorOpen")
                self.SOLID = False

            else:
                GAME_BOARD.draw_msg("Sorry! You don't have enough gems to open the door. You need %d more Gems." % (5 - (len(player.inventory))))
        
        if not self.SOLID:
            player.hover = self

class MasterDoor(Door):

    end_of_game = False

    def interact(self, player):
        if self.door_position == "closed":
            if (len(player.inventory)) >= 10:
                self.door_position = "open"
                del player.inventory[-10:]
                player.change_image("Princess")
                self.SOLID = False
                player.saved_score = None
                if player.saved_score:
                    if player.saved_score > player.SCORE:
                        GAME_BOARD.draw_msg("Oh no! You didn't beat your high score of %d. Play again!" % player.saved_score)
                    elif player.saved_score <= player.SCORE:
                        GAME_BOARD.draw_msg("Congratulations! You got the high score of %d!" % player.SCORE)
                else:
                    GAME_BOARD.draw_msg("Congratulations! You won in %d moves." % player.SCORE)

                self.end_of_game = True
                player.saved_score = player.SCORE

            else:
                GAME_BOARD.draw_msg("Sorry! You don't have enough gems to open the door. You need %d more Gems." % (10 - (len(player.inventory))))
        
        if not self.SOLID:
            player.hover = self

    def keyboard_handler(self, symbol, modifier):
        super(MasterDoor, self).keyboard_handler(symbol, modifier)
        if self.end_of_game == True:
            GAME_BOARD.draw_msg("Would you like to play again? Y/N")

        if symbol == key.Y:
            reset()
            self.end_of_game = False


class Gem(Object):
    SOLID = False

    def __init__(self, IMAGE):
        self.IMAGE = IMAGE

    def interact(self, player):
        player.inventory.append(self)
        GAME_BOARD.draw_msg("You just acquired a gem! You have %d items!" % (len(player.inventory)))

class Tree(Object):
    IMAGE = 'TallTree'

class Character(GameElement):
    IMAGE = 'Cat'
    SCORE = 0

    def __init__(self):
        GameElement.__init__(self)
        self.inventory = []
        self.hover = None

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
        self.SCORE += 1

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
                    hover = self.hover

                    if existing_el:
                        existing_el.interact(self)

                    # if existing_el and existing_el.SOLID:
                    #     self.board.draw_msg("There's something in my way!")
                    if existing_el is None or not existing_el.SOLID:
                        self.board.del_el(self.x, self.y)
                        if hover:
                            self.board.set_el(self.x, self.y, hover)
                            self.hover = None
                        self.board.set_el(next_x, next_y, self)


def initialize():
    """Put game initialization code here"""

    player = Character()
    GAME_BOARD.register(player)
    GAME_BOARD.set_el(0,0, player)

    rock_positions = [(1,0), (1,3), (1,6), (1,7), (1,9), (2,2), (2,3), (2,6), (3,1), (3,6), (4,0), (4,3), (4,6), (5,1), (6,1), (6,2), (6,5), (6,6), (8,1), (8,2), (8,3), (8,6), (8,7), (8,9)]
    rocks = []

    for pos in rock_positions:
        rock = Rock()
        GAME_BOARD.register(rock)
        GAME_BOARD.set_el(pos[0], pos[1], rock)
        rocks.append(rock)

    GAME_BOARD.draw_msg('This game is wicked awesome.')
    greengem_positions = [(0,5), (0,7), (0,9), (2,0), (3,2), (3,7), (5,0), (5,3), (5,7), (7,2), (7,8), (9,0), (9,4)]
    bluegem_positions = [(0,3), (0,8), (2,1), (2,9), (3,0), (3,5), (5,2), (5,6), (7,0), (7,5), (9,2), (9,6)]
    
    gems = [] 
    for pos in greengem_positions:
        gem = Gem('GreenGem')
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        gems.append(gem)


    for pos in bluegem_positions:
        gem = Gem('BlueGem')
        GAME_BOARD.register(gem)
        GAME_BOARD.set_el(pos[0], pos[1], gem)
        gems.append(gem)

    tree_positions = [(1,2), (1,4), (1,8), (2,4), (3,4), (3,8), (4,1), (4,4), (4,8), (5,8), (6,8), (6,7), (6,3), (6,4), (8,4), (8,5), (8,8)]    
    trees = []
    for pos in tree_positions:
        tree = Tree()
        GAME_BOARD.register(tree)
        GAME_BOARD.set_el(pos[0], pos[1], tree)
        trees.append(tree) 

    door_positions = [(0,6), (1,1), (6,9)]    
    doors = []
    for pos in door_positions:
        door = Door()
        GAME_BOARD.register(door)
        GAME_BOARD.set_el(pos[0], pos[1], door)
        doors.append(door) 

    masterdoor = MasterDoor()
    GAME_BOARD.register(masterdoor)
    GAME_BOARD.set_el(9, 9, masterdoor)


def reset():
    GAME_BOARD.update_list = []
    initialize()
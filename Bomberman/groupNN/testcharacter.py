# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from sensed_world import SensedWorld
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    def do(self, wrld):
        # Your code here
        dx, dy = 0, 0
        bomb = False
        self.move(dx, dy)
        if bomb:
            self.place_bomb()
    #gets the Move by creating a sensed world and then copying all possible moves. Then it finds the max value of those using get value
    #and returns the move used to get that max value
    def getMove(self,wrld):
        NewWrld = SensedWorld.from_world(self)
        c = next(iter(NewWrld.characters().values()))
        
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (c.x+dx >=0) and (c.x+dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is moving
                    if (dx != 0) or (dy != 0):
                        # Avoid out-of-bound indexing
                        if (c.y+dy >=0) and (c.y+dy < wrld.height()):
                            # No need to check impossible moves
                            if not wrld.wall_at(c.x+dx, c.y+dy):
                                # Set move in wrld
                                c.move(dx, dy)
                                # Get new world
                                (newWrldTwo,events) = NewWrld.next()
                                # TODO: do something with newworld and events
        return 0
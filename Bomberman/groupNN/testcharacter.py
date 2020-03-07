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
    
    #heuristic determines the distance between the nodes 
    #x1 and y1 are the search node coords, x2 and y2 are the destination coords
    def h(start, end):
        return (start[0]-start[1])**2 + (end[0]-end[1])**2
    
    
    #returns a distance to the goal from a current node
    def getPath(self,wrld):
        NewWrld = SensedWorld.from_world(self)
        c = next(iter(NewWrld.characters().values()))
        
        #define the starting location
        start = [self.x,self.y]
        #define the exit node
        exitNode = []
        for x in range(0, wrld.width):
            for y in range(0, wrld.height):
                if(wrld.exit_at(x,y)):
                    exitNode = [x,y]
        #define the point where the node is checking.
        startNode = [self.x,self.y,0]
        startNode.append(h(searchNode, exitNode))
        #define a list of possible moves to the goal.
        moveList = []
        
        #define a list to store the next node to search.
        nodeOrder = [startNode]
        nodeClosed = []
        
        while(len(nodeOrder)):
#           take search node and find all possible moves from it
            searchNode = nodeOrder[0]
            currIndex = 0
            
            for index, move in enumerate(nodeOrder):
                if(move[2]+move[3] < searchNode[2]+searchNode[3]):
                    currIndex = index
                    searchNode = move
            
            nodeOrder.pop(currIndex)
            nodeClosed.append(searchNode)
            
            #set start distance to a higher number if the start is a wall
            #return length to goal 
            if(searchNode[0]==exit[0] and searchNode[1] == exit[1]):
                return searchNode[2]
            
            #generate Children
            for dx in [-1, 0, 1]:
                if (c.x+dx >=0) and (c.x+dx < wrld.width()):
                    for dy in [-1, 0, 1]:
                        if (dx != 0) or (dy != 0):
                            if (c.y+dy >=0) and (c.y+dy < wrld.height()):
                                if not wrld.wall_at(c.x+dx, c.y+dy):
                                    testNode = (searchNode[0]+dx, searchNode[1]+dy, searchNode[0]+1)
                                    testNode.append(self.h(testNode, exitNode))
                                    moveList.append(testNode)
                                else:
                                    testNode = (searchNode[0]+dx, searchNode[1]+dy, searchNode[0]+5)
                                    testNode.append(self.h(testNode, exitNode))
                                    moveList.append(testNode)
#           For each child
            for move in moveList:
                #child is on the closed list
                for closedNode in nodeClosed:
                    if move[0] == closedNode[0] and move[1] == closedNode[1]:
                        continue
                    
                
                
                #child is in the
                for openNode in nodeOrder:
                    if move[0] == openNode[0] and move[1] == openNode[1] and move[2] > openNode[2]:
                        continue
                    
                    
                nodeOrder.append(move)
                                                
                                                
                                                
                                                
                                                
            
                                                
                                    
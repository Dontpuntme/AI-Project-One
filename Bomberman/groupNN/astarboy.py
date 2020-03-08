# This is necessary to find the main code
import sys
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity


from colorama import Fore, Back

from node import Node

from sensed_world import SensedWorld
class AStarBoy(CharacterEntity):

    def do(self, wrld):
        # Your code here
        print(self.x)
        print(self.y)
        if (self.bombPlacement(wrld)==True):
            self.place_bomb()
            print("Place bomb")
        else:
            Move=self.getMove(wrld)
            self.move(Move[1], Move[2])
        
            
    #gets the Move by creating a sensed world and then copying all possible moves. Then it finds the max value of those using get value
    #and returns the move used to get that max value
    def getMove(self,wrld):
      #  newWrld = SensedWorld.from_world(wrld)
      #  print(newWrld.characters[0])
      #  c = CharacterEntity.from_character(newWrld.characters[0])
        BestMove = [-10000000000000000,0,0]
        for dx in [-1, 0, 1]:
            # Avoid out-of-bound indexing
            if (self.x+dx >=0) and (self.x+dx < wrld.width()):
                # Loop through delta y
                for dy in [-1, 0, 1]:
                    # Make sure the monster is movings
                        # Avoid out-of-bound indexing
                        if (self.y+dy >=0) and (self.y+dy < wrld.height()):
                            # No need to check impossible moves
                            if not wrld.wall_at(self.x+dx, self.y+dy):
                                # Set move in 
                                # c.move(dx, dy)
                                # Get new world
                                
                                # TODO: do something with newworld and events
                                characterX = (self.x+dx)
                                characterY = (self.y+dy)
                                Astar = 0
                                PathLength= self.getPath(characterX,characterY,wrld)
                                BombValue = self.inBombPath(characterX,characterY,wrld)
                                Astar = Astar - PathLength + BombValue
                            
                                if Astar>BestMove[0]:
                                    BestMove[0]=Astar
                                    BestMove[1]=dx;
                                    BestMove[2]=dy;
        return BestMove
                                    
        
    
    #heuristic determines the distance between the nodes 
    #x1 and y1 are the search node coords, x2 and y2 are the destination coords
    def h(start, end):
        return (start[0]-start[1])**2 + (end[0]-end[1])**2
    
    
    #returns a distance to the goal from a current node
    def getPath(self,thex,they,wrld): 
        end = []
        for x in range(0, wrld.width()):
           for y in range(0, wrld.height()):
                if(wrld.exit_at(x,y)):
                    end = (x,y)
                    print(x)
                    print(y)
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0
        Manhattan_Distance = ((end[0] - thex)) + ((end[1] - they))
        return abs(Manhattan_Distance)
    def inBombPath(self,thex,they,wrld):
        bombx=0
        bomby=0
        if(wrld.explosion_at(thex,they)):
            return -1000      
        for x in range(0, wrld.width()):
           for y in range(0, wrld.height()):
                if(wrld.bomb_at(x, y)):
                    bombx=x
                    bomby=y
        for dx in [-4,-3,-2,-1, 0, 1,2,3,4]:
            # Avoid out-of-bound indexing
            if (bombx+dx >=0) and (bombx+dx < wrld.width()):
                if (bomby >=0) and (bomby < wrld.height()):
                    if not wrld.wall_at(bombx+dx, bomby):
                        if(thex==(bombx+dx) and they==(bomby)):
                            return -1000
                            
        for dy in [-4,-3,-2,-1, 0, 1,2,3,4]:
            if (bombx >=0) and (bombx < wrld.width()):
                if (bomby+dy >=0) and (bomby+dy < wrld.height()):
                    if not wrld.wall_at(bombx, bomby+dy):
                        if(thex==(bombx) and they==(bomby+dy)):
                            return -1000
                                # TODO: do something with newworld and events
        return 0
    def isBomb(self,wrld):
        for x in range(0, wrld.width()):
           for y in range(0, wrld.height()):
                if(wrld.bomb_at(x, y)):
                    return True
        return False
    def bombPlacement(self,wrld):
        if (self.isBomb(wrld)!=True):
            if self.y == 0:
                return False
            print("No bomb on map")
            bombx = 0
            bomby = 0
            bombx=self.x
            bomby=self.y
            edgex = 0
            edgey = 0
            if(bombx+1 < wrld.width()):
                edgex = 1
            if(bomby+1 < wrld.height()):
                edgey = 1
            for dx in [-4,-3,-2,-1, 0, 1,2,3,4]:
                # Avoid out-of-bound indexing
                if (bombx+dx >=0) and (bombx+dx < wrld.width()):
                    if (bomby >=0) and (bomby < wrld.height()):
                        if wrld.wall_at(bombx+dx, bomby) and bombx+bomby+dx>=bombx+edgex+bomby+edgey:
                            return True
                            
            for dy in [-4,-3,-2,-1, 0, 1,2,3,4]:
                if (bombx >=0) and (bombx < wrld.width()):
                    if (bomby+dy >=0) and (bomby+dy < wrld.height()):
                        # No need to check impossible moves
                        if wrld.wall_at(bombx, bomby+dy) and bombx+bomby+dy>=bombx+edgex+bomby+edgey:
                                return True
        return False
    
                    
                    
        
#        # Create start and end node
#        start_node = Node(None, (thex,they))
#        start_node.g = start_node.h = start_node.f = 0
#        end = []
#        for x in range(0, wrld.width()):
#            for y in range(0, wrld.height()):
#                if(wrld.exit_at(x,y)):
#                    end = (x,y)
#        end_node = Node(None, end)
#        end_node.g = end_node.h = end_node.f = 0
#        # Initialize both open and closed list
#        open_list = []
#        closed_list = []
#        # Add the start node
#        open_list.append(start_node)
#        # Loop until you find the end
#        while len(open_list) > 0:
#    
#        # Get the current node
#            
#            current_node = open_list[0]
#            current_index = 0
#            for index, item in enumerate(open_list):
#                if item.f < current_node.f:
#                    current_node = item
#                    current_index = index
#
#            # Pop current off open list, add to closed list
#            open_list.pop(current_index)
#            closed_list.append(current_node)
#
#            # Found the goal
#            if current_node == end_node:
#                print (current_node.g)
#                print ("found")
#                return current_node.g
#                
#                # Generate children
#            children = []
#            
#            #generate Children
#            for dx in [-1, 0, 1]:
#                #not sure if it should be switched for 1 and 0
#                if (current_node.position[1]+dx >=0) and (current_node.position[1]+dx < wrld.width()):
#                    for dy in [-1, 0, 1]:
#                        if (dx != 0) or (dy != 0):
#                            if (current_node.position[0]+dy >=0) and (current_node.position[0]+dy < wrld.height()):
#                                if not wrld.wall_at(current_node.position[1]+dx, current_node.position[0]+dy):
#                                    #testNode = (searchNode[0]+dx, searchNode[1]+dy, searchNode[0]+1)
#                                    new_node = Node(current_node, (current_node.position[1]+dx,current_node.position[0]+dy))
#                                    new_node.g = current_node.g + 1
#                                    children.append(new_node)
#                                else:
#                                   # testNode = (searchNode[0]+dx, searchNode[1]+dy, searchNode[0]+5)
#                                    new_node = Node(current_node, (current_node.position[1]+dx,current_node.position[0]+dy))
#                                    new_node.g = current_node.g + 3
#                                    children.append(new_node)
#
#            # Loop through children
#            for child in children:
#                # Child is on the closed list
#                broken = False;
#                for closed_child in closed_list:
#                    if child == closed_child:
#                        broken = True
#                        break
#                if broken:
#                    continue
#                    # Create the f, g, and h values
#                child.h = ((child.position[0] - end_node.position[0])) + ((child.position[1] - end_node.position[1]))
#                child.f = child.g + child.h
#                # Child is already in the open list
#                for open_node in open_list:
#                    if child == open_node:
#                        broken = True
#                        break
#                if broken:
#                    continue
#                open_list.append(child)
#        return 0                                        
                                                
                                                
                                                
                                                
            
                                                
                                    
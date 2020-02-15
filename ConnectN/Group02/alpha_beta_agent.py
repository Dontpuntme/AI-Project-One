import math
import agent

###########################
# Alpha-Beta Search Agent #
###########################

class AlphaBetaAgent(agent.Agent):
    """Agent that uses alpha-beta search"""

    # Class constructor.
    #
    # PARAM [string] name:      the name of this player
    # PARAM [int]    max_depth: the maximum search depth
    def __init__(self, name, max_depth, centerMultiplier = 1, threesMultiplier = 1):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth
        self.centerMultiplier = centerMultiplier
        self.threesMultiplier = threesMultiplier

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        freecols = brd.free_cols()
        return self.getMove(brd,freecols[0],self.max_depth,True,-1000000000,1000000000,self.what_player(brd))[1]
        
    # Get the successors of the given board.
    # PARAM [board.Board] brd: the board state
    # RETURN [list of (board.Board, int)]: a list of the successor boards,
    #                                      along with the column where the last
    #                                      token was added in it
    def get_successors(self, brd):
        """Returns the reachable boards from the given board brd. The return value is a tuple (new board state, column number where last token was added)."""
        # Get possible actions
        freecols = brd.free_cols()
        # Are there legal actions left?
        if not freecols:
            return []
        # Make a list of the new boards along with the corresponding actions
        succ = []
        for col in freecols:
            # Clone the original board
            nb = brd.copy()
            # Add a token to the new board
            # (This internally changes nb.player, check the method definition!)
            nb.add_token(col)
            # Add board to list of successors
            succ.append((nb,col))
        return succ
  
    
    def what_player(self,brd):
        #figures out what player the agent isjkm, m
        total = 0
        for x in range(brd.w):
            for y in range(brd.h):
                if (brd.board[y][x] == 1):
                    total +=1
                elif (brd.board[y][x] == 2):
                    total -=1
        if total==1:
            return 2
        else:
            return 1
        
                    


    def getMove(self, brd, col, depth, isMaximizingPlayer, alpha, beta,player):
        #alpha beta pruning with a cutoff if brds cause wins or losses
        if depth == 0 or brd.get_outcome() != 0:
            value = (depth + 1)*self.getValue(brd,player)
            return (brd, col, value)
        elif isMaximizingPlayer:
            bestValList = list((brd, col, -1000000000))
            for node in self.get_successors(brd):
                #                   board    col     depth     IsMaximizing
                MoveTuple=self.getMove(node[0], node[1], depth-1, False, alpha, beta,player)
                if MoveTuple[2]>bestValList[2]:
                    bestValList[0]=node[0]
                    bestValList[1]=node[1]
                    bestValList[2]=MoveTuple[2]        
                if bestValList[2]>=beta :
                    return bestValList
                alpha = max(alpha, bestValList[2])
               
            return bestValList
    
        else :
            bestValList = list((brd,col, 1000000000))
            for node in self.get_successors(brd):
                MoveTuple=self.getMove(node[0], node[1], depth-1, True, alpha, beta,player)
                if MoveTuple[2]<bestValList[2]:
                    bestValList[0]=node[0]
                    bestValList[1]=node[1]
                    bestValList[2]=MoveTuple[2]
                if bestValList[2]<=alpha :
                    return bestValList
                beta = min(beta, bestValList[2]) 

            return bestValList
        
        
    def getValue(self,brd,player):
        if brd.get_outcome() == player:
            return 10000
        if brd.get_outcome() !=0 and brd.get_outcome() !=player:
            return -10000
        else:
           return (self.centerMultiplier*self.centerPiecePreference(brd,player))+(self.threesMultiplier*self.num_threes(brd,player))
       #self.num_threes(brd,player)
       
    def is_three_at(self,brd, x, y, dx, dy, player):
        #returns a positive one of there is a set of threes connected to the players token a negative value if it's the other players token
        # Avoid out-of-bounds errors
        if ((x + (4-1) * dx >= brd.w) or
            (y + (4-1) * dy < 0) or (y + (4-1) * dy >= brd.h)):
            return 0
        # Get token at (x,y)
        t = brd.board[y][x]
        # Go through elements
        if t == 0:
            return 0
        total = 0
        for i in range(1, 4):
            if brd.board[y + i*dy][x + i*dx] != t and brd.board[y + i*dy][x + i*dx] != 0:
                total += 1
        if total>1 and player==t:
            return 1
        elif total>1 and player!=t:
            return -1
        else:
            return 0
    def num_threes_at(self,brd,x, y,player):
        #Returns if there is a set of three tokens at an x,y cordinate
        return (self.is_three_at(brd,x, y, 1, 0, player) + # Horizontal
                self.is_three_at(brd,x, y, 0, 1, player) + # Vertical
                self.is_three_at(brd,x, y, 1, 1, player) + # Diagonal up
                self.is_three_at(brd,x, y, 1, -1,player)) # Diagonal down
    def num_threes(self,brd,player):
        #returns the number of threes on the board
        total = 0
        for x in range(brd.w):
            for y in range(brd.h):
                if (brd.board[y][x] != 0):
                    total+=self.num_threes_at(brd,x,y,player)
        return total
    #Goes through a board state and subtracts or adds to the value of the board state based on how close pieces are to the center
    def centerPiecePreference(self,brd,player):
        centerBias=0
        for x in range(brd.w):
            for y in range(brd.h):
                if (brd.board[y][x] != 0):
                    if(brd.board[y][x]==player):
                        centerBias += (brd.w/2 - abs(x - brd.w/2))
                        centerBias += (brd.h/2 - abs(y - brd.h/2))
                    else:
                        centerBias -= (brd.w/2 - abs(x - brd.w/2))
                        centerBias += (brd.h/2 - abs(y - brd.h/2))
        return centerBias
        
THE_AGENT = AlphaBetaAgent("Group02",6,1)

    

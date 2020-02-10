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
    def __init__(self, name, max_depth):
        super().__init__(name)
        # Max search depth
        self.max_depth = max_depth

    # Pick a column.
    #
    # PARAM [board.Board] brd: the current board state
    # RETURN [int]: the column where the token must be added
    #
    # NOTE: make sure the column is legal, or you'll lose the game.
    def go(self, brd):
        """Search for the best move (choice of column for the token)"""
        return self.getMoveStarter(brd, self.max_depth)
        
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

    def getMoveStarter(self, brd, depth):
        best = (-1, float("-inf"))
        for node in self.get_successors(brd):
            move = self.getMove(node, depth, False, float("-inf"), float("inf"))
            if(move[1] >= best[1]):
                best = move
        return best[0]

    def getMove(self, brd, depth, isMaximizingPlayer, alpha, beta):
        if depth == 0:
            return (brd[1], self.getValue(brd))
        
        if isMaximizingPlayer:
            bestVal = (-1, float("-inf"))
            for node in self.get_successors(brd[0]):
                move = self.getMove(node, depth-1, False, alpha, beta)[0]
                if move[1]>=bestVal[1]:
                    bestVal = move
                alpha = max( alpha, bestVal[1])
                if beta <= alpha:
                    break
            return bestVal
    
        else :
            bestVal = (-1, float("inf"))
            for node in self.get_successors(brd[0]):
                move = self.getMove(node, depth-1, True, alpha, beta)
                if move[1] <= bestVal[1]:
                    bestVal = move
                beta = min( beta, bestVal[1])
                if beta <= alpha:
                    break
            return bestVal, 
        
        
    def getValue(self, brd):
        if brd[0].get_outcome() == 2:
            return 1000
        if brd[0].get_outcome() == 1:
            return -10000
        if brd[0].get_outcome() == 0:
            return 0
#Thomas Alpha Beta and 3 in a row counting.
#David most sets of N

    

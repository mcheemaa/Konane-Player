import game_rules, random
###########################################################################
# Explanation of the types:
# The board is represented by a row-major 2D list of characters, 0 indexed
# A point is a tuple of (int, int) representing (row, column)
# A move is a tuple of (point, point) representing (origin, destination)
# A jump is a move of length 2
###########################################################################

# I will treat these like constants even though they aren't
# Also, these values obviously are not real infinity, but close enough for this purpose
NEG_INF = -1000000000
POS_INF = 1000000000

class Player(object):
    """ This is the player interface that is consumed by the GameManager. """
    def __init__(self, symbol): self.symbol = symbol # 'x' or 'o'

    def __str__(self): return str(type(self))

    def selectInitialX(self, board): return (0, 0)
    def selectInitialO(self, board): pass

    def getMove(self, board): pass

    def h1(self, board, symbol):
        return -len(game_rules.getLegalMoves(board, 'o' if self.symbol == 'x' else 'x'))


# This class has been replaced with the code for a deterministic player.
class MinimaxPlayer(Player):
    def __init__(self, symbol, depth): 
        super(MinimaxPlayer, self).__init__(symbol)
        self.depth = depth  # so that i can access self.depth in my functions for initial value


    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    # Edit this one here. :)

    def getMove(self, board):
        
        final_move = self.maxValue(board, self.symbol, self.depth)[1]
        return final_move


    def maxValue(self, board, symbol, depth):
        
        legalMoves = game_rules.getLegalMoves(board, symbol)
        if len(legalMoves) == 0 or depth == 0:  # our terminal test state and if true returns a utility value
            return (self.h1(board, symbol), None)
        
        temp = (NEG_INF, None) # set to neg infinity 

        for i in range (len(legalMoves)): # checking for all the moves / successors and then going though each move 
            second = game_rules.makeMove(board, legalMoves[i])
            
            if (symbol == "x"):
                new_t = self.minValue(second, "o", depth - 1)[0]
            else:
                new_t = self.minValue(second, "x", depth - 1)[0]

            if (temp[0] < new_t):
                temp = (new_t, legalMoves[i])
        
        return temp


    def minValue(self, board, symbol, depth):

        legalMoves = game_rules.getLegalMoves(board, symbol)
        if len(legalMoves) == 0 or depth == 0:
            return (self.h1(board, symbol), None)

        temp = (POS_INF, None)

        for i in range (len(legalMoves)):
            second = game_rules.makeMove(board, legalMoves[i])
            
            if (symbol == "x"):
                new_t = self.maxValue(second, "o", depth - 1)[0]
            else:
                new_t = self.maxValue(second, "x", depth - 1)[0]

            if (temp[0] > new_t):
                temp = (new_t, legalMoves[i])
        
        return temp



# This class has been replaced with the code for a deterministic player.
class AlphaBetaPlayer(Player):
    def __init__(self, symbol, depth): 
        super(AlphaBetaPlayer, self).__init__(symbol)
        self.depth = depth  # so that i can access self.depth in my functions for initial value

    # Leave these two functions alone.
    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        
        final_move = self.maxValue(board, -999999999, 999999999, self.symbol, self.depth)[1] # sending intital values for alpha and beta 
        return final_move 


    def maxValue(self, board, a, b, symbol, depth):
        
        legalMoves = game_rules.getLegalMoves(board, symbol)

        if len(legalMoves) == 0 or depth == 0:
            return (self.h1(board, symbol), None)
        
        temp = (-999999999, None)

        for i in range (len(legalMoves)):
            second = game_rules.makeMove(board, legalMoves[i])
            
            if (symbol == "x"):
                new_t = self.minValue(second, a, b, "o", depth - 1)[0]
            else:
                new_t = self.minValue(second, a, b, "x", depth - 1)[0]

            if (temp[0] < new_t):
                temp = (new_t, legalMoves[i])

            a = max(a,temp[0]) 
            if (b <= a):        # check if b is less than equal to a then reutrn 
                return temp
        
        return temp


    def minValue(self, board, a, b, symbol, depth):

        legalMoves = game_rules.getLegalMoves(board, symbol)
        if len(legalMoves) == 0 or depth == 0:
            return (self.h1(board, symbol), None)

        temp = (999999999, None)

        for i in range (len(legalMoves)):
            second = game_rules.makeMove(board, legalMoves[i])
            
            if (symbol == "x"):
                new_t = self.maxValue(second, a, b, "o", depth - 1)[0]
            else:
                new_t = self.maxValue(second, a, b, "x", depth - 1)[0]

            if (temp[0] > new_t):
                temp = (new_t, legalMoves[i])
  
            b = min(b, temp[0])
            if (b <= a):        # check if b is less than equal to a then reutrn 
                return temp
        
        return temp


class RandomPlayer(Player):
    def __init__(self, symbol):
        super(RandomPlayer, self).__init__(symbol)

    def selectInitialX(self, board):
        validMoves = game_rules.getFirstMovesForX(board)
        return random.choice(list(validMoves))

    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return random.choice(list(validMoves))

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return random.choice(legalMoves)
        else: return None


class DeterministicPlayer(Player):
    def __init__(self, symbol): super(DeterministicPlayer, self).__init__(symbol)

    def selectInitialX(self, board): return (0,0)
    def selectInitialO(self, board):
        validMoves = game_rules.getFirstMovesForO(board)
        return list(validMoves)[0]

    def getMove(self, board):
        legalMoves = game_rules.getLegalMoves(board, self.symbol)
        if len(legalMoves) > 0: return legalMoves[0]
        else: return None


class HumanPlayer(Player):
    def __init__(self, symbol): super(HumanPlayer, self).__init__(symbol)
    def selectInitialX(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def selectInitialO(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')
    def getMove(self, board): raise NotImplementedException('HumanPlayer functionality is handled externally.')


def makePlayer(playerType, symbol, depth=1):
    player = playerType[0].lower()
    if player   == 'h': return HumanPlayer(symbol)
    elif player == 'r': return RandomPlayer(symbol)
    elif player == 'm': return MinimaxPlayer(symbol, depth)
    elif player == 'a': return AlphaBetaPlayer(symbol, depth)
    elif player == 'd': return DeterministicPlayer(symbol)
    else: raise NotImplementedException('Unrecognized player type {}'.format(playerType))

def callMoveFunction(player, board):
    if game_rules.isInitialMove(board): return player.selectInitialX(board) if player.symbol == 'x' else player.selectInitialO(board)
    else: return player.getMove(board)

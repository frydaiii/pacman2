# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        distance = float('inf')
        foodList = newFood.asList()

        if successorGameState.isWin():
            return float('inf')


        for state in newGhostStates:
            if state.getPosition() == newPos and (state.scaredTimer == 0):
                return float('-inf')

        for x in foodList:
            tempDistance = (manhattanDistance(newPos, x))
            if (tempDistance < distance):
                distance = tempDistance

        return 1.0/distance + successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def minimax(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            if agentIndex == 0: # pacman
                maxEval = -9999999
                for action in gameState.getLegalActions(agentIndex):
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    eval = minimax(nextState, depth, 1)
                    maxEval = max(maxEval, eval)
                return maxEval
            
            if agentIndex != 0: # ghosts
                minEval = 9999999
                for action in gameState.getLegalActions(agentIndex):
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    if agentIndex == gameState.getNumAgents() -1:
                        eval = minimax(nextState, depth + 1, 0)
                    else:
                        eval = minimax(nextState, depth, agentIndex + 1)
                    minEval = min(minEval, eval)
                return minEval

        eval = -9999999
        resultAction = ''
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            nextEval = minimax(nextState, 0, 1)
            if eval < nextEval:
                eval = nextEval
                resultAction = action
        return resultAction


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def minimax(gameState, depth, alpha, beta, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            
            if agentIndex == 0: # pacman
                maxEval = -9999999
                for action in gameState.getLegalActions(agentIndex):
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    eval = minimax(nextState, depth, alpha, beta, 1)
                    maxEval = max(maxEval, eval)
                    alpha = max(alpha, maxEval)
                    if alpha > beta:
                        break
                return maxEval
            
            if agentIndex != 0: # ghosts
                minEval = 9999999
                for action in gameState.getLegalActions(agentIndex):
                    nextState = gameState.generateSuccessor(agentIndex, action)
                    if agentIndex == gameState.getNumAgents() -1:
                        eval = minimax(nextState, depth + 1, alpha, beta, 0)
                    else:
                        eval = minimax(nextState, depth, alpha, beta, agentIndex + 1)
                    minEval = min(minEval, eval)
                    beta = min(beta, minEval)
                    if alpha > beta:
                        break
                return minEval

        eval = -9999999
        alpha = -9999999
        beta = 9999999
        resultAction = ''
        for action in gameState.getLegalActions(0):
            nextState = gameState.generateSuccessor(0, action)
            nextEval = minimax(nextState, 0, alpha, beta, 1)
            if eval < nextEval:
                eval = nextEval
                resultAction = action
            if nextEval > beta:
                return resultAction
            alpha = max(alpha, nextEval)
        return resultAction

        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        pacman_legal_actions = gameState.getLegalActions(0)
        max_value = float('-inf')
        max_action  = None

        for action in pacman_legal_actions:
            action_value = self.Min_Value(gameState.generateSuccessor(0, action), 1, 0)
            if ((action_value) > max_value ):
                max_value = action_value
                max_action = action

        return max_action
    def Max_Value (self, gameState, depth):
        """For the Max Player here Pacman"""

        if ((depth == self.depth)  or (len(gameState.getLegalActions(0)) == 0)):
            return self.evaluationFunction(gameState)

        return max([self.Min_Value(gameState.generateSuccessor(0, action), 1, depth) for action in gameState.getLegalActions(0)])

    def Min_Value (self, gameState, agentIndex, depth):
        """ For the MIN Players or Agents  """

        num_actions = len(gameState.getLegalActions(agentIndex))

        if (num_actions == 0):
            return self.evaluationFunction(gameState)

        if (agentIndex < gameState.getNumAgents() - 1):
            return sum([self.Min_Value(gameState.generateSuccessor(agentIndex, action), agentIndex + 1, depth) for action in gameState.getLegalActions(agentIndex)]) / float(num_actions)

        else:
            return sum([self.Max_Value(gameState.generateSuccessor(agentIndex, action), depth + 1) for action in gameState.getLegalActions(agentIndex)]) / float(num_actions)

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    
    """ Manhattan distance to the foods from the current state """
    foodList = newFood.asList()
    from util import manhattanDistance
    foodDistance = [0]
    for pos in foodList:
        foodDistance.append(manhattanDistance(newPos,pos))

    """ Manhattan distance to each ghost from the current state"""
    ghostPos = []
    for ghost in newGhostStates:
        ghostPos.append(ghost.getPosition())
    ghostDistance = [0]
    for pos in ghostPos:
        ghostDistance.append(manhattanDistance(newPos,pos))

    numberofPowerPellets = len(currentGameState.getCapsules())

    score = 0          
    sumScaredTimes = sum(newScaredTimes)
    sumGhostDistance = sum (ghostDistance)
    reciprocalfoodDistance = 0

    if sum(foodDistance) > 0:
        reciprocalfoodDistance = 1.0 / max(foodDistance)
        
    score += currentGameState.getScore()  + reciprocalfoodDistance

    if sumScaredTimes > 0:    
        score +=   sumScaredTimes + (-1 * numberofPowerPellets) + (-1 * sumGhostDistance)
    else :
        score +=  sumGhostDistance + numberofPowerPellets
    return score

# Abbreviation
better = betterEvaluationFunction

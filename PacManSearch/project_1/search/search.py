# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for 
# educational purposes provided that (1) you do not distribute or publish 
# solutions, (2) you retain this notice, and (3) you provide clear 
# attribution to UC Berkeley, including a link to 
# http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero 
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and 
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util


class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    stack = util.Stack()
    vs = set()
    current = {problem.getStartState(): []}
    while not problem.isGoalState(list(current.keys())[0]):
        p = list(current.keys())[0]
        if p not in vs:
            vs.add(p)
            for s in problem.getSuccessors(p):
                if s not in vs:
                    sList = list(current.values())[0].copy()
                    sList.append(s[1])
                    stack.push({s[0]: sList})
        current = stack.pop()
    return list(current.values())[0]

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    "*** YOUR CODE HERE ***"
    queue = util.Queue()
    vs = set()
    current = {problem.getStartState(): []}
    while not problem.isGoalState(list(current.keys())[0]):
        p = list(current.keys())[0]
        if p not in vs:
            vs.add(p)
            for s in problem.getSuccessors(p):
                if s not in vs:
                    sList = list(current.values())[0].copy()
                    sList.append(s[1])
                    queue.push({s[0]: sList})
        current = queue.pop()
    return list(current.values())[0]


def uniformCostSearch(problem):
    """
    Search the node of least total cost first.
    """
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue()
    vs = set()
    pq.push({problem.getStartState(): []}, 0)
    current = pq.pop()
    while not problem.isGoalState(list(current.keys())[0]):
        p = list(current.keys())[0]
        if p not in vs:
            vs.add(p)
            for s in problem.getSuccessors(p):
                sList = list(current.values())[0].copy()
                sList.append(s[1])
                if s not in vs:
                    pq.push({s[0]: sList}, problem.getCostOfActions(sList))
                else:
                    c = 0
                    for pair in pq.heap:
                        if s[0] == list(pair[2].keys())[0]:
                            if pair[0] > problem.getCostofActions(sList):
                                pq.heap[c] = (problem.getCostOfActions(sList), pq.heap[c][1], {s[0]: sList})
                        c += 1
        current = pq.pop()
    return list(current.values())[0]

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0


def aStarSearch(problem, heuristic=nullHeuristic):
    """
    Search the node that has the lowest combined cost and heuristic first.
    """
    "*** YOUR CODE HERE ***"
    pq = util.PriorityQueue()
    vs = set()
    pq.push({problem.getStartState(): []}, 0 + heuristic(problem.getStartState(), problem))
    current = pq.pop()
    while not problem.isGoalState(list(current.keys())[0]):
        p = list(current.keys())[0]
        if p not in vs:
            vs.add(p)
            for s in problem.getSuccessors(p):
                sList = list(current.values())[0].copy()
                sList.append(s[1])
                priority = problem.getCostOfActions(sList) + heuristic(s[0], problem)
                if s not in vs:
                    pq.push({s[0]: sList}, priority)
                else:
                    c = 0
                    for pair in pq.heap:
                        if s[0] == list(pair[2].keys())[0]:
                            if pair[0] > priority:
                                pq.heap[c] = (priority, pq.heap[c][1], {s[0]: sList})
                        c += 1
        current = pq.pop()
    return list(current.values())[0]


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch

import queue
import random
import math
import time
import copy
from random import randint

def DFS(matrix, start_location, end_location, dim): # Uses DFS to determine if one state is reachable from another
    fringe = []
    closed = []
    fringe.append(start_location)
    while(len(fringe) != 0):
        #print(fringe, "fringe") #prints fringe (NOT NEEDED)
        current = fringe.pop()  #Pops state from fringe and makes current
        #print(current, "current") #prints current state (NOT NEEDED)
        if(current == end_location):
            return True
        else:
            i = current[0]
            j = current[1]
            if((i + 1) >= 0 and (i + 1) < dim ):   # Checks if the following state is in the maze range   
                if(matrix[i+1][j] == "O" or matrix[i+1][j] == "G"):  #checks is the following state is a open or goal state
                    if(closed.count([i+1,j]) == 0 and fringe.count([i+1,j]) == 0): #checks if the following state isn't already closed or in the fringe
                        fringe.append([i+1,j])
            if((i - 1) >=0 and (i - 1) < dim):
                if(matrix[i-1][j] == "O" or matrix[i-1][j] == "G" ):
                    if(closed.count([i-1,j]) == 0 and fringe.count([i-1,j]) == 0):
                        fringe.append([i-1,j])
            if((j + 1) >=0 and (j + 1) < dim):
                if(matrix[i][j+1] == "O" or matrix[i][j+1] == "G"):
                    if(closed.count([i,j+1]) == 0 and fringe.count([i,j+1]) == 0):
                        fringe.append([i,j+1])  
            if((j - 1) >= 0 and (j - 1) < dim):
                if(matrix[i][j-1] == "O" or matrix[i][j-1] == "G"):
                    if(closed.count([i,j-1]) == 0 and fringe.count([i,j-1]) == 0):
                        fringe.append([i,j-1])
            closed.append(current)  #puts current state in closed after generating valid children
    return False

class BFS_state:
    def __init__(self, state, prev):
        self.state = state
        self.prev = prev

def BFS(matrix, start_location, end_location, dim, returnPath, isPrint): # Uses BFS to determine the shortest path from one state to another
    roundCounter = 0
    fringe = queue.Queue()
    closed = []
    shortest_path = []
    inFringe = []
    start_state = BFS_state(start_location, 0)
    fringe.put(start_state)
    while(fringe.empty() == False):
        roundCounter = roundCounter + 1
        current_state = fringe.get()  #Pops state from fringe and makes current
        current = current_state.state
        if(current == end_location):
            while(current != start_location):#Traces back through nodes to construct path
                shortest_path.append(current)
                current_state = current_state.prev
                current = current_state.state
            shortest_path.append(start_location)
            shortest_path.reverse()
            if(isPrint): 
                print(roundCounter, "rounds of BFS were performed.")
            if(returnPath):
                if(isPrint):
                    print("Shortest path is: " , shortest_path)
                return shortest_path
            else:
                return roundCounter
        else:
            i = current[0]
            j = current[1]
            if((i + 1) >= 0 and (i + 1) < dim ):   # Checks if the following state is in the maze range   
                if(matrix[i+1][j] == "O" or matrix[i+1][j] == "G"):  #checks is the following state is a open or goal state
                    if(closed.count([i+1,j]) == 0 and inFringe.count([i+1,j]) == 0 ): #checks if the following state isn't already closed or in the fringe
                        new_state = BFS_state([i+1,j], current_state)
                        fringe.put(new_state)
                        inFringe.append([i+1,j])
            if((i - 1) >=0 and (i - 1) < dim):
                if(matrix[i-1][j] == "O" or matrix[i-1][j] == "G" ):
                    if(closed.count([i-1,j]) == 0 and inFringe.count([i-1,j]) == 0 ):
                        new_state = BFS_state([i-1,j], current_state)
                        fringe.put(new_state)
                        inFringe.append([i-1,j])
            if((j + 1) >=0 and (j + 1) < dim):
                if(matrix[i][j+1] == "O" or matrix[i][j+1] == "G"):
                    if(closed.count([i,j+1]) == 0 and inFringe.count([i,j+1]) == 0  ):
                        new_state = BFS_state([i,j+1], current_state)
                        fringe.put(new_state)
                        inFringe.append([i,j+1]) 
            if((j - 1) >= 0 and (j - 1) < dim):
                if(matrix[i][j-1] == "O" or matrix[i][j-1] == "G"):
                    if(closed.count([i,j-1]) == 0 and inFringe.count([i,j-1]) == 0):
                        new_state = BFS_state([i,j-1], current_state)
                        fringe.put(new_state)
                        inFringe.append([i,j-1])
            closed.append(current)  #puts current state in closed after generating valid children
    print("there lies no path to the goal node. " , roundCounter, " rounds of BFS were performed.")
    if(returnPath):
        return []
    else:
        return roundCounter

#Node class for every position. Contains the position, the straightLine path from the position to the goal node, and a reference to the previous position.
class Node: 
    def __init__(self, position, heuristic, distance, prev=None) :
        self.position = position
        self.heuristic = heuristic
        self.distance = distance
        self.prev = prev

def Astar2(matrix, start_location, end_location, dim, returnPath, isPrint) :
    roundCounter = 0
    fringe = []
    inFringe = [] 
    closed = []
    path = []
    startNode = Node(start_location, 0, 0)
    fringe.append(startNode)
    inFringe.append([startNode.position[0], startNode.position[1]]) #List to check if the current position being expanded is in the fringe already.
    while( fringe ) :
        roundCounter = roundCounter + 1
        currentNode = fringe.pop(0)
        inFringe.remove([currentNode.position[0], currentNode.position[1]])
        x = currentNode.position[0]
        y = currentNode.position[1]
        if matrix[x][y] == 'G' :
            while( not(currentNode == startNode) ) : #Traces back through nodes to construct path.
                path.append(currentNode.position)
                currentNode = currentNode.prev
            path.append(startNode.position)
            path.reverse()
            if(isPrint):
                print(roundCounter, "rounds of A* were performed.")
            if(returnPath):
                if(isPrint):
                    print("Shortest path is: " , path)
                return path
            else:
                return roundCounter
        else :
            if ((x+1) >= 0 and (x+1) < dim) :
                if(matrix[x+1][y] == "O" or matrix[x+1][y] == "G"): #Ensures left position is not on fire.
                    if(closed.count([x+1,y]) == 0) and (inFringe.count([x+1, y]) == 0) : #Ensures left position is in the maze. 
                        node = Node([x+1, y], currentNode.distance + 1 + euclideanDistance([x+1,y], end_location), currentNode.distance + 1,  currentNode)
                        # ^ Constructs a node using the position, the straight line path from the position to goal node, the distance from the start node,
                        #   and the reference to the previous node.  
                        fringe = sortedInsert2(fringe, node) #Sorted insert based on euclidean heuristic.
                        inFringe.append([x+1, y])
            if ((x-1) >= 0 and (x-1) < dim) :
                if(matrix[x-1][y] == "O" or matrix[x-1][y] == "G"): #Ensures right position is not on fire. 
                    if(closed.count([x-1,y]) == 0) and (inFringe.count([x-1, y]) == 0) : #Ensures right position is in the maze                     
                        node = Node([x-1, y], currentNode.distance + 1 + euclideanDistance([x-1,y], end_location), currentNode.distance + 1,  currentNode)
                        # ^ Constructs a node using the position, the straight line path from the position to goal node, the distance from the start node,
                        #   and the reference to the previous node.  
                        fringe = sortedInsert2(fringe, node) #Sorted insert based on euclidean heuristic.
                        inFringe.append([x-1,y])
            if ((y+1) >= 0 and (y+1) < dim) :
                if(matrix[x][y+1] == "O" or matrix[x][y+1] == "G"): #Ensures bottom position is not on fire. 
                    if(closed.count([x,y+1]) == 0) and (inFringe.count([x,y+1]) == 0) : #Ensures bottom position is in the maze.
                        node = Node([x, y+1], currentNode.distance + 1 + euclideanDistance([x,y+1], end_location), currentNode.distance + 1,  currentNode)
                        # ^ Constructs a node using the position, the straight line path from the position to goal node, the distance from the start node,
                        #   and the reference to the previous node.  
                        fringe = sortedInsert2(fringe, node) #Sorted insert based on euclidean heuristic.
                        inFringe.append([x,y+1])
            if ((y-1) >= 0 and (y-1) < dim) :
                if(matrix[x][y-1] == "O" or matrix[x][y-1] == "G"): #Ensures top position is not on fire.
                    if(closed.count([x,y-1]) == 0) and (inFringe.count([x,y-1]) == 0): #Ensures top position is in the maze. 
                        node = Node([x, y-1], currentNode.distance + 1 + euclideanDistance([x,y-1], end_location), currentNode.distance + 1,  currentNode)
                        # ^ Constructs a node using the position, the straight line path from the position to goal node, the distance from the start node,
                        #   and the reference to the previous node.  
                        fringe = sortedInsert2(fringe, node) #Sorted insert based on euclidean heuristic.
                        inFringe.append([x,y-1])
        closed.append([currentNode.position[0], currentNode.position[1]]) #closes state.
    if(isPrint):
        print("there lies no path to the goal node. " , roundCounter, " rounds of A* were performed.")
    if(returnPath):
        return []
    else:
        return roundCounter

#Helper function for Astar2. 
def sortedInsert2(Alist, item) : 
    for i in range(len(Alist)) :
        if Alist[i].heuristic > item.heuristic : #sorts based on heuristic.
            retList = Alist[:i] + [item] + Alist[i:] 
            return retList
    Alist.append(item)
    return Alist

#Function for euclidean metric heuristic (straight line path between two points.)
def euclideanDistance(start_point, end_point): 
    horizontalDiff = math.sqrt((end_point[0] - start_point[0]) ** 2)
    verticalDiff = math.sqrt((end_point[1] - start_point[1]) ** 2)
    return math.sqrt((verticalDiff**2) + (horizontalDiff**2))
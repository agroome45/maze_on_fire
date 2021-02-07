import queue
import random
import math
from random import randint

def create_maze(dim,p): # creates a maze given dem and p
    maze=[]
    for i in range(dim):
        c=[]
        for j in range(dim):
            rand = randint(0,100) # calculates the change a state is filled or empty 
            chance = p * 100 
            if(i == 0 and j == 0): # stating state at upper left corner
                j = "S"
            elif(i == (dim-1) and j == (dim-1)): # goal state at lower right corner
                j = "G"
            elif(rand > chance):
                j = "O"
            else:
                j = "X"
            c.append(j)
        maze.append(c)
    return maze

def print_maze(maze,dim): #prints out the maze 
    for i in range(dim):
        for j in range(dim):
            print(maze[i][j],end="    ")
        print()
    print()
    
def DFS(matrix, start_location, end_location, dim): # Uses DFS to determine if one state is reachable from another
    fringe = []
    closed = []
    fringe.append(start_location)
    while(len(fringe) != 0):
        print(fringe, "Fringe") #prints fringe (NOT NEEDED)
        current = fringe.pop()  #Pops state from fringe and makes current
        print(current, "current") #prints current state (NOT NEEDED)
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

def BFS(matrix, start_location, end_location, dim): # Uses DFS to determine if one state is reachable from another
    fringe = queue.Queue()
    closed = []
    inFringe = []
    fringe.put(start_location)
    while(fringe.empty() == False):
        print(fringe.queue, "Fringe") #prints fringe (NOT NEEDED)
        current = fringe.get()  #Pops state from fringe and makes current
        print(current, "current") #prints current state (NOT NEEDED)
        if(current == end_location):
            return True
        else:
            i = current[0]
            j = current[1]
            if((i + 1) >= 0 and (i + 1) < dim ):   # Checks if the following state is in the maze range   
                if(matrix[i+1][j] == "O" or matrix[i+1][j] == "G"):  #checks is the following state is a open or goal state
                    if(closed.count([i+1,j]) == 0 and inFringe.count([i+1,j]) == 0 ): #checks if the following state isn't already closed or in the fringe
                        fringe.put([i+1,j])
                        inFringe.append([i+1,j])
            if((i - 1) >=0 and (i - 1) < dim):
                if(matrix[i-1][j] == "O" or matrix[i-1][j] == "G" ):
                    if(closed.count([i-1,j]) == 0 and inFringe.count([i-1,j]) == 0 ):
                        fringe.put([i-1,j])
                        inFringe.append([i-1,j])
            if((j + 1) >=0 and (j + 1) < dim):
                if(matrix[i][j+1] == "O" or matrix[i][j+1] == "G"):
                    if(closed.count([i,j+1]) == 0 and inFringe.count([i,j+1]) == 0  ):
                        fringe.put([i,j+1])
                        inFringe.append([i,j+1]) 
            if((j - 1) >= 0 and (j - 1) < dim):
                if(matrix[i][j-1] == "O" or matrix[i][j-1] == "G"):
                    if(closed.count([i,j-1]) == 0 and inFringe.count([i,j-1]) == 0):
                        fringe.put([i,j-1])
                        inFringe.append([i,j-1])
            closed.append(current)  #puts current state in closed after generating valid children
    return False  

#Node class for every position. Contains the position, the straightLine path from the position to the goal node, and a reference to the previous position.
class Node: 
    def __init__(self, position, heuristic, distance, prev=None) :
        self.position = position
        self.heuristic = heuristic
        self.distance = distance
        self.prev = prev

def Astar2(matrix, start_location, end_location, dim) :
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
            print(roundCounter, "rounds of A* were performed.")
            print("Shortest path is: " , path)
            return
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
                    if(closed.count([x,y-1]) == 0) and (inFringe.count([x,y+1]) == 0): #Ensures top position is in the maze. 
                        node = Node([x, y-1], currentNode.distance + 1 + euclideanDistance([x,y-1], end_location), currentNode.distance + 1,  currentNode)
                        # ^ Constructs a node using the position, the straight line path from the position to goal node, the distance from the start node,
                        #   and the reference to the previous node.  
                        fringe = sortedInsert2(fringe, node) #Sorted insert based on euclidean heuristic.
                        inFringe.append([x,y-1])
        closed.append([currentNode.position[0], currentNode.position[1]]) #closes state.
    print("there lies no path to the goal node. " , roundCounter, " rounds of A* were performed.")
    return

def sortedInsert2(Alist, item) : #Helper function for Astar2. 
    for i in range(len(Alist)) :
        if Alist[i].heuristic > item.heuristic : #sorts based on heuristic.
            retList = Alist[:i] + [item] + Alist[i:] 
            return retList
    Alist.append(item)
    return Alist

def euclideanDistance(start_point, end_point): #Function for euclidean metric heuristic (straight line path between two points.)
    horizontalDiff = math.sqrt((end_point[0] - start_point[0]) ** 2)
    verticalDiff = math.sqrt((end_point[1] - start_point[1]) ** 2)
    return math.sqrt((verticalDiff**2) + (horizontalDiff**2))

if __name__ == "__main__" :            
    dim = int(input("Enter Size dim: "))
    p = float(input("Enter Probability (0 < p < 1) p:"))

    print()
    maze = create_maze(dim, p)
    print_maze(maze, dim)
    print("DFS which determines if G can be reached from S")
    print(DFS(maze, [0,0], [dim-1,dim-1], dim))
    print()
    print("BFS which determines if G can be reached from S")
    print(BFS(maze, [0,0], [dim-1,dim-1], dim))
    print()
    print("Astar which determines the shortest path from S to G")
    print()
    Astar2(maze, [0,0], [dim-1, dim-1], dim)
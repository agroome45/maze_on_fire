import queue
import random
import math
import time
import copy
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
            elif(rand >= chance):
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

def start_fire(maze): #Randomly starts a fire at a singular point in the maze
    while(1):
        randX = randint(0, len(maze)-1)
        randY = randint(0, len(maze)-1)
        if(maze[randX][randY] == 'O' or maze[randX][randY] == 'G' or maze[randX][randY] == 'S') : #Checks if randomly generated position is an open position.
            maze[randX][randY] = 'F'
            return maze

def advance_fire_one_step(maze, q): #advances fire once step using maze and probability q
    adjacentFires = 0
    retMaze = copy.deepcopy(maze)
    for x in range(0, len(maze)):
        for y in range(0, len(maze)):
            if (maze[x][y] == 'O' or maze[x][y] == 'G'): #Checks if position is an open position.
                if((x+1) >= 0 and (x+1) < len(maze)): #Checks if position to the right is within the maze.
                    if(maze[x+1][y] == 'F'): #Checks if position to the right is on fire.
                        adjacentFires = adjacentFires + 1
                if((x-1) >= 0 and (x-1) < len(maze)): #Checks if position to the left is within the maze.
                    if(maze[x-1][y] == 'F'): #Checks if position to the left is on fire.
                        adjacentFires = adjacentFires + 1
                if((y+1) >= 0 and (y+1) < len(maze)): #Checks if position below is within the maze.
                    if(maze[x][y+1] == 'F'): #Checks if position below is on fire.
                        adjacentFires = adjacentFires + 1
                if((y-1) >= 0 and (y-1) < len(maze)): #Checks if position above is within the maze.
                    if(maze[x][y-1] == 'F'): #Checks if position above is on fire.
                        adjacentFires = adjacentFires + 1
                if(adjacentFires > 0):
                    probability = (1 - (1-q)**adjacentFires) * 100 #Calculates true probability of fire spreading to current position. 
                    random = randint(0,100)
                    if(probability > random):
                        retMaze[x][y] = 'F'
                    adjacentFires = 0
    return retMaze

def strategy_one(maze, dim, q):
    path = Astar2(maze, [0,0], [dim-1, dim-1], dim)
    maze = start_fire(maze)
    if(path == []):
        return False
    for i in range(len(path)):
        Agent = path[i]
        x = Agent[0]
        y = Agent[1]
        if(maze[x][y] == "F"):
            #print("Step :", i)
            #print_maze(maze, dim) 
            return False
        elif(maze[x][y] == "G"):
            #print("Step :", i)
            #print_maze(maze, dim) 
            return True
        maze[x][y] = "A"
        #print("Step :", i)
        #print_maze(maze, dim) #Can remove if maze is to big 
        maze = advance_fire_one_step(maze, q)
        
def strategy_two(maze, dim, q):
    maze = start_fire(maze)
    currentPos = [0,0]
    stepCounter = 0
    while (currentPos != [dim-1,dim-1]):
        #print("Agent at position ", currentPos)
        #print()
        path = Astar2(maze, currentPos, [dim-1, dim-1], dim)
        if(maze[currentPos[0]][currentPos[1]] == 'F'): #Agent has caught on fire.
            maze[currentPos[0]][currentPos[1]] = 'D'
            #print_maze(maze, dim)
            print("Agent is on fire! :(")
            return False
        if(path): #There still lies a path to the goal node.
            currentPos = path[1]
            stepCounter = stepCounter + 1
            maze[currentPos[0]][currentPos[1]] = 'A'
            #print_maze(maze, dim)
            maze = advance_fire_one_step(maze, q)
        else:# There no longer lies a path to the goal node.
            #print_maze(maze, dim)
            #print("Agent can no longer proceed to the exit. :(")
            return False
    #print("Agent has successfully reached the goal in ", stepCounter, "steps! :)")
    return True
        
def strategy_three(maze, dim, q):
    maze = start_fire(maze)
    currentPos = [0,0]
    stepCounter = 0
    while (currentPos != [dim-1,dim-1]):
        print("Agent at position ", currentPos)
        print()
        path = Astar2(maze, currentPos, [dim-1, dim-1], dim)
        if(maze[currentPos[0]][currentPos[1]] == 'F'): #Agent has caught on fire.
            maze[currentPos[0]][currentPos[1]] = 'D'
            print_maze(maze, dim)
            print("Agent is on fire! :(")
            return False
        if(path): #There still lies a path to the goal node.
            currentPos = path[1]
            oldPos = path[0]
            if(check_fire(currentPos, maze) == True):
                x = oldPos[0]
                y = oldPos[1]
                if((x-1) >= 0 and (x-1) < len(maze)): 
                    if(check_fire([x-1,y], maze) == False and maze[x-1][y] == "O" and DFS(maze,[x-1,y] ,[dim-1, dim-1] , dim)): 
                        currentPos = [x-1,y]
                if((y-1) >= 0 and (y-1) < len(maze) ): 
                    if(check_fire([x,y-1], maze)== False and maze[x][y-1] == "O" and DFS(maze,[x,y-1] ,[dim-1, dim-1] , dim)):
                        currentPos = [x,y-1]
                if((y+1) >= 0 and (y+1) < len(maze)): 
                    if(check_fire([x,y+1], maze) == False and maze[x][y+1] == "O" and DFS(maze,[x,y+1] ,[dim-1, dim-1] , dim)): 
                        currentPos = [x,y+1]
                if((x+1) >= 0 and (x+1) < len(maze)): 
                    if(check_fire([x+1,y], maze) == False and maze[x+1][y] == "O" and DFS(maze,[x+1,y] ,[dim-1, dim-1] , dim)): 
                        currentPos = [x+1,y]
            stepCounter = stepCounter + 1
            maze[currentPos[0]][currentPos[1]] = 'A'
            print_maze(maze, dim)
            maze = advance_fire_one_step(maze, q)
        else: #There no longer lies a path to the goal node.
            print_maze(maze, dim)
            print("Agent can no longer proceed to the exit. :(")
            return False
    print("Agent has successfully reached the goal in ", stepCounter, "steps! :)")
    return True


def check_fire(prosition, maze):
    x = prosition[0]
    y = prosition[1]
    if((x+1) >= 0 and (x+1) < len(maze)): 
        if(maze[x+1][y] == 'F'): 
            return True
    if((x-1) >= 0 and (x-1) < len(maze)): 
        if(maze[x-1][y] == 'F'): 
            return True
    if((y+1) >= 0 and (y+1) < len(maze)): 
        if(maze[x][y+1] == 'F'): 
            return True
    if((y-1) >= 0 and (y-1) < len(maze)): 
        if(maze[x][y-1] == 'F'): 
            return True
    return False
    

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

def BFS(matrix, start_location, end_location, dim): # Uses BFS to determine the shortest path from one state to another
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
            print(roundCounter, "rounds of BFS were performed.")
            #print("Shortest path is: " , shortest_path)
            return shortest_path
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
    return []

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
            #print(roundCounter, "rounds of A* were performed.")
            #print("Shortest path is: " , path)
            return path
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
    #print("there lies no path to the goal node. " , roundCounter, " rounds of A* were performed.")
    return []



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
    p = float(input("Enter Probability (0 < p < 1) p: "))
    maze = create_maze(dim, p)
    #print_maze(maze, dim)
    
    ######################Strategy One Code#########################
    
    index = 0
    success = 0
    while(index < 1000):
        maze = create_maze(dim, p)
        if(DFS(maze, [0,0], [dim-1,dim-1], dim) == True):
            if(strategy_two(maze, dim, .3) == True):
                success = success + 1
            index = index + 1
    print(success, "TWO")
    
    print()
    
    index = 0
    success = 0
    while(index < 1000):
        maze = create_maze(dim, p)
        if(DFS(maze, [0,0], [dim-1,dim-1], dim) == True):
            if(strategy_three(maze, dim, .3) == True):
                success = success + 1
            index = index + 1
    print(success, "THREE")
    
 #########################Strategy three Code##############################
    """
    print("Strategy Three")
    print(strategy_three(maze, dim, .2))
    print()
    """
 #########################test fire code####################################
    """
    start_fire(maze)
    print()
    print("Fire!!")
    print()
    print_maze(maze, dim)
    #maze = advance_fire_one_step(maze, 1) #Check if advance_fire_one_step() function is working.
    #print_maze(maze, dim)
    """

    ########################## Data Collection Code ################################
    """
    AstarRounds = 0
    BFSRounds = 0          
    print()
    #print("DFS which determines if G can be reached from S")
    #print(DFS(maze, [0,0], [dim-1,dim-1], dim))
    rounds = int(input("Enter how many rounds of implementation you would like to perform: "))
    for i in range(0, rounds) :
        maze = create_maze(dim, p)
        print("ITERATION ROUND" , i+1)
        print()
        bfs_start_time = time.time()
        print("BFS: ")
        BFSRounds = BFSRounds + BFS(maze, [0,0], [dim-1,dim-1], dim)
        bfs_end_time = time.time()
        print("time taken: " , bfs_end_time - bfs_start_time , "seconds")
        print()
        astar_start_time = time.time()
        print("Astar: ")
        AstarRounds = AstarRounds + Astar2(maze, [0,0], [dim-1, dim-1], dim)
        astar_end_time = time.time()
        print("time taken: ", astar_end_time - astar_start_time , "seconds.")
        print()
    averageDiff = (BFSRounds - AstarRounds) / rounds
    print()
    print("Average difference of nodes explored between Astar and BFS: " , averageDiff)
    
    """
    ##############################################################################



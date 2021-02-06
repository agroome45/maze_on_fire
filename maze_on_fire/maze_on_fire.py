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

def Astar(matrix, start_location, end_location, dim):
    fringe = []
    closed = []
    fringe.append(start_location)
    distance = 0
    while( fringe ):
        print(fringe, "Fringe")
        current = fringe.pop(0)
        print(current, "current")
        x = current[0]
        y = current[1]
        if matrix[x][y] == 'G' :
            return True  #TODO return path instead of boolean
        else :
            if ((x+1) >= 0 and (x+1) < dim) :
                if(matrix[x+1][y] == "O" or matrix[x+1][y] == "G"):
                    if(closed.count([x+1,y]) == 0 and fringe.count([x+1,y]) == 0) :
                        fringe = sortedInsert(fringe, [x+1, y, distance + euclideanDistance([x+1, y] , end_location)])
            if ((x-1) >= 0 and (x-1) < dim) :
                if(matrix[x-1][y] == "O" or matrix[x-1][y] == "G"):
                    if(closed.count([x-1,y]) == 0 and fringe.count([x-1,y]) == 0) :
                        fringe = sortedInsert(fringe, [x-1, y, distance + euclideanDistance([x-1, y] , end_location)])                        
            if ((y+1) >= 0 and (y+1) < dim) :
                if(matrix[x][y+1] == "O" or matrix[x][y+1] == "G"):
                    if(closed.count([x,y+1]) == 0 and fringe.count([x,y+1]) == 0) :
                        fringe = sortedInsert(fringe, [x, y+1, distance + euclideanDistance([x, y+1] , end_location)])
            if ((y-1) >= 0 and (y-1) < dim) :
                if(matrix[x][y-1] == "O" or matrix[x][y-1] == "G"):
                    if(closed.count([x,y-1]) == 0 and fringe.count([x,y-1]) == 0) :
                        fringe = sortedInsert(fringe, [x, y-1, distance + euclideanDistance([x, y-1] , end_location)])
        distance = distance + 1
        closed.append([current])
    return False
    #TODO add inFringe list to assure no duplicates are placed in the fringe.

def sortedInsert(Alist, item) : #Helper function for Astar. 

    for i in range(len(Alist)) :
        if Alist[i][2] >= item[2] : #[2] is the distance from the start_location.
            retList = Alist[:i] + [item] + Alist[i:] 
            return retList
    Alist.append(item)
    return Alist

def euclideanDistance(start_point, end_point): #Function for euclidean metric heuristic
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
    print("Astar which determines the shortest path from S to G")
    print(Astar(maze, [0,0], [dim-1, dim-1], dim))
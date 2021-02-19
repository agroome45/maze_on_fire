import search_algo
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
    retMaze = copy.deepcopy(maze)
    while(1):
        randX = randint(0, len(maze)-1)
        randY = randint(0, len(maze)-1)
        if(maze[randX][randY] == 'O' or maze[randX][randY] == 'G' or maze[randX][randY] == 'S') : #Checks if randomly generated position is an open position.
            retMaze[randX][randY] = 'F'
            return retMaze

def advance_fire_one_step(maze, q): #advances fire once step using maze and probability q
    adjacentFires = 0
    retMaze = copy.deepcopy(maze)
    for x in range(0, len(maze)):
        for y in range(0, len(maze)):
            if (maze[x][y] == 'O' or maze[x][y] == 'G' or maze[x][y] == 'A'): #Checks if position is an open position.
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

def strategy_one(maze, dim, q, isPrint):
    path = search_algo.Astar2(maze, [0,0], [dim-1, dim-1], dim, True, False)
    if(path == []):
        return False
    for i in range(len(path)):
        Agent = path[i]
        x = Agent[0]
        y = Agent[1]
        if(maze[x][y] == "F"):
            if(isPrint):
                print("Step :", i)
                print_maze(maze, dim) 
            return False
        elif(maze[x][y] == "G"):
            if(isPrint):
                print("Step :", i)
                print_maze(maze, dim) 
            return True
        maze[x][y] = "A"
        if(isPrint):
            print("Step :", i)
            print_maze(maze, dim) #Can remove if maze is to big 
        maze = advance_fire_one_step(maze, q)
        
def strategy_two(maze, dim, q, isPrint):
    currentPos = [0,0]
    stepCounter = 0
    while (currentPos != [dim-1,dim-1]):
        if(isPrint):
            print("Agent at position ", currentPos)
            print()
        path = search_algo.Astar2(maze, currentPos, [dim-1, dim-1], dim, True, False)
        if(maze[currentPos[0]][currentPos[1]] == 'F'): #Agent has caught on fire.
            maze[currentPos[0]][currentPos[1]] = 'D'
            if(isPrint):
                print_maze(maze, dim)
                print("Agent is on fire! :(")
            return False
        if(path): #There still lies a path to the goal node.
            currentPos = path[1]
            stepCounter = stepCounter + 1
            maze[currentPos[0]][currentPos[1]] = 'A'
            if(isPrint):
                print_maze(maze, dim)
            maze = advance_fire_one_step(maze, q)
        else:# There no longer lies a path to the goal node.
            if(isPrint):
                print_maze(maze, dim)
                print("Agent can no longer proceed to the exit. :(")
            return False
    if(isPrint):
        print("Agent has successfully reached the goal in ", stepCounter, "steps! :)")
    return True
        
def strategy_three(maze, dim, q, isPrint): #tries to avoid positions that are reachable by the fire. Adjusts path when fire is reachable. Predicts
    currentPos = [0,0]
    stepCounter = 0
    while (currentPos != [dim-1,dim-1]):
        if(isPrint):
            print("Agent at position ", currentPos)
            print()
        path = search_algo.Astar2(maze, currentPos, [dim-1, dim-1], dim, True, False)
        if(maze[currentPos[0]][currentPos[1]] == 'F'): #Agent has caught on fire.
            maze[currentPos[0]][currentPos[1]] = 'D'
            if(isPrint):
                print_maze(maze, dim)
                print("Agent is on fire! :(")
            return False
        if(path): #There still lies a path to the goal node.
            currentPos = path[1]
            oldPos = path[0]
            if(check_fire(currentPos, maze) == True): # checks if the next current position is next to a fire
                x = oldPos[0]
                y = oldPos[1]
                if((x-1) >= 0 and (x-1) < len(maze)): # Checks if the following state is in the maze range 
                    if(check_fire([x-1,y], maze) == False and maze[x-1][y] == "O" and DFS(maze,[x-1,y] ,[dim-1, dim-1] , dim)): 
                        #^ Checks if adjacent position is next to a fire, open, and reachable to the goal position
                        currentPos = [x-1,y]# if so readjust current position
                if((y-1) >= 0 and (y-1) < len(maze) ): # Checks if the following state is in the maze range 
                    if(check_fire([x,y-1], maze)== False and maze[x][y-1] == "O" and DFS(maze,[x,y-1] ,[dim-1, dim-1] , dim)):
                        #^ Checks if adjacent position is next to a fire, open, and reachable to the goal position
                        currentPos = [x,y-1]# if so readjust current position
                if((y+1) >= 0 and (y+1) < len(maze)): # Checks if the following state is in the maze range 
                    if(check_fire([x,y+1], maze) == False and maze[x][y+1] == "O" and DFS(maze,[x,y+1] ,[dim-1, dim-1] , dim)): 
                        #^ Checks if adjacent position is next to a fire, open, and reachable to the goal position
                        currentPos = [x,y+1]# if so readjust current position
                if((x+1) >= 0 and (x+1) < len(maze)): # Checks if the following state is in the maze range 
                    if(check_fire([x+1,y], maze) == False and maze[x+1][y] == "O" and DFS(maze,[x+1,y] ,[dim-1, dim-1] , dim)): 
                        #^ Checks if adjacent position is next to a fire, open, and reachable to the goal position
                        currentPos = [x+1,y]# if so readjust current position
                #if all adjacent positions are next to fire than use original current position
            stepCounter = stepCounter + 1
            maze[currentPos[0]][currentPos[1]] = 'A'
            if(isPrint):
                print_maze(maze, dim)
            maze = advance_fire_one_step(maze, q)
        else: #There no longer lies a path to the goal node.
            if(isPrint):
                print_maze(maze, dim)
                print("Agent can no longer proceed to the exit. :(")
            return False
    if(isPrint):
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


# MAIN: Uncomment one section of code at a time!
if __name__ == "__main__" :

    dim = int(input("Enter Size dim: "))
    p = float(input("Enter Maze Probability (0 < p < 1) p: "))
    q = float(input("Enter Firespread Probability (0 < q < 1) q: "))
    wantsPrintS = input("Would you like to see the maze upon every step taken?\n(WARNING: DO NOT DO THIS FOR DATA COLLECTION OR BIG MAZES!)\ny/n : ")
    wantsPrintS.lower()
    if(wantsPrintS == 'y' or wantsPrintS == 'yes'):
        wantsPrint = True
    elif(wantsPrintS == 'n' or wantsPrintS == 'no'):
        wantsPrint = False
    else:
        print("I'm sorry, I don't think I understand. I'll assume you do not want the graph visuals because they are gross anyway. ", end="\n\n")
        wantsPrint = False
        
    

    ########################### Strategy One Test ###################################
    """
    maze = create_maze(dim, p)
    maze = start_fire(maze)
    print("Strategy One")
    print(strategy_one(maze, dim, q, wantsPrint))
    print()

    """
    ########################### Strategy Two Test ###################################
    """
    maze = create_maze(dim, p)
    maze = start_fire(maze)
    print("Strategy Two")
    strategy_two(maze, dim, q, wantsPrint)
    print()

    """
    ########################## Strategy Three Test ##################################
    """
    maze = create_maze(dim, p)
    maze = start_fire(maze)
    print("Strategy Three")
    print(strategy_three(maze, dim, q, wantsPrint))
    print()
    
    """
    ############################### Fire Test ########################################
    """
    maze = create_maze(dim, p)
    start_fire(maze)
    print()
    print_maze(maze, dim)
    print()
    print("Fire!!", end="\n\n")
    print_maze(maze, dim)
    print("Firespread!!", end="\n\n")
    maze = advance_fire_one_step(maze, 1) #Check if advance_fire_one_step() function is working.
    print_maze(maze, dim)
    
    """
    ####################### Data Collection Code Qs 1-4 ################################
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
        BFSRounds = BFSRounds + BFS(maze, [0,0], [dim-1,dim-1], dim, False, True)
        bfs_end_time = time.time()
        print("time taken: " , bfs_end_time - bfs_start_time , "seconds")
        print()
        astar_start_time = time.time()
        print("Astar: ")
        AstarRounds = AstarRounds + search_algo.Astar2(maze, [0,0], [dim-1, dim-1], dim, False, True)
        astar_end_time = time.time()
        print("time taken: ", astar_end_time - astar_start_time , "seconds.")
        print()
    averageDiff = (BFSRounds - AstarRounds) / rounds
    print()
    print("Average difference of nodes explored between Astar and BFS: " , averageDiff, end="\n\n")
    
    """
    ##################### Data Collection Code Qs 5-8 ##################################
    #"""
    rounds = int(input("Enter how many rounds of implementation you would like to perform: "))
    print()
    
    
    one_wins = 0
    two_wins = 0
    three_wins = 0
    index = 0
    while(rounds > index):
        maze = create_maze(dim, p)
        maze = start_fire(maze)
        if(search_algo.DFS(maze, [0,0], [dim-1,dim-1], dim) == True):
            maze_2 = copy.deepcopy(maze)
            maze_3 = copy.deepcopy(maze)
            print("ITERATION ROUND", index+1, end="\n\n")
            isWin = strategy_one(maze, dim, q, wantsPrint)
            if(isWin):
                print("Strategy one has gotten the agent through the maze!", end="\n\n")
                one_wins = one_wins + 1
            else:
                print("Strategy one has doomed the agent. :(", end="\n\n")
            isWin = strategy_two(maze_2, dim, q, wantsPrint)
            if(isWin):
                print("Strategy two has gotten the agent through the maze!" , end="\n\n")
                two_wins = two_wins + 1
            else:
                print("Strategy two has doomed the agent. :(", end="\n\n")
            isWin = strategy_three(maze_3, dim, q, wantsPrint)
            if(isWin):
                print("Strategy three has gotten the agent through the maze!" , end="\n\n")
                three_wins = three_wins + 1
            else:
                print("Strategy three has doomed the agent. :(", end="\n\n")
            index = index + 1
    print()
    one_success_rate = (one_wins / rounds) * 100
    two_success_rate = (two_wins / rounds) * 100
    three_success_rate = (three_wins / rounds) * 100
    print("Average Success Rate of Strategy One: " , one_success_rate, "%" , end="\n\n")
    print("Average Success Rate of Strategy Two: ", two_success_rate, "%" , end="\n\n")
    print("Average Success Rate of Strategy Three: ", three_success_rate, "%", end="\n\n")
      


    #"""
    #################################################################################







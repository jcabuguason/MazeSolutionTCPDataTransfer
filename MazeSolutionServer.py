
import pygame
import time
import random
import math
import random
import socket 

WIDTH = 800
HEIGHT = 800
FPS = 30
grid = []
visited = []
solVisited = []
availableSpaces = {}
solution = []

direction = {
    "N":[0,-1],
    "S":[0,1],
    "E":[1,0],
    "W":[-1,0],
}

n = 10
w = WIDTH/n
h = HEIGHT/n

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Grid")
clock = pygame.time.Clock()
white = [255, 255, 255]
black = [0,0,0]
screen.fill(white)
pygame.display.update()



def drawGrid(n):
    w = WIDTH/n
    h = HEIGHT/n
    x = 0.0
    y = 0.0
    for i in range(0,n):
        for j in range(0,n):
            pygame.draw.line(screen, black,[x,y],[x+w,y],2) # TOP
            pygame.draw.line(screen, black,[x, y], [x, y+h],2) # LEFT
            pygame.draw.line(screen, black,[x + w, y], [x + w, y + h],2) # RIGHT
            pygame.draw.line(screen, black,[x, y + h], [x+w, y + h],2) # BOTTOM
            grid.append([x,y])
            availableSpaces[(x,y)] = []
            x += w
        x = 0.0
        y += h
    print(len(grid))
    pygame.display.update()

def carveMazefrom(x,y,grid):
    if [x,y] in visited or [x,y] not in grid:
        return
    else:
        visited.append([x,y])


    dir_order = ["N","S","E","W"]
    random.shuffle(dir_order)

    for i in range(0,len(dir_order)):
        next_x = x + (direction.get(dir_order[i])[0])*w
        next_y = y + (direction.get(dir_order[i])[1])*h
        
        if [next_x, next_y] not in visited and [next_x, next_y] in grid:
            if dir_order[i] == "N":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["N"]
                pygame.draw.line(screen, white,[x,y],[x+w,y],2)
            if dir_order[i] == "S":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["S"]
                pygame.draw.line(screen, white,[x, y + h], [x+w, y + h],2) 
            if dir_order[i] == "E":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["E"]
                pygame.draw.line(screen, white,[x + w, y], [x + w, y + h],2) 
            if dir_order[i] == "W":
                availableSpaces[(x,y)] = availableSpaces.get((x,y)) + ["W"]
                pygame.draw.line(screen, white,[x, y], [x, y+h],2)
            pygame.display.update()
            #time.sleep(0.05) # Comment This If You Dont Want To Wait For Maze To Generate
            carveMazefrom(next_x,next_y,grid)
        
def solveMaze (x,y,aSpaces,grid,currentPath):
    if ((x,y) in currentPath):
        return
    currentPath.append((x,y))

    if (x,y) == (WIDTH-w,HEIGHT-h):
        solution[:] = list(currentPath)
        currentPath.pop()
        return

    for i in range(0,len(aSpaces.get((x,y)))):
        next_x = x + (direction.get(aSpaces.get((x,y))[i])[0])*w
        next_y = y + (direction.get(aSpaces.get((x,y))[i])[1])*h
        if aSpaces.get((x,y))[i] == "N":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "S":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "E":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
        if aSpaces.get((x,y))[i] == "W":
            solveMaze(next_x,next_y,aSpaces,grid,currentPath)
    currentPath.pop()
    return

drawGrid(n)
carveMazefrom(0,0,grid)
solveMaze(0,0,availableSpaces,grid,[])
for i in solution:
    pygame.draw.circle(screen, [255,0,0],[ i[0]+(w/2) , i[1]+(h/2)],10)
    pygame.display.update()
    #time.sleep(0.05) # Comment This If You Dont Want To Wait For Solution To Generate

# Write your code here or make a new python file and run the code from here
# The array that contains the solution is called solution[], use this for the TCP Stream.



#display the solution array for reference
for i in solution:
    print(str(i[0])+"\t"+str(i[1]));

#convert the string to motor input

motorInput = []

#starting position is down, check if robot is moving down or to the right
#if going down no need to rotate robot at the start if going right rotate left
if(solution[0][0]+80 == solution[1][0]):
    motorInput.append("[255][0][0][255]")

prevChangeInX = 0
prevChangeInY = 0

for i in range(len(solution)):    

    if i+1 >= len(solution):
        break

    #variables to make code easier to read
    currentX = solution[i][0]
    currentY = solution[i][1]
    nextX = solution[i+1][0]
    nextY = solution[i+1][1]
    
    #if change in position move forward
    if (abs(currentX-nextX) == 80) or (abs(currentY-nextY) == 80 ):
        #move forward
        motorInput.append("[255][255][0][0]")

    #skip first iteration as no rotation needed
    if i == 0:
        continue;

    #variables to make code easier to read
    previousX = solution[i-1][0]
    previousY = solution[i-1][1]
    prevChangeInX = currentX-previousX
    prevChangeInY = currentY-previousY
    nextChangeInX = nextX - currentX 
    nextChangeInY = nextY - currentY

    #rotate right
    if (nextChangeInY == 80 and prevChangeInX == 80) or (nextChangeInX == -80 and prevChangeInY == 80) or (nextChangeInX == 80 and prevChangeInY == -80) or (nextChangeInY == -80 and prevChangeInX == -80):
        motorInput.append("[0][255][255][0]")
    #rotate left
    if (nextChangeInX == 80 and prevChangeInY == 80) or (nextChangeInX == -80 and prevChangeInY == -80) or (nextChangeInY == -80 and prevChangeInX == 80) or (nextChangeInY == 80 and prevChangeInX == -80):
        motorInput.append("[255][0][0][255]")

#forward one last time to get robot to destination 
motorInput.append("[255][255][0][0]")
motorInput.append("[0][0][0][0]")

#listen on the server
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("localhost",80))
s.listen(5)

while True:
    clientsocket, address = s.accept()
    print("Connnection from "+ str(address)+" has been established!")
    for i in motorInput:
        clientsocket.send(bytes(str(i),"utf-8"))
    clientsocket.close()

running = True 
while running:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


import pygame
import numpy as np
import time
pygame.init()

# Define some colors
GRID = (155,155,155)
DEATH = (70,70,70)
ALIVE = (222,222,222)

# Define element sizes
winSize = (1200,800)
cellSize = 25
dimX = int(winSize[0]/cellSize)
dimY = int(winSize[1]/cellSize)

#Get the number of neighbors alive surrounding the y,x position
def neighborsAlive(matrix:np.array, y:int, x:int) -> int:
    lenY = np.size(matrix,0)
    lenX = np.size(matrix,1)
    alive = matrix[y-1][x-1] + matrix[y-1][x] + matrix[y-1][(x+1)%lenX]
    alive += matrix[y][x-1] + matrix[y][(x+1)%lenX]
    alive += matrix[(y+1)%lenY][x-1] + matrix[(y+1)%lenY][x] + matrix[(y+1)%lenY][(x+1)%lenX]
    return alive

#Get the next matrix state
def getNextMatrix(matrix:np.array) -> np.array:
    lenY = np.size(matrix,0)
    lenX = np.size(matrix,1)
    nextMatrix = np.zeros([lenY,lenX],dtype = int)

    for y in range(lenY):
        for x in range(lenX):
            nAlive = neighborsAlive(matrix,y,x)
            if matrix[y][x] == 0 and nAlive == 3:
                nextMatrix[y][x] = 1
            if matrix[y][x] == 1 and (nAlive == 2 or nAlive == 3):
                nextMatrix[y][x] = 1
    return nextMatrix

def drawMatrix(screen:pygame.Surface,matrix:np.array):
    for y in range(dimY):
        for x in range(dimX):
            if matrix[y][x] == 1:
                pygame.draw.rect(screen, ALIVE, [x*cellSize,y*cellSize,cellSize,cellSize])

def drawGrid(screen:pygame.Surface):
    pygame.draw.rect(screen,GRID,[0,0,winSize[0],winSize[1]],1)
    for x in range(dimX):
        pygame.draw.line(screen, GRID, [x*cellSize,0],[x*cellSize,winSize[1]])
    for y in range(dimY):
        pygame.draw.line(screen, GRID, [0,y*cellSize],[winSize[0],y*cellSize])

def main():
    screen = pygame.display.set_mode(winSize)
    pygame.display.set_caption("Game of Life")
    carryOn = True
    runGame = False
    clock = pygame.time.Clock()

    # Initial Matrix
    globalMatrix = np.zeros([dimY,dimX],dtype = int)
    globalMatrix[16][4] = 1
    globalMatrix[16][5] = 1
    globalMatrix[16][6] = 1
    globalMatrix[14][4] = 1
    globalMatrix[14][6] = 1

    globalMatrix[0][30] = 1
    globalMatrix[2][30] = 1
    globalMatrix[1][31] = 1
    globalMatrix[2][31] = 1
    globalMatrix[2][29] = 1
    
    screen.fill(DEATH)
    drawGrid(screen)

    while carryOn:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                carryOn = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                runGame = not runGame
            if event.type == pygame.MOUSEBUTTONUP and runGame == False:
                print(pygame.mouse.get_pos())
        
        if runGame:
            curMatrix = getNextMatrix(globalMatrix)
            globalMatrix = curMatrix

            screen.fill(DEATH)
            drawMatrix(screen,curMatrix)
            drawGrid(screen)
            time.sleep(0.1)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
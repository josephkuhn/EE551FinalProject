import pygame
import random

pygame.init()

totalWidth = 600
totalHeight = 600

arenaWidth = 200
arenaHeight = 400
tetrominoSize = 20

initialX = (totalWidth - arenaWidth) / 2
initialY = totalHeight - arenaHeight
#used later for placement purposes

O = [['.....',
'.....',
'.xx...',
'.xx..',
'.....']]

I = [['..x..',
'..x..',
'..x..',
'..x..',
'.....'],
['.....',
'xxxx.',
'.....',
'.....',
'.....']]

S = [['.....',
'.....',
'..xx.',
'.xx..',
'.....'],
['.....',
'..x..',
'..xx.',
'...x.',
'.....']]

Z = [['.....',
'.....',
'.xx..',
'..xx.',
'.....'],
['.....',
'..x..',
'.xx..',
'.x...',
'.....']]

J = [['.....',
'..x..',
'..x..',
'.xx..',
'.....'],
['.....',
'.x...',
'.xxx.',
'.....',
'.....'],
['.....',
'..xx.',
'..x..',
'..x..',
'.....'],
['.....',
'.xxx.',
'...x.',
'.....',
'.....']]

L = [['.....',
'..x..',
'..x..',
'..xx.',
'.....'],
['.....',
'.....',
'.xxx.',
'.x...',
'.....'],
['.....',
'.xx..',
'..x..',
'..x..',
'.....'],
['.....',
'...x.',
'.xxx.',
'.....',
'.....']]

T = [['.....',
'..x..',
'.xxx.',
'.....',
'.....'],
['.....',
'..x..',
'..xx.',
'..x..',
'.....'],
['.....',
'.....',
'.xxx.',
'..x..',
'.....'],
['.....',
'..x..',
'.xx..',
'..x..',
'.....']]

tetrominoesList = [O, I, S, Z, J, L, T]
colors = [(255, 255, 0), (0, 255, 255), (0, 255, 0), (255, 0, 0), (255, 128, 0), (0, 0, 255), (128, 0, 255)]

class tetromino:
    def __init__(self, x, y, tetromino):
        self.x = x
        self.y = y
        self.tetromino = tetromino
        self.color = colors[tetrominoesList.index(tetromino)]
        self.rotation = 0

def createGrid(finalPos = {}):
    grid = [[(0, 0, 0) for x in range(10)]for x in range(20)]

    for a in range(len(grid)):
        for b in range(len(grid)):
            if (b, a) in finalPos:
                c = finalPos[(b, a)]
                grid[a][b] = c
    return grid

def drawGrid(surface, grid):
    for x in range(len(grid)):
        pygame.draw.line(surface, (128, 128, 128), (initialX, initialY + x * tetrominoSize), (initialX + arenaWidth, initialY + x * tetrominoSize))
        for y in range(len(grid[x])):
            pygame.draw.line(surface, (128, 128, 128), (initialX + y * tetrominoSize, initialY), (initialX + y * tetrominoSize, initialY + arenaHeight))

def drawWindow(instance, grid, score=0):
    instance.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('arial', 75)
    label = font.render('Tetris', 1, (255, 255, 255))
    instance.blit(label, (initialX + arenaWidth / 2 - (label.get_width() / 2), 30))

    font = pygame.font.SysFont('impact', 30)
    scoreText = font.render('Score: ' + str(score), 1, (255, 255, 255))

    newX = 2 * initialX / 7
    newY = totalHeight / 6

    instance.blit(scoreText, (newX, newY))

    for x in range(len(grid)):
        for y in range(len(grid[x])):
            pygame.draw.rect(instance, grid[x][y], (initialX + y * tetrominoSize, initialY + x * tetrominoSize, tetrominoSize, tetrominoSize), 0)

    pygame.draw.rect(instance, (0, 255, 255), (initialX, initialY, arenaWidth, arenaHeight), 3)

    drawGrid(instance, grid)

def drawNextShape(tetromino, instance):
    font = pygame.font.SysFont('arial', 30)
    label = font.render('Next Shape:', 1, (255, 255, 255))

    newX = totalWidth - 4 * initialX / 5
    newY = totalHeight / 6
    orient = tetromino.tetromino[tetromino.rotation % len(tetromino.tetromino)]

    for a, line in enumerate(orient):
        row = list(line)
        for b, column in enumerate(row):
            if column == 'x':
                pygame.draw.rect(instance, tetromino.color, (newX + 15 + b * tetrominoSize, newY + 30 + a * tetrominoSize, tetrominoSize, tetrominoSize), 0)
    instance.blit(label, (newX, newY))

def drawNextShape2(tetromino, instance):
    newX = totalWidth - 4 * initialX / 5
    newY = totalHeight / 6
    orient =  tetromino.tetromino[tetromino.rotation % len(tetromino.tetromino)]
    for a, line in enumerate(orient):
        row = list(line)
        for b, column in enumerate(row):
            if column == 'x':
                pygame.draw.rect(instance, tetromino.color, (newX + 15 + b * tetrominoSize, newY + 150 + a * tetrominoSize, tetrominoSize, tetrominoSize), 0)

def drawTextInMiddle(text, size, color, surface):
    font = pygame.font.SysFont("arial", size)
    label = font.render(text, 1, color)
    surface.blit(label, (initialX + arenaWidth / 2 - (label.get_width() / 2), totalHeight / 2 - label.get_height() / 2))

def getShape():
    return tetromino(5, 0, random.choice(tetrominoesList))

def convertTetromino(tetromino):
    positions = []
    orient = tetromino.tetromino[tetromino.rotation % len(tetromino.tetromino)]

    for a, line in enumerate(orient):
        row = list(line)
        for b, column in enumerate(row):
            if column == 'x':
                positions.append((tetromino.x + b, tetromino.y + a))

    for a, position in enumerate(positions):
        positions[a] = (position[0] - 2, position[1] - 4)

    return positions

def validSpace(tetromino, grid):
    validPos = [[(j, i) for j in range(10) if grid[i][j] == (0, 0, 0)] for i in range(20)]
    validPos = [j for sub in validPos for j in sub]

    converted = convertTetromino(tetromino)

    for pos in converted:
        if pos not in validPos:
            if pos[1] > -1:
                return False
    return True

def clearRow(grid, finalPos):
    num = 0
    for a in range(len(grid) - 1, -1, -1):
        row = grid[a]
        # check if the row is completely filled
        if (0, 0, 0) not in row:
            num += 1
            index = a
            for b in range(len(row)):
                try:
                    del finalPos[(b, a)]
                except:
                    continue
    #sort through from the bottom up
    if num > 0:
        for key in sorted(list(finalPos), key = lambda x: x[1])[::-1]:
            x, y = key
            if y < index:
                newKey = (x, y + num)
                finalPos[newKey] = finalPos.pop(key)
    return num

def checkEndGame(positions):
    for position in positions:
        x, y = position
        if y < 1:
            return True
    return False

def endGame(surface, score):
    pygame.draw.rect(win, (0, 0, 0), (0, 0, totalWidth, totalHeight), 0)
    font = pygame.font.SysFont("arial", 80)
    label = font.render("GAME OVER", 1, (255, 255, 255))
    surface.blit(label, (initialX + arenaWidth / 2 - (label.get_width() / 2), totalHeight / 3 - label.get_height() / 2))

    font = pygame.font.SysFont("arial", 40)
    label = font.render("Final Score: " + str(score), 1, (255, 255, 255))
    surface.blit(label, (initialX + arenaWidth / 2 - (label.get_width() / 2), totalHeight / 2 - label.get_height() / 2))

    font = pygame.font.SysFont("arial", 30)
    label = font.render("Press the space bar to go to the menu", 1, (255, 255, 255))
    surface.blit(label, (initialX + arenaWidth / 2 - (label.get_width() / 2), 2* totalHeight / 3 - label.get_height() / 2))

def testScore(prevScore, score, numRows):
    scoreTest1 = 10
    scoreTest2 = 30
    scoreTest3 = 60
    scoreTest4 = 100
    if numRows == 1:
        assert(prevScore + scoreTest1 == score)
        print("Clearing one row worked successfully.")
    if numRows == 2:
        assert(prevScore + scoreTest2 == score)
        print("Clearing two rows worked successfully.")
    if numRows == 3:
        assert(prevScore + scoreTest3 == score)
        print("Clearing three rows worked successfully.")
    if numRows == 4:
        assert(prevScore + scoreTest4 == score)
        print("Clearing four rows worked successfully.")

def testSpeed(initialFallSpeed, fallSpeed, speedUpCount):
    assert ((round((initialFallSpeed - speedUpCount) * 100) / 100.00) == fallSpeed)
    print("The fall speed is successfully increasing every 10 seconds.")
    if (speedUpCount * 100 == 1):
        print("The speed has increased " + str(int(speedUpCount * 100)) + " time.")
    else:
        print("The speed has increased " + str(int(speedUpCount * 100)) + " times.")

def testValidSpace(locationTest, currentLocation):
    assert (locationTest == currentLocation)
    return True

def main(win):
    finalPos = {}

    changePiece = False
    run = True
    currentPiece = getShape()
    nextPiece = getShape()
    nextPiece2 = getShape()
    clock = pygame.time.Clock()
    fallTime = 0
    fallSpeed = 0.30
    initialFallSpeed = fallSpeed
    speedUpCount = 0
    levelTime = 0
    score = 0
    prevScore = 0
    pygame.mixer.init()
    pygame.mixer.music.load('tetris.wav')
    pygame.mixer.music.play(-1)

    while run:
        grid = createGrid(finalPos)
        fallTime += clock.get_rawtime()
        levelTime += clock.get_rawtime()
        clock.tick()

        if levelTime / 1000 > 10:
            levelTime = 0
            if fallSpeed > 0.13:
                fallSpeed = round((fallSpeed - 0.01) * 100) / 100
                speedUpCount += round(.01 * 100) / 100
                testSpeed(initialFallSpeed, fallSpeed, speedUpCount)

        if fallTime / 1000 > fallSpeed:
            fallTime = 0
            currentPiece.y += 1
            if not validSpace(currentPiece, grid) and currentPiece.y > 0:
                currentPiece.y -= 1
                changePiece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    locationTest = currentPiece.x
                    currentPiece.x -= 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.x += 1
                        if testValidSpace(locationTest, currentPiece.x):
                            print("The piece was successfully stopped from moving more to the left.")
                if event.key == pygame.K_RIGHT:
                    locationTest = currentPiece.x
                    currentPiece.x += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.x -= 1
                        if testValidSpace(locationTest, currentPiece.x):
                            print("The piece was successfully stopped from moving more to the right.")
                if event.key == pygame.K_DOWN:
                    #pygame.key.set_repeat(50, 50)
                    locationTest = currentPiece.x
                    currentPiece.y += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.y -= 1
                        if testValidSpace(locationTest, currentPiece.x):
                            print("The piece was successfully stopped from moving down more.")
                if event.key == pygame.K_UP:
                    locationTest = currentPiece.rotation
                    currentPiece.rotation += 1
                    if not(validSpace(currentPiece, grid)):
                        currentPiece.rotation -= 1
                        if testValidSpace(locationTest, currentPiece.rotation):
                            print("The piece was successfully stopped from rotating again.")

        shapePos = convertTetromino(currentPiece)

        for i in range(len(shapePos)):
            x, y = shapePos[i]
            if y > -1:
                grid[y][x] = currentPiece.color

        if changePiece:
            for pos in shapePos:
                p = (pos[0], pos[1])
                finalPos[p] = currentPiece.color
            currentPiece = nextPiece
            nextPiece = nextPiece2
            nextPiece2 = getShape()
            changePiece = False
            numRows = clearRow(grid, finalPos)
            if numRows == 1:
                score += 10
            elif numRows == 2:
                score += 30
            elif numRows == 3:
                score += 60
            elif numRows == 4:
                score += 100
            testScore(prevScore, score, numRows)
            if numRows == 1:
                prevScore += 10
            elif numRows == 2:
                prevScore += 30
            elif numRows == 3:
                prevScore += 60
            elif numRows == 4:
                prevScore += 100

        drawWindow(win, grid, score)
        drawNextShape(nextPiece, win)
        drawNextShape2(nextPiece2, win)
        pygame.display.update()

        if checkEndGame(finalPos):
            endGame(win, score)
            pygame.display.update()
            run = False

    space = False
    while not space:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    space = True

def mainMenu(win):
    run = True
    while run:
        win.fill((0, 0, 0))
        drawTextInMiddle('Press the space bar to play', 50, (255, 255, 255), win)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    main(win)

win = pygame.display.set_mode((totalWidth, totalHeight))
pygame.display.set_caption("Tetris by Joey Kuhn")
mainMenu(win)
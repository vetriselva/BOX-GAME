import pygame, sys ,random
from pygame.locals import *

WINDOWWIDTH = 640 #window width size
WINDOWHEIGHT = 540 #window height size
CIRCLERADIUS = 6 #point cicle radious
CIRCLEDISTANCE = 50  #distance between two circles
BOXWIDTHPOINT = 4#int(input('Enter number of row values less then 8 : '))#number of x axis point
BOXHEIGHTPOINT = 4#int(input('Enter number of column values less then 8 : ')) #number of y axis point
BOXSIZE = 10
#find margin of x and y
XMARGIN = int((WINDOWWIDTH - (BOXWIDTHPOINT * (CIRCLERADIUS+CIRCLEDISTANCE)))/2)
YMARGIN = int((WINDOWWIDTH - (BOXHEIGHTPOINT * (CIRCLERADIUS+CIRCLEDISTANCE)))/2)

# #color
MYDICT =  []
MYDICT1 = []
MYDICT2 = []
MYDICT3 = []
MYDICT4 = []


m = 1
#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
HIGHLIGHTCOLOR = (255,255,255)
FPS = 30
RECT = []
ALLCOLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN,NAVYBLUE,GRAY)

def getRandomizedBoard():
    icons = []
    for color in ALLCOLORS:
        icons.append((color))
    random.shuffle(icons) # randomize the order of the icons list
    numIconsUsed = int(BOXWIDTHPOINT * BOXHEIGHTPOINT / 2) # calculate how many icons are needed
    icons = icons[:numIconsUsed] *BOXWIDTHPOINT  # make two of each
    random.shuffle(icons)
    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOXWIDTHPOINT):
        column = []
        for y in range(BOXHEIGHTPOINT):
            column.append(icons[0])
            del icons[0] # remove the icons as we assign them
        board.append(column)
    
    return board
def Reverse(lst): 
    return [ele for ele in reversed(lst)] 

def generateRevealedBoxesData(val):
    revealedBoxes = []
    for i in range(BOXWIDTHPOINT):
        revealedBoxes.append([val] * BOXHEIGHTPOINT)
   
    return revealedBoxes

def drawBoard(board, revealed, data = '',revealedBoxes=''):
    # Draws all of the boxes in their covered or revealed state.
    
    for boxx in range(BOXWIDTHPOINT):
        for boxy in range(BOXHEIGHTPOINT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            if (revealed[boxx][boxy] !=1 and  revealed[boxx][boxy] != 2) :
                # Draw a covered box.
                pygame.draw.circle(DISPLAYSURF,board[boxx][boxy] ,(left, top),CIRCLERADIUS)
            else:
                left,top = getCoordPos(boxx, boxy)
                pygame.draw.circle(DISPLAYSURF,board[boxx][boxy] ,(left, top),CIRCLERADIUS)
                
                if len(data)>=1:
                    
                    revealedBoxes[boxx][boxy] = 2 
                    
                    drawLine(data,revealedBoxes)
                
                         
def getCoordPos(boxx, boxy):
    
    left, top = leftTopCoordsOfBox(boxx, boxy)
    
    return left,top
    
def drawLine(linePoints, revealedBoxes=''):
    count = 1
    
    for i in range(0,len(linePoints)):
        secondPointx = linePoints[i][1][0]
        secondPointy = linePoints[i][1][1]
        x1, y1 = leftTopCoordsOfBox(linePoints[i][0][0],linePoints[i][0][1])
        x2, y2 = leftTopCoordsOfBox(secondPointx,secondPointy)
        fourRect = coorRect(secondPointx,secondPointy)
        if(i%2 == 0):
            if(len(MYDICT1) == 0):
                MYDICT1.append((secondPointx,secondPointy))
            else:
                fun(MYDICT1,(secondPointx,secondPointy))
            pygame.draw.line(DISPLAYSURF,RED,(x1,y1),(x2,y2),3)
        elif(i%2 == 1):
            if(len(MYDICT2) == 0):
                MYDICT2.append((secondPointx,secondPointy))
            else:
                fun(MYDICT2,(secondPointx,secondPointy))
            pygame.draw.line(DISPLAYSURF,GREEN,(x1,y1),(x2,y2),3)
        for row in range(0,len(fourRect)):
            match = set(linePoints)&set(fourRect[row]) 
            if len(match) == 4:
                if(len(MYDICT4) ==0):
                    MYDICT4.append((fourRect[row][0][0][0],fourRect[row][0][0][1]))
                    MYDICT.append(i) 
                else:
                    count = len(MYDICT4)
                    fun(MYDICT4,(fourRect[row][0][0][0],fourRect[row][0][0][1]))
                    if (count != len(MYDICT4)):
                        play1 = (set(set(MYDICT4)&set(MYDICT1))&(set(set(MYDICT4)&set(MYDICT2))))
                        play2 = (set(set(MYDICT4)&set(MYDICT2))&(set(set(MYDICT4)&set(MYDICT1))))
#                         print('player1',play1)
#                         print('player2',play2)
                        MYDICT.append(i) 
                pointData= tuple(match)
                pointx,pointy = leftTopCoordsOfBox(fourRect[row][0][0][0],fourRect[row][0][0][1])
                pygame.draw.rect(DISPLAYSURF,(66, 135, 245),(pointx,pointy,50,50))
#                 if(len(MYDICT3) == 0):
#                     MYDICT3.append((fourRect[row][0][0][0],fourRect[row][0][0][1]))
#                 else:
#                     fun(MYDICT3,(fourRect[row][0][0][0],fourRect[row][0][0][1]))
def coorRect(a,b):
    a1,b1 = (a, b+1)
    a2,b2 = (a+1,b+1)
    a3,b3 = (a+1,b)

    rect1 = [((a,b),(a1,b1)),((a1,b1),(a2,b2)),
             ((a2,b2),(a3,b3)),((a3,b3),(a,b)),
             ((a1,b1),(a,b)),((a2,b2),(a1,b1)),
             ((a3,b3),(a2,b2)),((a,b),(a3,b3))
    ]

    a4,b4 = (a-1,b)
    a5,b5 = (a-1,b+1)
    
    rect2 = [
                ((a4,b4),(a,b)),((a5,b5),(a1,b1)),
                ((a1,b1),(a,b)),((a,b),(a4,b4)),
                ((a5,b5),(a4,b4)),((a1,b1),(a5,b5)),
                ((a,b),(a1,b1)),((a4,b4),(a5,b5))
    ]
#     rect2Rev = Reverse(rect2)
    a6,b6 = (a,b-1) 
    a7,b7 = (a+1,b-1)
    
    rect3 = [
                ((a6,b6),(a,b)),((a,b),(a3,b3)),
                ((a3,b3),(a7,b7)),((a7,b7),(a6,b6)),
                ((a,b),(a6,b6)),((a3,b3),(a,b)),
                ((a7,b7),(a3,b3)),((a6,b6),(a7,b7))
    ]
#     rect3Rev = Reverse(rect3)
    a8,b8 = (a-1,b-1)
    
    rect4 = [
                ((a8,b8),(a6,b6)),((a6,b6),(a,b)),
                ((a,b),(a4,b4)),((a4,b4),(a8,b8)),
                ((a6,b6),(a8,b8)),((a,b),(a6,b6)),
                ((a4,b4),(a,b)),((a8,b8),(a4,b4))
    ]

    return [
        rect1 ,rect2,rect3,rect4

    ]

def fun(array,i):
    
    a = set(array)&set([i])

    if len(a)==0:
        array.append(i)
        return array
def leftTopCoordsOfBox(boxx, boxy):
    # Convert board coordinates to pixel coordinates
    left = boxx * (CIRCLEDISTANCE + CIRCLERADIUS) + XMARGIN
    top = boxy * (CIRCLEDISTANCE + CIRCLERADIUS) + YMARGIN
    return (left, top)


def getBoxAtPixel(x, y):
    for boxx in range(BOXWIDTHPOINT):
        for boxy in range(BOXHEIGHTPOINT):
            left, top = leftTopCoordsOfBox(boxx, boxy)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)

def drawHighlightBox(boxx, boxy):
    left, top = leftTopCoordsOfBox(boxx, boxy)
    pygame.draw.rect(DISPLAYSURF, HIGHLIGHTCOLOR, (left - 12, top - 12, BOXSIZE + 12, BOXSIZE + 12), 2)
def checkFullFill(x,y):
    row = x - 1
    col = y - 1
    numRect = int((row*col)*4)
    rowCommon = x - 2
    colCommon = y - 2
    comRowCol = int((rowCommon*row)+(colCommon*col))
    totalLine = numRect - comRowCol
    return totalLine
def hasWon(revealedBoxes):
    # Returns True if all the boxes have been revealed, otherwise False
    for i in revealedBoxes:
        
        if 0 in i or 1 in i:
            return False # return False if any boxes are covered.
    return True
# get the last key. 
def last(n): 
    return n[m]      
def sort(tuples): 
  
    return sorted(tuples, key = last) 
def plyerCount(array,player):
    count = 0

    for num in array: 
        if player ==1:
            if num % 2 == 0: 
                count += 1

        elif player == 2: 
            if num % 2 == 1: 
                count += 1
            
        
    return count
    
  def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
#     pygame.mixer.music.load('sound/piano.mp3')
#     pygame.mixer.music.play(-1)
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    mousex = 0 # used to store x coordinate of mouse event
    mousey = 0 # used to store y coordinate of mouse event
    pygame.display.set_caption('Box Game')

    mainBoard = getRandomizedBoard()
    revealedBoxes = generateRevealedBoxesData(0)
    
    firstSelection = None # stores the (x, y) of the first box clicked.
    
    DISPLAYSURF.fill((0,0,0))
    selectionValue = []
    
#     startGameAnimation(mainBoard)
    data = []
    xyvalue = []
    
    while True: # main game loop
        mouseClicked = False
        
   
        font = pygame.font.Font('freesansbold.ttf', 20) 
        plyPoint1 = len(set(MYDICT4)&set(MYDICT1)) 
        plyPoint2 = len(set(MYDICT4)&set(MYDICT2))
#         plyPoint1 = plyerCount(MYDICT,1)
#         plyPoint2 = plyerCount(MYDICT,2)
        plyPoint3 = len(MYDICT4)
        text = font.render('player 1:'+ str(plyPoint1), True, GREEN) 
        text1 = font.render('player2:'+str(plyPoint2), True, GREEN) 
        text2 = font.render('Nothing:'+str(plyPoint3), True, GREEN) 
        text3 = font.render('Nothing:'+str(MYDICT), True, GREEN) 

        textRect = text.get_rect()  
        textRect1 = text1.get_rect()
        textRect2 = text2.get_rect()
        textRect3 = text3.get_rect()

        textRect.center = (500, 40) 
        textRect1.center = (500,70)
        textRect2.center = (500,90)
        textRect3.center = (500,100)
        DISPLAYSURF.fill((0,0,0)) # drawing the window
        drawBoard(mainBoard, revealedBoxes,selectionValue, revealedBoxes)
        DISPLAYSURF.blit(text, textRect) 
        DISPLAYSURF.blit(text1, textRect1) 
#         DISPLAYSURF.blit(text2, textRect2)
#         DISPLAYSURF.blit(text3, textRect3)
        for event in pygame.event.get(): # event handling loop
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
                
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
            
#                 print(mousex, mousey)
        boxx, boxy = getBoxAtPixel(mousex, mousey)
        
        if boxx != None and boxy != None:
            drawHighlightBox(boxx, boxy)
            if mouseClicked:
                revealedBoxes[boxx][boxy] = 1# set the box as "revealed"
                if firstSelection == None: # the current box was the first box clicked
                    firstSelection = (boxx, boxy)
                else:
                    if (firstSelection[0], firstSelection[1])  != (boxx, boxy):
                        selectionValue.append(((firstSelection[0], firstSelection[1]),(boxx, boxy)))
                        firstSelection = None
            
        drawBoard(mainBoard, revealedBoxes,selectionValue,revealedBoxes)
#         MYDICT1.clear()
#         MYDICT2.clear()
#         MYDICT3.clear()
        tatal_line = checkFullFill(BOXWIDTHPOINT,BOXHEIGHTPOINT)
       
        if(len(selectionValue) == tatal_line):
            if hasWon(revealedBoxes): #check all the point clicked
                font = pygame.font.Font('freesansbold.ttf', 30) 
                if len(MYDICT1) > len(MYDICT2):
                    text2 = font.render('player 1 win', True, GREEN) 
                elif len(MYDICT1) < len(MYDICT2):
                    text2 = font.render('player 2 win', True, GREEN) 
                else:
                     text2 = font.render('Match Draw', True, GREEN) 

                textRect2 = text2.get_rect()   
                textRect2.center = (300, 300) 
                DISPLAYSURF.blit(text2,textRect2)
                MYDICT1.clear()
                MYDICT2.clear()
                MYDICT3.clear()
                pygame.display.update()
                pygame.time.wait(10000)
                # Reset the board
                main()
        # Redraw the screen and wait a clock tick.
        pygame.display.update()
        FPSCLOCK.tick(FPS)
       

if __name__ == '__main__':
    main()


import pygame, random, sys
from pygame.locals import *
import board

FPS = 30    #Framerate of the program
WINDOW_WIDTH = 640  #Pixel width of the window
WINDOW_HEIGHT = 480     #Pixel heigth of the window

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

BGCOLOR = NAVYBLUE
LIGHTBGCOLOR = GRAY
BOXCOLOR = WHITE
HIGHLIGHTCOLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)



def main():

    global DISPLAY_SURF, FPS_CLOCK
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    FPS_CLOCK = pygame.time.Clock()
    pygame.display.set_caption('Memory Game')
    DISPLAY_SURF.fill(BGCOLOR)

    #Store the x and y coordinates of the mouse
    mousex = 0
    mousey = 0

    b = board.Board(DISPLAY_SURF, FPS_CLOCK)

    main_board = b.getRandomizedBoard()
    revealed_boxes = b.generateRevealedBoxesData(False)
    first_selection = None  #Store the coordinate of the first tile chosen

    b.startGameAnimation()

    #Main game loop
    while True:
        mouse_clicked = False   #Check whether mouse has been clicked

        DISPLAY_SURF.fill(BGCOLOR)
        b.drawBoard(revealed_boxes)

        for event in pygame.event.get():
            #Close the game
            if event.type == pygame.QUIT or (event.type==KEYUP and event.type==K_ESCAPE):
                pygame.quit()
                sys.exit()
            #If mouse moved
            if event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            #If mouse was held down earlier and now released
            if event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouse_clicked = True

        #Returns the coordinates of the box where the mouse is currently at
        boxx, boxy = b.getBoxAtPixel(mousex, mousey)
        if boxx!=None and boxy!=None:
            #If the box is currently hidden, then highlight it
            if not revealed_boxes[boxx][boxy]:
                b.drawHighlightBox(boxx, boxy)

            #If mouse is clicked on the box, reveal box
            if not revealed_boxes[boxx][boxy] and mouse_clicked == True:
                b.revealBoxesAnimation([(boxx, boxy)])
                revealed_boxes[boxx][boxy] = True

                #If there isn't an already selected box
                if first_selection == None:
                    first_selection = (boxx, boxy)
                else:   #If there is an already selected box
                    icon1_shape, icon1_color = b.getShapeAndColor(first_selection[0], first_selection[1])
                    icon2_shape, icon2_color = b.getShapeAndColor(boxx, boxy)

                    if icon1_shape != icon2_shape or icon1_color != icon2_color:
                        #Boxes dont match. Wait for some time, then cover both up
                        pygame.time.wait(1000)
                        b.coverBoxesAnimation((first_selection, (boxx,boxy)))
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[boxx][boxy] = False
                    
                    #There is no need to worry if boxes match up. Just leave them be. We must however check if all pairs have been discovered
                    elif b.hasWon(revealed_boxes):
                        b.gameWonAnimation()
                        pygame.time.wait(10000)

                    first_selection = None

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


if __name__ == '__main__':
    main()

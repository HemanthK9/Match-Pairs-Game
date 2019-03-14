import random
from pygame import Rect
from pygame import draw
import pygame

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


class Board:
    def __init__(self, DISPLAY_SURF, FPS_CLOCK):
        self.board = []
        self.all_colors = ALL_COLORS
        self.all_shapes = ALL_SHAPES
        self.board_width = 10   #Number of boxes in a row
        self.board_height = 7   #Number of boxes in a column
        self.DISPLAY_SURF = DISPLAY_SURF
        self.FPS_CLOCK = FPS_CLOCK

        assert self.board_height * self.board_width % 2 == 0, "Number of boxes need to be even for there to be matching pairs"

        self.box_size = 40  #Dimensions of square box
        self.gap_size = 10  #Gap between boxes
        self.XMARGIN = int((WINDOW_WIDTH - (self.board_width * (self.box_size + self.gap_size))) / 2)
        self.YMARGIN = int((WINDOW_HEIGHT - (self.board_height * (self.box_size + self.gap_size))) / 2)
        self.reveal_speed = 8    #Speed at which box is covered or revealed

        assert len(self.all_colors) * len(self.all_shapes) * 2 >= self.board_width * self.board_height, "Board is too big for the number of shapes/colors defined."

        self.icons = []


    def getRandomizedBoard(self):
        
        for color in self.all_colors:
            for shape in self.all_shapes:
                self.icons.append((shape, color))
            
        random.shuffle(self.icons)
        number_icons_needed = self.board_width * self.board_height  #Find required number of icons
        self.icons = self.icons[:number_icons_needed] * 2   #Create duplicates of all icons
        random.shuffle(self.icons)

        #Create a board data structure with randomly assigned icons
        board = []
        for _ in range(self.board_width):
            column = []
            for _ in range(self.board_height):
                column.append(self.icons[0])
                del self.icons[0]   #Delete the icons as they are assigned

            board.append(column)
        self.board = board
        return board


    #Generate a board of the speciifed size with all values initialized to False
    def generateRevealedBoxesData(self, value):
        rev_board = []
        for _ in range(self.board_width):
            rev_board.append([False] * self.board_height)
        return rev_board


    #Return pixel coordinates of top left of a box, given its array coordinates
    def leftTopCoordsOfBox(self, boxx, boxy):
        #print(boxx, boxy)
        if(type(boxx) != int):
            print(boxx, boxy)
        x = self.XMARGIN + (self.box_size + self.gap_size) * boxx
        y = self.YMARGIN + (self.box_size + self.gap_size) * boxy
        return (x, y)


    #Return box list coordinates given x and y coordinates of mouse cursor postion
    def getBoxAtPixel(self, mousex, mousey):
        #pygame.Rect has collidepoint() which checks if a given point is inside the rectangle
        #Approach 1
        for i in range(self.board_width):
            for j in range(self.board_height):
                boxx, boxy = self.leftTopCoordsOfBox(i, j)
                #Create a rectangle solely to call collidePoint method
                rect = Rect(boxx, boxy, self.box_size, self.box_size)
                if rect.collidepoint(mousex, mousey):
                    return (i,j)
        
        return (None, None)

    
    #Draw the icon given its shape, color and position and the surface to draw on
    def drawIcon(self, shape, color, boxx, boxy):
        quarter = self.box_size // 4
        half = self.box_size // 2

        #Pixel coordinates of the box
        x,y = self.leftTopCoordsOfBox(boxx, boxy)
        
        (donut, square, diamond, lines, oval) = self.all_shapes

        if shape == donut:
            #pygame.draw.circle(self.DISPLAY_SURF color, pos, radius, width=0)
            draw.circle(self.DISPLAY_SURF, color, (x+half, y+half), half-5)
            draw.circle(self.DISPLAY_SURF, color, (x+half, y+half), quarter-5)

        elif shape == square:
            #pygame.draw.rect(self.DISPLAY_SURF color, Rect, width=0) -> Rect
            draw.rect(self.DISPLAY_SURF, color, (x+quarter, y+quarter, half, half))
        
        elif shape == diamond:
            #pygame.draw.polygon(self.DISPLAY_SURF color, pointlist, width=0) -> Rect
            #The pointlist argument is the tuple of vertices
            top = (x+half, y)
            right = (x+self.box_size-1, y+half)
            bottom = (x+half, y+self.box_size-1)
            left = (x, y+half)
            draw.polygon(self.DISPLAY_SURF, color, (top, right, bottom, left))

        elif shape == lines:
            #pygame.draw.line(self.DISPLAY_SURF color, start_pos, end_pos, width=1) -> Rect
            for i in range(0, self.box_size, 4):
                draw.line(self.DISPLAY_SURF, color, (x, y+i), (x+i, y))
                draw.line(self.DISPLAY_SURF, color, (x+i, y+self.box_size-1), (x+self.box_size-1, y+i))

        elif shape == oval:
            #pygame.draw.ellipse(self.DISPLAY_SURF color, Rect, width=0) -> Rect
            draw.ellipse(self.DISPLAY_SURF, color, (x, y+quarter, self.box_size, half))

    def getShapeAndColor(self, boxx, boxy):
        return (self.board[boxx][boxy][0], self.board[boxx][boxy][1])

    def drawBoxCovers(self, boxes, coverage):
        # Draws boxes being covered/revealed. "boxes" is a list
        # of two-item lists, which have the x & y spot of the box.
        #print(boxes)
        for box in boxes:
            
            x,y = self.leftTopCoordsOfBox(box[0], box[1])
            #Draw background color to cover up everything from the previous iteration
            draw.rect(self.DISPLAY_SURF, BGCOLOR, (x,y,self.box_size, self.box_size))
            shape, color = self.getShapeAndColor(box[0], box[1])
            self.drawIcon(shape, color, box[0], box[1])
            #Only draw the box cover if there is coverage
            if coverage > 0:
                draw.rect(self.DISPLAY_SURF, BOXCOLOR, (x,y, coverage, self.box_size))
        pygame.display.update()
        self.FPS_CLOCK.tick(FPS)  

    #Repeatedly draw covers with decreasing cover size (negative reveal speed) to put forth an
    #illusion of an animation
    def revealBoxesAnimation(self, boxes_to_reveal):
        for coverage in range(self.box_size, (-self.reveal_speed-1), -self.reveal_speed):
            self.drawBoxCovers(boxes_to_reveal, coverage)

    #Repeatedly draw covers with increasing cover size (positice reveal speed) to put forth an
    #illusion of an animation
    def coverBoxesAnimation(self, boxes_to_reveal):
        for coverage in range(0, self.box_size+self.reveal_speed, self.reveal_speed):
            self.drawBoxCovers(boxes_to_reveal, coverage)
    

    def drawBoard(self, revealed):
        for boxx in range(self.board_width):
            for boxy in range(self.board_height):
                x,y = self.leftTopCoordsOfBox(boxx, boxy)
                if not revealed[boxx][boxy]:
                    draw.rect(self.DISPLAY_SURF, BOXCOLOR, (x,y, self.box_size, self.box_size))
                #Draw icon
                else:
                    shape, color = self.getShapeAndColor(boxx, boxy)
                    self.drawIcon(shape, color, boxx, boxy)

    #To help the player recognize that they can click on a covered box to reveal it, we will make a blue outline appear around a box to highlight it. This outline is drawn with a call to pygame.draw.rect() to make a rectangle with a width of 4 pixels.        
    def drawHighlightBox(self, boxx, boxy):
        x, y = self.leftTopCoordsOfBox(boxx, boxy)
        draw.rect(self.DISPLAY_SURF, HIGHLIGHTCOLOR, (x-5, y-5, self.box_size+10, self.box_size+10), 4)
    

    def startGameAnimation(self):
        #Randomly reveal the boxes 8 at a time
        coveredBoxes = self.generateRevealedBoxesData(False)
        boxes = []
        for x in range(self.board_width):
            for y in range(self.board_height):
                boxes.append((x,y))

        random.shuffle(boxes)
        groups = []
        for i in range(0, len(boxes), 8):
            groups.append(boxes[i:i+8])
        
        self.drawBoard(coveredBoxes)
        for box_group in groups:
            self.revealBoxesAnimation(box_group)
            self.coverBoxesAnimation(box_group)


    # flash the background color when the player has won, and alternate colors
    def gameWonAnimation(self):
        covered_boxes = self.generateRevealedBoxesData(True)
        color1 = LIGHTBGCOLOR
        color2 = BGCOLOR

        for i in range(13):
            color1, color2 = color2, color1
            self.DISPLAY_SURF.fill(color1)
            self.drawBoard(covered_boxes)
            pygame.display.update()
            pygame.time.wait(300)

    
    # Returns True if all the boxes have been revealed, otherwise False
    def hasWon(self, revealed_boxes):
        for i in revealed_boxes:
            if False in i:
                return False
        return True
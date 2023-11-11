"""
main driver file. Responsible for handling user input and displaying the current GameState
"""

import pygame as p
import ChessEngine


p.init()
WIDTH = HEIGHT = 512
DIMENSION = 8  # dimensions are 8x8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15  # animations
IMAGES = {}

'''
Initialize a global dictionary of images. Called only once in the main
'''

def load_Images():
    pieces = ['wP', 'wR', 'wKn', 'wB', 'wQ', 'wKi', 'bP', 'bR', 'bKn', 'bB', 'bQ',
              'bKi']
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("chess images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

    # access any image by typing 'IMAGES['pawn']

"""
The main driver for code. Handles user input and updates graphics
"""


def main():
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    p.init()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()
    validMoves = gs.getValidMoves()
    moveMade = False #flag variable for when a move is made

    load_Images() # Only once, before while loop
    running = True
    sqSelected = () # no square initially selected, keeps track of last click of the user (tuple: (row, col))
    playerClicks = [] # keeps track of player clicks (two tuples: [(6, 4), (4,4)]
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            #mouse handler
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos() # (x, y) location of mouse
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if sqSelected == (row, col): # user clicked same square twice
                    sqSelected = () #deselect
                    playerClicks = [] #clear player clicks
                else:
                   sqSelected = (row, col)
                   playerClicks.append(sqSelected) #append for both 1st and end clicks
                if len(playerClicks) == 2: #after 2nd click
                    move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                    print(move.getChessNotation())
                    if move in validMoves:
                        gs.makeMove(move)
                        moveMade = True
                    sqSelected = () #resets user clicks
                    playerClicks = []
            # key handlers
            elif e.type == p.KEYDOWN:
                if e.key == p.K_z: #undo when 'z' is pressed
                    gs.undoMove()
                    moveMade = True

        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False

        drawGameState(screen, gs)
        clock.tick(MAX_FPS)
        p.display.flip()

"""
Draws the graphics  
"""

def drawGameState(screen, gs):
        drawBoard(screen) # draws squares on board
        drawPieces(screen, gs.board) # draws pieces

"""
Draws board
"""
def drawBoard(screen):
    colors = [p.Color("#feffeb"), p.Color("#D3BD8B")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[((r+c)%2)]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

"""
Draws board pieces
"""

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))


if __name__ == "__main__":
    main()

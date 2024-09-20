import sys
import pygame
import numpy as np

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)

class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_square = self.squares
        self.marked_square = 0

    def final(self):

    #return 0 if there is no win yet
    #returns 1 if player 1 wins
    #returns 2 if player 2 wins

        #vertical winning
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                return self.squares[0][col]
        
        #row winning
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                return self.squares[row][0]

        #descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            return self.squares[0][0]
        
        #ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            return self.squares[2][0]

        return 0
        
    def get_empty_square(self):
        empty_square = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty_square(row, col):
                    empty_square.append((row, col))

        return empty_square

    def marked(self, row, col, player):
        self.squares[row][col] = player
        self.marked_square = self.marked_square + 1

    def empty(self, row, col):
        return self.squares[row][col] == 0

    def full(self):
        return self.marked_square == 9

    def isempty(self):
        return self.marked_square == 0
    
class Game:
    
    def __init__(self):
        self.consoleBoard = Board()
        #self.ai = AI()
        self.gamemode = 'pvp'
        self.running = True
        self.player = 1
        self.lines()
        

    def lines(self):
        #vertical lines

        pygame.draw.line(screen, LINE_COLOR, (SQSIZE, 0), (SQSIZE, HEIGHT), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (WIDTH - SQSIZE, 0), (WIDTH-SQSIZE, HEIGHT), LINE_WIDTH)

        #horizontal
        pygame.draw.line(screen, LINE_COLOR, (0, SQSIZE), (WIDTH, SQSIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT-SQSIZE), (WIDTH, HEIGHT-SQSIZE), LINE_WIDTH)

    def switch(self):
        #1 is X, 2 is O
        if self.player == 1:
            self.player = 2
        else:
            self.player = 1

    def draw(self, row, col):
        if self.player == 1:
            #draw cross
            #descending line
            start_desc = (col*SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_desc, end_desc, CROSS_WIDTH)

            #ascending line
            start_asc = (col*SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc= (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, CROSS_COLOR, start_asc, end_asc, CROSS_WIDTH)

        else:
            #draw circle
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, CIRC_COLOR, center, RADIUS, CIRC_WIDTH)

def main():

    #call game objecct
    game = Game()
    board = game.consoleBoard
    #mainloop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                cur = event.pos
                #makes row, col more logical numbers
                row = cur[1] // SQSIZE
                col = cur[0] // SQSIZE
                
                #means can't mark if already marked
                if board.empty(row, col):
                    board.marked(row, col, game.player)
                    game.draw(row, col)
                    game.switch()
                    
                

                
        pygame.display.update()

main()
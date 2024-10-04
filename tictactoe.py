import sys
import pygame
import numpy as np
import random
import copy

from constants import *

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill(BG_COLOR)
class AI:
    
    def __init__(self, diff=1, player=2):
        self.diff = diff
        self.player=player
    
    def random(self, board):
        empty_sqr = board.get_empty_square()
        i = random.randrange(0, len(empty_sqr))
        return empty_sqr[i]
    
    def minimax(self, board, maximizing):
        
        #check terminal case
        case = board.final()
        #player 1 wins
        if case == 1:
            return 1, None

        
        #player 2 wins
        if case == 2:
            return -1, None

        elif board.full():

            return 0, None
        


        if maximizing:
        #must be any number less than 1
            max_eval = -101
            best_move = None
            empty_sqr = board.get_empty_square()

            for (row, col) in empty_sqr:
                temp = copy.deepcopy(board)
                temp.marked(row, col, 1)
                
                #false now cuz it's minimizing player
                eval = self.minimax(temp, False)[0]
                if eval > max_eval:
                    
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move
        elif not maximizing:
            #must be any number greater than 1
            min_eval = 101
            best_move = None
            empty_sqr = board.get_empty_square()
            for (row, col) in empty_sqr:
                temp = copy.deepcopy(board)
                temp.marked(row, col, self.player)
                eval = self.minimax(temp, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move
    
    def eval(self, main_board):
        #random
        if self.diff == 0:
            eval = 'random'
            move = self.random(main_board)
        #minimax
        else:
            eval, move = self.minimax(main_board, False)

        print(f'AI has marked square in position: {move} with an eval of: {eval}')
        return move

class Board:

    def __init__(self):
        self.squares = np.zeros((ROWS, COLS))
        self.empty_square = self.squares
        self.marked_square = 0

    def final(self, show=False):

    #return 0 if there is no win yet
    #returns 1 if player 1 wins
    #returns 2 if player 2 wins

        #vertical winning
        for col in range(COLS):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[0][col] == 2 else CROSS_COLOR
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, HEIGHT - 20)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[0][col]
        
        #row winning
        for row in range(ROWS):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color = CIRC_COLOR if self.squares[row][0] == 2 else CROSS_COLOR
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (WIDTH - 20, row*SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
                return self.squares[row][0]

        #descending diagonal
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, 20)
                fPos = (WIDTH - 20, HEIGHT - 20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]
        
        #ascending diagonal
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = CIRC_COLOR if self.squares[1][1] == 2 else CROSS_COLOR
                iPos = (20, HEIGHT - 20)
                fPos = (WIDTH - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, LINE_WIDTH)
            return self.squares[1][1]

        return 0
        
    def get_empty_square(self):
        empty_square = []
        for row in range(ROWS):
            for col in range(COLS):
                if self.empty(row, col):
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
        self.ai = AI()
        self.gamemode = 'ai'
        self.running = True
        self.player = 1
        self.lines()
        

    def lines(self):
        #background
        screen.fill( BG_COLOR )
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

    def change_gamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def restart(self):
        self.__init__()

    def isover(self):
        return self.consoleBoard.final(show=True) != 0 or self.consoleBoard.full()

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
    ai = game.ai
    #mainloop
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


            if event.type == pygame.KEYDOWN:

                #g - gamemode
                if event.key == pygame.K_g:
                    game.change_gamemode()

                #0 - random ai

                if event.key == pygame.K_0:
                    ai.diff = 0
                
                if event.key == pygame.K_1:
                    ai.diff = 1

                if event.key == pygame.K_r:
                    game.restart()
                    board = game.consoleBoard
                    ai = game.ai
                if event.key == pygame.K_q:
                    pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                cur = event.pos
                #makes row, col more logical numbers
                row = cur[1] // SQSIZE
                col = cur[0] // SQSIZE
                
                #means can't mark if already marked
                if board.empty(row, col) and game.running:
                    board.marked(row, col, game.player)
                    game.draw(row, col)
                    game.switch()

                    if game.isover():
                        game.running = False
                

            
                    
        if game.gamemode == 'ai' and game.player == ai.player and game.running:
            pygame.display.update()

            row, col = ai.eval(board)
            board.marked(row, col, ai.player)
            game.draw(row, col)
            game.switch()

            if game.isover():
                game.running = False
           

                
        pygame.display.update()

main()
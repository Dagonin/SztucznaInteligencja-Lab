import templates
from copy import deepcopy

class Game:
    def __init__(self):
        self.board = templates.start_game
        self.board_with_moves = deepcopy(templates.start_game)
        self.turn = 0
        self.player = 2


    def print_board(self):
        for row in self.board:
            print("  ".join(str(cell) for cell in row))

    def print_board_with_moves(self):
        for row in self.board_with_moves:
            print("  ".join(str(cell) for cell in row))

    def fill_board(self,board):
        self.board = board



    def show_all_moves(self):
        for i,row in enumerate(self.board):
            for j,cell in enumerate(row):
                if(cell == self.player):
                    self.mark_adjacent_cells(i,j,False)
        
        self.print_board_with_moves()

            

    
    def mark_adjacent_cells(self,x,y,jump_flag):
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                nx = x + dx
                ny = y + dy
                if( 0 <= nx < 16 and 0 <= ny < 16):
                    if(self.board[nx][ny] == 0 and jump_flag == False):
                        self.board_with_moves[nx][ny] = "h"
                    else:
                        self.mark_jump(nx,ny,dx,dy)


    def mark_jump(self,x,y,x_offset,y_offset):
        if(0 <= x+x_offset < 16 and 0 <= y+y_offset < 16):
            if((self.board_with_moves[x][y] == 2 or self.board_with_moves[x][y] == 1) and self.board_with_moves[x+x_offset][y+y_offset] == 0):
                self.board_with_moves[x+x_offset][y+y_offset] = "j"
                self.mark_adjacent_cells(x+x_offset,y+y_offset,True)

b = Game()

b.show_all_moves()
print("")
b.print_board()


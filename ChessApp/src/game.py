import pygame

from const import *
from board import Board
from dragger import Dragger

class Game():
    def __init__(self):
        self.next_player = 'white'
        self.board = Board()
        self.dragger = Dragger()
    
    # show methods
    def show_bg(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = (234, 235, 200) # light green
                else:
                    color = (119, 154, 88) # dark green
                    
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                
                pygame.draw.rect(surface, color, rect)
                
    def show_pieces(self, surface):
        for row in range(ROWS):
            for col in range(COLS):
                # piece ?
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    
                    if piece is not self.dragger.piece:
                        piece.set_texture(size=80)
                        img = pygame.image.load(piece.texture)
                        img_center = col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2
                        piece.texture_rect = img.get_rect(center=img_center)
                        surface.blit(img, piece.texture_rect)
                        
    def show_moves(self, surface):
        if self.dragger.dragging:
            piece = self.dragger.piece
            # loop through valid moves
            for move in piece.moves:
                # color
                color = 'red'
                center = (move.final.col * SQSIZE + 50, move.final.row * SQSIZE + 50)
                # blit
                pygame.draw.circle(surface, color, center, radius=12)
                
    def show_last_move(self, surface):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial, final]:
                # color 
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
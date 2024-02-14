import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move

class Main:
    
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption('Chess')
        self.game = Game()
        self.running = True  # Flag to control the main loop
        
    def mainLoop(self):
        
        game = self.game
        screen = self.screen
        board = self.game.board
        dragger = self.game.dragger
        
        
        while self.running:
            # show methods
            game.show_bg(screen)
            game.show_last_move(screen)
            game.show_pieces(screen)
            game.show_moves(screen)
            
            
            if dragger.dragging:
                dragger.update_blit(screen)
            
            for event in pygame.event.get():
                
                # click
                if event.type == pygame.MOUSEBUTTONDOWN:
                    dragger.update_mouse(event.pos)
                    
                    clicked_row = dragger.mouseY // SQSIZE
                    clicked_col = dragger.mouseX // SQSIZE
                    
                    # checks if square clicked has piece
                    if board.squares[clicked_row][clicked_col].has_piece():
                        piece = board.squares[clicked_row][clicked_col].piece
                        # check if valid piece and its color
                        if piece.color == game.next_player:
                            board.calc_moves(piece, clicked_row, clicked_col)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                            # show method
                            '''game.show_bg(screen)
                            game.show_moves(screen)
                            game.show_pieces(screen)'''
                        
                    
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        # show methods
                        '''game.show_bg(screen)
                        game.show_pieces(screen)
                        dragger.update_blit(screen)'''
                
                # click release
                elif event.type == pygame.MOUSEBUTTONUP:
                    
                    # checks the piece we want to move
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                        released_row = dragger.mouseY // SQSIZE
                        released_col = dragger.mouseX // SQSIZE
                        
                        # creates possible move
                        initial = Square(dragger.initial_row, dragger.initial_col)
                        final = Square(released_row, released_col)
                        move = Move(initial, final)
                        
                        # checks if possible move is a valid move
                        if board.valid_move(dragger.piece, move):
                            board.move(dragger.piece, move)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()
                            
                    dragger.undrag_piece()
                
                # Quit the application
                if event.type == pygame.QUIT:
                    self.running = False  # Set running to False to exit the loop
            
            pygame.display.update()
        
        pygame.quit()
        sys.exit()
        
main = Main()
main.mainLoop()

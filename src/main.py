import pygame
import sys

from const import *
from game import Game
from square import Square
from move import Move
from ai import AI

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
        need_move_calculation = True
        
        
        while self.running:
            # show methods
            game.show_bg(screen)
            game.show_hover(screen)
            game.show_last_move(screen)
            game.show_pieces(screen)
            game.show_moves(screen)
            
            if game.game_over:
                game.show_game_over(game.is_game_over())
            
            if board.turn_counter % 2 == 0:
                ai = AI(board, 'black', game)
                ai.make_random_move('black')
                self.game.next_turn()
            
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
                            # board.set_false_en_passant()
                            board.calc_moves(piece, clicked_row, clicked_col, bool)
                            dragger.save_initial(event.pos)
                            dragger.drag_piece(piece)
                
                # mouse motion
                elif event.type == pygame.MOUSEMOTION:
                    motion_row = event.pos[1] // SQSIZE
                    motion_col = event.pos[0] // SQSIZE
                    
                    # hover
                    game.set_hover(motion_row, motion_col)
                    if dragger.dragging:
                        dragger.update_mouse(event.pos)
                
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
                            captured = board.squares[released_row][released_col].has_piece()
                            board.move(dragger.piece, move)
                            
                            board.set_true_en_passant(dragger.piece, dragger.initial_row, released_row, dragger.initial_col)
                            game.play_sound(captured)
                            # show methods
                            game.show_bg(screen)
                            game.show_last_move(screen)
                            game.show_pieces(screen)
                            game.next_turn()
                            
                            
                            
                    dragger.undrag_piece()
                
                elif event.type == pygame.KEYDOWN:
                    
                    if event.key == pygame.K_t:
                        game.change_theme()

                    if event.key == pygame.K_r:
                        game.reset()
                        game = self.game
                        board = self.game.board
                        dragger = self.game.dragger
                    
                    
                # Quit the application
                if event.type == pygame.QUIT:
                    self.running = False  # Set running to False to exit the loop
            
            pygame.display.update()
        
        pygame.quit()
        sys.exit()
        
main = Main()
main.mainLoop()

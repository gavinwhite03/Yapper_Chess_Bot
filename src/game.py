import pygame
import sys

from const import *
from board import Board
from dragger import Dragger
from config import Config
from square import Square

class Game():

    def __init__(self):
        self.next_player = 'white'
        self.hovered_sq = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()
        self.game_over = False
        self.running = True
    
    # show methods
    def show_bg(self, surface):
        theme = self.config.theme
        
        for row in range(ROWS):
            for col in range(COLS):
                color = theme.bg.light if (row + col) % 2 == 0 else theme.bg.dark                
                rect = (col * SQSIZE, row * SQSIZE, SQSIZE, SQSIZE)
                pygame.draw.rect(surface, color, rect)
                
                # row cordinate labels
                if col == 0:
                    color = theme.bg.dark if row % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    lbl_pos = (5, 5 + row * SQSIZE)
                    surface.blit(lbl, lbl_pos)
                    
                # col cordinate labels
                if row == 7:
                    color = theme.bg.dark if (row + col) % 2 == 0 else theme.bg.light
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    lbl_pos = (col * SQSIZE + SQSIZE - 20, HEIGHT - 20)
                    surface.blit(lbl, lbl_pos)
                
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
        theme = self.config.theme
        
        if self.dragger.dragging:
            piece = self.dragger.piece
            # loop through valid moves
            for move in piece.moves:
                # color
                color = theme.moves.light if (move.final.row + move.final.col) % 2 == 0 else theme.moves.dark
                center = (move.final.col * SQSIZE + 50, move.final.row * SQSIZE + 50)
                # blit
                pygame.draw.circle(surface, color, center, radius=12)
                
    def show_last_move(self, surface):
        theme = self.config.theme
        
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            
            for pos in [initial, final]:
                # color 
                color = theme.trace.light if (pos.row + pos.col) % 2 == 0 else theme.trace.dark
                rect = (pos.col * SQSIZE, pos.row * SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(surface, color, rect)
                
    def show_hover(self, surface):
        if self.hovered_sq:
            color = (180, 180, 180)
            rect = (self.hovered_sq.col * SQSIZE, self.hovered_sq.row * SQSIZE, SQSIZE, SQSIZE)
            pygame.draw.rect(surface, color, rect, width=3)

    def show_game_over(self, winner):
        pygame.init()
        gameover_width = 400
        gameover_height = 200

        # Create the new window for the game over message
        gameover_screen = pygame.display.set_mode((gameover_width, gameover_height))
        pygame.display.set_caption("Game Over")

        # Create font object
        font = pygame.font.SysFont(None, 48)

        # Determine the message based on the winner
        if winner == 'black':
            message = "Black wins!"
        elif winner == 'white':
            message = "White wins!"
        else:
            message = "Draw!"

        # Render the text
        text = font.render(message, True, (255, 255, 255))
        text_rect = text.get_rect(center=(gameover_width // 2, gameover_height // 2))

        # Fill the game over window with black color
        gameover_screen.fill((0, 0, 0))

        # Draw the text onto the game over window
        gameover_screen.blit(text, text_rect)

        # Update the display for the game over window
        pygame.display.flip()
        
        # Main loop to handle events for the game over window
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click(event.pos)


    



    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'
        self.board.turn_counter += 1
        print(self.board.turn_counter)
        
    def set_hover(self, row, col):
        self.hovered_sq = self.board.squares[row][col]
        
    def change_theme(self):
        self.config.change_theme()
        
    def play_sound(self, captured = False):
        if captured:
            self.config.capture_sound.play()
        else:
            self.config.move_sound.play()
            
    def reset(self):
        self.__init__()
        
    def is_game_over(self):
        black_king = self.board.get_black_king()
        white_king = self.board.get_white_king()
        white_moves = self.board.calculate_all_moves_white()
        black_moves = self.board.calculate_all_moves_black()

        white_has_moves = any(move for moves in white_moves for move in moves)
        black_has_moves = any(move for moves in black_moves for move in moves)

        if not white_has_moves:
            if self.board.in_check(white_king, None):
                self.game_over = True
                return 'black'  # White is in checkmate, so black wins
            else:
                self.game_over = True
                return 'draw'   # White has no moves, but it's not checkmate, so it's a draw

        if not black_has_moves:
            if self.board.in_check(black_king, None):
                self.game_over = True
                return 'white'  # Black is in checkmate, so white wins
            else:
                self.game_over = True
                return 'draw'   # Black has no moves, but it's not checkmate, so it's a draw
        
        self.game_over = False
        return None  # Game is not over yet

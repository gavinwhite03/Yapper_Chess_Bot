from board import Board
from move import Move
from square import Square
from game import Game
import random

class AI:
    def __init__(self, board, color, game):
        self.board = board
        self.color = color
        self.game = game
        
    def generate_possible_moves(self, color):
        self.color = color
        possible_moves = []
        if self.color == 'white':
            possible_moves.extend(self.board.calculate_all_moves_white())
            print(possible_moves) 

        if self.color == 'black':
            possible_moves.extend(self.board.calculate_all_moves_black())
            print(possible_moves)
        return possible_moves
            
    def make_random_move(self, color):
        possible_moves = self.generate_possible_moves(color)
        all_possible_moves = [move for sublist in possible_moves for move in sublist]

        if all_possible_moves:
            print('Possible moves is not empty')
            random_move = random.choice(all_possible_moves)
            initial = random_move.initial
            final = random_move.final
            piece = self.board.squares[initial.row][initial.col].piece
            move = Move(initial, final)
            self.board.calc_moves(piece, initial.row, initial.col, bool)
            print(move, piece)
            if self.board.valid_move(piece, move):
                print(move, 'is a valid move')
                captured = self.board.squares[final.row][final.col].has_piece()
                self.board.move(piece, move)
                self.board.set_true_en_passant(piece, initial.row, final.row, initial.col)
                self.game.play_sound(captured)
        else:
            return None



            

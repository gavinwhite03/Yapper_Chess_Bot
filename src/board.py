from const import *
from square import Square
from piece import *
from move import Move
import copy

class Board():
    turn_counter = 1
    def __init__(self):
        self.squares = [[0, 0, 0, 0, 0, 0, 0, 0] for col in range(COLS)]
        self.last_move = None
        self.all_possible_moves = []
        
        self._create()
        self._add_piece('white')
        self._add_piece('black')
    
    def calculate_all_moves_white(self):
        all_possible_moves_white = []
        temp_board = copy.deepcopy(self)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_piece():
                    p = temp_board.squares[row][col].piece
                    if p.color == 'white':
                        temp_board.calc_moves(p, row, col)
                        all_possible_moves_white.append(p.moves)
        return all_possible_moves_white

    def calculate_all_moves_black(self):
        all_possible_moves_black = []
        temp_board = copy.deepcopy(self)
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_piece():
                    p = temp_board.squares[row][col].piece
                    if p.color == 'black':
                        temp_board.calc_moves(p, row, col)
                        all_possible_moves_black.append(p.moves)
        return all_possible_moves_black


    def get_black_king(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece
                    if isinstance(piece, King) and piece.color == 'black':
                        return piece
        return None
    
    def get_white_king(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.squares[row][col].has_piece():
                    piece = self.squares[row][col].piece
                    if isinstance(piece, King) and piece.color == 'white':
                        return piece
        return None
                    
    def opponent_pieces(self, color):
        opponent_color = 'black' if color == 'white' else 'white'
        opponent_pieces = []
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if piece and piece.color == opponent_color:
                    opponent_pieces.append(piece)
        return opponent_pieces
                           
    def move(self, piece, move, testing=False):
        if move is None:
            return
        initial = move.initial
        final = move.final
        en_passant_empty = self.squares[final.row][final.col].is_empty()

        # console board move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece
        
        #  pawn promotion 
        if isinstance(piece, Pawn):
            # en passant capture
            diff = final.col - initial.col
            if diff != 0 and en_passant_empty:
                # console board move update
                self.squares[initial.row][initial.col + diff].piece = None
                self.squares[final.row][final.col].piece = piece
            # check promotion
            else:
                self.check_promotion(piece, final)
        
        # king castling
        if isinstance(piece, King):
            if self.castling(initial, final) and not testing:
                diff = final.col - initial.col
                rook = piece.left_rook if (diff < 0) else piece.right_rook
                self.move(rook, rook.moves[-1])
        # move
        piece.moved = True
        
        # clear valid moves
        piece.clear_moves()
        
        # set last move
        self.last_move = move
    
    def valid_move(self, piece, move):
        return move in piece.moves
       
    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
            
    def castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def set_true_en_passant(self, piece, start_row, end_row, start_col):
        if not isinstance(piece, Pawn):
            return
        if abs(start_row - end_row) == 2:
            piece.turn_where_set_true = self.turn_counter
            print('Turn where set true: ', piece.turn_where_set_true)
        else:
            piece.turn_where_set_true = None  # Reset turn_where_set_true if not moving two squares
        # No need to set en_passant here, it will be set during pawn_moves()

    def set_false_en_passant(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.squares[row][col].piece
                if isinstance(piece, Pawn):
                    # Reset en passant flag for pawns if their turn_where_set_true is not equal to the previous turn
                    if piece.turn_where_set_true != self.turn_counter - 1:
                        print(f'Set {self.squares[row][col]}{piece.en_passant} to False')
                        piece.en_passant = False

                        
    def in_check(self, piece, move):
        temp_peice = copy.deepcopy(piece)
        temp_board = copy.deepcopy(self)
        temp_board.move(temp_peice, move, testing=True)
        
        for row in range(ROWS):
            for col in range(COLS):
                if temp_board.squares[row][col].has_enemy_piece(piece.color):
                    p = temp_board.squares[row][col].piece
                    temp_board.calc_moves(p, row, col, bool=False)
                    for m in p.moves:
                        if isinstance(m.final.piece, King):
                            return True
            
        return False
    
    def calc_moves(self, piece, row, col, bool=True):
        piece.clear_moves()
        def pawn_moves():
            steps = 1 if piece.moved else 2

            # straight moves
            start = row + piece.dir
            end = row + (piece.dir * (1 + steps))
            for possible_move_row in range(start, end, piece.dir):
                if Square.in_range(possible_move_row):
                    if self.squares[possible_move_row][col].is_empty():
                        initial = Square(row, col)
                        final = Square(possible_move_row, col)
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)
                    else:
                        break
                else:
                    break

            # diagonal attack
            possible_move_row = row + piece.dir
            possible_move_cols = [col - 1, col + 1]
            for possible_move_col in possible_move_cols:
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                        else:
                            piece.add_move(move)

            # en passant moves
            r = 3 if piece.color == 'white' else 4
            fr = 2 if piece.color == 'white' else 5
            # left en passant
            if Square.in_range(col - 1) and row == r:
                if self.squares[row][col - 1].has_enemy_piece(piece.color):
                    p = self.squares[row][col - 1].piece
                    if isinstance(p, Pawn):
                        if p.turn_where_set_true == self.turn_counter - 1:
                            initial = Square(row, col)
                            final = Square(fr, col - 1, p)
                            # create new move
                            move = Move(initial, final)
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)

            # right en passant
            if Square.in_range(col + 1) and row == r:
                if self.squares[row][col + 1].has_enemy_piece(piece.color):
                    p = self.squares[row][col + 1].piece
                    if isinstance(p, Pawn):
                        if p.turn_where_set_true == self.turn_counter - 1:
                            initial = Square(row, col)
                            final = Square(fr, col + 1, p)
                            # create new move
                            move = Move(initial, final)
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
            
        def straight_line_moves(incrs):
            for incr in incrs:
                row_incr, col_incr = incr
                possible_move_row = row + row_incr
                possible_move_col = col + col_incr

                while True:
                    if Square.in_range(possible_move_row, possible_move_col):
                        # create squares of the possible new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create a possible new move
                        move = Move(initial, final)

                        # empty = continue looping
                        if self.squares[possible_move_row][possible_move_col].is_empty():
                             # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)

                        # has enemy piece = add move + break
                        elif self.squares[possible_move_row][possible_move_col].has_enemy_piece(piece.color):
                            # check potential checks
                            if bool:
                                if not self.in_check(piece, move):
                                    piece.add_move(move)
                            else:
                                piece.add_move(move)
                            break

                        # has team piece = break
                        elif self.squares[possible_move_row][possible_move_col].has_team_piece(piece.color):
                            break
                    
                    # not in range
                    else: break

                    # incrementing incrs
                    possible_move_row = possible_move_row + row_incr
                    possible_move_col = possible_move_col + col_incr
                        
        
        def king_moves():
            adj = [
                # 8 possible moves
                (row-1, col+0),
                (row-1, col+1),
                (row+0, col+1),
                (row+1, col+1),
                (row+1, col+0),
                (row+1, col-1),
                (row+0, col-1),
                (row-1, col-1)
            ]
            
            for possible_move in adj:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        # create squares of new move
                        initial = Square(row, col)
                        final = Square(possible_move_row, possible_move_col)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)  
                        else:
                            piece.add_move(move)
                        
            # Castling moves
            if not piece.moved:
                # Long castle
                left_rook = self.squares[row][0].piece
                if isinstance(left_rook, Rook):
                    if not left_rook.moved:
                        for c in range(1, 4):
                            if self.squares[row][c].has_piece():
                                break
                            initial = Square(row, col)
                            final = Square(row, 3)
                            move = Move(initial, final)
                            test2_initial = Square(row, col)
                            test2_final = Square(row, 2)
                            test_move2 = Move(test2_initial, test2_final)
                            if c == 3 and not self.in_check(piece, move) and not self.in_check(piece, test_move2):
                                piece.left_rook = left_rook
                                initial = Square(row, 0)
                                final = Square(row, 3)
                                moveR = Move(initial, final)
                                # King move
                                initial = Square(row, col)
                                final = Square(row, 2)
                                moveK = Move(initial, final)
                                # Check potential checks
                                if bool:
                                    if not self.in_check(piece, moveK) and not self.in_check(left_rook, moveR):
                                        left_rook.add_move(moveR)
                                        piece.add_move(moveK)
                                else:
                                    left_rook.add_move(moveR)
                                    piece.add_move(moveK)
                # Short castle
                if not piece.moved:
                    right_rook = self.squares[row][7].piece
                    if isinstance(right_rook, Rook):
                        if not right_rook.moved:
                            for c in range(5, 7):
                                if self.squares[row][c].has_piece():
                                    break
                                initial = Square(row, col)
                                final = Square(row, 5)
                                move = Move(initial, final)
                                if c == 6 and not self.in_check(piece, move):
                                    piece.right_rook = right_rook
                                    initial = Square(row, 7)
                                    final = Square(row, 5)
                                    moveR = Move(initial, final)
                                    # King move
                                    initial = Square(row, col)
                                    final = Square(row, 6)
                                    moveK = Move(initial, final)
                                    # Check potential checks
                                    if bool:
                                        if not self.in_check(piece, moveK) and not self.in_check(right_rook, moveR):
                                            right_rook.add_move(moveR)
                                            piece.add_move(moveK)
                                    else:
                                        right_rook.add_move(moveR)
                                        piece.add_move(moveK)
        
        def knight_moves():
            # 8 possible moves
            possible_moves = [
                (row-2, col+1),
                (row-1, col+2),
                (row+1, col+2),
                (row+2, col+1),
                (row+2, col-1),
                (row+1, col-2),
                (row-1, col-2),
                (row-2, col-1)
            ]
            
            for possible_move in possible_moves:
                possible_move_row, possible_move_col = possible_move
                if Square.in_range(possible_move_row, possible_move_col):
                    if self.squares[possible_move_row][possible_move_col].is_empty_or_enemy(piece.color):
                        # create squares of new move
                        initial = Square(row, col)
                        final_piece = self.squares[possible_move_row][possible_move_col].piece
                        final = Square(possible_move_row, possible_move_col, final_piece)
                        # create new move
                        move = Move(initial, final)
                        # append new valid move
                        # check potential checks
                        if bool:
                            if not self.in_check(piece, move):
                                piece.add_move(move)
                            else: break
                        else:
                            piece.add_move(move)
                 
        
        # calculate all valid moves in a position
        if isinstance(piece, Pawn): pawn_moves()
        
        elif isinstance(piece, Knight): knight_moves()
        
        elif isinstance(piece, Bishop): 
            straight_line_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1)
            ])
        
        elif isinstance(piece, Rook):
            straight_line_moves([
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
            
        elif isinstance(piece, Queen):
            straight_line_moves([
                (-1, 1),
                (-1, -1),
                (1, 1),
                (1, -1),
                (-1, 0),
                (0, 1),
                (1, 0),
                (0, -1)
            ])
        
        elif isinstance(piece, King): king_moves()
        
    def _create(self):
        
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)
    
    def _add_piece(self, color):
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # creating pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))
            
        # creating knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))
        
        # creating bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))
        
        # creating rooks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))
        
        # creating queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))
        
        # creating king
        self.squares[row_other][4] = Square(row_other, 4, King(color))
                                            
b = Board()
b._create()
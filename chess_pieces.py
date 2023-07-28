import numpy as np
import string
import math
from copy import deepcopy

class Board:
    def __init__(self):
        self.board = np.empty(shape=(8,8),dtype=object)
        self.white_pieces = list()
        self.black_pieces = list()
        self.turn = "white"
        self.white_king_loc = ()
        self.black_king_loc = ()
        self.score = 0
    
    # CALCULATES SCORE OF CURRENT BOARD TO USE IN AB-PRUNING
    # SCORE = WEIGHT OF WHITE PIECES - WEIGHT OF BLACK PIECES
    def calculate_static_eval(self):
        white_score = 0
        black_score = 0
        
        for piece in self.white_pieces:
            white_score += piece.value
        for piece in self.black_pieces:
            black_score += piece.value
        
        self.score = white_score - black_score

    # CHECKS IF USER ENTERS INVALID SQUARE
    def is_valid_selection(self, x : int, y : int):
        piece = self.board[x][y]
        if piece == "-":
            return False, "You cannot select empty square"
        elif piece.color == self.turn:
            return True, ""
        else:
            return False, f"Please choose {self.turn} piece"

    def get_index(self,piece):
        if piece.color == "white":
            idx = self.white_pieces.index(piece)
            return idx
        else:
            idx = self.black_pieces.index(piece)
            return idx
    
    # CHECKS IF MOVE IS POSSIBLE
    # MOVES THE PIECE, CHECKS AND UNDOS MOVE
    def is_move_possible(self, piece, x, y):
        start_loc_x = deepcopy(piece.x)
        start_loc_y = deepcopy(piece.y) 
        destination_piece = self.board[x][y]

        removed_piece = None
        self.board[piece.x][piece.y] = "-"
        piece.x = x
        piece.y = y

        if destination_piece != "-":
            removed_piece = deepcopy(self.board[x][y])
            if destination_piece.color == "white":
                try:
                    self.white_pieces.remove(destination_piece)
                except: pass
            else:
                try:
                    self.black_pieces.remove(destination_piece)        
                except: pass        
        self.board[x][y] = piece

        if piece.name == "king":
            if piece.color == "white":
                self.white_king_loc = (x, y)
            else:
                self.black_king_loc = (x, y)
        
        is_check = self.is_self_check()
        
        if removed_piece != None:
            if removed_piece.color == "white":
                self.white_pieces.append(removed_piece)
                self.board[x][y] = self.white_pieces[-1]
            else:
                self.white_pieces.append(removed_piece)
                self.board[x][y] = self.black_pieces[-1]
        else:
            self.board[x][y] = "-"
        piece.x = start_loc_x
        piece.y = start_loc_y
        self.board[piece.x][piece.y] = piece

        if piece.name == "king":
            if piece.color == "white":
                self.white_king_loc = (start_loc_x, start_loc_y)
            else:
                self.black_king_loc = (start_loc_x, start_loc_y)

        if is_check == True:
            return False
        else:
            return True

    # CHECKS IF CURRENT PLAYER IS IN A CHECK MATE
    def is_self_checkmate(self) -> bool:
        pieces = None
        if self.turn == "black":
            pieces = self.black_pieces
        if self.turn == "white":
            pieces = self.white_pieces
        
        for piece in pieces:
            piece.possible_moves(self)
            if piece.moves:    
                for move in piece.moves:
                    move = move[1]
                    can_move = self.is_move_possible(piece, move[0], move[1])
                    if can_move == True:
                        return False
        return True
    
    # CHECKS IF CURRENT PLAYER IS IN A CHECK
    def is_self_check(self):
        if self.turn == "black":
            for wp in self.white_pieces:
                wp.possible_moves(self)
            for wp in self.white_pieces:
                if wp.moves:
                    for move in wp.moves:
                        move = move[1]
                        if move == self.black_king_loc:
                            return True
            return False
        else:
            for bp in self.black_pieces:
                bp.possible_moves(self)
            for bp in self.black_pieces:
                if bp.moves:
                    for move in bp.moves:
                        move = move[1]
                        if move == self.white_king_loc:
                            return True
            return False
    
    # CHECKS IF ENEMY PLAYER IS IN A CHECK
    def is_enemy_check(self):
        if self.turn == "black":
            for bp in self.black_pieces:
                bp.possible_moves(self)
            for bp in self.black_pieces:
                if bp.moves:    
                    for move in bp.moves:
                        move = move[1]
                        if move == self.white_king_loc:
                            return True
            return False
        else:
            for wp in self.white_pieces:
                wp.possible_moves(self)
            for wp in self.white_pieces:
                if wp.moves:
                    for move in wp.moves:
                        move = move[1]
                        if move == self.black_king_loc:
                            return True
            return False

    # TAKES START AND DESTINATION LOCATION
    # MOVES THE PIECE FROM START TO DEST
    
    def move(self, x, y, new_x, new_y) -> bool:
        piece = self.board[x][y]
        if piece == "-":
            return False
        else:
            piece.possible_moves(self)
            if self.turn == "white" and piece.color != "white":
                return False
            
            if self.turn == "black" and piece.color != "black":
                return False
            if (piece.move(new_x, new_y, self)):
                return True
            else:
                return False

    # INITIALIZES BOARD BY PLACING PIECES
    def initialize(self):
        for i in range(8):
            for j in range(8):
                self.board[i][j] = "-"
        
        self.white_pieces.append(King(7, 4, "white"))
        self.white_king_loc = (self.white_pieces[-1].x, self.white_pieces[-1].y)
        
        self.black_pieces.append(King(0, 4, "black"))
        self.black_king_loc = (self.black_pieces[-1].x, self.black_pieces[-1].y)

        
        for i in range(8):
            self.white_pieces.append(Pawn(6, i, "white"))
        for i in range(8):
            self.black_pieces.append(Pawn(1, i, "black"))
        
        self.white_pieces.append(Rook(7, 0, "white"))
        self.white_pieces.append(Rook(7, 7, "white"))

        self.black_pieces.append(Rook(0, 0, "black"))
        self.black_pieces.append(Rook(0, 7, "black"))

        self.white_pieces.append(Knight(7, 1, "white"))
        self.white_pieces.append(Knight(7, 6, "white"))

        self.black_pieces.append(Knight(0, 1, "black"))
        self.black_pieces.append(Knight(0, 6, "black"))

        self.white_pieces.append(Bishop(7, 2, "white"))
        self.white_pieces.append(Bishop(7, 5, "white"))

        self.black_pieces.append(Bishop(0, 2, "black"))
        self.black_pieces.append(Bishop(0, 5, "black"))

        self.white_pieces.append(Queen(7, 3, "white"))

        self.black_pieces.append(Queen(0, 3, "black"))
        

        for piece in self.white_pieces:
            self.board[piece.x][piece.y] = piece
        
        for piece in self.black_pieces:
            self.board[piece.x][piece.y] = piece
    
    # PRINTS BOARD
    def print_board(self):
        print("\t", end="")
        for i in range(8):
            print(string.ascii_lowercase[i], end="|\t")
        print()
        
        row = 8
        for i in range(8):
            print(row, end="|\t")
            row -= 1
            for j in range(8):
                print(self.board[i][j],end="\t")
            print()

################################
######## PIECES CLASSES ########
################################
class Pawn:
    def __init__(self,x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.name = "pawn"
        self.value = 1
        if color == "white":
            self.image = u'\u265F'
        else:
            self.image = u'\u2659'
        self.moves = list()
    
    # MOVES PIECE ON BOARD
    def move(self, x, y, chess_board : Board) -> bool:
        if not self.moves:
            return False
        if [(self.x, self.y), (x,y)] in self.moves:
            # current_piece = chess_board.board[self.x][self.y]
            start_loc_x = deepcopy(self.x)
            start_loc_y = deepcopy(self.y) 
            piece = chess_board.board[x][y]

            # removed_idx = -1
            removed_piece = None
            
            chess_board.board[self.x][self.y] = "-"
            self.x = x
            self.y = y
            
            if piece != "-":
                removed_piece = deepcopy(chess_board.board[x][y])
                if piece.color == "white":
                    chess_board.white_pieces.remove(piece)
                else:
                    chess_board.black_pieces.remove(piece)        
            chess_board.board[x][y] = self
            
            if chess_board.is_self_check():
                # UNDO MOVE IF CHECK
                if removed_piece != None:
                    if removed_piece.color == "white":
                        chess_board.white_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.white_pieces[-1]
                    else:
                        chess_board.black_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.black_pieces[-1]
                else:
                    chess_board.board[x][y] = "-"
                self.x = start_loc_x
                self.y = start_loc_y
                chess_board.board[self.x][self.y] = self
                # print("You are checked!")
                return False
            
            if chess_board.is_enemy_check():
                pass
            
            return True
        else:
            return False

    # FINDING POSSIBLE MOVES
    def possible_moves(self,chess_board : Board):
        self.moves.clear()
        if self.color == "white":
            if self.x != 0:
                if chess_board.board[self.x - 1][self.y] == "-":
                    self.moves.append([(self.x, self.y),(self.x - 1,self.y)])
                    if self.x == 6:
                        if chess_board.board[self.x - 2][self.y] == "-":
                            self.moves.append([(self.x, self.y),(self.x - 2,self.y)])
                if self.y == 0:
                    if chess_board.board[self.x - 1][self.y + 1] != "-":
                        if chess_board.board[self.x - 1][self.y + 1].color != "white":
                            self.moves.append([(self.x, self.y),(self.x - 1,self.y + 1)])
                elif self.y == 7:
                    if chess_board.board[self.x - 1][self.y - 1] != "-":
                        if chess_board.board[self.x - 1][self.y - 1].color != "white":
                            self.moves.append([(self.x, self.y),(self.x - 1,self.y - 1)])
                else:
                    if chess_board.board[self.x - 1][self.y + 1] != "-":
                        if chess_board.board[self.x - 1][self.y + 1].color != "white":
                            self.moves.append([(self.x, self.y),(self.x - 1,self.y + 1)])
                    
                    if chess_board.board[self.x - 1][self.y - 1] != "-":
                        piece = chess_board.board[self.x - 1][self.y - 1]
                        if piece.color != "white":    
                            self.moves.append([(self.x, self.y),(self.x - 1,self.y - 1)])
        
        if self.color == "black":
            if self.x != 7:
                if chess_board.board[self.x + 1][self.y] == "-":
                    self.moves.append([(self.x, self.y),(self.x + 1,self.y)])
                    if self.x == 1:
                        if chess_board.board[self.x + 2][self.y] == "-":
                            self.moves.append([(self.x, self.y),(self.x + 2,self.y)])
                if self.y == 0:
                    if chess_board.board[self.x + 1][self.y + 1] != "-":
                        if chess_board.board[self.x + 1][self.y + 1].color != "black":
                            self.moves.append([(self.x, self.y),(self.x + 1,self.y + 1)])
                elif self.y == 7:
                    if chess_board.board[self.x + 1][self.y - 1] != "-":
                        if chess_board.board[self.x + 1][self.y - 1].color != "black":
                            self.moves.append([(self.x, self.y),(self.x + 1,self.y - 1)])
                else:
                    if chess_board.board[self.x + 1][self.y + 1] != "-":
                        if chess_board.board[self.x + 1][self.y + 1].color != "black":
                            self.moves.append([(self.x, self.y),(self.x + 1,self.y + 1)])
                    
                    if chess_board.board[self.x + 1][self.y - 1] != "-":
                        if chess_board.board[self.x + 1][self.y - 1].color != "black":    
                            self.moves.append([(self.x, self.y),(self.x + 1,self.y - 1)])
                


    def __str__(self):
        return self.image
    
    def __repr__(self):
        return self.__str__()

class Rook:
    def __init__(self,x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.name = "rook"
        self.value = 5
        if color == "white":
            self.image = u'\u265C'
        else:
            self.image = u'\u2656'
        self.moves = list()
    
    # MOVES PIECE ON BOARD
    def move(self, x, y, chess_board : Board) -> bool:
        if not self.moves:
            return False
        if [(self.x, self.y), (x,y)] in self.moves:
            # current_piece = chess_board.board[self.x][self.y]
            start_loc_x = deepcopy(self.x)
            start_loc_y = deepcopy(self.y) 
            piece = chess_board.board[x][y]

            # removed_idx = -1
            removed_piece = None
            
            chess_board.board[self.x][self.y] = "-"
            self.x = x
            self.y = y
            
            if piece != "-":
                removed_piece = deepcopy(chess_board.board[x][y])
                if piece.color == "white":
                    chess_board.white_pieces.remove(piece)
                else:
                    chess_board.black_pieces.remove(piece)        
            chess_board.board[x][y] = self
            
            if chess_board.is_self_check():
                # UNDO MOVE
                if removed_piece != None:
                    if removed_piece.color == "white":
                        chess_board.white_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.white_pieces[-1]
                    else:
                        chess_board.black_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.black_pieces[-1]
                else:
                    chess_board.board[x][y] = "-"
                self.x = start_loc_x
                self.y = start_loc_y
                chess_board.board[self.x][self.y] = self
                # print("You are checked!")
                return False
            
            if chess_board.is_enemy_check():
                pass
            
            return True
        else:
            return False

    # FINDING POSSIBLE MOVES
    def possible_moves(self,chess_board : Board):
        self.moves.clear()
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8):
                new_x = self.x + d[0] * i
                new_y = self.y + d[1] * i
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if chess_board.board[new_x][new_y] == "-":
                        self.moves.append([(self.x, self.y),(new_x, new_y)])
                    else:
                        piece = chess_board.board[new_x][new_y]
                        if piece.color != self.color:
                            self.moves.append([(self.x, self.y),(new_x, new_y)])
                        break
                else: 
                    break

    
    def __str__(self):
        return self.image
    
    def __repr__(self):
        return self.__str__()

class Knight:
    def __init__(self,x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.name = "knight"
        self.value = 3
        if color == "white":
            self.image = u'\u265E'
        else:
            self.image = u'\u2658'
        self.moves = list()
    
    # MOVES PIECE ON BOARD
    def move(self, x, y, chess_board : Board) -> bool:
        if not self.moves:
            return False
        if [(self.x, self.y), (x,y)] in self.moves:
            # current_piece = chess_board.board[self.x][self.y]
            start_loc_x = deepcopy(self.x)
            start_loc_y = deepcopy(self.y) 
            piece = chess_board.board[x][y]

            # removed_idx = -1
            removed_piece = None
            
            chess_board.board[self.x][self.y] = "-"
            self.x = x
            self.y = y
            
            if piece != "-":
                removed_piece = deepcopy(chess_board.board[x][y])
                if piece.color == "white":
                    chess_board.white_pieces.remove(piece)
                else:
                    chess_board.black_pieces.remove(piece)        
            chess_board.board[x][y] = self
            
            if chess_board.is_self_check():
                # UNDO MOVE
                if removed_piece != None:
                    if removed_piece.color == "white":
                        chess_board.white_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.white_pieces[-1]
                    else:
                        chess_board.black_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.black_pieces[-1]
                else:
                    chess_board.board[x][y] = "-"
                self.x = start_loc_x
                self.y = start_loc_y
                chess_board.board[self.x][self.y] = self
                # print("You are checked!")
                return False
            
            if chess_board.is_enemy_check():
                pass
            
            return True
        else:
            return False

    # FINDING POSSIBLE MOVES
    def possible_moves(self,chess_board : Board):
        self.moves.clear()
        directions = ((-1,-2), (-2,-1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2))
        for d in directions:
            new_x = self.x + d[0]
            new_y = self.y + d[1]
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                if chess_board.board[new_x][new_y] == "-":
                    self.moves.append([(self.x, self.y),(new_x, new_y)])
                else:
                    piece = chess_board.board[new_x][new_y]
                    if piece.color != self.color:
                        self.moves.append([(self.x, self.y),(new_x, new_y)])

    def __str__(self):
        return self.image
    
    def __repr__(self):
        return self.__str__()

class Bishop:
    def __init__(self,x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.name = "bishop"
        self.value = 3
        if color == "white":
            self.image = u'\u265D'
        else:
            self.image = u'\u2657'
        self.moves = list()
    
    # MOVES PIECE ON BOARD
    def move(self, x, y, chess_board : Board) -> bool:
        if not self.moves:
            return False
        if [(self.x, self.y), (x,y)] in self.moves:
            # current_piece = chess_board.board[self.x][self.y]
            start_loc_x = deepcopy(self.x)
            start_loc_y = deepcopy(self.y) 
            piece = chess_board.board[x][y]

            # removed_idx = -1
            removed_piece = None
            
            chess_board.board[self.x][self.y] = "-"
            self.x = x
            self.y = y
            
            if piece != "-":
                removed_piece = deepcopy(chess_board.board[x][y])
                if piece.color == "white":
                    chess_board.white_pieces.remove(piece)
                else:
                    chess_board.black_pieces.remove(piece)        
            chess_board.board[x][y] = self
            
            if chess_board.is_self_check():
                # UNDO MOVE
                if removed_piece != None:
                    if removed_piece.color == "white":
                        chess_board.white_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.white_pieces[-1]
                    else:
                        chess_board.black_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.black_pieces[-1]
                else:
                    chess_board.board[x][y] = "-"
                self.x = start_loc_x
                self.y = start_loc_y
                chess_board.board[self.x][self.y] = self
                # print("You are checked!")
                return False
            
            if chess_board.is_enemy_check():
                pass
            
            return True
        else:
            return False

    # FINDING POSSIBLE MOVES
    def possible_moves(self,chess_board : Board):
        self.moves.clear()
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1))
        for d in directions:
            for i in range(1, 8):
                new_x = self.x + d[0] * i
                new_y = self.y + d[1] * i
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if chess_board.board[new_x][new_y] == "-":
                        self.moves.append([(self.x, self.y),(new_x, new_y)])
                    else:
                        piece = chess_board.board[new_x][new_y]
                        if piece.color != self.color:
                            self.moves.append([(self.x, self.y),(new_x, new_y)])
                        break
                else: 
                    break

    
    def __str__(self):
        return self.image
    
    def __repr__(self):
        return self.__str__()

class Queen:
    def __init__(self,x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.name = "queen"
        self.value = 9
        if color == "white":
            self.image = u'\u265B'
        else:
            self.image = u'\u2655'
        self.moves = list()
    
    # MOVES PIECE ON BOARD
    def move(self, x, y, chess_board : Board) -> bool:
        if not self.moves:
            return False
        if [(self.x, self.y), (x,y)] in self.moves:
            # current_piece = chess_board.board[self.x][self.y]
            start_loc_x = deepcopy(self.x)
            start_loc_y = deepcopy(self.y) 
            piece = chess_board.board[x][y]

            # removed_idx = -1
            removed_piece = None
            
            chess_board.board[self.x][self.y] = "-"
            self.x = x
            self.y = y
            
            if piece != "-":
                removed_piece = deepcopy(chess_board.board[x][y])
                if piece.color == "white":
                    chess_board.white_pieces.remove(piece)
                else:
                    chess_board.black_pieces.remove(piece)        
            chess_board.board[x][y] = self
            
            if chess_board.is_self_check():
                # UNDO MOVE
                if removed_piece != None:
                    if removed_piece.color == "white":
                        chess_board.white_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.white_pieces[-1]
                    else:
                        chess_board.black_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.black_pieces[-1]
                else:
                    chess_board.board[x][y] = "-"
                self.x = start_loc_x
                self.y = start_loc_y
                chess_board.board[self.x][self.y] = self
                # print("You are checked!")
                return False
            
            if chess_board.is_enemy_check():
                pass
            
            return True
        else:
            return False

    # FINDING POSSIBLE MOVES
    def possible_moves(self,chess_board : Board):
        self.moves.clear()
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            for i in range(1, 8):
                new_x = self.x + d[0] * i
                new_y = self.y + d[1] * i
                if 0 <= new_x < 8 and 0 <= new_y < 8:
                    if chess_board.board[new_x][new_y] == "-":
                        self.moves.append([(self.x, self.y),(new_x, new_y)])
                    else:
                        piece = chess_board.board[new_x][new_y]
                        if piece.color != self.color:
                            self.moves.append([(self.x, self.y),(new_x, new_y)])
                        break
                else: 
                    break

    
    def __str__(self):
        return self.image
    
    def __repr__(self):
        return self.__str__()

class King:
    def __init__(self,x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.name = "king"
        self.value = 900
        if color == "white":
            self.image = u'\u265A'
        else:
            self.image = u'\u2654'
        self.moves = list()
    
    # MOVES PIECE ON BOARD
    def move(self, x, y, chess_board : Board) -> bool:
        if not self.moves:
            return False
        if [(self.x, self.y), (x,y)] in self.moves:
            # current_piece = chess_board.board[self.x][self.y]
            start_loc_x = deepcopy(self.x)
            start_loc_y = deepcopy(self.y) 
            piece = chess_board.board[x][y]

            # removed_idx = -1
            removed_piece = None
            
            chess_board.board[self.x][self.y] = "-"
            self.x = x
            self.y = y
            
            if piece != "-":
                removed_piece = deepcopy(chess_board.board[x][y])
                if piece.color == "white":
                    chess_board.white_pieces.remove(piece)
                else:
                    chess_board.black_pieces.remove(piece)        
            chess_board.board[x][y] = self
            
            if self.color == "white":
                chess_board.white_king_loc = (x ,y)
            else:
                chess_board.black_king_loc = (x ,y)

            if chess_board.is_self_check():
                # UNDO MOVE
                if removed_piece != None:
                    if removed_piece.color == "white":
                        chess_board.white_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.white_pieces[-1]
                    else:
                        chess_board.black_pieces.append(removed_piece)
                        chess_board.board[x][y] = chess_board.black_pieces[-1]
                else:
                    chess_board.board[x][y] = "-"
                self.x = start_loc_x
                self.y = start_loc_y
                chess_board.board[self.x][self.y] = self

                if self.color == "white":
                    chess_board.white_king_loc = (start_loc_x ,start_loc_y)
                else:
                    chess_board.black_king_loc = (start_loc_x ,start_loc_y)
                # print("You are checked!")
                return False
            
            if chess_board.is_enemy_check():
                pass
            
            return True
        else:
            return False

    # FINDING POSSIBLE MOVES
    def possible_moves(self,chess_board : Board):
        self.moves.clear()
        directions = ((-1, -1), (-1, 1), (1, -1), (1, 1), (-1, 0), (0, -1), (1, 0), (0, 1))
        for d in directions:
            new_x = self.x + d[0]
            new_y = self.y + d[1]
            if 0 <= new_x < 8 and 0 <= new_y < 8:
                if chess_board.board[new_x][new_y] == "-":
                    self.moves.append([(self.x, self.y),(new_x, new_y)])
                else:
                    piece = chess_board.board[new_x][new_y]
                    if piece.color != self.color:
                        self.moves.append([(self.x, self.y),(new_x, new_y)])
    
    def __str__(self):
        return self.image
    
    def __repr__(self):
        return self.__str__()
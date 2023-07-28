###################################################
#################### RUNS GAME ####################

import math
from chess_pieces import *
import random

# DICTIONARIES USED FOR INDEXING
cols = {
    "a": 0,
    "b": 1,
    "c": 2,
    "d": 3,
    "e": 4,
    "f": 5,
    "g": 6,
    "h": 7,
}

rows = {
    "8": 0,
    "7": 1,
    "6": 2,
    "5": 3,
    "4": 4,
    "3": 5,
    "2": 6,
    "1": 7,
}

inv_cols = {
    0: "a",
    1: "b",
    2: "c",
    3: "d",
    4: "e",
    5: "f",
    6: "g",
    7: "h",
}

inv_rows = {
    0: "8",
    1: "7",
    2: "6",
    3: "5",
    4: "4",
    5: "3",
    6: "2",
    7: "1",
}

def print_pieces(pieces):
    for piece in pieces:
        print(f"{piece}: {inv_cols[piece.y]}{inv_rows[piece.x]}")


# FUNCTION USED TO PLAY GAME
def run_game():
    my_board = Board()
    my_board.initialize()

    maximizer = True
    while(1):
        # PRINTING BOARD
        print(my_board.turn.capitalize(), "'s Turn")
        my_board.print_board()
        if my_board.is_self_checkmate():
            print("You have been Check mated!")
            if(my_board.turn == "white"):
                print("Black Wins!")
            if(my_board.turn == "black"):
                print("White Wins!")
            break
        if my_board.is_self_check():
            print("You have been Checked!")
        
        ################################  BLACK'S TURN  ########################################
        if maximizer == True:
            print("Finding best move...")
            
            # FINDS BEST MOVE FOR AI (BLACK) USING ALPHA BETA PRUNING
            best_move, eval = ab_pruning(my_board, 3, -100000, 100000, maximizer)
            
            print(f"Best_move: {inv_cols[best_move[0][1]]}{inv_rows[best_move[0][0]]} -> {inv_cols[best_move[1][1]]}{inv_rows[best_move[1][0]]}")
            start_loc = best_move[0]
            end_loc = best_move[1]
            
            captured_piece = deepcopy(my_board.board[end_loc[0]][end_loc[1]])
            
            # APPLYING MOVE
            moved = my_board.move(start_loc[0], start_loc[1], end_loc[0], end_loc[1])
            
            if(moved == False):
                print("Invalid input, cannot move there")
                continue
            else:
                white_piece = my_board.board[end_loc[0]][end_loc[1]]
                print(f"{white_piece.name}: {inv_cols[best_move[1][1]]}{inv_rows[best_move[1][0]]}")
                if captured_piece != "-":
                    print("White Captured: ", captured_piece.name)
                my_board.turn = "black" if my_board.turn == "white" else "white"
                maximizer = False
            continue

        # best_move, eval = ab_pruning(my_board, 3, -100000, 100000, maximizer)

        # print(f"Best_move: {inv_cols[best_move[0][1]]}{inv_rows[best_move[0][0]]} -> {inv_cols[best_move[1][1]]}{inv_rows[best_move[1][0]]}")
        # start_loc = best_move[0]
        # end_loc = best_move[1]
        # moved = my_board.move(start_loc[0], start_loc[1], end_loc[0], end_loc[1])
        # my_board.print_board()
        
        ################################  WHITE'S TURN  ########################################
        
        # TAKING INPUT FROM USER
        start_loc = input("Enter location of piece to move <letter><number>: ")
        if start_loc == "E":
            break
        try:
            x = rows[start_loc[1]]
            y = cols[start_loc[0].lower()]
        except:
            print("Invalid input format")
            continue
        is_valid, msg = my_board.is_valid_selection(x ,y)
        if is_valid == False:
            print(msg)
            continue
        new_loc = input("Enter new location of piece to move <letter><number>: ")
        new_x = rows[new_loc[1]]
        new_y = cols[new_loc[0].lower()]
        
        captured_piece = deepcopy(my_board.board[new_x][new_y])
        
        # APPLYING MOVE
        moved = my_board.move(x, y, new_x, new_y)
        
        if(moved == False):
            print("Invalid input, cannot move there")
            continue
        else:
            black_piece = my_board.board[new_x][new_y]
            print(black_piece.name + ": " + new_loc[0].lower() + new_loc[1])
            if captured_piece != "-":
                print("Black Captured: ", captured_piece.name)
            my_board.turn = "black" if my_board.turn == "white" else "white"
            maximizer = True


# MAXIMIZING PLAYER 1 -> WHITE
# MAXIMIZING PLAYER 0 -> BLACK
def ab_pruning(chess_board : Board, depth, alpha : int, beta : int, maximizingPlayer : bool):
    if depth == 0 or chess_board.is_self_checkmate():
        # CALCULATING HEURISTIC OF CURRENT POSITION ON BOARD
        chess_board.calculate_static_eval()
        return None, chess_board.score
    
    if maximizingPlayer:
        # GETTING ALL POSSIBLE MOVES FOR WHITE IN CURRENT BOARD
        white_moves = list()
        for piece in chess_board.white_pieces:
            piece.possible_moves(chess_board)
            white_moves += piece.moves
        
        optimal_move = random.choice(white_moves)
        
        maxEval = -100000 # NEGATIVE INFINITY
        random.shuffle(white_moves)
        for move in white_moves:
            start = move[0]
            dest = move[1]
            new_chess_board = deepcopy(chess_board)
            moved = new_chess_board.move(start[0], start[1], dest[0], dest[1])
            if moved:
                new_chess_board.turn = "black"
                eval = ab_pruning(new_chess_board, depth - 1, alpha, beta, False)[1]
                # CHOOSING BEST EVAL FOR WHITE
                if eval > maxEval:
                    maxEval = eval
                    optimal_move = move
                alpha = max(alpha, eval)
                
                # PRUNIG PATH IF REQUIRED
                if beta <= alpha:
                    break
        return optimal_move, maxEval
    
    else:
        # GETTING ALL POSSIBLE MOVES FOR BLACK IN CURRENT BOARD
        black_moves = list()
        for piece in chess_board.black_pieces:
            piece.possible_moves(chess_board)
            black_moves += piece.moves

        optimal_move = random.choice(black_moves)

        minEval = 100000 # POSITIVE INFINITY
        random.shuffle(black_moves)
        for move in black_moves:
            start = move[0]
            dest = move[1]
            new_chess_board = deepcopy(chess_board)
            moved = new_chess_board.move(start[0], start[1], dest[0], dest[1])
            if moved:
                new_chess_board.turn = "white"
                eval = ab_pruning(new_chess_board, depth - 1, alpha, beta, True)[1]
                # CHOOSING BEST EVAL FOR BLACK
                if eval < minEval:
                    minEval = eval    
                    optimal_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return optimal_move, minEval

def main():

    my_board = Board()
    my_board.initialize()

    while(1):
        print(my_board.turn.capitalize(), "'s Turn")
        my_board.print_board()
        if my_board.is_self_checkmate():
            print("You have been Check mated!")
            break
        # (1,6), (2,5)
        start_loc = input("Enter location of piece to move: ")
        if start_loc == "E":
            break
        try:
            x = rows[start_loc[1]]
            y = cols[start_loc[0].lower()]
        except:
            print("Invalid input format")
            continue
        is_valid, msg = my_board.is_valid_selection(x ,y)
        if is_valid == False:
            print(msg)
            continue
        new_loc = input("Enter new location of piece to move: ")
        new_x = rows[new_loc[1]]
        new_y = cols[new_loc[0].lower()]
        
        moved = my_board.move(x, y, new_x, new_y)
        if(moved == False):
            print("Invalid input, cannot move there")
            continue
        else:
            my_board.turn = "black" if my_board.turn == "white" else "white"
        
    
run_game() # USED FOR PLAYER VS AI
# main() # USED FOR PLAYER VS PLAYER
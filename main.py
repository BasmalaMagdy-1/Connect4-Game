import numpy as np
import random
import pygame
import sys
import math
import time
import tkinter as tk
from tkinter import *

import Board
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
EMPTY = 0
PLAYER_PIECE = 1
AI_PIECE = 2
ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER = 0
AI = 1


WINDOW_LENGTH = 4


def create_board():
    #board=Board()
    board = np.zeros((ROW_COUNT,COLUMN_COUNT))
    return board

def print_board(board):
    #np.flip(board, 0)
    for r in range(5,-1,-1):
        row=""
        for c in range(7):
            if(board[r][c]==0):
                row+='*'
            if (board[r][c] == 1):
                row+='R'
            if (board[r][c] == 2):
                row+='B'
        print(row)
    print("-------------------------")


def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def drop_piece(board, row, col, piece):
    board[row][col] = piece



def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(7 - 3):
        for r in range(6):
            if board[r][c] == board[r][c + 1] and board[r][c] == board[r][c + 2] and board[r][c] == board[r][c + 3] and \
                    board[r][c] == piece:
                return True

    # Check vertical locations for win
    for c in range(7):
        for r in range(6 - 3):
            if board[r][c] == board[r + 1][c] and board[r][c] == board[r + 2][c] and board[r][c] == board[r + 3][c] and \
                    board[r][c] == piece:
                return True

    # Check positively sloped diaganols
    for c in range(7 - 3):
        for r in range(6 - 3):
            if board[r][c] == board[r + 1][c + 1] and board[r][c] == board[r + 2][c + 2] and board[r][c] == \
                    board[r + 3][c + 3] and board[r][c] == piece:
                return True

    # Check negatively sloped diaganols
    for c in range(7 - 3):
        for r in range(3, 6):
            if board[r][c] == board[r - 1][c + 1] and board[r][c] == board[r - 2][c + 2] and board[r][c] == \
                    board[r - 3][c + 3] and board[r][c] == piece:
                return True
    return False


def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE
    if piece == opp_piece:
        opp_piece = AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

def is_terminal_node(board):
    return winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(get_valid_locations(board)) == 0



def score_position(board, piece):
    score = 0

    ## Score center column
    center_array = [int(i) for i in list(board[:, 7 // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    ## Score Horizontal
    for r in range(6):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(7 - 3):
            window = row_array[c:c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score Vertical
    for c in range(7):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(6 - 3):
            window = col_array[r:r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    ## Score posiive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

def minimax_withoutAlphBeta(board, depth, maximizing_player):
    valid_locations = [col for col in range(COLUMN_COUNT) if is_valid_location(board, col)]
    is_terminal = winning_move(board, PLAYER_PIECE) or winning_move(board, AI_PIECE) or len(valid_locations) == 0
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -100000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if not maximizing_player:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, PLAYER_PIECE)
            new_score = minimax_withoutAlphBeta(temp_board, depth - 1, True)[1]
            if new_score < value:
                value = new_score
                column = col
        return column, value
    else:
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            temp_board = board.copy()
            drop_piece(temp_board, row, col, AI_PIECE)
            new_score = minimax_withoutAlphBeta(temp_board, depth - 1, False)[1]
            if new_score > value:
                value = new_score
                column = col
        return column, value


def minimax(board, depth, alpha, beta, maximizingPlayer):
    valid_locations = get_valid_locations(board)
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:  # Game is over, no more valid moves
                return (None, 0)
        else:  # Depth is zero
            return (None, score_position(board, AI_PIECE))
    if not maximizingPlayer:
        value = math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < value:
                value = new_score
                column = col
            beta = min(beta, value)
            if alpha >= beta:
                break
        return column, value

    else:  # Minimizing player
        value = -math.inf
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1]
            if new_score > value:
                value = new_score
                column = col
            alpha = max(alpha, value)
            if alpha >= beta:
                break
        return column, value



def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations


def pick_best_move(board, piece):
    valid_locations = get_valid_locations(board)
    best_score = -10000
    best_col = random.choice(valid_locations)
    for col in valid_locations:
        row = get_next_open_row(board, col)
        temp_board = board.copy()
        drop_piece(temp_board, row, col, piece)
        score = score_position(temp_board, piece)
        if score > best_score:
            best_score = score
            best_col = col

    return best_col

'''def clickButton(root):
     draw_board()
def gui():
    root = Tk()

    # Adding widgets
    # Label
    lbl = Label(root, text="Enter difficulty level:")
    lbl.grid(row=0, column=0)

    # Entry
    e = Entry(root)
    type = e
    e.grid(row=0, column=1)
    exitButton = Button(root, text="Exit", command=clickButton(root))

    # Enter the main Loop
    root.mainloop()
    root.destroy()
'''
def draw_board(board):

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, WHITE, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (
            int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == PLAYER_PIECE:
                pygame.draw.circle(screen, RED, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == AI_PIECE:
                pygame.draw.circle(screen, BLUE, (
                int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()


board = create_board()
#(newboard,game_end)=board.get_game_grid(board)
#board.print_grid(board,newboard)
print("Enter the required difficulty level")
print("Enter 1 for easy level")
print("Enter 2 for meduim level")
print("Enter 3 for hard level")
type=int(input())
while(type!=1 and type !=2 and type!=3):
    print("invalid type,please try again :)")
    print("Enter the required difficulty level")
    print("Enter 1 for easy level")
    print("Enter 2 for meduim level")
    print("Enter 3 for hard level")
    type = int(input())
print("Enter the required algorithm")
print("Enter 1 for Min-max")
print("Enter 2 for Min-max with alpha-beta brunning")
type2=int(input())
while(type2!=1 and type2 !=2 ):
    print("invalid type,please try again :)")
    print("Enter the required algorithm")
    print("Enter 1 for Min-max")
    print("Enter 2 for Min-max with alpha-beta brunning")
    type2 = int(input())

print_board(board)
game_over = False

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()

myfont = pygame.font.SysFont("monospace", 75)

turn = random.randint(PLAYER, AI)

while not game_over:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

            # print(event.pos)
            # Ask for Player 1 Input
        if turn == PLAYER and not game_over:#computer
            random_column = random.randint(0, 6)

            if is_valid_location(board, random_column):
                row = get_next_open_row(board, random_column)
                drop_piece(board, row, random_column, PLAYER_PIECE)

                if winning_move(board, PLAYER_PIECE):
                    label = myfont.render("Player 1 wins!!", 1, RED)
                    screen.blit(label, (40, 10))
                    game_over = True

                turn ^=1

                print_board(board)
                draw_board(board)
                #(newboard, game_end) = board.get_game_grid(board)
                #board.print_grid(board, newboard)

                time.sleep(1)

    # # Ask for Player 2 Input
    if turn == AI and not game_over:
        depth=0
        if type==1:
            depth=3
        elif type==2:
            depth=4
        elif type==3:
            depth=5
        if type2==2:
           col, minimax_score = minimax(board, depth, -math.inf, math.inf, True)
        elif type2==1:
            col, minimax_score = minimax_withoutAlphBeta(board, depth,True)
        if is_valid_location(board, col):
            row = get_next_open_row(board, col)
            drop_piece(board, row, col, AI_PIECE)

            if winning_move(board, AI_PIECE):
                label = myfont.render("Player 2 wins!!", 1, BLUE)
                screen.blit(label, (40, 10))
                game_over = True

            draw_board(board)
           # (newboard, game_end) = board.get_game_grid(board)
            print_board(board)


            time.sleep(1)
            turn^=1

    if game_over:
        pygame.time.wait(1000)
from operator import le
from random import randint
import copy

def random_move(board, num_cols, num_rows, inrow):
    cols = []
    for i in range(num_cols):
        if board[0][i] == 0:
            cols.append(i)
        
    x = randint(0, len(cols)-1)
    return cols[x]



def valid_coordinate(num_cols, num_rows, x, y):
    if x<0 or x>=num_rows or y<0 or y>=num_cols:
        return 0
    return 1


def count_inrow_v(board, num_cols, num_rows, inrow, count, player, x, y):
    c = 0
    for i in range(x, x+inrow):
        if not valid_coordinate(num_cols, num_rows, i, y):  return 0
        if board[i][y] == player:
            c+=1
        elif board[i][y] != 0:   return 0
    return c==count

def count_inrow_h(board, num_cols, num_rows, inrow, count, player, x, y):
    c = 0
    for i in range(y, y+inrow):
        if not valid_coordinate(num_cols, num_rows, x, i):  return 0
        if board[x][i] == player:
            c+=1
        elif board[x][i] != 0:   return 0
    return c==count

def count_inrow_d1(board, num_cols, num_rows, inrow, count, player, x, y):
    c = 0
    for i in range(inrow):
        if not valid_coordinate(num_cols, num_rows, x+i, y-i):  return 0
        if board[x+i][y-i] == player:
            c+=1
        elif board[x+i][y-i] != 0:   return 0
    return c==count

def count_inrow_d2(board, num_cols, num_rows, inrow, count, player, x, y):
    c = 0
    for i in range(inrow):
        if not valid_coordinate(num_cols, num_rows, x+i, y+i):  return 0
        if board[x+i][y+i] == player:
            c+=1
        elif board[x+i][y+i] != 0:   return 0
    return c==count
        

def count_inrow(board, num_cols, num_rows, inrow, count, player):
    c = 0
    #print(f'count inrow count:{count} player:{player}')
    for i in range(num_rows):
        for j in range(num_cols):
            c+=count_inrow_v(board, num_cols, num_rows, inrow, count, player, i, j)
            c+=count_inrow_h(board, num_cols, num_rows, inrow, count, player, i, j)
            c+=count_inrow_d1(board, num_cols, num_rows, inrow, count, player, i, j)
            c+=count_inrow_d2(board, num_cols, num_rows, inrow, count, player, i, j)
            #print(f'  {i}, {j}: {c}')
    return c


def drop(board, col, num_rows, player):
    row = 0
    while row+1<num_rows and board[row+1][col]==0:
        row+=1
    board[row][col] = player
    return board


def calc_value(board, num_cols, num_rows, inrow, player):
    p_4 = count_inrow(board, num_cols, num_rows, inrow, inrow, 3-player)
    p_3 = count_inrow(board, num_cols, num_rows, inrow, inrow-1, 3-player)
    p_2 = count_inrow(board, num_cols, num_rows, inrow, inrow-2, 3-player)

    a_4 = count_inrow(board, num_cols, num_rows, inrow, inrow, player)
    a_3 = count_inrow(board, num_cols, num_rows, inrow, inrow-1, player)
    a_2 = count_inrow(board, num_cols, num_rows, inrow, inrow-2, player)

    value = 100000000*a_4 + 1000*a_3 + 1*a_2 - 100*p_2 - 10000*p_3 - 1000000*p_4
    return value


def possible_moves(board, num_cols):
    cols = []
    for i in range(num_cols):
        if board[0][i] == 0:
            cols.append(i)
    return cols

def one_move_lookahead(board, num_cols, num_rows, inrow):
    
    cols = possible_moves(board, num_cols)
    max_value = -1000000
    best_cols = [cols[0]]

    for col in cols:
        #print(f'\n\n\n\n\n col: {col}')
        new_board = drop(copy.deepcopy(board), col, num_rows, 2)
        #print(new_board)
        value = calc_value(new_board, num_cols, num_rows, inrow, 2)

        if value > max_value:
            max_value = value
            best_cols = [col]
        elif value==max_value:
            best_cols.append(col)

    x = randint(0, len(best_cols)-1)
    return best_cols[x]


def game_over(board, num_cols, num_rows, inrow):
    if count_inrow(board, num_cols, num_rows, inrow, inrow, 1) or count_inrow(board, num_cols, num_rows, inrow, inrow, 2):
        return True
    return False


def minimax(board, num_cols, num_rows, inrow, depth, player):
    if game_over(board, num_cols, num_rows, inrow) or depth==0:
        return calc_value(board, num_cols, num_rows, inrow, player), []
    

    cols = possible_moves(board, num_cols)
    #player is either 1 (for player ) or 2 (agent - who we want to win)
    if player==2:
        best_score = float('-inf')
        best_move = None
        for col in cols:
            new_board = drop(copy.deepcopy(board), col, num_rows, player)
            value, _ = minimax(new_board, num_cols, num_rows, inrow, depth-1, 1)
            if value > best_score:
                best_score = value
                best_move = [col]
            elif value==best_score:
                best_move.append(col)
    if player==1:
        best_score = float('inf')
        best_move = None
        for col in cols:
            new_board = drop(copy.deepcopy(board), col, num_rows, player)
            value, _ = minimax(new_board, num_cols, num_rows, inrow, depth-1, 2)
            if value < best_score:
                best_score = value
                best_move = [col]
            elif value==best_score:
                best_move.append(col)
    return best_score, best_move




def minimax_alpha_beta(board, num_cols, num_rows, inrow, depth, player, alpha, beta):
    cols = possible_moves(board, num_cols)
    if len(cols) == 0 or depth==0:
        return calc_value(board, num_cols, num_rows, inrow, player), []
    
    #player is either 1 (for player ) or 2 (agent - who we want to win)
    if player==2:
        best_score = float('-inf')
        best_move = None
        for col in cols:
            new_board = drop(copy.deepcopy(board), col, num_rows, player)
            value, _ = minimax_alpha_beta(new_board, num_cols, num_rows, inrow, depth-1, 1, alpha, beta)
            if value > best_score:
                best_score = value
                best_move = [col]
            elif value==best_score:
                best_move.append(col)
            if best_score>beta:
                break
            alpha = max(alpha, best_score)
    if player==1:
        best_score = float('inf')
        best_move = None
        for col in cols:
            new_board = drop(copy.deepcopy(board), col, num_rows, player)
            value, _ = minimax_alpha_beta(new_board, num_cols, num_rows, inrow, depth-1, 2, alpha, beta)
            if value < best_score:
                best_score = value
                best_move = [col]
            elif value==best_score:
                best_move.append(col)
            if best_score<alpha:
                break
            beta = min(beta, best_score)
    return best_score, best_move



def n_moves_lookahead(board, num_cols, num_rows, inrow, n=4):
    best_score, best_move = minimax(board, num_cols, num_rows, inrow, n, 2)
    x = randint(0, len(best_move)-1)
    return best_move[x]

def n_moves_lookahead_alpha_beta(board, num_cols, num_rows, inrow, n=4):
    best_score, best_move = minimax_alpha_beta(board, num_cols, num_rows, inrow, n, 2, float('-inf'), float('inf'))
    x = randint(0, len(best_move)-1)
    return best_move[x]


    

def move(board, num_cols, num_rows, inrow):
    #return random_move(board, num_cols, num_rows, inrow)
    #return one_move_lookahead(board, num_cols, num_rows, inrow)
    #return n_moves_lookahead(board, num_cols, num_rows, inrow)
    return n_moves_lookahead_alpha_beta(board, num_cols, num_rows, inrow)
    

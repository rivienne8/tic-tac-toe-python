import sys
import os
import random
import string

ZNAK_A = ord("A")  #jako zmienna globalna
player_1 = "X"
player_2 = "O"

def init_board(row_count):
    """Returns an empty 3-by-3 board (with .)."""
    board = []
    for i in range(0,row_count):
        position_list = []
        for i in range(0,row_count):
            position_list.append(".")
        board.append(position_list)
    return board


def get_move(board, player):
    """Returns the coordinates of a valid move for player on board."""
    letter = list(string.ascii_lowercase)
    number = list(range(1,30))
    # letter = []
    # number = []
    # for i in range(1,len(board)+1):
    #     letter.append((chr(ZNAK_A+i)).lower())
    #     number.append(i+1)

    board_names = []  
    for i in range(0,len(board)):
        for j in range(0,len(board)):
            board_names.append(letter[i]+str(number[j]))
    # wszsystkie zmienne po angielsku
    ruch = player_input(f"\033[;31mQuit\033[;0m or {player} give your move: ").lower()    
    while True: # dać jakiś warunek, żeby sie konczyła
        if ruch in board_names:
            r = ruch[0]
            c = int(ruch[1])
            for i in range(0, len(board)):
                if r == letter[i]:
                    row = i
            for i in range(0, len(board)):
                if c == number[i]:
                    col = i
            if board[row][col] != ".":
                ruch = player_input("Quit or give new move? ").lower()
                continue
            else:
                #print(row, col)
                return row, col
        else:
            ruch = player_input("Wrong move, try again or quit!: ").lower()
           
    # return row, col ==>niepotrzebna


def AI_move_diag_easy_win(board, player, is_reversed=""):
    row, col = -1, -1
    diag_sign_count = 0
    empty_count = 0
    enemy_sign = False
    while empty_count <= 1 and diag_sign_count <len(board)-1 and not enemy_sign:
        for i in range(0,len(board)):
            j = i
            if is_reversed == "up":
                j = len(board)-1-i 

            if board[i][j] == player:
                diag_sign_count += 1
            elif board[i][j] == ".":
                empty_count +=1
                missing_index, missing_2index = i,j                
            else:
                row, col = -1, -1
                enemy_sign = True

    if empty_count == 1 and diag_sign_count == len(board) - 1:      
        row, col = missing_index, missing_2index

    return row, col


def AI_move_row_easy_win(board,player, vertical=""): 
    row, col = -1, -1
    row_potential = []
    if vertical == "col":
        board= [[row[i] for row in board] for i in range(0,len(board))]
    for i in range(0,len(board)):
        for j in range(0,len(board)):
            if board[i][j] == player:
                row_potential.append((i,j))
        if len(row_potential) == len(board) - 1:
            if "." in board[i]:
                missing_index = board[i].index(".")
                row, col = i,missing_index                
        row_potential.clear()
            
    if vertical == "col":
        board = [[row[i] for row in board] for i in range(0,len(board))]
        return col, row
    else:
        return row, col


def AI_easy_win(board,player):
    row, col = -1, -1
    row, col = AI_move_row_easy_win(board,player,) # i row, col w parametrach,wtedy if w jednym poziomie czy True / False
    if row == -1:
        row, col = AI_move_row_easy_win(board, player,"col")
        if row == -1:
            row, col = AI_move_diag_easy_win(board, player)
            if row == -1:
                row, col = AI_move_diag_easy_win(board,player, "up")

    return row, col


def AI_prevents_easy_lose(board,player):
    if player == player_1:
        player = player_2
    else:
        player = player_1

    row, col = AI_easy_win(board,player)

    return row, col


def best_choice_for_3x3():
    best_choice = random.choice([(0,0),(0,2), (2,2),(2,0)])
    return  best_choice[0],best_choice[1]
    

def AI_try_not_loose(board,player):    
    row, col = -1,-1
    if len(board) ==3:
        list_of_position_in_board = []
        for i in range(0,len(board)):
            list_of_position_in_board += board[i]
        if all(position == "." for position in list_of_position_in_board):        
            row, col = best_choice_for_3x3()
        elif player == player_2 and all(position != player for position in list_of_position_in_board):
            if board[1][1] == ".":
                row, col = 1,1
            else:
                row, col = best_choice_for_3x3()
        elif player == player_1:
            if board[1][1] == ".":
                row, col = 1,1
            else:
                corner_count = 0
                while corner_count<=3:
                    row, col = best_choice_for_3x3()
                    if board[row][col] != ".":
                        row, col = -1,-1
                        corner_count +=1 
             
    
    return row, col


def get_ai_move(board,player):
    """Returns the coordinates of a valid move for player on board."""
    row, col = AI_easy_win(board,player)
    if row == -1 :
        row, col = AI_prevents_easy_lose(board,player)
        if row == -1:             
            row, col = AI_try_not_loose(board,player)
            if row == -1:
                possible_moves = []
                for i in range(0,len(board)):
                    for j in range(0,len(board)):
                        if board[i][j] == ".":
                            possible_moves.append((i,j))
                    
                move = random.choice(possible_moves)
                row = move[0]
                col = move[1]
    
    return row, col


def mark(board, player, row, col):
    """Marks the element at row & col on the board for player."""
    if board[row][col] == ".":
        board[row][col] = player
    else:
        print("Next turn")
    
    return board


def has_won(board, player):
    """Returns True if player has won the game."""
    result_list = set()
    for i in range(0,len(board)):    
        result = all(position == player for  position in board[i])
        result_list.add(result)

    transpose_board = [[row[i] for row in board] for i in range(0,len(board))]    
    for i in range(0,len(transpose_board)):
        result = all(position == player for  position in transpose_board[i])
        result_list.add(result)        

    diagonal_down = [] 
    diagonal_up = [] 
    for i in range(0,len(board)):
        diagonal_down.append(board[i][i])
    result = all(position == player for position in diagonal_down)
    result_list.add(result)

    for i in range(0,len(board)):
        k = len(board)-1-i
        diagonal_up.append(board[i][k])   
    result = all(position == player for position in diagonal_up) 
    result_list.add(result) 
  
    result = any(result_list)
    
    return result


def check_diagonal_position_equal(list,sign, is_reversed=""):
    coordinates_list = []
    if  all(position == sign for  position in list) == True:
        if is_reversed == "up":
            for i in range(0,len(list)):
                coordinates_list.append((i,len(list)-1-i))
        else:
            for i in range(0,len(list)):
                coordinates_list.append((i,i))
    return coordinates_list 


def check_all_position_equal(board,sign, vertical=""):
    coordinates_list = []
    for i in range(0,len(board)):    
        if  all(position == sign for  position in board[i]) == True:
            if vertical == "col":
                for j in range(0,len(board)):
                    coordinates_list.append((j,i))
            else:    
                for j in range(0,len(board)):
                    coordinates_list.append((i,j))
    
    return coordinates_list    


def find_win_coordinates(board,sign):    
    transpose_board = [[row[i] for row in board] for i in range(0,len(board))]
    diagonal_down = [board[i][i] for i in range(0,len(board))]
    diagonal_up = [board[i][len(board)-1-i] for i in range(0,len(board))]
        
    win_row_coordinates = check_all_position_equal(board,sign)
    win_diag_down = check_diagonal_position_equal(diagonal_down,sign)
    win_diag_up = check_diagonal_position_equal(diagonal_up,sign,"up") 
    win_col_coordinates = check_all_position_equal(transpose_board,sign, "col")
  
    win_coordinates_list = win_row_coordinates + win_diag_down + win_diag_up + win_col_coordinates
    return win_coordinates_list


def is_full(board):
    """Returns True if board is full."""
    result = set()
    for i in range(0,len(board)):
        for j in range(0,len(board)):
            if board[i][j] == ".":
                result.add(board[i][j])
    if result != set():            
        return False
    else:
        return True


def print_board(board, win_coordinates=()):
    """Prints a 3-by-3 board on the screen with borders."""
    
    position = f" . |"
    row_count = len(board)
    print(5*" ",end="")
    for column in range(1,row_count+1):
        print(f"{column}   ",end="")
    print() 
     
    for i in range(0,row_count):
        row_name = chr(ZNAK_A+i)
        position = ""
        row_inside = ""
        for j in range(0,row_count):
            position = board[i][j]            
            if (i,j) in win_coordinates:
                row_inside +=f" \033[31;1;4m{position}\033[;0m "                
            else:
                row_inside +=f" {position} " 

            if j< row_count -1:
                row_inside +="|"
        print(f"{row_name}   {row_inside} ")
        if i <row_count -1:
            print("    ---"+("+---"*(row_count-1)))
    pass


def print_result(winner=""):
    """Congratulates winner or proclaims tie (if winner equals zero)."""
    if winner != "":
        print(f"\033[;01m\033[;36mCongratulations! Player {winner} has won!\033[;0m")
    else:
        print("\033[;01m\033[;36mIt is a tie!\033[;0m ")

    pass


def tictactoe_game(row_count, player, dict_names, mode):
    board = init_board(row_count)
    print_board(board)
    if mode == 3 :
        player_input("Press Enter to start ")
    while True:
        if mode == 1:
            row, col = get_move(board, dict_names[player])
        if mode == 4:
            row,col = get_ai_move(board,player)
            player_input("Press Enter for next AI move: ")
        if mode == 2:
            if player == player_1:
                row, col = get_move(board, dict_names[player])
            else:
                row,col = get_ai_move(board,player) 
        if mode == 3:            
            if player == player_1:
                row,col = get_ai_move(board,player)               
            else:
                row, col = get_move(board, dict_names[player])

        mark(board,player,row, col)
        os.system("cls")
        print_board(board)
        if has_won(board,player) == True:
            win_coordinates = find_win_coordinates(board,player)
            os.system("cls")
            print_board(board, win_coordinates)
            winner = dict_names[player]  
            print_result(winner)
            break
        elif is_full(board) == True:
            os.system("cls")
            print_board(board)
            print_result()
            break
                    
        if player == player_1:
            player = player_2
        else:
            player = player_1   
     

# funkcja do wprowadzania tekstu przez użytkownika, zawierajaca opcje "quit"
def player_input(text):
    player_text = input(text)
    if player_text == "quit":
        sys.exit("You quit the game")
    return player_text


def main_menu():
    
    print ("\033[;33m===============================\033[;0m")
    print ("       \033[;01m\033[;36mTIC TAC TOE GAME\033[;0m")
    print ("\033[;33m===============================\033[;0m")
    
    setup_game = {}
    while True:        
        game_mode = int(player_input("Choice game mode:\n 1 for HUMAN - HUMAN \n 2 for HUMAN - AI\n 3 for AI - HUMAN\n 4 for AI - AI\nIf you want to end the game, enter \033[31m 'quit'\033[;0m at any time.\n"))
        if game_mode in [1,2,3,4]:
            setup_game["game mode"] = game_mode
            break      
        else:
            print("Wrong input, try again")
            #os.system("cls")
    
    row_count= 0
    while not (row_count > 0 and row_count <=26):
        try:
            row_count = int(player_input("Enter the size of the game board: "))  # wybór wielkości pola do gry
        except ValueError:
            print("Specify a number")
        

    setup_game["board size"] = row_count
    
    
    return setup_game


def define_players(mode):
    players_names = {}
    
    if mode == 2:
        players_names[player_1] = player_input("Enter your name: ")
        players_names[player_2] = "AI"
    elif mode == 3:
        players_names[player_1] = "AI"
        players_names[player_2] = player_input("Enter your name: ")
    elif mode == 4:
        players_names[player_1] = "C-3PO"
        players_names[player_2] = "R2-D2"
    elif mode == 1:
        player_1_name = player_input("Enter name of Player 1: \033[;34m")
        player_2_name = player_input("\033[;0mEnter name of Player 2: \033[;32m")
        players_names[player_2] = player_2_name
        players_names[player_1] = player_1_name

    return players_names
   
# if __name__ == '__main__':
#     main_menu()

def main():
    game_mode = main_menu()
    row_count = game_mode["board size"]
    mode = game_mode["game mode"]
    players_names = define_players(mode)
    

    print(f"\033[;0mYou have chosen to play on the \033[;31m{row_count}x{row_count} field\033[;0m")
    print(f"{players_names[player_1]} is Player 1 and plays with \033[;34m'X'\033[;0m")
    print(f"{players_names[player_2]} is Player 2 and plays with \033[;32m'O'\033[;0m")
    if mode ==1 or mode == 2:
        print(f"{players_names[player_1]}  - you are starting.")
    else:
        print(f"{players_names[player_1]} starts.")

    continue_game = True
    while continue_game:
        tictactoe_game(row_count,player_1, players_names, mode)
        continuing = player_input("Do you want to play again? (\033[;32m Yes \033[;0m/ \033[;31m No \033[;0m ) ")
        if continuing.lower() == "no":
            continue_game = False
            sys.exit("End of game")
        else:
            os.system("cls")

main()
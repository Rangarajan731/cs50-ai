import tictactoe as ttt

def print_board(board):
    for i in range(3):
        for j in range(3):
            print(board[i][j], end="|")
        print()

    print()



if __name__ == "__main__":
    board = ttt.initial_state()
    user = None
    ai_turn = False

    selected_player = input("please select player X or O")
    if selected_player == "X":
        user = ttt.X
    else:
        user = ttt.O

    print("Starting the game!!!")
    print("initial state:")
    print_board(board)

    while not ttt.terminal(board):
        if user != ttt.player(board):
            action = ttt.minimax(board)
            board = ttt.result(board, action)
        
        else:
            print_board(board)
            action = input(f"make a move {user}: ")
            action = action.split(",")
            action = tuple(map(int, action))
            board = ttt.result(board, action)


    print_board(board)
    print(f"The winner is {ttt.winner(board)}!!!")
import minesweeper


if __name__ == "__main__":
    m = minesweeper.Minesweeper(16,16,40, 5,5)
    m.uncover_tile(5,5)
    m.print_user_game_board()
    #m.print_game_board()

from random import sample

class Minesweeper:

    def __init__(self, rows, columns, mines, startX, startY):

        self._rows = rows
        self._columns = columns
        self._uncovered = 0
        self._user_board = [[-1 for _ in range(columns) ] for _ in range(rows)] #-1 signifies an uncovered tile
        self._game_board = [[0 for _ in range(columns)] for _ in range(rows)] #0 will signifiy an empty tile
        self._mines = mines
        start_neighbors = self._get_neighbors(startX, startY)
        board_coords = [(r,c) for r in range(rows) for c in range(columns) if r != startX and c != startY and (r,c) not in start_neighbors]
        self._mine_coords = sample(board_coords, mines)

        for x,y in self._mine_coords:
            self._game_board[x][y] = '*'
            for a,b in self._get_neighbors(x,y):
                if self._game_board[a][b] != "*":
                    self._game_board[a][b] += 1

        self._flags_placed = 0
        self.uncover_tile(startX,startY)

    def place_flag(self, row, col):

        if self._flags_placed != self._mines and (self._user_board[row][col] == -1 or self._user_board== 'F'):

            self._user_board[row][col] = 'F' #this signifies a mine is expected there
            self._flags_placed += 1
            return True
        return False
    def remove_flag(self, row,col):

        if self._flags_placed > 0:
            self._user_board[row][col] = -1 #this signifies a mine is expected there
            self._flags_placed -= 1

    def is_flagged(self,row,col):
        return self._user_board[row][col] == 'F'

    def print_user_game_board(self):

        for r in range(self._rows):
            for c in range(self._columns):
                print(f'{self._user_board[r][c]} \t', end = "")

            print()

    def print_game_board(self):

        for r in range(self._rows):
            for c in range(self._columns):
                print(f'{self._game_board[r][c]} \t', end = "")

            print()

    def _reveal_mines(self):

        for r,c in self._mine_coords:
            self._user_board[r][c] = '*'

    def uncover_tile(self,row,col):

        if self._game_board[row][col] == '*':
            self._reveal_mines()
            self._user_board[row][col] = '**'
            return False

        elif self._game_board[row][col] > 0:
            self._uncover_helper(row,col)
        else:
            self._uncover_zero_tile(row,col)
        return True
    def _uncover_helper(self, row,col):
        self._user_board[row][col] = self._game_board[row][col]
        self._uncovered += 1



    def _get_neighbors(self, row, col):

        directions = [(0,1),(1,0),(1,1),(-1,0),(0,-1),(-1,-1),(-1,1),(1,-1)]
        neighbors = []
        for d in directions:
            neighbor = (row + d[0], col + d[1])
            if  -1 < neighbor[0] < self._rows and -1 < neighbor[1] < self._columns:
                neighbors.append(neighbor)
        return neighbors

    def get_cell(self,row,col):
        return self._user_board[row][col]

    def _uncover_zero_tile(self,row,col):

        self._uncovered+=1
        self._user_board[row][col] = self._game_board[row][col]
        uncovered = set()
        frontier = [(row,col)]

        while frontier:

            r,c = frontier.pop(0)
            if self._game_board[r][c] == 0:
                for x,y in self._get_neighbors(r,c):
                    if self._game_board[x][y] == 0 and (x,y) not in uncovered:
                        frontier.append((x,y))

                    self._uncover_helper(r,c)
                    self._uncover_helper(x,y)
                    uncovered.add((r,c))


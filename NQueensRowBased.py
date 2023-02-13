import enum


class House(enum.Enum):
    Empty = 0
    Queen = 1
    Obstacle = 2


class Step(enum.Enum):
    Up = (0, 1)
    Down = (0, -1)
    Right = (1, 0)
    Left = (-1, 0)
    UpRight = (1, 1)
    UpLeft = (-1, 1)
    DownRight = (1, -1)
    DownLeft = (-1, -1)


def check_inside_board(row: int, col: int) -> bool:
    if row >= 0 and row < len(board):
        if col >= 0 and col < len(board[row]):
            return True
    return False


def check_safety(row: int, col: int) -> bool:
    for step in Step:
        if not check_path_safety(row, col, step):
            return False
    return True


def check_path_safety(row: int, col: int, step: Step) -> bool:
    while check_inside_board(row + step.value[0], col + step.value[1]):
        if board[row + step.value[0]][col + step.value[1]] == House.Queen:
            return False
        elif board[row + step.value[0]][col + step.value[1]] == House.Obstacle:
            return True
        else:
            row += step.value[0]
            col += step.value[1]
    return True


def detect_existence(res, board):
    def detect_diff(board: list, anotherBoard: list):
        for i in range(len(board)):
            for j in range(len(board[i])):
                if board[i][j] != anotherBoard[i][j]:
                    return True
        return False

    for aboard in res:
        if not detect_diff(board, aboard):
            return True
    return False


# dfs search on board
def dfs(
    placed_queens: int,
    row: int,
    column: int = 0,
):
    if placed_queens == queen_numbers and not detect_existence(results, board):
        print_board()
        results.append([board[row][:] for row in range(len(board))])
        return True
    if row >= len(board) or column >= len(board[row]):
        return False

    for col in range(0, len(board[row])):
        if board[row][col] == House.Empty and check_safety(row, col):
            # place queen
            board[row][col] = House.Queen

            # check if we can place the rest of the queens in this row
            for r in range(len(board)):
                dfs(
                    placed_queens + 1,
                    r,
                    (column + 1),
                )
            # check if we can place the rest of the queens in the next row
            dfs(
                placed_queens + 1,
                (row + 1),
                column,
            )
            # backtrack
            board[row][col] = House.Empty

    return False  # we reached the end of the board and still haven't placed all queens


def print_board():
    for row in board:
        for col in row:
            if col == House.Queen:
                fo.write("👑")
                # print("👑", end="")
            elif col == House.Obstacle:
                fo.write("⬛")
                # print("⬛", end="")
            else:
                fo.write("⬜")
                # print("⬜", end="")
        fo.write("\n")
    fo.write("------------------------\n")


def main(results: list, board: list, queen_numbers: int, obstacles: list = []):
    global fo
    fo = open("output.txt", "w")
    for o in obstacles:
        board[o[0]][o[1]] = House.Obstacle
    for q in placed_queens:
        board[q[0]][q[1]] = House.Queen
    for i in range(len(board)):
        dfs(0, i)
    # for result in results:
    #   print_board(result)
    fo.close()


if __name__ == "__main__":
    global results
    global board
    global queen_numbers
    dimension = 8
    queen_numbers = 8
    results = []
    obstacles = []
    obstacles = [(3, 0), (3, 3), (6, 2)]
    placed_queens = []
    board = [[House.Empty for j in range(dimension)] for i in range(dimension)]
    main(results, board, queen_numbers, obstacles)
    print(len(results))

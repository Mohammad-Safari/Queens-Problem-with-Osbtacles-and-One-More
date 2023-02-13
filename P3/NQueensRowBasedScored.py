import enum
import random


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


def check_inside_board(board: list, row: int, col: int) -> bool:
    if row >= 0 and row < len(board):
        if col >= 0 and col < len(board[row]):
            return True
    return False


def check_path_safety(board: list, row: int, col: int, step: Step) -> bool:
    while check_inside_board(board, row + step.value[0], col + step.value[1]):
        if board[row + step.value[0]][col + step.value[1]] == House.Queen:
            return False
        elif board[row + step.value[0]][col + step.value[1]] == House.Obstacle:
            return True
        else:
            row += step.value[0]
            col += step.value[1]
    return True


def check_safety(board: list, row: int, col: int) -> bool:
    for step in Step:
        if check_path_safety(board, row, col, step) == False:
            return False
    return True


def get_safe_houses(board: list) -> list:
    safe_houses = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if check_safety(board, i, j) and board[i][j] == House.Empty:
                safe_houses.append((i, j))
    return safe_houses


def get_path_unsafety(board: list, row: int, col: int, step: Step) -> bool:
    path = []
    while check_inside_board(board, row + step.value[0], col + step.value[1]):
        if board[row + step.value[0]][col + step.value[1]] != House.Empty:
            break
        else:
            row += step.value[0]
            col += step.value[1]
            path.append(tuple((row, col)))
    return path


def get_unsafe_houses(board: list, row: int, col: int) -> list:
    unsafe_houses = []
    for step in Step:
        unsafe_houses += get_path_unsafety(board, row, col, step)
    return unsafe_houses


# dfs search on board
def dfs(
    results: list,
    queen_numbers: int,
    placed_queens: int,
    board: list,
    scores:list,
    row: int,
    column: int = 0,
):
    if placed_queens == queen_numbers:
        calculate_board(board,scores)
        print_board(board)
        results.append([board[row][:] for row in range(len(board))])
        return True
    if row >= len(board) or column >= len(board[row]):
        return False

    for col in range(column, len(board[row])):
        if board[row][col] == House.Empty and check_safety(board, row, col):
            # place queen
            board[row][col] = House.Queen

            # check if we can place the rest of the queens in this row
            dfs(
                results,
                queen_numbers,
                placed_queens + 1,
                board,
                row,
                (column + 1),
            )
            # check if we can place the rest of the queens in the next row
            dfs(
                results,
                queen_numbers,
                placed_queens + 1,
                board,
                (row + 1),
                column,
            )
            # backtrack
            board[row][col] = House.Empty

    return False  # we reached the end of the board and still haven't placed all queens


def print_board(board: list):
    for row in board:
        for col in row:
            if col == House.Queen:
                print("👑", end="")
            elif col == House.Obstacle:
                print("⬛", end="")
            else:
                print("⬜", end="")
        print()
    print("------------------------")


def calculate_board(board, scores):
    sum = 0
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == House.Queen:
                sum += scores[i][j]
    return sum


def main():
    results = []
    dimension = 8
    queen_numbers = 8
    obstacles = [(3, 0), (3, 3), (6, 2)]
    scores = [
        [random.randint(0, dimension ** 2) for j in range(dimension)]
        for i in range(dimension)
    ]
    board = [[House.Empty for j in range(dimension)] for i in range(dimension)]
    for o in obstacles:
        board[o[0]][o[1]] = House.Obstacle

    for i in range(dimension):
        dfs(results, queen_numbers, 0, board, scores,i)

    print(len(results))
    for result in results:
        calculate_board(board,scores)
        print_board(result)


if __name__ == "__main__":
    main()

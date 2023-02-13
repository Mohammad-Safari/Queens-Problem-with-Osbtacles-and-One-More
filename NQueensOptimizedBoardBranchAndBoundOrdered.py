from asyncore import read
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


def check_danger(queen: tuple, row: int, col: int) -> bool:
    def is_path_blocked_by_obstacle(
        queen: tuple, row: int, col: int, rd: int, cd: int
    ) -> bool:
        step = (
            1 if rd > 0 else 0 if rd == 0 else -1,
            1 if cd > 0 else 0 if cd == 0 else -1,
        )
        if House.Obstacle in [
            board[row + step[0] * i][col + step[1] * i] for i in range(max(abs(rd), abs(cd)))
        ]:
            return True
        return False

    rd = queen[0] - row
    cd = queen[1] - col
    diagonal = 1 if abs(rd) == abs(cd) else 0
    if rd == 0 or cd == 0 or diagonal == 1:
        return not is_path_blocked_by_obstacle(queen, row, col, rd, cd)
    return False


def get_safe_houses(queens: list) -> list:
    def check_house_danger(queens: list, row: int, col: int) -> bool:
        for q in queens:
            if check_danger(q, row, col):
                return True
        return False

    safe_houses = []
    for i in range(len(board)):
        for j in range(len(board[i])):
            if board[i][j] == House.Empty:
                if check_house_danger(queens, i, j) == False:
                    safe_houses.append((i, j))
    return safe_houses


def get_unsafe_houses(queens: list) -> list:
    unsafe_houses = [[False for house in row] for row in board]

    def get_path_unsafety(row: int, col: int, step: Step) -> bool:
        path = []
        while check_inside_board(board, row + step.value[0], col + step.value[1]):
            if board[row + step.value[0]][col + step.value[1]] != House.Empty:
                break
            else:
                row += step.value[0]
                col += step.value[1]
                path.append(tuple((row, col)))
        return path

    def check_house_unsafe(row: int, col: int) -> list:
        for step in Step:
            get_path_unsafety(board, row, col, step)
        for h in unsafe_houses:
            unsafe_houses[h[0]][h[1]] = True

    for i in range(len(board)):
        for j in range(len(board[i])):
            if unsafe_houses[i][j] == True:
                continue
            if check_house_unsafe(queens, i, j) == False:
                unsafe_houses.append((i, j))
    return unsafe_houses


def detect_existence(queens):
    def detect_diff(board: list, queens: list):
        for queen in queens:
            if board[queen[0]][queen[1]] != House.Queen:
                return True

    for aboard in results:
        if not detect_diff(aboard, queens):
            return True
    return False


def compare_location(loc1, loc2):
    if loc1[0] > loc2[0] or (loc1[0] == loc2[0] and loc1[1] >= loc2[1]):
        return True
    else:
        return False


# dfs search on board
def dfs(placed_queens: list):
    if len(placed_queens) == queen_numbers and not detect_existence(placed_queens):
        print_board()
        results.append([board[row][:] for row in range(len(board))])
        print("*", end="")
        return True

    safe_houses = get_safe_houses(placed_queens)
    # safe_houses.sort(key=lambda h: h[0] * 10 + h[1])
    if len(safe_houses) == 0:
        return False
    for safe_house in safe_houses:
        if compare_location(
            placed_queens[-1] if len(placed_queens) > 0 else (-1, -1), safe_house
        ):
            continue
        board[safe_house[0]][safe_house[1]] = House.Queen
        dfs(
            placed_queens + [safe_house],
        )
        board[safe_house[0]][safe_house[1]] = House.Empty

    return False


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
        # print()
    fo.write("------------------------\n")
    fo.flush()
    # print("------------------------")


def main(results: list, board: list, queen_numbers: int, obstacles: list = []):
    global fo
    fo = open("output.txt", "w")
    for o in obstacles:
        board[o[0]][o[1]] = House.Obstacle
    for q in placed_queens:
        board[q[0]][q[1]] = House.Queen
    dfs(placed_queens)
    # for result in results:
    #   print_board(result)
    fo.close()


if __name__ == "__main__":
    global results
    global board
    global queen_numbers
    # global flag
    dimension = 8
    queen_numbers = 8
    results = []
    obstacles = []
    obstacles = [(3, 0), (3, 3), (6, 2)]
    placed_queens = []
    board = [[House.Empty for j in range(dimension)] for i in range(dimension)]
    flag = [
        [[False for j in range(dimension)] for i in range(dimension)]
        for k in range(queen_numbers)
    ]
    main(results, board, queen_numbers, obstacles)
    print(len(results))

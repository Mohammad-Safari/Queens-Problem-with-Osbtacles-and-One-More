# Quick Sort
import random
from tkinter.messagebox import NO


def quick_sort(dict: dict, ascending=False) -> dict:
    if len(dict) <= 1:
        return dict
    import random
    pivot = random.randrange(0, len(dict) - 1)
    left = []
    right = []
    for i in range(len(dict)):
        if i == pivot:
            continue
        if (ascending and dict[i][0] < dict[pivot][0]) or (
            not ascending and dict[i][0] > dict[pivot][0]
        ):
            left.append(dict[i])
        else:
            right.append(dict[i])
    return quick_sort(left, ascending) + [dict[pivot]] +  quick_sort(right, ascending)


def stackBox(cubes, weight, lastSide="Ground", height=0):
    if weight <= 0:
        return height
    # if not weight in cubes:
    #     return stackBox(cubes, weight - 1, lastSide, height)
    tempHeight = height
    for next_weight in range(weight, 0, -1):
        for color in cubes[next_weight]:
            for side in range(6):
                if (
                    lastSide == "Ground" or color[side] == lastSide
                ):  # if color match in this pose put
                    temp = None
                    if dp[next_weight - 1][color[get_opposite(side)]] == None:
                        temp = stackBox(
                            cubes,
                            next_weight - 1,
                            color[get_opposite(side)],
                            height + 1,
                        )
                    tempHeight = max(tempHeight, temp)

    return tempHeight


def get_opposite(side):
    o = {5: 1, 1: 5, 4: 2, 2: 4, 6: 3, 3: 6}
    return o[side + 1] - 1


if __name__ == "__main__":
    global dp
    LEGAL_COLORS = ["a", "b", "c", "d", "e", "f", "g"]
    # Getting inputs from user
    # weights = [int(x) for x in input("Enter the weights: \n").split()]
    # weights = [13, 4, 5, 5, 2, 8, 16, 13]

    # colors = [
    #     str(
    #         input(
    #             "Color for "
    #             + str(w)
    #             + ("st" if w == 1 else "nd" if w == 2 else "rd" if w == 3 else "th")
    #             + " cube:"
    #         )
    #         * 6
    #     )[-6:]
    #     for w in range(len(weights))
    # ]

    # colors = [
    #     ''.join(random.sample(["a", "h", "s", "d", "g", "j", "l", "t", "w"], 6))
    #     for w in range(len(weights))
    # ]
    weights = [1, 2, 3]
    colors = ["ababab", "ffffff", "ababab"]

    #           ______
    #           |  1 |
    #           |    |
    #      _________________
    #      | 2  |  3 | 4(2)|
    #      |    |    |     |
    #      _________________
    #           |5(1)|
    #           |    |
    #           ______
    #           |6(3)|
    #           |    |
    #           ------
    #
    #
    # Sort cubes by weight in descending order
    cubes = list(zip(weights, colors))
    cubes.sort(key=lambda c: c[0])
    dp = [{color: None for color in LEGAL_COLORS+['Ground']} for weight in weights]
    # cubesSets = {weight: set() for weight in weights}
    cubesSets = {
        weight + 1: set() for weight in range(len(weights))
    }  ## replacing absolute weights with n to 1

    # classifying cubes according to weights
    for weight, color in cubes:
        cubesSets[weight].add(color)

    # height = 0
    # for weight, colorSet in cubes:
    #     height = max(height,stackBox(cubesSets, weight))
    height = stackBox(cubesSets, max(weights))
    print(height)

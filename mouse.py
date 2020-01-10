import pyautogui
import time
import sys

pos_list = []
dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
min_y = 0
max_y = 4
min_x = 0
max_x = 4
block_size = 107
padding_y = 474
padding_x = 585
num_blocks_per_row = 4
visited = [[False for _ in range(0, num_blocks_per_row)] for _ in range(0, num_blocks_per_row)]
coord = [
    [
        (587, 475),
        (695, 477),
        (803, 476),
        (907, 474)
    ],
    [
        (586, 584),
        (692, 583),
        (802, 583),
        (908, 580)
    ],
    [
        (589, 686),
        (691, 688),
        (802, 688),
        (912, 692)
    ],
    [
        (588, 795),
        (696, 796),
        (799, 794),
        (906, 795)
    ]
]
start = time.time()

def is_valid_pos(x, y):
    return min_x <= x < max_x and min_y <= y < max_y


def get_coord(x, y):
    # return x * block_size + padding_x, y * block_size + padding_y
    return coord[y][x]


def drag():
    if time.time() - start > 85:
        print(len(pos_list), time.time() - start)
        sys.exit()
    coord_x, coord_y = get_coord(*pos_list[0])
    pyautogui.moveTo(coord_x, coord_y)
    pyautogui.mouseDown()
    for i in range(1, len(pos_list)):
        coord_x, coord_y = get_coord(*pos_list[i])
        pyautogui.moveTo(coord_x, coord_y)
    pyautogui.mouseUp()

def dfs(x, y, length):
    if length == 0:
        drag()
        return

    for dy, dx in dirs:
        new_x = x + dx
        new_y = y + dy
        if is_valid_pos(new_y, new_x) and not visited[new_y][new_x]:
            visited[new_y][new_x] = True
            pos_list.append((new_x, new_y))
            dfs(new_x, new_y, length - 1)
            pos_list.pop()
            visited[new_y][new_x] = False


def main():
    global pos_list

    pyautogui.PAUSE = 0.0325
    for length in range(1, 16):
        for y in range(0, 4):
            for x in range(0, 4):
                pos_list = [(x, y)]
                dfs(x, y, length)



if __name__ == "__main__":
    main()

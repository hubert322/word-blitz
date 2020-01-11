from PyDictionary import PyDictionary

import pyautogui
import time
import sys
import json

min_y = 0
max_y = 4
min_x = 0
max_x = 4

block_size = 107
padding_y = 474
padding_x = 585
# block_size = 94
# padding_y = 506
# padding_x = 498
num_blocks_per_row = 4
start = time.time()

pos_list = []
dictionaries = []
used_words = set()
dirs = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
letters = [[0 for _ in range(0, num_blocks_per_row)] for _ in range(0, num_blocks_per_row)]
visited = [[False for _ in range(0, num_blocks_per_row)] for _ in range(0, num_blocks_per_row)]

def set_dictionaries():
    with open("words_dictionary.json", "r", encoding="utf-8") as f:
        dictionaries.append(json.load(f))


def set_letters(tmp):
    for i in range(0, len(letters)):
        for j in range(0, len(letters[0])):
            letters[i][j] = tmp[num_blocks_per_row * i + j]


def dfs(x, y, length, word):
    if length == 0:
        if word not in used_words:
            used_words.add(word)
            for i, dictionary in enumerate(dictionaries):
                if word in dictionary:
                    print(word, i)
                    drag()
                    break
        return

    for dy, dx in dirs:
        new_x = x + dx
        new_y = y + dy
        if is_valid_pos(new_y, new_x) and not visited[new_y][new_x]:
            visited[new_y][new_x] = True
            pos_list.append((new_x, new_y))
            dfs(new_x, new_y, length - 1, word + letters[new_y][new_x])
            pos_list.pop()
            visited[new_y][new_x] = False


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


def is_valid_pos(x, y):
    return min_x <= x < max_x and min_y <= y < max_y


def get_coord(x, y):
    return x * block_size + padding_x, y * block_size + padding_y


def main():
    global pos_list

    set_dictionaries()

    tmp = input("Letters: ")
    set_letters(tmp)

    pyautogui.PAUSE = 0.0325

    for length in range(7, 0, -1):
        for y in range(0, 4):
            for x in range(0, 4):
                pos_list = [(x, y)]
                dfs(x, y, length, letters[y][x])


if __name__ == "__main__":
    main()

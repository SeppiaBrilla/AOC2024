from time import sleep
from os import system
from sys import setrecursionlimit

setrecursionlimit(1000000000)

EMPTY = '.'
WALL = '#'
END = 'E'
START = 'S'

UP = (-1,0)
DOWN = (1,0)
RIGHT = (0,1)
LEFT = (0,-1)
DIRECTIONS = [UP, DOWN, LEFT, RIGHT]

def get_map(str_map:str) -> list[list[str]]:
    return [list(line) for line in str_map.splitlines()]
def print_map(map:list[list[str]]) -> None:
    for line in map:
        print(''.join(line))
def clear():
    system('clear')

def is_opposite(current_direction:tuple[int,int], next_direction:tuple[int,int]) -> bool:
    return (current_direction == UP and next_direction == DOWN) \
        or (current_direction == DOWN and next_direction == UP) \
        or (current_direction == LEFT and next_direction == RIGHT) \
        or (current_direction == RIGHT and next_direction == LEFT)

def get_path(map:list[list[str]], current_position:tuple[int,int], visited:set[tuple[int,int]]|None=None, current_path:list[tuple[int,int]] = []) -> list[tuple[int,int]]:
    if visited is None:
        visited = set()
    i, j = current_position
    updated_path = current_path.copy()
    updated_path.append(current_position)
    if map[i][j] == END:
        return updated_path
    visited.add(current_position)
    best_path = []
    m, n = len(map), len(map[0])
    for ii, jj in DIRECTIONS:
        _i, _j = ii + i, jj + j
        if _i < 0 or _j < 0 or _i > m or _j > n:
            continue
        if map[_i][_j] == WALL:
            continue
        if (_i, _j) in visited:
            continue
        best_path.append(get_path(map, (_i,_j), visited, updated_path))
    return min(best_path, key= lambda x: len(x))

def get_next_steps(map:list[list[str]], path:list[tuple[int,int]], current_position:tuple[int,int], direction:tuple[int,int]) -> list[list[tuple[int,int]]]:
    steps = []
    m, n = len(map), len(map[0])
    for next_dir in DIRECTIONS:
        if is_opposite(direction, next_dir):
            continue
        step = current_position[0] + next_dir[0], current_position[1] + next_dir[1]
        if step[0] < 0 or step[1] < 0 or step[0] > n or step[1] > m:
            continue
        if step in path:
            steps.append([current_position, step])
    return steps


def get_shortcuts(map:list[list[str]], path:list[tuple[int,int]]) -> list[list[tuple[int,int]]]:
    paths_with_shortcuts = []
    for idx, (i, j) in enumerate(path):
        for ii, jj in DIRECTIONS:
            _i, _j = ii + i, jj + j
            if (_i, _j) in path: 
                continue
            shortcuts = get_next_steps(map, path[idx:], (_i, _j), (ii, jj))
            for shortcut in shortcuts:
                second_idx = path.index(shortcut[1])
                new_path = path[:idx+1] + shortcut + path[second_idx+1:]
                paths_with_shortcuts.append(new_path)

    return paths_with_shortcuts

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    map = get_map(content)
    starting_point = 0,0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == START:
                starting_point = (i,j)
                break

    path = get_path(map, starting_point)
    path_length = len(path) - 1
    short_path = get_shortcuts(map, path)
    saves = {}
    for sp in short_path:
        save = path_length - (len(sp) - 1)
        if save == 0:
            continue
        if not save in saves:
            saves[save] = 0
        saves[save] += 1
    saves = {k:v for k,v in sorted(saves.items(), key=lambda x: x[0])}
    at_least_100 = 0
    for k,v in saves.items():
        if k >= 100:
            at_least_100 += v
        print(f' there are {v} path that save {k} picoseconds')
    print(f'there are {at_least_100} path that save at least 100 picoseconds')

if __name__ == "__main__":
    main()

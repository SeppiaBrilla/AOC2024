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

def get_path(
        map:list[list[str]], 
        current_position:tuple[int,int], 
        end_position:tuple[int,int], 
        visited:set[tuple[int,int]]|None=None, 
        full_dist:bool=True,
        max_length:int=-1) -> list[tuple[int,int]]:
    if visited is None:
        visited = set()
    visiting_list = [(current_position, [])]
    def dist(c):
        return abs(end_position[0] - c[0]) + abs(end_position[1] - c[1])
    def compute_dist(x):
        if full_dist:
            return len(x[1][1]) + dist(x[1][0])
        return dist(x[1][0])
    while len(visiting_list) > 0:
        idx, (current_position, path) = min(enumerate(visiting_list), key=compute_dist )
        visiting_list.pop(idx)
        i,j = current_position
        visited.add(current_position)
        if len(path) > max_length and max_length > 0:
            continue
        if current_position == end_position:
            return path + [current_position]
        m, n = len(map), len(map[0])
        for ii, jj in DIRECTIONS:
            _i, _j = ii + i, jj + j
            if _i < 0 or _j < 0 or _i >= m or _j >= n:
                continue
            if map[_i][_j] == WALL:
                continue
            if (_i, _j) in visited:
                continue
            visiting_list.append(((_i,_j), path + [current_position]))
    return []

def get_shortcuts(path:list[tuple[int,int]]) -> list[int]:
    paths_with_shortcuts = []
    for idx1, point1 in enumerate(path):
        for idx2, point2 in enumerate(path):
            if point1 == point2:
                continue
            if idx2 - idx1 < 2:
                continue
            dist = abs(point1[0] - point2[0]) + abs(point1[1] - point2[1])
            if dist > 20:
                continue
            # print('shortening:', point1, point2, dist < (idx2 - idx1))
            if dist < (idx2 - idx1):
                paths_with_shortcuts.append(len(path) - (idx2 - idx1) + dist)
    return paths_with_shortcuts

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    map = get_map(content)
    starting_point = 0,0
    ending_point = 0,0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == START:
                starting_point = (i,j)
            elif map[i][j] == END:
                ending_point = (i,j)

    path = get_path(map, starting_point, ending_point)
    path_length = len(path) - 1
    # print('found path', path_length)
    short_path = get_shortcuts(path)
    saves = {}
    for sp in short_path:
        save = path_length - (sp - 1)
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
        if not k > 49:
            continue
        print(f' there are {v} path that save {k} picoseconds')
    print(f'there are {at_least_100} path that save at least 100 picoseconds')

if __name__ == "__main__":
    main()

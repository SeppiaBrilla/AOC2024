from typing import Literal
from itertools import combinations

def to_map(content:str) -> list[list[str]]:
    map = []
    for line in content.splitlines():
        map.append(list(line))
    return map

def print_map(map:list[list[str]]):
    for line in map:
        print(''.join(line))

def distance(point1: tuple[int,int], point2: tuple[int,int]) -> tuple[int,int]:
    x1, y1 = point1
    x2, y2 = point2
    return (abs(x1 - x2), abs(y1 - y2))

def get_directions(point1: tuple[int,int], point2: tuple[int,int]) -> Literal['vertical', 'horizontal', 'main_diag', 'second_diag']:
    x1, y1 = point1
    x2, y2 = point2
    if x1 == x2:
        return 'horizontal'
    if y1 == y2:
        return 'vertical'
    low = point1 if y1 > y2 else point2
    high = point1 if y1 < y2 else point2

    if low[0] > high[0]:
        return 'main_diag'
    if low[0] < high[0]:
        return 'second_diag'

    raise Exception('unrecognized direction')

def get_antennas_dict(map:list[list[str]]) -> dict[str, list[tuple[int,int]]]:
    antennas = {}
    for i, row in enumerate(map):
        for j, spot in enumerate(row):
            if spot == '.':
                continue
            if not spot in antennas:
                antennas[spot] = []
            antennas[spot].append((i, j))
    return antennas

def add_points(p1: tuple[int,int], p2: tuple[int,int], map:list[list[str]], overwrite:bool=True) -> list[list[str]]:
    direction = get_directions(p1,p2)
    dists = distance(p1,p2)
    if direction == 'main_diag':
        low = p1 if p1[1] > p2[1] else p2
        high = p1 if p1[1] < p2[1] else p2

        new_x1, new_y1 = high[0] - dists[0], high[1] - dists[1]
        new_x2, new_y2 = low[0] + dists[0], low[1] + dists[1]

        if new_x1 >= 0 and new_y1 >= 0:
            if overwrite:
                map[new_x1][new_y1] = '#'
        if new_x2 < len(map) and new_y2 < len(map[0]):
            if overwrite:
                map[new_x2][new_y2] = '#'
    elif direction == 'second_diag':
        low = p1 if p1[1] > p2[1] else p2
        high = p1 if p1[1] < p2[1] else p2

        new_x1, new_y1 = high[0] + dists[0], high[1] - dists[1]
        new_x2, new_y2 = low[0] - dists[0], low[1] + dists[1]

        if new_x1 < len(map[0]) and new_y1 >= 0:
            if overwrite:
                map[new_x1][new_y1] = '#'
        if new_x2 >= 0 and new_y2 < len(map[0]):
            if overwrite:
                map[new_x2][new_y2] = '#'
    elif direction == 'vertical':
        low = p1 if p1[1] > p2[1] else p2
        high = p1 if p1[1] < p2[1] else p2

        new_y1 = high[1] - dists[1]
        new_y2 = low[1] + dists[1]

        if new_y1 >= 0:
            if overwrite:
                map[low[0]][new_y1] = '#'
        if new_y2 <= len(map):
            if overwrite:
                map[low[0]][new_y2] = '#'
    elif direction == 'horizontal':
        low = p1 if p1[1] > p2[1] else p2
        high = p1 if p1[1] < p2[1] else p2

        new_x1 = high[0] - dists[0]
        new_x2 = low[0] + dists[0]

        if new_x1 >= 0:
            if overwrite:
                map[new_x1][low[0]] = '#'
        if new_x2 <= len(map[0]):
            if overwrite:
                map[new_x2][low[0]] = '#'
    return map


def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    map = to_map(content)
    antennas = get_antennas_dict(map)
    pts = 0
    for antenna_type in antennas.keys():
        for (p1, p2) in combinations(antennas[antenna_type], 2):
            map = add_points(p1,p2,map)

    for line in map:
        for el in line:
            if el == '#':
                pts += 1
    print_map(map)
    print(pts)

if __name__ == "__main__":
    main()

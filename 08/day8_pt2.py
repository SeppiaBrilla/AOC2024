from typing import Literal
from itertools import combinations

def to_map(content:str) -> list[list[str]]:
    map = []
    for line in content.splitlines():
        map.append(list(line))
    return map

def is_point_on_line(point1: tuple, point2: tuple, point3: tuple) -> bool:
    x1, y1 = point1
    x2, y2 = point2
    x3, y3 = point3
    return (x2 - x1) * (y3 - y1) == (y2 - y1) * (x3 - x1)

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
    for i in range(len(map)):
        for j in range(len(map[0])):
            if is_point_on_line(p1,p2,(i,j)):
                map[i][j] = '#'
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
            if el != '.':
                pts += 1
    print_map(map)
    print(pts)

if __name__ == "__main__":
    main()

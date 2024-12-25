from os import system

EMPTY = '.'
WALL = '#'

def clear():
    system('clear')

def get_map(max_size:int) -> list[list[str]]:
    return [['.' for _ in range(max_size+1)] for _ in range(max_size+1)]

def print_map(map:list[list[str]]):
    for line in map:
        print(''.join(line))

def get_coordinates(str_coordinates:str, invert=True) -> list[tuple[int,int]]:
    coordinates = []
    for line in str_coordinates.splitlines():
        s = line.split(',')
        x, y = int(s[0]), int(s[1])
        if invert:
            coordinates.append((y,x))
        else:
            coordinates.append((x,y))
    return coordinates

def find_best_route(map, starting_point:tuple[int,int], ending_point:tuple[int,int]) -> int:
    visiting_list = [(starting_point, [])]
    visited = set()
    m, n = len(map), len(map[0])
    def get_dist(coords):
        return abs(ending_point[0] - coords[0]) + abs(ending_point[1] - coords[1])
    while len(visiting_list) > 0:
        idx, (coords, steps) = min(enumerate(visiting_list), key= lambda x: len(x[1][1]) + get_dist(x[1][0]))
        visiting_list.pop(idx)
        if coords in visited:
            continue
        visited.add(coords)
        if coords == ending_point:
            return len(steps)
        y, x = coords
        c = [l.copy() for l in map]
        for i,j in steps:
            c[i][j] = 'W'
        clear()
        print_map(c)
        # print_map(map)
        for (i, j) in [(-1,0),
                (0, -1),    (0,1),
                       (1, 0)]:
            yi, xi = y+i, x+j
            if yi >= m or xi >= n or xi < 0 or yi < 0:
                continue
            if not ((yi, xi) in visited or map[yi][xi] == WALL):
                visiting_list.append(((yi,xi),steps + [(yi, xi)]))
    return -1

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    grid_max_val = 70
    map = get_map(grid_max_val)
    coordinates = get_coordinates(content)
    for (y,x) in coordinates[:1024]:
        map[y][x] = '#'

    print_map(map)
    print(find_best_route(map,(0,0),(grid_max_val,grid_max_val)))


if __name__ == "__main__":
    main()

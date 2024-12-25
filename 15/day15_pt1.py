from copy import deepcopy as copy

UP = '^'
DOWN = 'v'
RIGHT = '>'
LEFT = '<'
ROBOT = '@'
BOX = 'O'
WALL = '#'
EMPTY = '.'

def print_map(map:list[list[str]]) -> None:
    for line in map:
        print(''.join(line))

def get_map(str_map:str) -> list[list[str]]:
    return [list(line) for line in str_map.splitlines()]

def get_movements_list(str_movements:str) -> list[str]:
    return [m for m in list(str_movements) if m != '\n']

def move_block(map:list[list[str]], direction:str, location:tuple[int,int]) -> bool:
    i, j = location
    if map[i][j] == EMPTY:
        return True
    if map[i][j] == WALL:
        return False

    if direction == DOWN:
        _i = i+1
        moved = move_block(map, direction, (_i, j))
        if moved:
            map[_i][j] = map[i][j]
            map[i][j] = EMPTY
    elif direction == UP:
        _i = i-1
        moved = move_block(map, direction, (_i, j))
        if moved:
            map[_i][j] = map[i][j]
            map[i][j] = EMPTY
    elif direction == RIGHT:
        _j = j+1
        moved = move_block(map, direction, (i, _j))
        if moved:
            map[i][_j] = map[i][j]
            map[i][j] = EMPTY
    elif direction == LEFT:
        _j = j-1
        moved = move_block(map, direction, (i, _j))
        if moved:
            map[i][_j] = map[i][j]
            map[i][j] = EMPTY
    else:
        raise Exception(f'direction {direction} not found')
    return moved

def apply_movement(map:list[list[str]], movement:str, robot_location:tuple[int,int]) -> tuple[list[list[str]], tuple[int,int]]:
    cmap = copy(map)
    i,j = robot_location
    if move_block(cmap, movement, robot_location):
        if movement == DOWN:
            _i = i+1
            robot_location = (_i, j)
        elif movement == UP:
            _i = i-1
            robot_location = (_i, j)
        elif movement == RIGHT:
            _j = j+1
            robot_location = (i, _j)
        elif movement == LEFT:
            _j = j-1
            robot_location = (i, _j)
        else:
            raise Exception(f'movement {movement} not found')
    return cmap, robot_location

def compute_GPS(map:list[list[str]]) -> int:
    gps = 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == BOX:
                gps += (i * 100) + j
    return gps

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    content_split = content.split('\n\n')
    assert len(content_split) == 2, len(content_split)
    map, movements = get_map(content_split[0]), get_movements_list(content_split[1])

    print("initial configuration:")
    print_map(map)
    print()
    ri, rj = 0, 0
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == ROBOT:
                ri,rj = i,j
                break

    for movement in movements:
        map, (ri,rj) = apply_movement(map, movement, (ri,rj))
    print("final configuration:")
    print_map(map)
    print(compute_GPS(map))

if __name__ == "__main__":
    main()

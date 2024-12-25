from copy import deepcopy as copy
from os import system

def clear():
    system('clear')

UP = '^'
DOWN = 'v'
RIGHT = '>'
LEFT = '<'
ROBOT = '@'
BOX_OPEN = '['
BOX_CLOSE = ']'
WALL = '#'
EMPTY = '.'

def print_map(map:list[list[str]]) -> None:
    for line in map:
        print(''.join(line))

def get_map(str_map:str) -> list[list[str]]:
    str_map = str_map.replace('#','##').replace('O','[]').replace('.','..').replace('@','@.')
    return [list(line) for line in str_map.splitlines()]

def get_movements_list(str_movements:str) -> list[str]:
    return [m for m in list(str_movements) if m != '\n']

def check_box(map:list[list[str]], direction:str, location_open:tuple[int,int], location_close:tuple[int,int]) -> bool:
    oi, oj = location_open
    ci, cj = location_close
    if map[oi][oj] == EMPTY and map[ci][cj] == EMPTY:
        return True
    if map[oi][oj] == WALL or map[ci][cj] == WALL:
        return False

    if direction == DOWN:
        _oi, _ci = oi+1, ci+1
        moved = True
        if map[_oi][oj] == BOX_OPEN:
            moved = check_box(map, direction, (_oi,oj),(_ci,cj))
        elif map[_oi][oj] == BOX_CLOSE: 
            moved = check_box(map, direction, (_oi,oj-1), (_oi,oj)) 
        else:
            moved = not map[_oi][oj] == WALL

        if map[_ci][cj] == BOX_OPEN:
            moved = moved and check_box(map, direction, (_ci,cj),(_ci,cj+1)) 
        elif map[_ci][cj] == BOX_CLOSE: 
            moved = moved and check_box(map, direction, (_oi,oj),(_ci,cj))
        else:
            moved = moved and not map[_ci][cj] == WALL

    elif direction == UP:
        _oi, _ci = oi-1, ci-1
        moved = True
        if map[_oi][oj] == BOX_OPEN:
            moved = check_box(map, direction, (_oi,oj),(_ci,cj))
        elif map[_oi][oj] == BOX_CLOSE: 
            moved = check_box(map, direction, (_oi,oj-1), (_oi,oj)) 
        else:
            moved = not map[_oi][oj] == WALL

        if map[_ci][cj] == BOX_OPEN:
            moved = moved and check_box(map, direction, (_ci,cj),(_ci,cj+1)) 
        else:
            moved = moved and not map[_ci][cj] == WALL
    else:
        raise Exception(f'direction {direction} not found')

    return moved   

def move_box(map:list[list[str]], direction:str, location_open:tuple[int,int], location_close:tuple[int,int]) -> None:
    oi, oj = location_open
    ci, cj = location_close
    if map[oi][oj] == EMPTY and map[ci][cj] == EMPTY:
        return 
    assert map[oi][oj] != WALL and map[ci][cj] != WALL, f'wall found at {location_open, location_close}'

    if direction == DOWN:
        _oi, _ci = oi+1, ci+1
        if map[_oi][oj] == BOX_OPEN:
            move_box(map, direction, (_oi,oj),(_ci,cj))
        elif map[_oi][oj] == BOX_CLOSE: 
            move_box(map, direction, (_oi,oj-1), (_oi,oj)) 
        else:
            assert not map[_oi][oj] == WALL, f'wall found at {_oi, oj}'
        map[_oi][oj] = map[oi][oj]
        map[oi][oj] = EMPTY

        if map[_ci][cj] == BOX_OPEN:
            move_box(map, direction, (_ci,cj),(_ci,cj+1)) 
        else:
            assert not map[_ci][cj] == WALL, f'wall found at {_ci, cj}'
        map[_ci][cj] = map[ci][cj]
        map[ci][cj] = EMPTY

    elif direction == UP:
        _oi, _ci = oi-1, ci-1
        if map[_oi][oj] == BOX_OPEN:
            move_box(map, direction, (_oi,oj),(_ci,cj))
        elif map[_oi][oj] == BOX_CLOSE: 
            move_box(map, direction, (_oi,oj-1), (_oi,oj)) 
        else:
            assert not map[_oi][oj] == WALL, f'wall found at {_oi, oj}'
        map[_oi][oj] = map[oi][oj]
        map[oi][oj] = EMPTY

        if map[_ci][cj] == BOX_OPEN:
            move_box(map, direction, (_ci,cj),(_ci,cj+1)) 
        else:
            assert not map[_ci][cj] == WALL, f'wall found at {_ci, cj}'
        map[_ci][cj] = map[ci][cj]
        map[ci][cj] = EMPTY
    else:
        raise Exception(f'direction {direction} not found')



def move_block(map:list[list[str]], direction:str, location:tuple[int,int]) -> bool:
    i, j = location
    if map[i][j] == EMPTY:
        return True
    if map[i][j] == WALL:
        return False

    if map[i][j] == BOX_OPEN:
        assert map[i][j+1] == BOX_CLOSE, f'expected ], found: {map[i][j+1]}'
    elif map[i][j] == BOX_CLOSE:
        assert map[i][j-1] == BOX_OPEN, f'expected [, found: {map[i][j+1]}'

    if direction == DOWN:
        _i = i+1
        if map[_i][j] == BOX_OPEN:
            moved = check_box(map, direction, (_i,j), (_i,j+1))
            if moved:
                move_box(map, direction, (_i,j), (_i,j+1))
        elif map[_i][j] == BOX_CLOSE:
            moved = check_box(map, direction, (_i,j-1), (_i,j))
            if moved:
                move_box(map, direction, (_i,j-1), (_i,j)) 
        else:
            moved = move_block(map, direction, (_i, j))
        if moved:
            map[_i][j] = map[i][j]
            map[i][j] = EMPTY
    elif direction == UP:
        _i = i-1
        if map[_i][j] == BOX_OPEN:
            moved = check_box(map, direction, (_i,j), (_i,j+1))
            if moved:
                move_box(map, direction, (_i,j), (_i,j+1))
        elif map[_i][j] == BOX_CLOSE:
            moved = check_box(map, direction, (_i,j-1), (_i,j))
            if moved:
                move_box(map, direction, (_i,j-1), (_i,j)) 
        else:
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
            if map[i][j] == BOX_OPEN:
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
        clear()
        print_map(map)
    print("final configuration:")
    print_map(map)
    print(compute_GPS(map))

if __name__ == "__main__":
    main()

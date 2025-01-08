from typing import Literal
from copy import deepcopy as copy
from time import sleep

def loop(new, old) -> bool:
    if new == old:
        return True
    if new == '|' and (old== '^' or old == 'v'):
        return True
    if new == '-' and (old== '>' or old == '<'):
        return True
    return new == '+'

def print_map(map):
    for i in range(len(map)):
        print(''.join(map[i]))

def to_map(board:str) -> list[list[Literal['.','#','^','>','<','v']]]:
    map = []
    for line in board.splitlines():
        map.append(list(line))
    return map

to_string_direction = {
    '^': 'up',
    '>': 'right',
    '<': 'left',
    'v': 'down'
}

to_symbol_direction = {
    'up': '^',
    'right': '>',
    'left': '<',
    'down': 'v'
}

turn = {
    'down': 'left',
    'left': 'up',
    'right': 'down',
    'up': 'right'
}

get_direction = {
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1),
    'up': (-1, 0)
}

def forward(map:list[list[str]], 
            current_state:tuple[Literal['up','down','right','left'], int, int, str], 
            count_mark:bool=False) -> tuple[list[list[str]], int, int, str]|Literal['end','turn', 'loop']:
    str_state, y, x, old_symbol = current_state
    y_mod, x_mod = get_direction[str_state]

    if y + y_mod >= len(map) or x + x_mod >= len(map[0]):
        return 'end'
    if y + y_mod < 0 or x + x_mod < 0:
        return 'end'

    new_position = map[y+y_mod][x+x_mod]
    # assert  map[y][x] in to_string_direction, f"inconsistent current position. Expected guard, got: {map[y][x]}"
    # assert not map[y+y_mod][x+x_mod] in to_string_direction, f"inconsistent current position. Expected generic map location, got: {map[y+y_mod][x+x_mod]}"
    if new_position == '#' or new_position == "0":
        return 'turn'
    next_old = '0' if map[y+y_mod][x+x_mod] == '.' else map[y+y_mod][x+x_mod]
    map[y+y_mod][x+x_mod] = map[y][x] 
    if count_mark:
        if new_position != '.' and int(new_position) > 3:
            return 'loop'
        map[y][x] = str(int(old_symbol) + 1)
    else:
        map[y][x] = 'X'
    return map, y+y_mod, x+x_mod, next_old

def get_loops(map:list[list[str]], start_state:tuple[Literal['up','down','right','left'], int, int], obstacle_positions:list[tuple[int,int]]) -> int:
    loops = 0
    for (oi, oj) in obstacle_positions:
        obstacle_map = copy(map)
        obstacle_map[oi][oj] = "0"
        current_state = copy(start_state)
        next = forward(obstacle_map, current_state, count_mark=True)
        while next != 'end' and next != 'loop':
            if next == 'turn':
                # print('turn', end= ' ')
                current_direction, i, j, old_symbol = current_state
                current_state = (turn[current_direction], i, j, old_symbol)
                obstacle_map[i][j] = to_symbol_direction[current_state[0]]
            else:
                # print('step', end= ' ')
                obstacle_map, i, j, old_symbol = next
                current_state = current_state[0], i, j, old_symbol
            # print(i,j)
            # print_map(obstacle_map)
            next = forward(obstacle_map, current_state, count_mark=True)
            # sleep(.2)

        loops += 1 if next == 'loop' else 0
        # print(next)
    return loops

def main():
    f = open('input.txt')
    content = f.read()
    f.close()

    map = to_map(content)
    current_state = None
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] in ['^','>','<','v']:
                current_state = (to_string_direction[map[i][j]], i, j, '0')
                break

    assert current_state is not None, "unknown current state"

    p_obstacle_positions = [[(i,j) for j in range(len(map[0]))] for i in range(len(map))]
    obstacle_positions = []
    for l in p_obstacle_positions:
        obstacle_positions += l
    print('got obstacles')
    loops = get_loops(map, current_state, obstacle_positions)
    print(loops)
if __name__ == "__main__":
    main()

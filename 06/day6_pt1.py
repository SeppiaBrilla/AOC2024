from typing import Literal

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

def forward(map:list[list[Literal['.','#','^','>','<','v', 'X']]], 
            current_state:tuple[Literal['up','down','right','left'], int, int]) -> tuple[list[list[Literal['.','#','^','>','<','v', 'X']]], int, int, int]|Literal['end','turn']:
    str_state, y, x = current_state
    y_mod, x_mod = get_direction[str_state]

    if y + y_mod >= len(map) or x + x_mod >= len(map[0]):
        return 'end'
    if y + y_mod < 0 or x + x_mod < 0:
        return 'end'

    new_position = map[y+y_mod][x+x_mod]
    assert not map[y][x] == '.' and not map[y][x] == '#', f"inconsistent current position. Expected guard, got: {map[y][x]}"
    assert new_position == '.' or new_position == '#' or new_position == 'X', f"inconsistent current position. Expected generic map location, got: {map[y+y_mod][x+x_mod]}"
    if new_position == '#':
        return 'turn'
    visited = 1 if new_position != 'X' else 0
    map[y+y_mod][x+x_mod] = map[y][x]
    map[y][x] = 'X'
    return map, y+y_mod, x+x_mod, visited

def main():
    f = open('input.txt')
    content = f.read()
    f.close()

    map = to_map(content)
    current_state = None
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] in ['^','>','<','v']:
                current_state = (to_string_direction[map[i][j]], i, j)
                break

    assert current_state is not None, "unknown current state"

    next = forward(map, current_state)
    visited = 1
    while next != 'end':
        if next == 'turn':
            # print('turn', end=' ')
            current_direction, i, j = current_state
            current_state = (turn[current_direction], i, j)
            map[i][j] = to_symbol_direction[current_state[0]]
        else:
            map, i, j, new_visited = next
            current_state = current_state[0], i, j
            visited += new_visited
            # print('step', end=' ')
        # print(visited, i, j)
        # print_map(map)
        next = forward(map, current_state)
    print(visited)

if __name__ == "__main__":
    main()

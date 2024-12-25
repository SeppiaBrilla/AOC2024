from os import system

START = 'S'
END = 'E'
WALL = '#'
PATH = '.'

NORTH = 0
EAST = 1
SOUTH = 2
OVEST = 3

dir_txt = {
    NORTH: '^',
    SOUTH: 'v',
    OVEST: '<',
    EAST: '>'
}

class PartialPath:
    def __init__(self, location:tuple[int,int], past_steps:list[tuple[tuple[int,int],int]], direction:int, turn:int, cost:int, end_location:tuple[int,int]) -> None:
        self.location = location
        self.path = past_steps + [(self.location, direction)]
        self.direction = direction
        self.turn = turn
        self.past_cost = cost
        self.end_location = end_location
        self.T = (location, direction)

    def cost(self):
        return self.turn * 1000 + len(self.path) - 1

    def small_cost(self):
        return self.past_cost + abs(self.location[0] - self.end_location[0]) + abs(self.location[1] - self.end_location[1])

    def add_path(self, map:list[list[str]]) -> list[list[str]]:
        new_map = map.copy()
        for ((i,j), dir) in self.path:
            new_map[i][j] = f'\33[31m{dir_txt[dir]}\33[0m'
        return new_map

def is_opposite(current_direction:int, next_direction:int) -> bool:
    if current_direction == NORTH:
        return not next_direction == SOUTH
    elif current_direction == SOUTH:
        return not next_direction == NORTH
    elif current_direction == EAST:
        return not next_direction == OVEST
    else:
        assert current_direction == OVEST
        return not next_direction == EAST

def clear():
    system('clear')

def get_map(map_str:str) -> list[list[str]]:
    return [list(line) for line in map_str.splitlines()]

def print_map(map:list[list[str]]) -> None:
    for line in map:
        print(''.join(line))

def get_direction(next_direction:tuple[int,int]) -> int:
    if next_direction == (-1, 0):
        return NORTH
    if next_direction == ( 0, -1):
        return OVEST
    if next_direction == ( 0, 1):
        return EAST
    if next_direction == ( 1, 0):
        return SOUTH
    raise Exception(f'next direction {next_direction} not found')

def explore(map:list[list[str]], starting_point:tuple[tuple[int,int], int], end_location:tuple[int,int]) -> list[PartialPath]|None:
    neibs = [          (-1, 0), 
             ( 0, -1),          ( 0, 1), 
                       ( 1, 0)]

    visited = set()
    visited.add(starting_point)
    starting_point_path = PartialPath(starting_point[0], [], starting_point[1], 0, 0, end_location)
    visiting_list = [starting_point_path]
    ends = []
    while len(visiting_list) > 0:
        idx, path = min(enumerate(visiting_list), key= lambda x: x[1].cost())
        current_location, direction = path.T
        visiting_list.pop(idx)
        i,j = current_location

        if map[i][j] == END:
            ends.append(path)

        visited.add(((i,j), direction))
        print(len(visiting_list), end='\r')

        for (k, v) in neibs:
            ni, nj = i+k, j+v
            if map[ni][nj] == WALL:
                continue
            next_direction = get_direction((k,v))
            if not is_opposite(direction, next_direction):
                pass
            if not map[ni][nj] == WALL:
                if not ((ni,nj), next_direction) in visited:
                    new_turn = path.turn
                    if next_direction != direction:
                        new_turn += 1
                    new_path = PartialPath((ni,nj), path.path, next_direction, new_turn, path.small_cost(), end_location)
                    visiting_list.append(new_path)
        
    if len(ends) > 0:
        mins = []
        v = min(ends, key = lambda x: x.cost())
        for e in ends:
            if e.cost() == v.cost():
                mins.append(e)
        return mins
    return None

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    start_location = (0,0)
    end_location = (0,0)
    map = get_map(content)
    for i in range(len(map)):
        for j in range(len(map[0])):
            if map[i][j] == START:
                start_location = (i,j)
            if map[i][j] == END:
                end_location = (i,j)
    mins = explore(map, (start_location, EAST), end_location)
    assert mins is not None
    spots = set()
    for m in mins:
        for p in m.path:
            if not p[0] in spots:
                map[p[0][0]][p[0][1]] = '\33[31mO\33[0m'
                spots.add(p[0])

    clear()
    print_map(map)
    print(len(spots))

    
if __name__ == "__main__":
    main()

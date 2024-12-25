import os

def clear():
    os.system('clear')

def print_map(map:list[list[str]]) -> None:
    for line in map:
        print(''.join(line))

def get_robots(robot_list:str) -> list[dict[str,tuple[int,int]]]:
    robots = []
    for line in robot_list.splitlines():
        s = line.split(' ')
        assert 'p=' in s[0] and 'v=' in s[1], s
        position_str, velocity_str = s[0].replace('p=','').split(','), s[1].replace('v=','').split(',')

        robots.append({'p': (int(position_str[0]), int(position_str[1])), 'v':(int(velocity_str[0]), int(velocity_str[1]))})

    return robots

def place_robots(map:list[list[str]], robots:list[dict[str,tuple[int,int]]]) -> list[list[str]]:
    for robot in robots:
        j,i = robot['p']
        map[i][j] = '1' if map[i][j] == '.' else str(int(map[i][j]) + 1)

    return map

def move(robot:dict[str,tuple[int,int]], map_size:tuple[int,int]) -> dict[str,tuple[int,int]]:
    m, n = map_size
    j, i = robot['p']
    vj, vi = robot['v']

    robot['p'] = ((j + vj) % n, (i + vi) % m)

    return robot

def move_all_robots(robots:list[dict[str,tuple[int,int]]], map_size:tuple[int,int]) -> list[dict[str,tuple[int,int]]]:
    return [move(robot, map_size) for robot in robots]

def check_stop(map:list[list[str]]) -> bool:
    for i in range(4, len(map) - 4):
        for j in range(4, len(map[0]) - 4):
            if map[i][j] == '.':
                continue
            stop = True
            for k in range(i-4, i+5):
                for f in range(j-4,j+5):
                    stop = stop and map[k][f] !='.'
            if stop:
                return True

    return False

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    m, n = 103, 101
    map = [['.' for _ in range(n)] for _ in range(m)]
    robots = get_robots(content)
    i = ''
    evolutions = 0
    while i != 'stop':
        clear()
        robots = move_all_robots(robots, (m,n))
        map = [['.' for _ in range(n)] for _ in range(m)]
        map = place_robots(map, robots)
        print_map(map)
        evolutions += 1
        if check_stop(map):
            i = input(f'{evolutions} ?')

    print(evolutions)
if __name__ == "__main__":
    main()

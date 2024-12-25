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

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    m, n = 103, 101
    middle_m, middle_n = m // 2, n // 2
    print(middle_m, middle_n, m,n)
    map = [['.' for _ in range(n)] for _ in range(m)]
    robots = get_robots(content)
    for _ in range(100):
        robots = move_all_robots(robots, (m,n))
    map = place_robots(map, robots)
    print_map(map)
    quadrants = [
        [m[:middle_n] for m in map[:middle_m]], 
        [m[middle_n+1:] for m in map[middle_m+1:]], 
        [m[middle_n+1:] for m in map[:middle_m]], 
        [m[:middle_n] for m in map[middle_m+1:]]
    ]

    safety_factor = 1
    for quadrant in quadrants:
        q_safety = 0
        for r in quadrant:
            for p in r:
                if p != '.':
                    q_safety += int(p)
        safety_factor *= q_safety 

    print(safety_factor)

if __name__ == "__main__":
    main()

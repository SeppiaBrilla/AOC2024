def get_machines(content:str) -> list[dict[str,dict[str,int]]]:
    machines = []
    machines_str = content.split('\n\n')
    for machine_str in machines_str:
        machine = {}
        for line in machine_str.splitlines():
            if 'A' in line:
                removed = line.replace('Button A:','').replace('X','').replace('Y','')
                removed = removed.split(', ')
                machine ['A'] = {'X':int(removed[0]),'Y': int(removed[1])}
            elif 'B' in line:
                removed = line.replace('Button B:','').replace('X','').replace('Y','')
                removed = removed.split(', ')
                machine ['B'] = {'X':int(removed[0]),'Y': int(removed[1])}
            else:
                assert 'Prize' in line, line
                removed = line.replace('Prize:','').replace('X','').replace('Y','').replace('=','')
                removed = removed.split(', ')
                machine ['prize'] = {'X':int(removed[0]),'Y': int(removed[1])}
        machines.append(machine)
    return machines

def go_greedy(machine:dict[str,dict[str,int]]) -> list[tuple[int,int]]:
    max_press = 100
    prize = machine['prize']
    prize_x, prize_y = prize['X'], prize['Y']
    main_button = 'A'
    secondary_button = 'B'
    main_machine = machine[main_button]
    main_press, secondary_press = 0, 0
    secondary_machine = machine[secondary_button]
    current_x, current_y = 0, 0
    solutions = []

    while  True:
        if max_press < main_press:
            break
        
        main_press += 1

        current_x = main_press * main_machine['X']
        current_y = main_press * main_machine['Y']

        remain_x, remain_y = prize_x - current_x, prize_y - current_y
        secondary_x, secondary_y = remain_x // secondary_machine['X'], remain_y // secondary_machine['Y']
        if secondary_x == secondary_y:
            if secondary_x * secondary_machine['X'] - remain_x == 0 and secondary_y * secondary_machine['Y'] - remain_y == 0:
                secondary_press = secondary_x
                solutions.append((main_press, secondary_press))
        
    return solutions

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    machines = get_machines(content)
    spent_tokens = 0
    for machine in machines:
        solutions = go_greedy(machine)
        if len(solutions) > 0:
            min_token = 1000000
            for solution in solutions:
                solution_tokens = solution[0] * 3 + solution[1]
                if solution_tokens < min_token:
                    min_token = solution_tokens
            spent_tokens += min_token   
        
    print(spent_tokens)

if __name__ == "__main__":
    main()

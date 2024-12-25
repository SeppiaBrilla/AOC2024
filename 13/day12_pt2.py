from sympy import symbols, Eq, solve

def get_machines(content:str) -> list[dict[str,dict[str,int]]]:
    machines = []
    machines_str = content.split('\n\n')
    conversion_error = 10000000000000
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
                machine ['prize'] = {'X':int(removed[0]) + conversion_error,'Y': int(removed[1]) + conversion_error}
        machines.append(machine)
    return machines

def get_solutions(machine:dict[str,dict[str,int]]) -> tuple[int,int]:
    x1, x2 = symbols('x1 x2')
    eq1 = Eq(machine['A']['X']* x1 + machine['B']['X'] * x2, machine['prize']['X'])
    eq2 = Eq(machine['A']['Y']* x1 + machine['B']['Y'] * x2, machine['prize']['Y'])
    eq_solutions = solve((eq1, eq2), (x1, x2))
    for s in eq_solutions:
        if not eq_solutions[s] == int(eq_solutions[s]):
            return -1, -1
    return (eq_solutions[x1], eq_solutions[x2])

def main():
    f = open('input.txt')
    content = f.read()
    f.close()

    machines = get_machines(content)
    spent_tokens = 0
    for machine in machines:
        solution = get_solutions(machine)
        if (-1, -1) == solution:
            continue
        solution_tokens = solution[0] * 3 + solution[1]
        spent_tokens += solution_tokens
        
    print(spent_tokens)

if __name__ == "__main__":
    main()

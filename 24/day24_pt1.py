from typing import Literal, Callable

TRUE = 1
FALSE = 0

BOOLEAN = Literal[0, 1]
LOGIC_GATE = tuple[tuple[str,str],Callable, str]

def and_gate(i1:BOOLEAN, i2:BOOLEAN) -> BOOLEAN:
    return min(i1,i2)

def or_gate(i1:BOOLEAN, i2:BOOLEAN) -> BOOLEAN:
    return max(i1,i2)

def xor_gate(i1:BOOLEAN, i2:BOOLEAN) -> BOOLEAN:
    return TRUE if i1 != i2 else FALSE

logic_gates_functions = {
    'AND': and_gate,
    'OR': or_gate,
    'XOR': xor_gate
}

def get_initial_values(initial_values_str:str) -> list[tuple[str,BOOLEAN]]:
    initial_values = []
    for line in initial_values_str.splitlines():
        line_split = line.split(': ')
        initial_values.append((line_split[0], int(line_split[1])))
    return initial_values

def get_logic_gates(logic_gates_str:str) -> list[LOGIC_GATE]:
    logic_gates = []
    for line in logic_gates_str.splitlines():
        line_first_split = line.split(' -> ')
        function = line_first_split[0]
        result = line_first_split[1].replace(' ','')
        line_second_split = function.split(' ')
        logic_gates.append(((line_second_split[0], line_second_split[2]), logic_gates_functions[line_second_split[1]], result))
    return logic_gates

def simulate(logic_gate:LOGIC_GATE, variables:dict[str,BOOLEAN]) -> tuple[str,BOOLEAN]:
    (v1, v2), function, res = logic_gate
    return (res, function(variables[v1],variables[v2]))

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    
    split_content = content.split('\n\n')
    initial_values = get_initial_values(split_content[0])
    logic_gates = get_logic_gates(split_content[1])
    variables = {}
    for val in initial_values:
        variables[val[0]] = val[1]

    i = 0
    while len(logic_gates) > 0:
        # print(len(logic_gates), i)
        logic_gate = logic_gates[i]
        (v1,v2), _, _ = logic_gate
        if v1 in variables and v2 in variables:
            logic_gates.pop(i)
            res_name, res_value = simulate(logic_gate, variables)
            variables[res_name] = res_value
            i = max(i-1, 0)
        else:
            i += 1
            i = i % len(logic_gates)

    z_vars = sorted([v for v in variables.keys() if v[0] == 'z'], reverse=True)
    res =''.join([str(variables[v]) for v in z_vars])
    print(res, int(res,2))
    

if __name__ == "__main__":
    main()

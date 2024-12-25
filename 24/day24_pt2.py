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

def left_pad(g, pad): 
    while len(g) < pad:
        g = '0' + g
    return g

class TreeNode:
    def __init__(self, variable_name:str, op:Callable|None=None, child1:'TreeNode|None'=None, child2:'TreeNode|None'=None, value:int|None=None) -> None:
        self.variable = variable_name
        self.op = op
        self.child1 = child1
        self.child2 = child2
        self.value = value
    def solve(self, variables:dict[str,BOOLEAN]):
        if self.variable in variables:
            return variables[self.variable]
        assert self.child2 is not None and self.child1 is not None and self.op is not None, self.variable
        return self.op(self.child1.solve(variables), self.child2.solve(variables))

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

def has_x(tree:TreeNode) -> bool:
    if 'x' in tree.variable:
        return True
    one = has_x(tree.child1) if tree.child1 is not None else False
    two = has_x(tree.child2) if tree.child2 is not None else False
    return one or two

def has_y(tree:TreeNode) -> bool:
    if 'y' in tree.variable:
        return True
    one = has_y(tree.child1) if tree.child1 is not None else False
    two = has_y(tree.child2) if tree.child2 is not None else False
    return one or two

def is_complete(tree:TreeNode) -> bool:
    return has_x(tree) and has_y(tree)

def all_binary_comb(elem:int) -> list[list[int]]:
    if elem == 1:
        return [[0], [1]]
    all = []
    for e in all_binary_comb(elem-1):
        all += [[0] + e, [1] + e]
    return all

def print_tree(node: TreeNode|None, indent: int = 0, skipp=set()) -> None:
    if node is None:
        return

    op_conv = {or_gate: 'or', xor_gate:'xor', and_gate:'and'}

    prefix = " " * (indent * 2)
    node_info = f"{node.variable}"
    if node.op is not None:
        node_info += f" [op: {op_conv[node.op]}]" 
    print(prefix + node_info)

    if node.child1:
        if node.child1.variable in skipp:
            print(" " * ((indent+1) * 2) + node.child1.variable)
        else:
            print_tree(node.child1, indent + 1)
    if node.child2:
        if node.child2.variable in skipp:
            print(" " * ((indent+1) * 2) + node.child2.variable)
        else:
            print_tree(node.child2, indent + 1)

def get_variables(tree:TreeNode) -> set[str]:
    s = set()
    s.add(tree.variable)
    if tree.child1 is not None:
        s = s.union(get_variables(tree.child1))
    if tree.child2 is not None:
        s = s.union(get_variables(tree.child2)) 
    return s

def get_subtree(name:str, tree:TreeNode) -> TreeNode|None:
    if tree.variable == name:
        return tree
    if tree.child1 is not None:
        t = get_subtree(name, tree.child1)
        if t is not None:
            return t
    if tree.child2 is not None:
        t = get_subtree(name, tree.child2)
        if t is not None:
            return t
    return None

def get_adder_trees(logic_gates:list[LOGIC_GATE], variables:dict[str,int]) -> list[TreeNode]:
    trees = []
    partials = {}
    for gate in logic_gates:
        (v1, v2), op, ve = gate
        if not v1 in partials:
            if 'x' in v1 or 'y' in v1:
                partials[v1] = TreeNode(v1, value=variables[v1])
            else:
                partials[v1] = TreeNode(v1)
        if not v2 in partials:
            if 'x' in v2 or 'y' in v2:
                partials[v2] = TreeNode(v2, value=variables[v2])
            else:
                partials[v2] = TreeNode(v2)
        assert not ('x' in ve or 'y' in ve), gate
        if ve in partials:
            assert partials[ve].child1 == None and partials[ve].child2 == None and partials[ve].value == None and partials[ve].op == None
            partials[ve].child1 = partials[v1]
            partials[ve].child2 = partials[v2]
            partials[ve].op = op
        else:
            partials[ve] = TreeNode(ve, child1=partials[v1], child2=partials[v2], op=op)
    for k,v in partials.items():
        if 'z' in k:
            assert is_complete(v), f'tree {k} not complete'
            trees.append(v)
    return trees

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
    errors = set()
    for ((v1,v2),op, ve) in logic_gates:
        if ve[0] == 'z' and op != xor_gate and ve != 'z45': # all z operations (but the last one) must be the result of a xor operation
            errors.add(ve)
        if op == xor_gate: 
            if all(not x[0] in ['x', 'y', 'z'] for x in [v1,v2,ve]): # all xor operations are the result of a base value or have as result a final value
                errors.add(ve)
            if any(ve in [vv1,vv2] and op2 == or_gate for ((vv1, vv2), op2, _) in logic_gates): # all final values of a xor cannot be used as initial operator of an or
                errors.add(ve)
        if op == and_gate:
            if any(ve in [vv1, vv2] and not op2 == or_gate for ((vv1,vv2), op2, _) in logic_gates): # all and operations are the initial value of a or gate (if not x00 is an operand)
                if 'x00' not in [v1,v2]:
                    errors.add(ve)

    print(','.join(sorted(errors)))

if __name__ == "__main__":
    main()

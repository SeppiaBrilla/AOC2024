def unroll(l:list):
    if len(l) == 0:
        return l
    if isinstance(l[0][0],str):
        return l

    if isinstance(l[0], list):
        lu = []
        for li in l:
            lu += unroll(li)
        return lu
    return l

def get_operations_recursive(ops=[], steps=0):
    if steps == 0:
        return ops
    return [get_operations_recursive(ops=ops+['+'], steps=steps-1), get_operations_recursive(ops=ops+['*'], steps=steps-1), get_operations_recursive(ops=ops+['|'], steps=steps-1)]

def get_operations(steps:int) -> list[list[str]]:
    ops = get_operations_recursive(steps=steps)
    unrolled = unroll(ops)
    s = set([''.join(u) for u in unrolled])
    return [list(o) for o in list(s)]
    
def mult(x):
    res = 1
    for xi in x:
        res *= xi
    return res

def concatenate(x):
    return int(''.join([str(xi) for xi in x]))

def test(test_value:int, numbers:list[int], operations:list[list[str]]) -> bool:
    ops_dict = {'+':sum, '*': mult, '|': concatenate}

    for ops in operations:
        if len(ops) == 1:
            if test_value == ops_dict[ops[0]](numbers):
                return True
        else:
            val = ops_dict[ops[0]]([numbers[0],numbers[1]])
            for i in range(1, len(ops)):
                val = ops_dict[ops[i]]([val,numbers[i+1]])
            if val == test_value:
                return True
    return False

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    equations = []
    for line in content.splitlines():
        line = line.split(':')
        test_value = int(line[0])
        numbers = [int(v) for v in line[1].split(' ') if v != '']
        equations.append({
            'test_value': test_value,
            'numbers': numbers,
            'operations': len(numbers) - 1
        })
    # print(equations[2])
    # ops = get_operations(equations[2]['operations'])
    # print(test(equations[2]['test_value'], equations[2]['numbers'], ops))
    all_ops = {}
    calib_res = 0
    for eq in equations:
        if not eq['operations'] in all_ops:
            all_ops[eq['operations']] = get_operations(eq['operations'])
        ops = all_ops[eq['operations']]
        if test(eq['test_value'], eq['numbers'], ops):
            calib_res += eq['test_value']

    print(calib_res)

if __name__ == "__main__":
    main()

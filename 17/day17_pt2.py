class Device:
    def __init__(self, A:int, B:int, C:int) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.pointer = 0
        self.out_res = []
        self.op_code = {
            0: self.__adv,
            1: self.__bxl,
            2: self.__bst,
            3: self.__jnz,
            4: self.__bxc,
            5: self.__out,
            6: self.__bdv,
            7: self.__cdv,
        }
        self.operands = {
            0: lambda : 0,
            1: lambda : 1,
            2: lambda : 2,
            3: lambda : 3,
            4: self.__get_A,
            5: self.__get_B,
            6: self.__get_C
        }

    def __get_A(self):
        return self.A
    def __get_B(self):
        return self.B
    def __get_C(self):
        return self.C
    def __adv(self, x):
        self.A = int(self.__get_A() / 2 ** self.operands[x]())
        self.pointer += 2
    def __bxl(self, x):
        self.B = self.__get_B() ^ x
        self.pointer += 2
    def __bst(self, x):
        self.B = self.operands[x]() % 8
        self.pointer += 2
    def __jnz(self, x):
        self.pointer = self.pointer + 2 if self.__get_A() == 0 else x
    def __bxc(self, x):
        self.B = self.__get_B() ^ self.__get_C()
        self.pointer += 2
    def __out(self, x):
        x = self.operands[x]() % 8
        self.out_res.append(x)
        self.pointer += 2
    def __bdv(self, x):
        self.B = int(self.__get_A() / 2 ** self.operands[x]())
        self.pointer += 2
    def __cdv(self, x):
        self.C = int(self.__get_A() / 2 ** self.operands[x]())
        self.pointer += 2


    def execute_instructions(self, instruction_list:list[int], verbose = True) -> None:
        self.pointer = 0
        max_idx = len(instruction_list)
        while self.pointer < max_idx - 1:
            operation, parameter = instruction_list[self.pointer], instruction_list[self.pointer +1]
            self.op_code[operation](parameter)
        if verbose:
            print(','.join([str(x) for x in self.out_res]))
            
    def execute_instruction(self, operation:int, parameter:int):
        self.op_code[operation](parameter)

def get_registers_and_program(content:str) -> tuple[tuple[int,int,int],list[int]]:
    content_split = content.split('\n\n')
    A, B, C = 0, 0, 0
    for line in content_split[0].splitlines():
        if 'A' in line:
            A = int(line.replace('Register A: ', ''))
        if 'B' in line:
            B = int(line.replace('Register B: ', ''))
        if 'C' in line:
            C = int(line.replace('Register C: ', ''))
    program = [int(v) for v in content_split[1].replace('Program: ','').split(',')]
    return (A, B, C), program

def check(A,B,C, program) -> bool|tuple[list[int],int]:
    machine = Device(A,B,C)
    len_computed = 0
    while machine.pointer < len(program) - 1:
        if len_computed != len(machine.out_res):
            len_computed = len(machine.out_res)
            if program[len_computed-1] != machine.out_res[len_computed -1]:
                print(program, machine.out_res, len_computed-1)
                return machine.out_res, len_computed-1
        machine.execute_instruction(program[machine.pointer],program[machine.pointer+1])
    if len(program) == len(machine.out_res):
        return True
    return [], 0

def find_A(program:list[int],_A,B,C,depth) -> int:
    if depth == -1:
        return _A
    vals = [1e20]
    for i in range(8):
        A = _A + i * 8 ** depth
        m = Device(A,B,C)
        m.execute_instructions(program, verbose=False)
        if len(m.out_res) == len(program) and m.out_res[depth] == program[depth]:
            vals.append(
                find_A(program, A, B, C, depth-1)
            )
    return min(vals)

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    (_, B, C), program  = get_registers_and_program(content)

    print(f'value of A: {find_A(program,0,B,C, len(program)-1)}')

if __name__ == "__main__":
    main()

class Device:
    def __init__(self, A:int, B:int, C:int) -> None:
        self.A = A
        self.B = B
        self.C = C
        self.__pointer = 0
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
        self.__pointer += 2
    def __bxl(self, x):
        self.B = self.__get_B() ^ x
        self.__pointer += 2
    def __bst(self, x):
        self.B = self.operands[x]() % 8
        self.__pointer += 2
    def __jnz(self, x):
        self.__pointer = self.__pointer + 2 if self.__get_A() == 0 else x
    def __bxc(self, x):
        self.B = self.__get_B() ^ self.__get_C()
        self.__pointer += 2
    def __out(self, x):
        x = self.operands[x]() % 8
        self.out_res.append(x)
        self.__pointer += 2
    def __bdv(self, x):
        self.B = int(self.__get_A() / 2 ** self.operands[x]())
        self.__pointer += 2
    def __cdv(self, x):
        self.C = int(self.__get_A() / 2 ** self.operands[x]())
        self.__pointer += 2


    def execute_instructions(self, instruction_list:list[int]) -> None:
        self.__pointer = 0
        max_idx = len(instruction_list)
        # print(instruction_list)
        while self.__pointer < max_idx - 1:
            operation, parameter = instruction_list[self.__pointer], instruction_list[self.__pointer +1]
            self.op_code[operation](parameter)
        print(','.join([str(x) for x in self.out_res]))
            

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
        
def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    (A, B, C), program  = get_registers_and_program(content)
    machine = Device(A, B, C)
    machine.execute_instructions(program)

if __name__ == "__main__":
    main()

class KeyPad:
    def __init__(self) -> None:
        self.position = (3,2)
        self.size = (4,3)
        self.states = [['7', '8', '9'],['4', '5', '6'], ['1', '2', '3'], ['Dead', '0', 'A']]
        self.state_position = {}
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.state_position[self.states[i][j]] = (i,j)
    
    def move_to(self, state:str) -> str:
        assert state in self.state_position.keys(), f'state {state} not recognized'

        state_position = self.state_position[state]
        left = state_position[1] < self.position[1]
        up = state_position[0] < self.position[0]
        x_mov = ('<' if left else '>') * abs(state_position[1] - self.position[1])
        y_mov = ('^' if up else 'v') * abs(state_position[0] - self.position[0])
        str_movs = []
        ymov = abs(state_position[0] - self.position[0])
        if up:
            ymov = -ymov
        xmov = abs(state_position[1] - self.position[1])
        if left:
            xmov = -xmov
        if self.states[self.position[0]][self.position[1] + xmov] != "Dead":
            str_movs.append(x_mov + y_mov)

        if self.states[self.position[0] + ymov][self.position[1]] != "Dead":
            str_movs.append(y_mov + x_mov)
        self.position = state_position
        if len(str_movs) == 1:
            return str_movs[0]
        if '>' in x_mov:
            return y_mov + x_mov
        else:
            assert '<' in x_mov or x_mov == ''
            return x_mov + y_mov
        
class MovePad:
    def __init__(self) -> None:
        self.position = (0,2)
        self.size = (2,3)
        self.states = [['Dead', '^', 'A'], ['<', 'v', '>']]
        self.state_position = {}
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                self.state_position[self.states[i][j]] = (i,j)

    def move_to(self, state:str) -> list[str]:
        assert state in self.state_position.keys(), f'state {state} not recognized'

        state_position = self.state_position[state]
        left = state_position[1] < self.position[1]
        up = state_position[0] < self.position[0]
        x_mov = ('<' if left else '>') * abs(state_position[1] - self.position[1])
        y_mov = ('^' if up else 'v') * abs(state_position[0] - self.position[0])
        str_movs = []
        ymov = abs(state_position[0] - self.position[0])
        if up:
            ymov = -ymov
        xmov = abs(state_position[1] - self.position[1])
        if left:
            xmov = -xmov
        if self.states[self.position[0]][self.position[1] + xmov] != "Dead":
            str_movs.append(x_mov + y_mov)

        if self.states[self.position[0] + ymov][self.position[1]] != "Dead":
                str_movs.append(y_mov + x_mov)
        self.position = state_position
        return str_movs
        # if len(str_movs) == 1:
        #     return str_movs[0]
        # if '>' in x_mov:
        #     return y_mov + x_mov
        # else:
        #     assert '<' in x_mov or x_mov == ''
        #     return x_mov + y_mov
        

    # def press(self) -> str:
    #     return self.move_to('A')

class Full_process:
    def __init__(self) -> None:
        self.keypad = KeyPad()
        self.last = 24
        self.seen = {}

    def compute_sequence_cost(self, letter:str) -> int:
        button_movements = self.keypad.move_to(letter) + 'A'
        # cost = 0
        return self.compute_numeric_cost(button_movements)


    def compute_numeric_cost(self, mov:str, depth=25) -> int:
        if depth == 0:
            return len(mov)
        
        if (mov, depth) in self.seen:
            return self.seen[(mov, depth)]
        
        m = MovePad()
        seq = []
        for e in mov:
            poss = m.move_to(e)
            seq.append(poss) 
        parts = []
        for p in seq:
            tmp = []
            for sp in p:
                tmp.append("".join(sp) + 'A')
            parts.append(tmp)

        sub_sequences = parts
        cost = 0
        for part in sub_sequences:
            cost += min([self.compute_numeric_cost(seq, depth-1) for seq in part])
        
        self.seen[(mov, depth)] = cost
        return cost

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    
    process = Full_process()

    codes = content.splitlines()
    tot = 0
    for code in codes:
        code_number = int(code.replace('A',''))
        movements = 0
        # print(code)
        for letter in code:
            # print(letter)
            movements += process.compute_sequence_cost(letter)
        difficulty = code_number * movements
        tot += difficulty
        print(code, difficulty)
    print(process.seen)
    print(tot)



if __name__ == "__main__":
    main()


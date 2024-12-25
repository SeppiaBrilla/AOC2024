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
        # print(self.position, state_position, ymov, xmov)
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
        

    def press(self) -> str:
        return self.move_to('A')

class Full_process:
    def __init__(self) -> None:
        self.keypad = KeyPad()
        self.first_movepad = MovePad()
        self.second_movepad = MovePad()

    def compute_letter(self, letter:str) -> str:
        movements = ''
        button_movements = self.keypad.move_to(letter) + 'A'
        button_first_movepad = ''
        for mov in button_movements:
            button_first_movepad += self.first_movepad.move_to(mov) + 'A'
        for mov in button_first_movepad:
            movements += self.second_movepad.move_to(mov) + 'A'
        assert self.first_movepad.position == self.first_movepad.state_position['A'] \
            and self.second_movepad.position == self.second_movepad.state_position['A'], 'wrong positions'
        return movements

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    
    process = Full_process()

    codes = content.splitlines()
    tot = 0
    for code in codes:
        code_number = int(code.replace('A',''))
        movements = ''
        for letter in code:
            movements += process.compute_letter(letter)
        difficulty = code_number * len(movements)
        tot += difficulty
        print(code, code_number, len(movements))
    print(tot)



if __name__ == "__main__":
    main()


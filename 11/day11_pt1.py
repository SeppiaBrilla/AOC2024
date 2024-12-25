from typing import Literal

def get_rule(number:int) -> Literal['to_1', 'split', 'by_2024']:
    if number == 0:
        return 'to_1'
    if len(str(number)) % 2 == 0:
        return 'split'
    return 'by_2024'

def apply_rule(number:int, rule: Literal['to_1', 'split', 'by_2024']) -> list[int]:
    if rule == 'to_1':
        return [1]
    elif rule == 'split':
        half = len(str(number)) // 2
        n = str(number)
        return [int(n[:half]), int(n[half:])]
    elif rule == 'by_2024':
        return [number * 2024]

def blink(stones:list[int]) -> list[int]:
    new_stones = []
    for stone in stones:
        rule = get_rule(stone)
        result = apply_rule(stone, rule)
        # print(rule, stone, result)
        new_stones += result
    return new_stones

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    stones = [int(c) for c in content.split(' ')]
    # print(stones)
    generations = 4
    for gen in range(generations):
        stones = blink(stones)
        print(stones)
        # print(f'After {gen} blinks:\n{stones}\n')
    print(len(stones))

if __name__ == "__main__":
    main()

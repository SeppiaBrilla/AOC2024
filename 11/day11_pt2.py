from tqdm import tqdm

def apply_rule(number:int):
    if number == 0:
        return [1]
    elif len(str(number)) % 2 == 0:
        half = len(str(number)) // 2
        n = str(number)
        v =  [int(n[:half]), int(n[half:])]
        del n, half
        return v
    else:
        return [number * 2024]

def blink(stones:dict[int,int]) -> dict[int,int]:
    new_stones = {}
    for stone in stones.keys():
        res = apply_rule(stone)
        for s in res:
            if not s in new_stones:
                new_stones[s] = 0
            new_stones[s] += stones[stone]
    return new_stones

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    stones = {int(c):1 for c in content.split(' ')}
    generations = 75
    for _ in tqdm(range(generations)):
        new_stones = blink(stones)
        stones = new_stones
    print(sum(stones.values()))

if __name__ == "__main__":
    main()

def mix(number1:int, number2:int) -> int:
    return number1 ^ number2

def prune(number:int) -> int:
    return number % 16777216

def rule1(number:int) -> int:
    mult = number * 64
    mixed = mix(number, mult)
    return prune(mixed)

def rule2(number:int) -> int:
    div = number // 32
    mixed = mix(number, div)
    return prune(mixed)

def rule3(number:int) -> int:
    mul = number * 2048
    mixed = mix(number, mul)
    return prune(mixed)

def next_secret_number(number:int) -> int:
    return rule3(rule2(rule1(number)))

def get_price(number:int) -> int:
    return int(str(number)[-1])

def get_buyers(buyers_list:str) -> list[int]:
    return [int(buyer) for buyer in buyers_list.splitlines()]

def main():
    f = open('input.txt')
    content = f.read()
    f.close()

    buyers = get_buyers(content)
    tot_seq = {}
    for buyer in buyers:
        secret_n = buyer
        numbers = []
        for _ in range(2000):
            prev = secret_n
            secret_n = next_secret_number(secret_n)
            change = get_price(secret_n) - get_price(prev)
            numbers.append((change, get_price(secret_n)))
        sequences = {}
        for i in range(len(numbers) - 4):
            seq = (numbers[i][0], numbers[i+1][0], numbers[i+2][0], numbers[i+3][0])
            if seq in sequences:
                continue
            sequences[seq] = numbers[i+3][1]
        for seq, price in sequences.items():
            if not seq in tot_seq:
                tot_seq[seq] = 0
            tot_seq[seq] += price
    print(max(tot_seq.items(), key=lambda x: x[1]))

if __name__ == "__main__":
    main()

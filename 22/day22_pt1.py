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

def get_buyers(buyers_list:str) -> list[int]:
    return [int(buyer) for buyer in buyers_list.splitlines()]

def main():
    f = open('input.txt')
    content = f.read()
    f.close()

    buyers = get_buyers(content)
    final_sum = 0
    for buyer in buyers:
        secret_n = buyer
        for _ in range(2000):
            secret_n = next_secret_number(secret_n)
        # print(buyer, ':', secret_n)
        final_sum += secret_n
    print(final_sum)

if __name__ == "__main__":
    main()

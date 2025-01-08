import re

def main():
    f = open("input.txt")
    content = f.read()
    f.close()

    regex = r'(mul\([0-9]{1,3},[0-9]{1,3}\)|don\'t\(\)|do\(\))'
    results = re.findall(regex, content)
    res = 0
    do = True
    for r in results:
        if r == "do()":
            do = True
        elif r == "don't()":
            do = False
        elif do:
            assert "mul(" in r
            r = r.replace("mul(","").replace(")","")
            r = r.split(",")
            n1, n2 = r[0], r[1]
            res += int(n1) * int(n2)

    print(res)

if __name__ == "__main__":
    main()

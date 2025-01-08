import re

def main():
    f = open("input.txt")
    content = f.read()
    f.close()

    regex = r'mul\(([0-9]{1,3},[0-9]{1,3})\)'
    results = re.findall(regex, content)
    res = 0
    for r in results:
        r = r.split(",")
        n1, n2 = r[0], r[1]
        res += int(n1) * int(n2)

    print(res)

if __name__ == "__main__":
    main()

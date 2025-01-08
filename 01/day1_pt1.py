def main():
    f = open('input.txt')
    content = f.read()
    f.close()

    l1, l2 = [], []
    for line in content.splitlines():
        elements = line.split("   ")
        l1.append(int(elements[0]))
        l2.append(int(elements[1]))

    l1 = sorted(l1)
    l2 = sorted(l2)
    
    distance = 0
    for i in range(len(l1)):
        distance += abs(l1[i] - l2[i])

    print(distance)

if __name__ == "__main__":
    main()

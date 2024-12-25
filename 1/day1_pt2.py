def index(lst, target, left=0, right=None):
    if right is None:
        right = len(lst) - 1
    if left > right:
        return -1
    mid = (left + right) // 2
    
    if lst[mid] == target:
        return mid
    elif lst[mid] < target:
        return index(lst, target, mid + 1, right)
    else:
        return index(lst, target, left, mid - 1)

def count(x, l):
    c = 0
    idx = index(l, x)

    if idx == -1:
        return 0

    left, right = idx, idx + 1
    while l[left] == x:
        c += 1
        left -= 1
    while l[right] == x:
        c += 1
        right += 1

    return c

def main():
    f = open('input.txt')
    content = f.read()
    f.close()

    l1, l2 = [], []
    for line in content.splitlines():
        elements = line.split("   ")
        l1.append(int(elements[0]))
        l2.append(int(elements[1]))

    l2 = sorted(l2)
    
    similarity = 0
    for i in range(len(l1)):
        similarity += l1[i] * count(l1[i], l2)
    
    print(similarity)

if __name__ == "__main__":
    main()

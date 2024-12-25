
def look_around(grid:list[str], idx:tuple[int,int]) -> int:
    count = 0
    x, y = idx
    try:
        if grid[x-1][y-1] == "m" and grid[x+1][y+1] == "s" and x >= 1 and y >= 1:
            count +=1
        elif grid[x+1][y+1] == "m" and grid[x-1][y-1] == "s" and x >= 1 and y >= 1:
            count +=1
    except:
        pass
    try:
        if grid[x-1][y+1] == "m" and grid[x+1][y-1] == "s" and x >= 1 and y >= 1:
            count +=1
        elif grid[x+1][y-1] == "m" and grid[x-1][y+1] == "s" and x >= 1 and y >= 1:
            count +=1
    except:
        pass
    return 1 if count == 2 else 0

def main():
    f = open("input.txt")
    content = f.read()
    f.close()
    content = content.lower().splitlines()

    xmas = 0
    for x in range(len(content)):
        for y in range(len(content[0])):
            if content[x][y] == "a":
                xmas += look_around(content, (x,y))
    print(xmas)


if __name__ == "__main__":
    main()

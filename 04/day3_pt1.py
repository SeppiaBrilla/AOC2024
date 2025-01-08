
def look_around(grid:list[str], idx:tuple[int,int]) -> int:
    count = 0
    x, y = idx
    try:
        if grid[x-1][y-1] == "m" and grid[x-2][y-2] == "a" and grid[x-3][y-3] == "s" and x >= 3 and y >=3:
            count +=1
    except:
        pass
    try:
        if grid[x+1][y+1] == "m" and grid[x+2][y+2] == "a" and grid[x+3][y+3] == "s":
            count +=1
    except:
        pass
    try:
        if grid[x-1][y+1] == "m" and grid[x-2][y+2] == "a" and grid[x-3][y+3] == "s" and x >= 3:
            count +=1
    except:
        pass
    try:
        if grid[x+1][y-1] == "m" and grid[x+2][y-2] == "a" and grid[x+3][y-3] == "s" and y >= 3:
            count +=1
    except:
        pass
    try:
        if grid[x][y-1] == "m" and grid[x][y-2] == "a" and grid[x][y-3] == "s" and y >= 3:
            count +=1
    except:
        pass
    try:
        if grid[x][y+1] == "m" and grid[x][y+2] == "a" and grid[x][y+3] == "s":
            count +=1
    except:
        pass
    try:
        if grid[x-1][y] == "m" and grid[x-2][y] == "a" and grid[x-3][y] == "s" and x >= 3:
            count +=1
    except:
        pass
    try:
        if grid[x+1][y] == "m" and grid[x+2][y] == "a" and grid[x+3][y] == "s":
            count +=1
    except:
        pass
    return count

def main():
    f = open("input.txt")
    content = f.read()
    f.close()
    content = content.lower().splitlines()

    xmas = 0
    for x in range(len(content)):
        for y in range(len(content[0])):
            if content[x][y] == "x":
                xmas += look_around(content, (x,y))
    print(xmas)


if __name__ == "__main__":
    main()

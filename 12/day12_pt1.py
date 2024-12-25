def get_area(map:list[list[str]], starting_point:tuple[int,int], visited:set[tuple[int,int]]) -> int:
    visited.add(starting_point)
    ii,ij = starting_point
    current_area_name = map[ii][ij]
    curren_area = 1
    m, n = len(map), len(map[0])
    for (i, j) in [(ii+1, ij), (ii-1,ij), (ii, ij+1), (ii, ij-1)]:
        if i < n and j < m and i >= 0 and j >= 0:
            if map[i][j] == current_area_name and (i,j) not in visited:
                curren_area += get_area(map, (i,j), visited)
    return curren_area

def get_perimeter(places:set[tuple[int,int]]) -> int:
    perimeter = 0
    for (i,j) in places:
        ij_perimeter = 4
        for neib in [(i+1, j), (i-1,j), (i, j+1), (i, j-1)]:
            if neib in places:
                ij_perimeter -= 1
        perimeter += ij_perimeter
    
    return perimeter

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    map = [list(line) for line in content.splitlines()]
    m, n = len(map), len(map[0])
    places = []
    areas = []
    plants = []
    perimeters = []
    all_visited = set()
    for i in range(n):
        for j in range(m):
            if (i,j) not in all_visited:
                places.append(set())
                area = get_area(map, (i,j), places[-1])
                areas.append(area)
                plants.append(map[i][j])
                perimeters.append(get_perimeter(places[-1]))
                all_visited = all_visited.union(places[-1])

    total_cost = 0
    for i in range(len(places)):
        total_cost += areas[i] * perimeters[i]
    print(total_cost)

if __name__ == "__main__":
    main()

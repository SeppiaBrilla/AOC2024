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

def get_vertical_contiguos(t:int, top_places:list) -> int:
    sorted_places = [(i,j) for (i,j) in sorted(top_places) if i == t]
    tops = 1 if len(sorted_places) >= 1 else 0
    for p in range(1, len(sorted_places)):
        _, j = sorted_places[p]
        _, pj = sorted_places[p-1]
        if pj != j-1:
            tops += 1
    return tops

def get_horizontal_contiguos(t:int, left_places:list) -> int:
    sorted_places = [(i,j) for (i,j) in sorted(left_places) if j == t]
    lefts = 1 if len(sorted_places) >= 1 else 0
    for p in range(1, len(sorted_places)):
        i, _ = sorted_places[p]
        pi, _ = sorted_places[p-1]
        if pi != i-1:
            lefts += 1
    return lefts

def get_sides(places:set[tuple[int,int]]) -> int:
    current_sides = 0

    top_places = [(i, j) for (i,j) in places if not (i-1, j) in places]
    bottom_places = [(i, j) for (i,j) in places if not (i+1, j) in places]
    left_places = [(i, j) for (i,j) in places if not (i, j-1) in places]
    right_places = [(i, j) for (i,j) in places if not (i, j+1) in places]

    i_s = set()
    j_s = set()
    for (i,j) in places:
        i_s.add(i)
        j_s.add(j)
    for i in i_s:
        tops = get_vertical_contiguos(i, top_places)
        current_sides += tops
        bottoms = get_vertical_contiguos(i, bottom_places)
        current_sides += bottoms
    for j in j_s:
        lefts = get_horizontal_contiguos(j, left_places)
        current_sides += lefts
        rights = get_horizontal_contiguos(j, right_places)
        current_sides += rights
    return current_sides

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    map = [list(line) for line in content.splitlines()]
    m, n = len(map), len(map[0])
    places = []
    areas = []
    plants = []
    sides = []
    all_visited = set()
    for i in range(n):
        for j in range(m):
            if (i,j) not in all_visited:
                places.append(set())
                area = get_area(map, (i,j), places[-1])
                areas.append(area)
                plants.append(map[i][j])
                sides.append(get_sides(places[-1]))
                all_visited = all_visited.union(places[-1])

    total_cost = 0
    for i in range(len(places)):
        total_cost += areas[i] * sides[i]
    print(total_cost)

if __name__ == "__main__":
    main()

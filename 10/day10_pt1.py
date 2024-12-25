import numpy as np
def to_map(map:str) -> np.ndarray:
    int_map = []
    for line in map.splitlines():
        int_map.append([int(v) for v in list(line)])
    return np.array(int_map)

def get_trail_heads(map:np.ndarray) -> list[tuple[int,int]]:
    trailheads = []
    h, w = map.shape
    for i in range(h):
        for j in range(w):
            if map[i,j] == 0:
                trailheads.append((i,j))
    return trailheads

def get_n_hikes(map:np.ndarray, current_position:tuple[int,int]) -> list[tuple[int,int]]:
    current_heinght = map[current_position]
    if current_heinght == 9:
        return [current_position]
    ci, cj = current_position
    h, w = map.shape
    hikes = []
    for (i,j) in [ (ci + 1, cj), (ci - 1, cj), (ci, cj + 1), (ci, cj - 1) ]:
        if i < h and j < w and i >= 0 and j >= 0:
            if map[i,j] == current_heinght + 1:
                hikes += get_n_hikes(map, (i,j))
    return hikes

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    map = to_map(content)
    trailheads = get_trail_heads(map)
    scores = []
    for trailhead in trailheads:
        scores.append(len(set(get_n_hikes(map, trailhead))))

    print(sum(scores))

if __name__ == "__main__":
    main()

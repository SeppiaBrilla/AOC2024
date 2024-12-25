FILL = '#'
EMPTY = '.'

def print_2d(m:list[str]):
    for l in m:
        print(''.join(l))

def get_lock_and_keys(lock_and_keys_str:str) -> tuple[list[list[str]],list[list[str]]]:
    lock, keys = [], []
    for lk in lock_and_keys_str.split('\n\n'):
        is_key = True
        for s in lk[0]:
            if s == FILL:
                is_key = False
        if not is_key:
            lock.append(lk.splitlines())
        else:
            keys.append(lk.splitlines())
    return lock, keys

def get_lock_height(lock:list[str]) -> list[int]:
    heights = [[] for _ in range(len(lock[0]))]
    for i in range(len(lock)):
        for j in range(len(lock[0])):
            if lock[i][j] == FILL:
                heights[j].append(i)
    return [len(h) - 1 for h in heights]

def get_key_height(key:list[str]) -> list[int]:
    heights = [[] for _ in range(len(key[0]))]
    for i in range(len(key)):
        for j in range(len(key[0])):
            if key[i][j] == FILL:
                heights[j].append(i)
    return [len(h) - 1 for h in heights]

def fit(lock:list[int], key:list[int], max_height:int) -> bool:
    assert len(lock) == len(key), f'lock: {lock}, key:{key}'
    for i in range(len(lock)):
        if lock[i] + key[i] + 2 > max_height:
            return False
    return True

def main():
    f = open('input.txt')
    content = f.read()
    f.close()


    locks, keys = get_lock_and_keys(content)
    locks_heights = [get_lock_height(l) for l in locks]
    keys_heights = [get_key_height(k) for k in keys]
    fits = 0
    max_height = len(keys[0])
    for i, l in enumerate(locks_heights):
        for j, k in enumerate(keys_heights):
            if fit(lock=l, key=k, max_height=max_height):
                fits +=1
                # print(f'lock {l} fits with key {k}')
            else:
            #     _fit = True
                ii = 0
                for h in range(len(locks[i])):
                    for w in range(len(locks[i][0])):
                        if locks[i][h][w] == FILL:
                            if keys[j][h][w] == FILL:
                                ii = w
                # print(f'lock {l} overlaps with key {k} at {ii}')


    print(fits)

if __name__ == '__main__':
    main()

from copy import deepcopy as copy

def print_blocks_and_ids(blocks, ids):
    blocs_str = ''.join([str(block) * block for block in blocks])
    print(blocs_str)
    print(''.join(ids))

def get_block_id(blocks:list[int]) -> list[str]:
    ids = []
    is_file = True
    id = 0
    for b in blocks:
        if is_file:
            is_file = False
            ids += [str(id) for _ in range(b)]
            id += 1
        else:
            is_file = True
            ids += ['.' for _ in range(b)]
    return ids

def get_block_and_id(blocks:list[int], ids:list[str]) -> list[tuple[int, str]]:
    prev = 0
    bi = []
    for b in blocks:
        bi += [(b, ids[i]) for i in range(prev, prev+b)]
        prev += b
    return bi

def compact(block_ids:list[tuple[int,str]]) -> list[tuple[int,str]]:
    copy_block = copy(block_ids)
    first_idx, last_idx = 0, len(block_ids) - 1
    while last_idx > 0:
        bi = block_ids[last_idx]
        is_file = not bi[1] == '.'
        if is_file:
            break
        last_idx -= 1
    while first_idx < len(block_ids):
        bi = copy_block[first_idx]
        is_file = not bi[1] == '.'
        if not is_file:
            copy_block[first_idx], copy_block[last_idx] = copy_block[last_idx], copy_block[first_idx]
            while copy_block[last_idx][1] == '.':
                last_idx -= 1
        if last_idx <= first_idx:
            break
        first_idx += 1
    return copy_block

def compute_checksum(blocks_ids:list[tuple[int,str]]) -> int:
    checksum = 0
    for i in range(len(blocks_ids)):
        if blocks_ids[i][1] == '.':
            continue
        checksum += i * int(blocks_ids[i][1])

    return checksum

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    blocks = [int(b) for b in content if b != '\n']
    ids = get_block_id(blocks)
    # print_blocks_and_ids(blocks, ids)
    block_ids = get_block_and_id(blocks, ids)
    ordered_blocks_ids = compact(block_ids)
    checksum = compute_checksum(ordered_blocks_ids)
    # print(''.join([bi[1] for bi in ordered_blocks_ids]))
    print(checksum)



if __name__ == "__main__":
    main()

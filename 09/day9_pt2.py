from copy import deepcopy as copy

class File:
    def __init__(self, blocks:int, id:str) -> None:
        self.blocks = blocks
        self.id = id

    def __str__(self) -> str:
        return f"({self.blocks},{self.id})"

    def is_empty(self):
        return self.id == '.'

class Empty(File):
    def __init__(self, blocks: int) -> None:
        super().__init__(blocks, '.')

def get_block_id(blocks:list[int]) -> list[str]:
    ids = []
    is_file = True
    id = 0
    for _ in blocks:
        if is_file:
            is_file = False
            ids += [str(id)]
            id += 1
        else:
            is_file = True
            ids += ['.']
    return ids

def to_files(blocks:list[int], ids:list[str]) -> list[File]:
    files = []
    for i in range(len(blocks)):
        if ids[i] == '.':
            files.append(Empty(blocks[i]))
        else:
            files.append(File(blocks[i],ids[i]))
    return files

def compact(original_files:list[File]) -> list[File]:
    files = copy(original_files)
    last = len(files) - 1
    while last > 0:
        while files[last].is_empty():
            last -= 1
        assert not files[last].is_empty()
        for i in range(len(files)):
            if files[i].is_empty() and i < last:
                if files[i].blocks == files[last].blocks:
                    # print("=" * 100)
                    # print("pre", ''.join([file.id * file.blocks for file in files]))
                    # print("current", files[last], last)
                    files[i], files[last] = files[last], files[i]
                    # print('pst', ''.join([file.id * file.blocks for file in files]))
                    break
                elif files[i].blocks > files[last].blocks:
                    # print("=" * 100)
                    # print("pre", ''.join([file.id * file.blocks for file in files]))
                    # print("current", files[last], last)
                    last_blocks = files[last].blocks
                    remaining_space  = files[i].blocks - files[last].blocks
                    files = files[:i] + [files[last], Empty(remaining_space)] + files[i+1:]
                    last += 1
                    files[last] = Empty(last_blocks)
                    # print('pst', ''.join([file.id * file.blocks for file in files]))
                    break
        last -= 1

    return files


def compute_checksum(blocks_ids:list[str]) -> int:
    checksum = 0
    for i in range(len(blocks_ids)):
        if blocks_ids[i] == '.':
            continue
        checksum += i * int(blocks_ids[i])

    return checksum

def to_block_ids(files: list[File]) -> list[str]:
    ids = []
    for file in files:
        ids += [file.id for _ in range(file.blocks)]
    return ids
def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    blocks = [int(b) for b in content if b != '\n']
    ids = get_block_id(blocks)
    # print_blocks_and_ids(blocks, ids)
    files = to_files(blocks, ids)
    ordered_files = compact(files)
    block_ids = to_block_ids(ordered_files)
    print(''.join(block_ids))
    checksum = compute_checksum(block_ids)
    # print(''.join([bi[1] for bi in ordered_blocks_ids]))
    print(checksum)



if __name__ == "__main__":
    main()

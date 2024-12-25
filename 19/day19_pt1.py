def get_possible_stripes(str_stripes:str) -> list[str]:
    return str_stripes.split(', ')

def get_desired_patterns(str_patterns:str) -> list[str]:
    return str_patterns.split('\n')

def is_pattern_possible(pattern:str, stripes:list[str], seen:set[str], visited:set[str], current_pattern:str='') -> bool:
    if current_pattern in visited:
        return False
    visited.add(current_pattern)
    if current_pattern == pattern:
        return True
    lc = len(current_pattern)
    if pattern[lc:] in seen:
        return True
    for stripe in stripes:
        combined = current_pattern + stripe
        l = len(stripe)
        seen.add(combined)
        if stripe == pattern[lc:lc+l]:
            if is_pattern_possible(pattern, stripes, seen, visited, combined):
                return True
    return False

def main():
    f = open('input.txt')
    content = f.read()
    f.close()
    content_split = content.split('\n\n')

    stripes = get_possible_stripes(content_split[0])
    patterns = get_desired_patterns(content_split[1])
    possible_patterns = 0

    stripes = sorted(stripes, key= lambda x: len(x), reverse=True)
    ps = len(patterns)
    seen = set()
    for i, pattern in enumerate(patterns):
        if pattern == '' or pattern == '\n':
            continue
        print(pattern, f'{i}/{ps}')
        pattern_stripes = [stripe for stripe in stripes if stripe in pattern]
        visited = set()
        if is_pattern_possible(pattern, pattern_stripes, seen, visited):
            possible_patterns += 1

    print(possible_patterns)


if __name__ == "__main__":
    main()

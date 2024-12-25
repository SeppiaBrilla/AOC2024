def get_possible_stripes(str_stripes:str) -> list[str]:
    return str_stripes.split(', ')

def get_desired_patterns(str_patterns:str) -> list[str]:
    return str_patterns.split('\n')

def is_pattern_possible(pattern:str, stripes:list[str], visited:set[str], current_pattern:str='') -> bool:
    if current_pattern in visited:
        return False
    visited.add(current_pattern)
    if current_pattern == pattern:
        return True
    lc = len(current_pattern)
    for stripe in stripes:
        combined = current_pattern + stripe
        l = len(stripe)
        if stripe == pattern[lc:lc+l]:
            if is_pattern_possible(pattern, stripes, visited, combined):
                return True
    return False

def number_of_possible_patterns(pattern:str, stripes:list[str], visited:dict[str, int], current_pattern:str='') -> int:
    if current_pattern in visited:
        return visited[current_pattern]
    if current_pattern == pattern:
        visited[current_pattern] = 1
        return 1
    lc = len(current_pattern)
    all = 0
    for stripe in stripes:
        combined = current_pattern + stripe
        l = len(stripe)
        if stripe == pattern[lc:lc+l]:
            visited[combined] = number_of_possible_patterns(pattern, stripes, visited, combined) 
            all += visited[combined]
    return all

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
    print(stripes)
    for i, pattern in enumerate(patterns):
        if pattern == '' or pattern == '\n':
            continue
        print(pattern, f'{i}/{ps}')
        pattern_stripes = [stripe for stripe in stripes if stripe in pattern]
        seen = {}
        all = number_of_possible_patterns(pattern, pattern_stripes, seen)
        print(all)
        possible_patterns += all
    print(possible_patterns)


if __name__ == "__main__":
    main()

def check_ordering(rules:list[tuple[int,int]], update:list[int]) -> bool:
    for rule in rules:
        pre, post = rule
        if not pre in update:
            continue
        if not post in update:
            continue
        if update.index(pre) > update.index(post):
            return False
    return True

def reorder(rules:list[tuple[int,int]], update:list[int]) -> list[int]:
    while not check_ordering(rules, update):
        for rule in rules:
            pre, post = rule
            if not pre in update:
                continue
            if not post in update:
                continue

            idx_pre = update.index(pre)
            idx_post = update.index(post)
            if idx_pre > idx_post:           
                update[idx_pre], update[idx_post] = update[idx_post], update[idx_pre]
    return update

def get_middle_element(vals: list[int]) -> int:
    middle = len(vals) // 2
    return vals[middle]

def main():
    f = open('input.txt')
    content = f.read()
    f.close()

    content_split = content.split('\n\n')
    rules_str = content_split[0]
    updates_str = content_split[1]

    rules = []
    for rule_str in rules_str.splitlines():
        rule_split = rule_str.split('|')
        rule = (int(rule_split[0]), int(rule_split[1]))
        rules.append(rule)

    updates = []
    for update_str in updates_str.splitlines():
        updates.append([
            int(e) for e in update_str.split(',')
        ])

    result = 0
    for update in updates:
        if not check_ordering(rules, update):
            correct_update = reorder(rules, update)
            result += get_middle_element(correct_update)

    print(result)

if __name__ == "__main__":
    main()

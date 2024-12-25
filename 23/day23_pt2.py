from itertools import combinations

def get_connections(connections_str:str) -> list[tuple[str,str]]:
    connections_split = connections_str.splitlines()
    connections = []
    for connection_str in connections_split:
        split = connection_str.split('-')
        connections.append((split[0],split[1]))
    return connections

def get_connections_dict(connections:list[tuple[str,str]]) -> dict[str,set[str]]:
    connections_dict = {}
    for conn in connections:
        key, val = min(conn), max(conn)
        if not key in connections_dict:
            connections_dict[key] = set()
        connections_dict[key].add(val)
    return connections_dict

def get_lans(connections:dict[str,set[str]], all_pcs:list[str]) -> list[set[str]]:
    connections_sets = []
    for pc in all_pcs:
        for lan in connections_sets:
            is_connected = True
            for _pc in lan:
                pc1, pc2 = min(pc, _pc), max(pc, _pc)
                is_connected = is_connected and pc1 in connections and pc2 in connections[pc1]
            if is_connected:
                lan.add(pc)
        connections_sets.append({pc})

    return connections_sets

def get_t_starting(connections:list[tuple[str,str,str]]) -> list[tuple[str,str,str]]:
    t_starting = []
    for conn in connections:
        if conn[0][0] == 't' or conn[1][0] == 't' or conn[2][0] == 't':
            t_starting.append(conn)
    return t_starting

def main():
    f = open('input.txt')
    content = f.read()
    f.close()


    connections = get_connections(content)
    connections_dict = get_connections_dict(connections)
    all_pcs = set()
    for pc1,pc2 in connections:
        all_pcs.add(pc1)
        all_pcs.add(pc2)
    all_pcs = list(all_pcs)
    lans = get_lans(connections_dict, all_pcs)
    lan = list(max(lans, key = lambda x: len(x)))
    print(','.join(sorted(lan)))
    # t = get_t_starting()
    # print(len(t))


if __name__ == "__main__":
    main()

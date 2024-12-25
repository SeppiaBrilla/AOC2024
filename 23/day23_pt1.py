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

def get_three_way_connections(connections:dict[str,set[str]]) -> list[tuple[str,str,str]]:
    threeplets = []
    for pc1, conns in connections.items():
        for pcs in combinations(conns, 2):
            pc2, pc3 = min(pcs), max(pcs)
            if not pc2 in connections:
                continue
            if pc3 in connections[pc2]:
                threeplets.append((pc1, pc2, pc3))
    return threeplets

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
    threeplets = get_three_way_connections(connections_dict)
    t = get_t_starting(threeplets)
    print(len(t))



if __name__ == "__main__":
    main()

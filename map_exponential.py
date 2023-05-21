def getMap()->tuple[int, list[list[tuple[int, int, int, int, int]]]]:
    num_turns = 128
    map = []
    for i in range(8):
        row = []
        for j in range(8):
            n = i + j + 2
            m = int(2 ** (n/4))
            row.append((max(1, int(m/2)), m, n, 0, n))
        map.append(row)
    map[1][3] = [2, 2, 0, 1, 0]
    map[3][1] = [2, 2, 0, -1, 0]
    return num_turns, map

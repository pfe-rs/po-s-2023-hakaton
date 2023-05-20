def getMap()->tuple[list[list[tuple[int, int, int, int, int]]]]:
    num_turns = 128
    map = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append((1, 1, 0, 0, 1))
        map.append(row)
    map[0][0] = (1, 2, 0, 1, 0)
    map[7][7] = (1, 2, 0, -1, 0)
    map[3][3] = (0, 16, 16, 0, 16)
    map[3][4] = (0, 16, 16, 0, 16)
    map[4][3] = (0, 16, 16, 0, 16)
    map[4][4] = (0, 16, 16, 0, 16)
    return num_turns, map

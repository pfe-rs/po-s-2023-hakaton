def getMap()->tuple[int, list[list[tuple[int, int, int, int, int]]]]:
    num_turns = 128
    map = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append((1, 4, 1, 0, 0))
        map.append(row)
    for i in range(8):
        map[3][i] = (0, 16, 0, 0, 16)
        map[4][i] = (0, 16, 0, 0, 16)
    map[0][0] = (4, 4, 1, 1, 4)
    map[7][0] = (4, 4, 1, -1, 4)
    return num_turns, map

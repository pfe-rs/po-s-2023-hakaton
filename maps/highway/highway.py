def getMap()->list[list[tuple[int, int, int, int, int]]]:
    map = [];
    for i in range(8):
        row = []
        for j in range(8):
            row.append((0, 16, 0, 0, 16))
        map.append(row)
    for i in range(4):
        map[1][i*2 - 1] = (2, 2, 0, 0, 2)
        map[6][i*2 - 1] = (2, 2, 0, 0, 2)
    for i in range(8):
        map[i][4] = (0, 16, 0, 0, 1)
        map[0][i] = (0, 16, 0, 0, 1)
        map[7][i] = (0, 16, 0, 0, 1)
    map[0][0] = (1, 16, 0, 1, 0)
    map[7][0] = (1, 16, 0, -1, 0)
    map[0][7] = (1, 16, 8, 0, 1)
    map[7][7] = (1, 16, 8, 0, 1)
    return map

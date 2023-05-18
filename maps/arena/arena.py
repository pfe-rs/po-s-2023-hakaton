def getMap()->list[list[tuple[int, int, int, int, int]]]:
    map = [];
    for i in range(8):
        row = []
        for j in range(8):
            row.append((1, 2, 0, 0, 2))
        map.append(row)
    map[0][0] = (2, 4, 0, 1, 0)
    map[7][7] = (2, 4, 0, -1, 0)
    map[0][7] = (2, 4, 0, 0, 4)
    map[7][0] = (2, 4, 0, 0, 4)
    map[3][3] = (4, 4, 0, 0, 4)
    map[3][4] = (4, 4, 0, 0, 4)
    map[4][3] = (4, 4, 0, 0, 4)
    map[4][4] = (4, 4, 0, 0, 4)
    for i in range(2,6):
        map[i][2] = (2, 4, 0, 0, 4)
        map[i][6] = (2, 4, 0, 0, 4)
        map[2][i] = (2, 4, 0, 0, 4)
        map[6][i] = (2, 4, 0, 0, 4)
    map[1][1] = (2, 4, 4, 0, 4)
    map[1][6] = (2, 4, 4, 0, 4)
    map[6][1] = (2, 4, 4, 0, 4)
    map[6][6] = (2, 4, 4, 0, 4)
    return map

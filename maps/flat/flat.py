def getMap()->list[list[tuple[int, int, int, int, int]]]:
    map = [];
    for i in range(4):
        row = []
        for j in range(4):
            row.append((1, 4, 1, 0, 4))
        map.append(row)
    map[0][0] = [1, 4, 1, 1, 4]
    map[3][3] = [1, 4, 1, -1, 4]
    return map

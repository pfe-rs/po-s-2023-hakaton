def copyMap(map:list[list[tuple[int, int, int, int, int]]])->list[list[tuple[int, int, int, int, int]]]:
    newmap = [];
    for i in range(8):
        row = []
        for j in range(8):
            row.append(map[i][j])
        newmap.append(row)
    return newmap
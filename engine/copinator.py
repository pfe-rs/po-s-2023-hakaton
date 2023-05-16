def copyMap(map:list[list[tuple[int, int, int, int, int]]])->list[list[tuple[int, int, int, int, int]]]:
    newmap = [];
    for i in range(len(map)):
        row = []
        for j in range(len(map[0])):
            row.append(map[i][j])
        newmap.append(row)
    return newmap
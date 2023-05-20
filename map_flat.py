def getMap()->tuple[int, list[list[tuple[int, int, int, int, int]]]]:
    num_turns = 128
    map = []
    for i in range(8):
        row = []
        for j in range(8):
            row.append((1, 4, 1, 0, 4))
        map.append(row)
    map[0][0] = (1, 4, 1, 1, 4)
    map[7][7] = (1, 4, 1, -1, 4)
    return num_turns, map

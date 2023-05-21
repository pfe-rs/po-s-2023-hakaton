def getMap()->tuple[int, list[list[tuple[int, int, int, int, int]]]]:
    num_turns = 128
    map = []
    for i in range(8):
        row = []
        for j in range(8):
            if (i + j) % 2 == 0:
                row.append((4, 16, 1, 0, 16))
            else:
                row.append((1, 4, 1, 0, 4))
        map.append(row)
    map[0][7] = [2, 2, 0, 1, 0]
    map[7][0] = [2, 2, 0, -1, 0]
    return num_turns, map

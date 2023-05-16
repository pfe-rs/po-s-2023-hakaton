import copinator

def playActions(actions:list[list[int]], map:list[list[tuple[int, int, int, int, int]]], purplecash:int, orangecash: int)->tuple[list[list[tuple[int, int, int, int, int]]], int, int]:
    newmap = []
    for row in range(len(map)):
        newmap.append([])
        for column in range(len(map[0])):
            cpu = map[row][column][0]
            ram = map[row][column][1]
            print = map[row][column][2]
            side = map[row][column][3]
            V0 = map[row][column][4]
            p = 0 if actions[row][column] >= 1 and actions[row][column] <= 4 else 1
            Vprod = cpu if actions[row][column] == 0 else 0
            inpurple = 0
            inorange = 0

            if row - 1 >= 0 and actions[row-1][column] == 3:
                if map[row-1][column][3] == 1:
                    inpurple += map[row-1][column][4]
                else:
                    inorange += map[row-1][column][4]

            if row + 1 < len(map) and actions[row+1][column] == 1:
                if map[row+1][column][3] == 1:
                    inpurple += map[row+1][column][4]
                else:
                    inorange += map[row+1][column][4]

            if column - 1 >= 0 and actions[row][column-1] == 2:
                if map[row][column-1][3] == 1:
                    inpurple += map[row][column-1][4]
                else:
                    inorange += map[row][column-1][4]
            
            if column + 1 < len(map[0]) and actions[row][column+1] == 4:
                if map[row][column+1][3] == 1:
                    inpurple += map[row][column+1][4]
                else:
                    inorange += map[row][column+1][4]
            
            V = V0*p + Vprod

            if map[row][column][3] == 0:
                Vop = max(inpurple, inorange)
                V -= Vop
                if V < 0:
                    if inpurple > inorange:
                        V = -V
                        side = 1
                    elif inorange > inpurple:
                        V = -V
                        side = -1
                    else:
                        V = 0
            elif map[row][column][3] == 1:
                Vin = inpurple
                Vop = inorange
                V += Vin - Vop
                if V < 0:
                    V = -V
                    side = -1
                if actions[row][column] == 5:
                    purplecash += print
            elif map[row][column][3] == -1:
                Vin = inorange
                Vop = inpurple
                V += Vin - Vop
                if V < 0:
                    V = -V
                    side = 1
                if actions[row][column] == 5:
                    orangecash += print
            
            if V > ram:
                V = ram
            
            newmap[row].append((cpu, ram, print, side, V))
    return (newmap, purplecash, orangecash)
from random import randrange, uniform
import time
from math import sqrt

money_coords = []

def act(row: int, column: int, team: int, turn: int, purplecash: int, orangecash: int, map: list[list[tuple[int, int, int, int, int]]]) -> int:
    start = time.time()
    
    global money_coords
    if len(money_coords) == 0:
        for y in range(len(map)):
            for x in range(len(map[0])):
                if map[y][x][2]:
                    money_coords.append((y,x))

    # randomness
    theta = 0
    if len(money_coords) / (len(map) * len(map[0])) > 0.5:
        theta = uniform(35,50)
    
    if uniform(0, 100) < 20 + theta:
        if map[row][column][2] and uniform(0,100) < 10:
            return 6

        roll = True
        while roll:
            out = randrange(5)
            roll = False
            if out == 1 and row == 0:
                roll = True
            if out == 2 and column == len(map[0])-1:
                roll = True
            if out == 3 and row == len(map)-1:
                roll = True
            if out == 4 and column == 0:
                roll = True
            if out >= 1 and out <= 4 and map[row][column][4] == 0:
                return 0
        return out

    # prvo proveri da li mozes da stampas kes
    if map[row][column][2]:
        # ukoliko se protivnik nalazi u blizini pravi nove viruse dok se ne napuni RAM
        if row == 0 and column == 0:
            if map[row + 1][column][3] == -team or map[row][column + 1][3] == -team:
                # protivnik u blizini
                if map[row][column][4] < map[row][column][1]:
                    return 0
        elif row == 0 and column == len(map[0]) - 1:
            if map[row + 1][column][3] == -team or map[row][column - 1][3] == -team:
                # protivnik u blizini
                if map[row][column][4] < map[row][column][1]:
                    return 0
        elif row == len(map) - 1 and column == len(map[0]) - 1:
            if map[row - 1][column][3] == -team or map[row][column - 1][3] == -team:
                # protivnik u blizini
                if map[row][column][4] < map[row][column][1]:
                    return 0
        elif row == len(map) - 1 and column == 0:
            if map[row - 1][column][3] == -team or map[row][column + 1][3] == -team:
                # protivnik u blizini
                if map[row][column][4] < map[row][column][1]:
                    return 0
        else:
            if map[row - 1][column][3] == -team or map[row][column + 1][3] == -team or map[row + 1][column][3] == -team or map[row][column - 1][3] == -team:
                # protivnik u blizini
                if map[row][column][4] < map[row][column][1]:
                    return 0

        # ako nema protivnika u blizini stampaj
        return 5


    # ukoliko stampanje nije moguce => generisi viruse do 50% kapaciteta
    if map[row][column][4] / map[row][column][1] <= 0.5 and map[row][column][4] < 5:
        return 0

    # ukoliko nije potrebno stvaranje novih virusa => pomeri se

    # ukoliko se nalazis pored polja sa jacom generacijom od svog => preuzmi ga
    if row == 0:
        if column == 0:
            if map[row + 1][column][0] > map[row][column][0] and map[row + 1][column][3] != team:
                return 3
            elif map[row][column + 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 2
        elif column == len(map[0]) - 1:
            if map[row + 1][column][0] > map[row][column][0] and map[row + 1][column][3] != team:
                return 3
            elif map[row][column - 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 4
        else:
            if map[row + 1][column][0] > map[row][column][0] and map[row + 1][column][3] != team:
                return 3
            elif map[row][column + 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 2
            elif map[row][column - 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 4
    elif row == len(map) - 1:
        if column == 0:
            if map[row - 1][column][0] > map[row][column][0] and map[row - 1][column][3] != team:
                return 1
            elif map[row][column + 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 2
        elif column == len(map[0]) - 1:
            if map[row - 1][column][0] > map[row][column][0] and map[row - 1][column][3] != team:
                return 1
            elif map[row][column - 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 4
        else:
            if map[row - 1][column][0] > map[row][column][0] and map[row - 1][column][3] != team:
                return 1
            elif map[row][column + 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 2
            elif map[row][column - 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 4
    else:
        if column == 0:
            if map[row - 1][column][0] > map[row][column][0] and map[row - 1][column][3] != team:
                return 1
            if map[row + 1][column][0] > map[row][column][0] and map[row + 1][column][3] != team:
                return 3
            elif map[row][column + 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 2
        elif column == len(map[0]) - 1:
            if map[row - 1][column][0] > map[row][column][0] and map[row - 1][column][3] != team:
                return 1
            elif map[row + 1][column][0] > map[row][column][0] and map[row + 1][column][3] != team:
                return 3
            elif map[row][column - 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 4
        else:
            if map[row - 1][column][0] > map[row][column][0] and map[row - 1][column][3] != team:
                return 1
            elif map[row + 1][column][0] > map[row][column][0] and map[row + 1][column][3] != team:
                return 3
            elif map[row][column + 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 2
            elif map[row][column - 1][0] > map[row][column][0] and map[row][column + 1][3] != team:
                return 4
    
    # kreci se ka najblizem slobodnom ili protivnickom polju koje stampa kes
    dists = []
    i = 0
    for moneyPlace in money_coords:
        if map[moneyPlace[0]][moneyPlace[1]][3] == team:
            continue
        dist = sqrt((moneyPlace[0]-row)*(moneyPlace[0]-row) + (moneyPlace[1]-column)*(moneyPlace[1]-column))
        dists.append((dist, i))
        i += 1

    coords = money_coords[min(dists)[1]]
    if row < coords[0]:
        # pomeri se na gore
        return 3
    elif row > coords[0]:
        # pomeri se na dole
        return 1
    elif column < coords[1]:
        # pomeri se na desno
        return 2
    elif column > coords[1]:
        # pomeri se na levo
        return 4

    end = time.time()

    print(end - start)

    return 0
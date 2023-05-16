from random import randrange
import time

def act(row: int, column: int, team: int, turn: int, mycash: int, opcash: int, map:list[list[tuple[int, int, int, int, int]]])->int:
    roll = True
    while roll:
        out = randrange(6)
        roll = False
        if out == 1 and row == 0:
            roll = True
        if out == 2 and column == 7:
            roll = True
        if out == 3 and row == 7:
            roll = True
        if out == 4 and column == 0:
            roll = True
        if out >= 1 and out <= 4 and map[row][column][4] == 0:
            roll = True
        if out == 5 and map[row][column][2] == 0:
            roll = True
    return out

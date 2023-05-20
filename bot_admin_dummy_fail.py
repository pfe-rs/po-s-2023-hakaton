from random import randrange
import time

def act(row: int, column: int, team: int, turn: int, mycash: int, opcash: int, map:list[list[tuple[int, int, int, int, int]]])->int:
    if randrange(2) == 0:
        return 5
    else:
        a = 5
        while True:
            a *= a

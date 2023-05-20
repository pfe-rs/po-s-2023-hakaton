import importlib
import sys
import func_timeout
from dataclasses import dataclass
import copinator
import actinator

@dataclass
class State:
    # a matrix of state
    curr_map: list[list[tuple[int, int, int, int, int]]]
    # holds max turns in the game
    max_turns: int
    # turn number, starts at 0, if even bot1 plays
    turn: int

    score1: int
    score2: int

    # actions that led to this state (mostly for visualization purposes)
    last_played_actions: list[list[int]]

def create_def_state(max_turns, map):
    return State(map, max_turns, 0, 0, 0, get_empty_actions(map))

def get_empty_actions(map):
    actions = []
    for row in range(len(map)):
        actions.append([])
        for column in range(len(map[0])):
            actions[row].append(6)
    return actions

def resolve_map(map):
    spec = importlib.util.spec_from_file_location(map, "maps/"+map+"/"+map+".py")
    mapinator = importlib.util.module_from_spec(spec)
    sys.modules["flat"] = mapinator
    spec.loader.exec_module(mapinator)
    return mapinator

def resolve_bot(bot):
    spec = importlib.util.spec_from_file_location(bot, "bots/"+bot+"/"+bot+".py")
    purple = importlib.util.module_from_spec(spec)
    sys.modules["dummy"] = purple
    spec.loader.exec_module(purple)
    return purple

class Game():

    def __init__(self, bot1, bot2, map):
        self.bot1 = resolve_bot(bot1)
        self.bot2 = resolve_bot(bot2)
        self.map = resolve_map(map)
        
        max_turns, map = self.map.getMap()
        self.currState = create_def_state( max_turns, map)

    def bot1plays(self):
        return (self.currState.turn % 2 == 0)

    def fill_new_action(self):
        
        curr_map = self.currState.curr_map
        actions = get_empty_actions(curr_map)
        for row in range(len(curr_map)):
            for column in range(len(curr_map[0])):
                if curr_map[row][column][3] == 1:
                    try:
                        actions[row][column] = func_timeout.func_timeout(0.1, self.bot1.act, (row, column,  1, self.currState.turn, self.currState.score1, self.currState.score2, copinator.copyMap(self.currState.curr_map)))
                    except:
                        actions[row][column] = -1
                if curr_map[row][column][3] == -1:
                    try:
                        actions[row][column] = func_timeout.func_timeout(0.1, self.bot2.act, (row, column,  -1, self.currState.turn, self.currState.score1, self.currState.score2, copinator.copyMap(self.currState.curr_map)))
                    except:
                        actions[row][column] = -1
        self.currState.last_played_actions = actions
        return self.currState

    def fill_new_map(self):
        self.currState.curr_map, self.currState.score1, self.currState.score2 = actinator.playActions(self.currState.last_played_actions, self.currState.curr_map, self.currState.score1, self.currState.score2)
        self.currState.turn +=1
        return self.currState
    
    def is_game_finished(self):
        return self.currState.turn >= self.currState.max_turns

    def step(self):
        self.fill_new_action()
        self.fill_new_map()

        return self.currState, self.is_game_finished()


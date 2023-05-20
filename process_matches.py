from common import execute_command, execute_query
from runinator import Game, State
from datetime import datetime
from random import randrange, shuffle

def evaluate_gameplay(bot1, bot2, map):
    game = Game(bot1, bot2, map)
    states_to_persist = []
    states_to_persist.append(game.get_state_copy())
    while not game.is_game_finished():
        game.step()
        state = game.get_state_copy()
        states_to_persist.append(state)
        print(f"game step turn {state.turn}, score1 {state.score1}, score2 {state.score2}")
    
    return states_to_persist

def commit_gameplay_states(bot1, bot2, map, states):
    for state in states:
        execute_command("insert into gameplay values (?, ?, ?, ?, ?)", (bot1, bot2, map, state.turn, str(state)))

def process_match(mch):
    print(f"processing match {mch[0]} {mch[1]} {mch[2]}")
    states_to_persist = evaluate_gameplay(mch[0], mch[1], mch[2])
    score1 = states_to_persist[-1].score1
    score2 = states_to_persist[-1].score2

    commit_gameplay_states(mch[0], mch[1], mch[2], states_to_persist)

    execute_command("update runs set "
                    f"runtime = '{datetime.now()}', "
                    "run = 'true', "
                    f"score1 = {score1}, "
                    f"score2 = {score2}  "
                    f"where bot1='{mch[0]}' "
                    f"and bot2='{mch[1]}' "
                    f"and map='{mch[2]}'")


def get_all_unplayed_randomized(n):
    res = execute_query("select * from runs where run = 'false'")
    print (f"Found {len(res)} still unplayed")
    shuffle(res)
    return res[:n]

def get_single_unplayed():
    res = get_all_unplayed_randomized()
    if len(res)!= 0:
        return res[randrange(len(res))]
        # return res[0]
    else:
        return None

print(datetime.now())
# mch = get_single_unplayed()
# if (mch):
#     process_match(mch)
for mch in get_all_unplayed_randomized(1):
    process_match(mch)

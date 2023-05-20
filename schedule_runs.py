import os
from common import execute_command, execute_query
from datetime import datetime

# should be scheduled to run occassionally.

rel_path = os.path.dirname(os.path.realpath(__file__))

def get_all_bots():
    bots = [file.replace(".py", "") for file in os.listdir(rel_path) if file.startswith("bot_")]
    print(f"Found bots {bots}")
    return bots

def get_all_maps():
    maps = [file.replace(".py", "") for file in os.listdir(rel_path) if file.startswith("map_")]
    print(f"Found maps {maps}")
    return maps

def get_all_combinations(bots, maps):
    res = []
    for bot in bots:
        for bot2 in bots:
            if bot == bot2:
                continue
            for mapp in maps:
                res.append((bot, bot2, mapp))

    print(f"Found combinations {res}")
    return res

def calculate_rankings(results):
    bots_res = {}
    for res in results:
        bot1, bot2, score1, score2 = res[0], res[1], res[6], res[7]
        if bot1 not in bots_res:
            bots_res[bot1] = {
                "wins": 0,
                "loses": 0,
                "score": 0,
            }
        if bot2 not in bots_res:
            bots_res[bot2] = {
                "wins": 0,
                "loses": 0,
                "score": 0,
            }
        bots_res[bot1]["score"] += score1
        bots_res[bot2]["score"] += score2
        if score1 > score2:
            bots_res[bot1]["wins"] += 1
            bots_res[bot2]["loses"] += 1
        elif score2 > score1:
            bots_res[bot2]["wins"] += 1
            bots_res[bot1]["loses"] += 1
    print(f"Calculated rankings {bots_res}")
    return bots_res

def get_committed_runs():
    res = execute_query("select * from runs")
    
    already_existing = set()
    for row in res:
        already_existing.add((row[0], row[1], row[2]))

    print(f"Get existing runs {already_existing}")
    return already_existing

def get_completed_runs():
    res = execute_query("select * from runs where run = 'true'")
    print(f"Get completed runs {res}")
    return res    

def add_new_runs():
    all_possible_runs = get_all_combinations(get_all_bots(), get_all_maps())
    already_existing = get_committed_runs()

    for run in all_possible_runs:
        if run not in already_existing:
            print(f"inserting run '{run[0]}', '{run[1]}', '{run[2]}")
            execute_command(f"insert into runs values ('{run[0]}', '{run[1]}', '{run[2]}', '{datetime.now()}', 'null', 'false', '0', '0')")

def update_rankings():
    calc_rankings = calculate_rankings(get_completed_runs())
    if len(calc_rankings) > 0:
        max_score = max([rank["score"] for rank in calc_rankings.values()])
        for bot, rank in calc_rankings.items():
            print(f"Updating rank {bot}")
            execute_command(f"insert or replace into rankings values (?, ?, ?, ?, ?)", (bot, rank["wins"], rank["loses"], rank["score"], rank["score"]/max_score))

print(datetime.now())
add_new_runs()
update_rankings()
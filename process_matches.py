from common import execute_command, execute_query
from runinator import Game, State
from datetime import datetime
from random import randrange, shuffle
import pygame
import renderinator
import os
import subprocess

rel_path = os.path.dirname(os.path.realpath(__file__))
image_loc = os.path.join(rel_path, "static")

def evaluate_gameplay(bot1, bot2, map):
    game = Game(bot1, bot2, map)
    states_to_persist = []
    states_to_persist.append(game.get_state_copy())
    while not game.is_game_finished():
        game.step()
        state = game.get_state_copy()
        states_to_persist.append(state)
        print(f"{datetime.now()} game step turn {state.turn}, score1 {state.score1}, score2 {state.score2}")
    
    return states_to_persist

def commit_gameplay_states(bot1, bot2, map, states):
    for state in states:
        execute_command("insert or replace into gameplay values (?, ?, ?, ?, ?)", (bot1, bot2, map, state.turn, str(state)))

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
    
    for state in states_to_persist:
        render_image(mch[0], mch[1], mch[2], state)


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

def render_image(bot1, bot2, map, state: State):
    image_prefix = bot1 + "_" + bot2 + "_" + map + "_" + str(state.turn)
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    renderinator.render(screen, state.curr_map, state.last_played_actions, state.score1, state.score2, state.turn, state.max_turns)
    outimg = os.path.join(image_loc, image_prefix + ".jpg")
    os.makedirs(image_loc, exist_ok=True)
    pygame.image.save(screen, outimg)
    print(f"{datetime.now()} rendered image to {outimg}")

def render_gifs(bot1, bot2, map):
    gif_prefix = bot1 + "_" + bot2 + "_" + map + "_"
    images_str = gif_prefix + "%d.jpg"
    for fps in ["1", "10"]:
        out_gif = gif_prefix + fps + "fps.gif"
        inp_img = os.path.join(image_loc, images_str)

        print(f"Rendering gif at {out_gif}")
        subprocess.run(["ffmpeg", 
                        "-framerate", fps,
                        "-i", inp_img,
                        out_gif])


print(datetime.now())
# mch = get_single_unplayed()
# if (mch):
#     process_match(mch)
for mch in get_all_unplayed_randomized(10):
    process_match(mch)

import sys
import pygame
import renderinator
import time
from runinator import Game, get_empty_actions


def main():
    pygame.init()

    game = Game(sys.argv[2], sys.argv[3], sys.argv[1])

    screen = pygame.display.set_mode((1000, 800))


    game_finished = False
    curr_state = game.currState
    empty_actions = get_empty_actions(curr_state.curr_map)

    while not game_finished:
        pygame.event.get()
        time.sleep(0.3)
        

        renderinator.render(screen, curr_state.curr_map, empty_actions, curr_state.score1, curr_state.score2, curr_state.turn, curr_state.max_turns)
        pygame.display.flip()
        pygame.event.get()
        time.sleep(0.3)

        curr_state = game.fill_new_action()
        
        renderinator.render(screen, curr_state.curr_map, curr_state.last_played_actions, curr_state.score1, curr_state.score2, curr_state.turn, curr_state.max_turns)
        pygame.display.flip()
        pygame.event.get()
        time.sleep(0.3)

        curr_state = game.fill_new_map()
        
        renderinator.render(screen, curr_state.curr_map, curr_state.last_played_actions, curr_state.score1, curr_state.score2, curr_state.turn, curr_state.max_turns)
        pygame.display.flip()

        game_finished = game.is_game_finished()
    
    print(curr_state.score1, curr_state.score2)


if __name__ == "__main__":
    main()

import importlib.util
import sys
import copinator
import actinator
import func_timeout
import pygame
import renderinator
import time

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 800))
    spec = importlib.util.spec_from_file_location(sys.argv[1], "maps/"+sys.argv[1]+"/"+sys.argv[1]+".py")
    mapinator = importlib.util.module_from_spec(spec)
    sys.modules["flat"] = mapinator
    spec.loader.exec_module(mapinator)
    spec = importlib.util.spec_from_file_location(sys.argv[2], "bots/"+sys.argv[2]+"/"+sys.argv[2]+".py")
    purple = importlib.util.module_from_spec(spec)
    sys.modules["dummy"] = purple
    spec.loader.exec_module(purple)
    spec = importlib.util.spec_from_file_location(sys.argv[3], "bots/"+sys.argv[3]+"/"+sys.argv[3]+".py")
    orange = importlib.util.module_from_spec(spec)
    sys.modules["dummy"] = orange
    spec.loader.exec_module(orange)

    map = mapinator.getMap()
    purplecash = 0
    orangecash = 0

    for turn in range(128):
        pygame.event.get()
        time.sleep(0.03)
        actions = []
        for row in range(len(map)):
            actions.append([])
            for column in range(len(map[0])):
                actions[row].append(6)
        renderinator.render(screen, map, actions, purplecash, orangecash)
        pygame.display.flip()
        pygame.event.get()
        time.sleep(0.3)
        for row in range(len(map)):
            for column in range(len(map[0])):
                if map[row][column][3] == 1:
                    try:
                        actions[row][column] = func_timeout.func_timeout(1, purple.act, (row, column,  1, turn, purplecash, orangecash, copinator.copyMap(map)))
                    except:
                        actions[row][column] = -1
                if map[row][column][3] == -1:
                    try:
                        actions[row][column] = func_timeout.func_timeout(1, orange.act, (row, column,  1, turn, purplecash, orangecash, copinator.copyMap(map)))
                    except:
                        actions[row][column] = -1
        renderinator.render(screen, map, actions, purplecash, orangecash)
        pygame.display.flip()
        pygame.event.get()
        time.sleep(0.3)
        map, purplecash, orangecash = actinator.playActions(actions, map, purplecash, orangecash)
        renderinator.render(screen, map, actions, purplecash, orangecash)
        pygame.display.flip()
    
    print(purplecash, orangecash)


if __name__ == "__main__":
    main()

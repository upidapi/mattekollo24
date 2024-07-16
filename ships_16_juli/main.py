import argparse
import importlib.util
import sys
import json
import copy
import dataclasses
from os import path
from game import Game

# Returns the winner:
# 1 or 2
# 0 for draws.
def simulate_game():
    # 1: Load player classes
    # 2: Setup game
    # 3: Run game loop
    # 4: Declare winner
    parser = argparse.ArgumentParser()    
    parser.add_argument("-a", "--player_a", required=True)
    parser.add_argument("-b", "--player_b", required=True)
    parser.add_argument("-n", "--no_gui", default = False, action="store_const", const = True)
    parser.add_argument("-o", "--output", action="store", default = None)
    parser.add_argument("-m", "--map_number", action="store", default = 1)
    # args = parser.parse_args()
    
    class args:
        # player_a = "nothing.py" # "mine/main.py"
        player_a = "mine/main.py"
        player_b = "nothing.py"
        map_number =  1
        no_gui = False
        output = None

    

    try:
        player_1 = load_player(args.player_a, 1, map_number=int(args.map_number))
    except Exception as e:
        print(e)
        print("Can't load player 1")
        return 2
    try:
        player_2 = load_player(args.player_b, 2, map_number=int(args.map_number))
    except Exception as e:
        print(e)
        print("Can't load player 2")
        return 1
    
    game = Game(player_1, player_2, map_number=int(args.map_number))

    if args.no_gui:
        graphics = None
    else:
        from gui import Graphics
        graphics = Graphics(fps = 30)

    if args.output:
        history = []
    else:
        history = None

    while game.is_running():
        game.update()
        if history is not None:
            history.append([
                copy.deepcopy([dataclasses.asdict(s) for s in game.ships.values()]),
                copy.deepcopy([dataclasses.asdict(p) for p in game.powerups]),
                (game.score_1, game.score_2)
                           ])
        if graphics:
            graphics.render(game)

    if history is not None:
        history.append({"winner": game.winner()})

        with open(path.join(path.dirname(__file__), args.output), "w+") as f:
            f.write(json.dumps(history))
    
    return game.winner()


def import_module_from_file(file_name):
    # Create a module spec from the file location
    spec = importlib.util.spec_from_file_location("dynamic_module", file_name)
    if spec is None:
        raise ImportError(f"Cannot find module from {file_name}")
    
    # Create a module from the spec
    module = importlib.util.module_from_spec(spec)
    
    # Execute the module
    spec.loader.exec_module(module)
    
    # Optionally, add the module to sys.modules
    sys.modules["dynamic_module"] = module
    
    return module

def load_player(file_name, playerID, map_number=1):
    module = import_module_from_file(file_name)
    player = module.Player(playerID, map_number)
    return player

if __name__ == "__main__":
    winner = simulate_game()
    print("The winner is", winner)
    sys.exit(winner)
else:
    print("What are you doing you fool??")
    sys.exit(0)

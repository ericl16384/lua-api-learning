import logging, json, traceback

# https://pypi.org/project/lupa/
import lupa
import lupa.lua54

# Initialize Lua runtime
lua = lupa.LuaRuntime(
    register_eval=False,
    unpack_returned_tuples=True,
    # attribute_handlers=(getter, setter),
    # attribute_filter=filter_attribute_access,
)
globals = lua.globals()

# Block dangerous functions (very important to security!!!)
# https://www.lua.org/manual/5.4/
blocked_globals = [
    "debug", "dofile", "io", "load", "loadfile", "os", "package", "python", "require"
]
for b in blocked_globals:
    globals[b] = None

# Capture print statments (otherwise they go to stdout)
logger = logging.getLogger("lua")
with open("scripts/game.log", "w") as f: pass # clear file
logging.basicConfig(filename="scripts/game.log", encoding="utf-8", level=logging.DEBUG,
    format="%(asctime)s %(levelname)s:\t%(message)s",
    datefmt="%m/%d/%Y %I:%M:%S %p"
)
# def log_lua_print(*args):
#     out = []
#     for a in args:
#         if lupa.lua_type(args[0]) == "table":
#             print(a)
#             print(dict(a))
#             print(json.dumps(dict(a)))
#             # args[0] = json.dumps(args[0])
#             out.append()
#     logger.info(out)
globals.print = logger.info

# handy util



# scripts

print("loading script files")

with open("scripts/game.lua", "r") as f:
    game_script = f.read()

with open("scripts/player.lua", "r") as f:
    player_script = f.read()



# start a little game

lua.execute(game_script)





# a little game

# import numpy as np
import random

facings = ( # counterclockwise
    (1, 0),
    (0, 1),
    (-1, 0),
    (0, -1)
)

pos = (0, 0)
facing = 0
map = {tuple(pos): "empty"}

# a little maze
# def clear_area(min_xy, max_xy):
#     for x in range(min_xy[0], max_xy[0] + 1):
#         for y in range(min_xy[1], max_xy[1] + 1):
#             map[(x, y)] = "empty"
# clear_area((0, 0), (4, 0))
# clear_area((4, -2), (4, 3))
for k, v in globals.map.items():
    print(k, v)
    xy = k.split(",")
    x = int(xy[0])
    y = int(xy[1])
    map[x, y] = v
    # input()

def get_tile(xy):
    xy = tuple(xy)
    if xy not in map:
        r = random.random()
        # if r < 0.1:
        if max(xy) > 1 or min(xy) < -1:
            map[xy] = "wall"
        else:
            map[xy] = "empty"
    return map[xy]

import visualization
visualization.init()

def print_state(action):
    out = ""
    out += ["east", "north", "west", "south"][facing]
    out += "\t"
    out += str(pos)
    out += "\t--> "
    out += action
    print(out)

    visualization.draw_map(map, pos, facing)

def move(new_pos):
    global pos
    new_pos = tuple(new_pos)

    print_state("move")

    if get_tile(new_pos) == "empty":
        pos = new_pos
        return True
    return False

def turn(amount):
    assert amount in (1, -1)
    global facing

    print_state("turn " + {1:"left",-1:"right"}[amount])

    facing += amount
    facing %= len(facings)


# globals.move_up = lambda: move((pos[0], pos[1] + 1))
# globals.move_left = lambda: move((pos[0] - 1, pos[1]))
# globals.move_down = lambda: move((pos[0], pos[1] - 1))
# globals.move_right = lambda: move((pos[0] + 1, pos[1]))

globals.move_forward = lambda: move((
    pos[0] + facings[facing][0],
    pos[1] + facings[facing][1]
))
globals.turn_right = lambda: turn(-1)
globals.turn_left = lambda: turn(1)








# try:
lua.execute(player_script)
# except:
#     print(traceback.format_exc())

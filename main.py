import traceback

# https://pypi.org/project/lupa/
import lupa

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
print_log = []
globals.print = lambda *args: print_log.append(args)





# a little game

import numpy as np
import random

pos = (0, 0)
map = {tuple(pos): "empty"}

def get_tile(xy):
    xy = tuple(xy)
    if xy not in map:
        r = random.random()
        # if r < 0.1:
        if max(xy) > 2 or min(xy) < -2:
            map[xy] = "wall"
        else:
            map[xy] = "empty"
    return map[xy]

def move(new_pos):
    global pos

    print(pos)
    input()

    if get_tile(new_pos) == "empty":
        pos = new_pos
        return True
    return False

globals.move_up = lambda: move((pos[0], pos[1] + 1))
globals.move_left = lambda: move((pos[0] - 1, pos[1]))
globals.move_down = lambda: move((pos[0], pos[1] - 1))
globals.move_right = lambda: move((pos[0] + 1, pos[1]))








# Load script
with open("script.lua", "r") as f:
    script = f.read()
# try:
lua.execute(script)
# except:
#     print(traceback.format_exc())


print("caught print output:")
# for l in globals.__caught_print_output.split("\n"):
#     print(">>>", l)
for l in print_log:
    print(" ".join(l))


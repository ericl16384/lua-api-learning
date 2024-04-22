import logging, json, traceback

# https://pypi.org/project/lupa/
import lupa
import lupa.lua54

def create_lua_environment():

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

    return lua, globals

# handy util



# scripts

print("loading script files")

with open("scripts/game.lua", "r") as f:
    game_script = f.read()

with open("scripts/player.lua", "r") as f:
    player_script = f.read()



# start a little game

lua, globals = create_lua_environment()

lua.execute(game_script)



# a little game

import visualization
visualization.init()

def visualize():
    map = {}
    for k, v in globals.map.items():
        # print(k, v)
        xy = k.split(",")
        x = int(xy[0])
        y = int(xy[1])
        map[x, y] = v
        # input()
    # visualization.draw_map(map, pos, facing)
    visualization.draw_map(map, (
        globals.units[1].x, globals.units[1].y
    # ), facing)
    ), 0)
globals.turn_end = visualize




# try:
lua.execute(player_script)
# except:
#     print(traceback.format_exc())

import logging, random, traceback

# logging_formatter = logging.Formatter("%(asctime)s: %(message)s")
logging_formatter = logging.Formatter("%(message)s")

# https://stackoverflow.com/questions/11232230/logging-to-two-files-with-different-settings
def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file)        
    handler.setFormatter(logging_formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


# https://pypi.org/project/lupa/
# import lupa
import lupa.lua54

def create_lua_environment(logger_filename):
    # Initialize Lua runtime
    lua = lupa.lua54.LuaRuntime(
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
    with open(logger_filename, "w"): pass # clear file
    logger = setup_logger(logger_filename, logger_filename, logging.INFO)
    globals.print = logger.info

    return lua, globals



# scripts

print("loading script files")

with open("scripts/game.lua", "r") as f:
    game_script = f.read()

with open("scripts/player.lua", "r") as f:
    player_script = f.read()



# start a little game

import visualization
visualization.init()

def visualize(lua_globals):
    map = {}
    for k, v in lua_globals.map.items():
        # print(k, v)
        xy = k.split(",")
        x = int(xy[0])
        y = int(xy[1])
        map[x, y] = v
        # input()
    # visualization.draw_map(map, pos, facing)
    visualization.draw_map(map, (
        lua_globals.units[1].x, lua_globals.units[1].y
    # ), facing)
    ), 0)


player_lua, player_globals = create_lua_environment("scripts/player.log")
game_lua, game_globals = create_lua_environment("scripts/game.log")



# init_globals_keys = list(globals.keys())

game_globals.turn_end = lambda : visualize(game_globals)

# player_lua.execute("print('Hello World')")


game_lua.execute(game_script)


def get_interface_function(func_name):
    def out(*args):
        return game_globals[func_name](*args)
    return out
for func_name in game_globals["INTERFACE_FUNCTIONS"].values():
    player_globals[func_name] = get_interface_function(func_name)


# interface = list(globals.INTERFACE.values())

# saved_variables = init_globals_keys + interface

# for key, value in globals.items():
#     print(key)
#     if key not in saved_variables:
#         globals[key] = None
#         print("        DELETED")


visualize(game_globals)

# try:
player_lua.execute(player_script)
# except:
#     print(traceback.format_exc())

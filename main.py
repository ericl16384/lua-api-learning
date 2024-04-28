import logging#, random, traceback

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
    globals.print = lambda *args: logger.info(" ".join([str(arg) for arg in args]))

    return lua, globals



# scripts

def load_script(name):
    with open(f"scripts/{name}.lua", "r") as f:
        return f.read()



# start a little game

import visualization
visualization.init()

def visualize(lua_globals):
    # map = {}
    # for k, v in lua_globals.map.items():
    # # for k, v in lua_globals.known_map.items():
    #     # print(k, v)
    #     xy = k.split(",")
    #     x = int(xy[0])
    #     y = int(xy[1])
    #     map[x, y] = v
    #     # input()
    # # visualization.draw_map(map, pos, facing)

    if lua_globals.fog_of_war:
        map = lua_globals.known_map
    else:
        map = lua_globals.map

    visualization.draw_map(map, (
        lua_globals.units[1].x, lua_globals.units[1].y
    # ), facing)
    ), 0)




class GameInstance:
    def __init__(self, game_script, player_script):
        self.game_script = game_script
        self.player_script = player_script

        self.game_lua, self.game_globals = create_lua_environment(f"scripts/game_{hash(game_script)}.log")
        self.player_lua, self.player_globals = create_lua_environment(f"scripts/player_{hash(player_script)}.log")

        self.game_globals.turn_end = lambda : visualize(self.game_globals)
        self.game_lua.execute(game_script)

        def get_interface_function(func_name):
            def out(*args):
                return self.game_globals[func_name](*args)
            return out
        for func_name in self.game_globals["INTERFACE_FUNCTIONS"].values():
            self.player_globals[func_name] = get_interface_function(func_name)

    def run_player(self):
        visualize(self.game_globals)

        # try:
        self.player_lua.execute(self.player_script)
        # except:
        #     print(traceback.format_exc())

        # while True:
        #     visualize(self.game_globals)



# main()
game = GameInstance(load_script("game"), load_script("player"))
game.run_player()

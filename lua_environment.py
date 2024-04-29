import hashlib, logging

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

# import visualization
# visualization.init()

# def visualize(lua_globals):
#     # map = {}
#     # for k, v in lua_globals.map.items():
#     # # for k, v in lua_globals.known_map.items():
#     #     # print(k, v)
#     #     xy = k.split(",")
#     #     x = int(xy[0])
#     #     y = int(xy[1])
#     #     map[x, y] = v
#     #     # input()
#     # # visualization.draw_map(map, pos, facing)

#     if lua_globals.fog_of_war:
#         map = lua_globals.known_map
#     else:
#         map = lua_globals.map

#     visualization.draw_map(map, (
#         lua_globals.units[1].x, lua_globals.units[1].y
#     # ), facing)
#     ), 0)


def basic_hash(x):
    return hashlib.sha256(bytes(x, "utf-8")).hexdigest()

class GameInstance:
    class DisplayInterface:
        def __init__(self):
            # self.framerate = 1

            self.events = []

        # def get_HTML_canvas(self, width=1024, height=576):
        #     # self_hash = basic_hash(self)

        #     out = f"<canvas id='DisplayInterface' width='{width}' height='{height}' style='border:1px solid #000000;'>Sorry, you browser dones not support canvas.</canvas>"
        #     out += "<script type='text/javascript'>"
        #     out += f"var DisplayInterface_frame = 0;"
        #     out += f"function DisplayInterface()"
        #     out += "{"
        #     out += "const canvas = document.getElementById('drawCanvas');"
        #     out += "const ctx = canvas.getContext('2d');"
        #     out += "DisplayInterface_frame++;"
        #     out += "}"
        #     out += f"DisplayInterface();"
        #     out += f"window.setInterval(DisplayInterface, {1000 / self.framerate});"
        #     out += "</script>"
        #     return out

        def clear_display(self):
            self.events.append(("clear_display",))

        def draw_rect(self, x, y, w, h, color):
            x = float(x)
            y = float(y)
            w = float(w)
            h = float(h)


            # TEMPORARY
            def transform(pos, translate=True):
                tile_size = 20
                # if tile_offset:
                #     pos = [i-0.5 for i in pos]
                center = (1024/2, 576/2)
                pos = (
                    pos[0] * tile_size,
                    pos[1] * tile_size
                )
                if translate:
                    pos = (
                        pos[0] + center[0],
                        pos[1] + center[1]
                    )
                return pos
            x, y = transform((x, y))
            w, h = transform((w, h), False)


            self.events.append(("draw_rect", x, y, w, h, color))

        def sleep(self, seconds):
            self.events.append(("sleep", seconds*1000))

    def __init__(self, game_script, player_script):
        self.game_script = game_script
        self.player_script = player_script

        self.game_lua, self.game_globals = create_lua_environment("scripts/game.log")
        self.player_lua, self.player_globals = create_lua_environment("scripts/player.log")

        # draw = []

        # self.game_globals.turn_end = lambda : visualize(self.game_globals)
        # self.game_globals.turn_end = lambda : input("end turn")

        self.display_interface = self.DisplayInterface()
        self.game_globals.clear_display = self.display_interface.clear_display
        self.game_globals.draw_rect = self.display_interface.draw_rect
        self.game_globals.sleep = self.display_interface.sleep

        self.game_lua.execute(game_script)

        def get_interface_function(func_name):
            def out(*args):
                return self.game_globals[func_name](*args)
            return out
        for func_name in self.game_globals["INTERFACE_FUNCTIONS"].values():
            self.player_globals[func_name] = get_interface_function(func_name)

    def run_player(self):
        # visualize(self.game_globals)

        # try:
        self.player_lua.execute(self.player_script)
        # except:
        #     print(traceback.format_exc())

        # while True:
        #     visualize(self.game_globals)



def main():
    game = GameInstance(load_script("game"), load_script("player"))
    game.run_player()


    import json
    with open("scripts/history.json", "w") as f:
        f.write(json.dumps(game.display_interface.events))

if __name__ == "__main__": main()

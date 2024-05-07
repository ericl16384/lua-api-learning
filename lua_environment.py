import json
import hashlib
import logging
import multiprocessing
import multiprocessing.connection
import os
import time
import traceback

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

def create_lua_environment(print_function):
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
    # with open(logger_filename, "w"): pass # clear file
    # logger = setup_logger(logger_filename, logger_filename, logging.INFO)
    # globals.print = lambda *args: logger.info(" ".join([str(arg) for arg in args]))
    globals.print = print_function

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


def refresh_replays_index(replays_directory):
    index_filename = "__index__.log"
    replays_directory_index = replays_directory + index_filename

    old_replays = set()
    if os.path.exists(replays_directory_index):
        with open(replays_directory_index, "r") as f:
            for l in f.readlines():
                old_replays.add(json.loads(l)["replay_hash"])
    else:
        if not os.path.exists(replays_directory):
            os.mkdir(replays_directory)
            with open(replays_directory_index, "w"): pass

    new_replays = []
    for filename in os.listdir(replays_directory):
        filepath = replays_directory + filename

        if not os.path.isfile(filepath):
            continue

        if filename == index_filename:
            continue

        if filename.endswith(".json"):
            with open(filepath, "r") as f:
                info = json.loads(f.read())["info"]
                if info["replay_hash"] in old_replays:
                    continue
                new_replays.append(info)

    with open(replays_directory_index, "a") as f:
        for replay in new_replays:
            f.write(json.dumps(replay) + "\n")


def basic_hash(x):
    if isinstance(x, (dict, list)):
        x = json.dumps(x)
    return hashlib.sha256(bytes(x, "utf-8")).hexdigest()

class GameInstance:
    class DisplayInterface:
        def __init__(self, game_hash, player_hash):
            # self.framerate = 1

            self.game_hash = game_hash
            self.player_hash = player_hash

            self.events = []

        def save_as_replay(self, replays_directory):
            if not os.path.exists(replays_directory):
                os.mkdir(replays_directory)

            replay_id = basic_hash(self.events)
            filename = f"{replays_directory}{replay_id}.json"
            out = {
                "info": {
                    "replay_hash": basic_hash(self.events),
                    "game_hash": self.game_hash,
                    "player_hash": self.player_hash,
                    "save_time": time.time()
                },
                "events": self.events
            }
            with open(filename, "w") as f:
                f.write(json.dumps(out))

            refresh_replays_index(replays_directory)

            return replay_id

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
        
        def print(self, *msgs):
            self.events.append(("print", " ".join([str(msg) for msg in msgs])+"\n"))

    def __init__(self, game_script, player_script):
        self.game_script = game_script
        self.player_script = player_script

        self.display_interface = self.DisplayInterface(
            basic_hash(self.game_script), basic_hash(self.player_script)
        )
        
        self.game_lua, self.game_globals = create_lua_environment(self.display_interface.print)
        self.player_lua, self.player_globals = create_lua_environment(self.display_interface.print)

        # draw = []

        # self.game_globals.turn_end = lambda : visualize(self.game_globals)
        # self.game_globals.turn_end = lambda : input("end turn")

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



def run_new_game(game_script, player_script):
    game = GameInstance(game_script, player_script)
    game.run_player()

    return game.display_interface.save_as_replay("replays/")

    # events = game.display_interface.events

    # with open(f"replays/{basic_hash(events)}.json", "w") as f:
    #     f.write(json.dumps(events))

def run_new_game_process(connection:multiprocessing.connection.Connection, *args, **kwargs):
    """returns (success, result)"""

    # try:
    # out.value = run_new_game(*args, **kwargs)
    # except Exception as err:
    #     out.value = traceback.format_exc()
    try:
        result = run_new_game(*args, **kwargs)
        success = True
    except:
        result = traceback.format_exc()
        success = False
    
    connection.send((success, result))

def main():
    run_new_game(load_script("game"), load_script("player"))

if __name__ == "__main__": main()

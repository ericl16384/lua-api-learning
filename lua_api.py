# not really working yet. a hope for the future



# https://pypi.org/project/lupa/
import lupa

class LockedLuaAPI:
    def __init__(self):
        # Initialize Lua runtime
        self.lua = lupa.LuaRuntime(
            register_eval=False, # lua execute Python code as exec()
            unpack_returned_tuples=True,
            # attribute_handlers=(getter, setter),
            # attribute_filter=filter_attribute_access,
        )

        # Load environment (very important to security!!!)
        # assert self.lua.execute(environment) == "environment success"
        with open("environment.lua", "r") as f:
            assert self.lua.execute(f.read()) == "environment.lua success"

    def run_script(self, script):
        self.lua.execute(script)

    def run_file(self, filename):
        with open(filename, "r") as f:
            self.run_script(f.read())

    def get_print_log(self):
        # I'll want a better way to do this...
        # print("caught print output:")
        # for l in globals.__caught_print_output.split("\n"):
        #     print(">>>", l)
        # self.__caught_print_output = globals.__caught_print_output
        return self.lua.globals().__caught_print_output

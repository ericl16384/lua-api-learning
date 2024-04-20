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


# globals.zzz = "seven"


# Load script
with open("script.lua", "r") as f:
    script = f.read()
try:
    lua.execute(script)
except:
    print(traceback.format_exc())


print("caught print output:")
# for l in globals.__caught_print_output.split("\n"):
#     print(">>>", l)
for l in print_log:
    print(" ".join(l))


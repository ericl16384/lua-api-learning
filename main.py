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
blocked_globals = ["debug", "io", "os", "package", "python"]
for b in blocked_globals:
    globals[b] = None

# Capture print statments (otherwise they go to stdout)
print_log = []
globals.print = lambda *args: print_log.append(args)


# globals.zzz = "seven"


# Load script
with open("script.lua", "r") as f:
    script = f.read()
lua.execute(script)


print("caught print output:")
# for l in globals.__caught_print_output.split("\n"):
#     print(">>>", l)
for l in print_log:
    print("\t".join(l))


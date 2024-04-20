# https://pypi.org/project/lupa/
import lupa


# set up lua security

# attribute_blacklist = ["io"]

# def getter(obj, attr_name):
#     print(obj, attr_name)
#     for a in attribute_blacklist:
#         if attr_name.startswith(a):
#             raise AttributeError(f"not allowed to read attribute {attr_name}")
#     return getattr(obj, attr_name)
# def setter(obj, attr_name, value):
#     print(obj, attr_name)
#     for a in attribute_blacklist:
#         if attr_name.startswith(a):
#             raise AttributeError(f"not allowed to write attribute {attr_name}")
#     setattr(obj, attr_name, value)

# def filter_attribute_access(obj, attr_name, is_setting):
#     # if isinstance(attr_name, unicode):
#     if not attr_name.startswith("_"):
#         return attr_name
#     raise AttributeError("access denied")


# Initialize Lua runtime
lua = lupa.LuaRuntime(
    register_eval=False,
    unpack_returned_tuples=True,
    # attribute_handlers=(getter, setter),
    # attribute_filter=filter_attribute_access,
)
globals = lua.globals()

# Load environment (very important to security!!!)
with open("environment.lua", "r") as f:
    assert lua.execute(f.read()) == "environment.lua success"



# Load script
with open("script.lua", "r") as f:
    script = f.read()
lua.execute(script)


print("caught print output:")
for l in globals.__caught_print_output.split("\n"):
    print(">>>", l)




# func = lua.eval("function(f, n) return f(n) end")

# # Expose a Python function to Lua
# # @lua.register
# def add(a, b):
#     return a + b

# # Load and execute Lua script
# lua.execute("""
# result = add(10, 20)
# print(result)
# """)

# # Accessing Lua variables from Python
# result = lua.globals().result
# print("Result from Lua:", result)
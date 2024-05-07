import ctypes, multiprocessing

# import lua_environment
import server


# out = multiprocessing.Manager().Value(ctypes.c_char_p, "")

game_id = "a1495a341f055c14f052c0c2d0abd4d3e2171e3fe5661fbad68ef37b422b4bba"
print(server.RequestHandler.get_script(None, game_id))





import os
cwd = os.getcwd()
print(cwd)




input()

import ctypes, multiprocessing
import lua_environment


out = multiprocessing.Manager().Value(ctypes.c_char_p, "")

from ctypes import *
from complementaryc.bin.osSelect import SelectOS


def current_year():
    my_path = SelectOS().the_path
    shared_library_functions = CDLL(my_path)

    return shared_library_functions.currentYear()

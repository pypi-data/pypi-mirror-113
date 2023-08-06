import subprocess
from complementaryc.bin.osSelect import SelectOS


def complementaryStrand(sequence):
    my_path = SelectOS().the_path

    out = subprocess.run([my_path, sequence])
    return out

from shutil import copy2
import os

f = open("D:\Archieve-Copy\Programok\Dos\ROLMusic\LIST.SCR", "w")

for root, dirs, files in os.walk("D:\Archieve-Copy\Programok\Dos\ROLMusic"):
    for file in files:
        if (".ROL" in file.upper()):
            f.write(
                "/R " + file + "\n"
            )

f.close()
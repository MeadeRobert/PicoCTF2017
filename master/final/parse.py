import re
import numpy as np

text = open("wizard_sight.txt").read()
addresses = [int(i, 16) for i in re.findall(r"0x[0-9a-f]+", text)]



print addresses
print np.diff(addresses)

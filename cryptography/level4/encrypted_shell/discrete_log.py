from math import ceil, log

def isqrt(n):
    res = 0
    bit = 4**int(ceil(log(n, 4))) if n else 0
    while bit:
        if n >= res + bit:
            n -= res + bit
            res = (res >> 1) + bit
        else:
            res >>= 1
        bit >>= 2
    # ceil
    if res**2 == n:
        return res
    else:
        return res+1
            
def discrete_log():
    pass
    

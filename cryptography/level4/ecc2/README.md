# ECC2

For this problem, we used the Pohlig-Hellman algorithm, keeping in mind that every small increase in the scalar of a subgroup results in a large change to the final scalar and the overall bound, we better computer the bounds for each Baby Step-Giant Step search on the subgroups.

```python
#! /usr/bin/env sage

# Constants

M = 93556643250795678718734474880013829509320385402690660619699653921022012489089
A = 66001598144012865876674115570268990806314506711104521036747533612798434904785

P = (56027910981442853390816693056740903416379421186644480759538594137486160388926, 65533262933617146434438829354623658858649726233622196512439589744498050226926)
nP = (30399321663277778915789435918669378136486628773979001534946407690195669208748, 1973041983573227486868025872751342101679089524467602053850914626437554196117)

b = 400000000000000000000000000000

# Compute B with basic modular arithmetic
B = (P[1]**2 - P[0]**3 - A*P[0]) % M

# Define curve and points
F = GF(M)
E = EllipticCurve(F, [A,B])

base = E(P)
res = E(nP)

# Step is the amount that every increment of this subgroup's
# scalar will increase the overall scalar by
step = 1
# Start is the residue under the modulus step of the final
# scalar value
start = 0

for p, k in factor(E.order()):
    # Pohlig-Hellman over this factor (https://en.wikipedia.org/wiki/Pohlig%E2%80%93Hellman_algorithm)
    f = p ** k
    nbase = base * (E.order() // f)
    nres = res * (E.order() // f)
    # Find whether it is faster to compute using the given
    # bound and our start point and step or from the order
    # of the subgroup as the bounds
    if b // (step - start) < f:
        bounds = (start, start + b // (step - start))
    else:
        bounds = (0, f)
    # Find this subgroup's discrete log using those bounds (part of Pohlig-Hellman)
    r = bsgs(nbase, nres, bounds, operation='+')
    # Change start to include start % f == r
    start = crt(start, r, step, f)
    # Because all factors are mutually coprime, we can just
    # multiply the step to get the step for the next subgroup
    step *= f

# Once we've iterated through all of the factors, step == E.order()
# and so the residue (start) is the solution to the problem
print(start)
```

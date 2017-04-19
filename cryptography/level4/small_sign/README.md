# SmallSign

```
This service outputs a flag if you can forge an RSA signature!
nc shell2017.picoctf.com 7541
smallsign.py
HINTS
RSA encryption (and decryption) is multiplicative.
```

Taking a look at the sourcecode for smallsign.py, we can see that the program is computing decrypted values of encrypted inputs by the [RSA Algorithm](https://en.wikipedia.org/wiki/RSA_%28cryptosystem%29). That is, for a given user defined ciphertext ```c```, unknown private exponent ```d```, and modulus ```N```, it is computing ```c^d mod N```. The result is coined the RSA "signature" of the input value. We are given both the product of 2 unknown prime numbers ```p``` and ```q``` as ```N``` and the public exponent ```e``` as a [Fermat Prime](http://mathworld.wolfram.com/FermatPrime.html): ```65537```. The program will provide us with only 60 seconds to glean necessary information and then requires that we produce one of these signatures for an arbitrary 32 bit unsigned integer.

Brute force to factorize ```N``` back into its 2 prime factors is the most straight forward approach. Too bad that would take longer than we will be alive without access to quantum computers capable of running Shor's algorithm. Maybe the machines will finish after we're gone. As for now, we'll have to find a better approach. Looking for a vulnerability, we can see none in the implementation nor in the RSA Algorithm. We can, however, defeat this challenge without having to crack the entire mapping for all natural numbers. 

Referencing the hint it is important to note that RSA is multiplicative, provides us with a shortcut. That is, a chosen ciphertext attack is possible because ```(a*b)^d ≡ a^d * b^d (mod n)```. Put simply, if we have the decrypted values for the factors of the random number, then we can build the signature of the random number from these components. This approach will rely on a bit of luck, which makes demonstrations great when you're have a bad day, but it is likely to work without having to take too many guesses.

We used 2 python scripts and 2 separate terminals for this attack. Our first python script reads primes from a file of primes and prints a range of them defined by command line arguments separated by newlines. We used primes1.txt from [https://primes.utm.edu/lists/small/millions/](https://primes.utm.edu/lists/small/millions/). Below lies ```primes.py```.

```Python
import sys

primes = []
with open("primes1.txt") as file:
    for line in file:
        primes += [int(num) for num in line.split()]
        
print('\n'.join([str(p) for p in primes[int(sys.argv[1]):int(sys.argv[2])]]))
file = open("primes", "w")
file.write('\n'.join([str(p) for p in primes[int(sys.argv[1]):int(sys.argv[2])]])+'\n')
file.close()
``` 

We pipe the first thousand primes out of this script and into the netcat application and send the result to a file to be used by our other script, taking care to pass stdin back in when we're done with ```cat```.

Terminal 1:
```
$ (python primes.py 0 1000; cat) | nc shell2017.picoctf.com 7541 | tee data.txt
You have 60 seconds to forge a signature! Go!
N: 27208753377347696160166401580094236985599417996499479963420552855740404022794951216026741091717168054822858161169888488265959960813083720558598639133804010926538361833105440213378984037873337776367399320554761589019374606875477579548916005117750722547447002321632147116086299090906800429347090550131165847082761942297626475614652495860347862452894755526716636661528762878212274519116229059977534733434987389680315273333956172925509131098512530668846374073814867346135741091481741512069358168347303873889182459227884954011618019526764432395539909018723208384387126071377395520819441506175262835995331314765864360221247
e: 65537
Enter a number to sign (-1 to stop): Signature: 26040328839242273662746916889490780427107395026940140192760547692611840177849552386858477216706975858210001751684734251933770655287210244702455419901865897199378639829956068012617047837425721953320896283591650093214171723219790309031719858025802019677027623328993182745059370803613240516555017453181041674357279778058774194603266759746351080763119915320173538517448370188571669994109192333437388700007498067045072985618157365937383489741143192159858422264991481152153962290903371952625111491474713127389788640073880897791417183491418032389541801100538217690111946498254714158329349808133147873939338177109252119852794
...
...
Enter a number to sign (-1 to stop): Signature: 2582439823301394614176069487536939117321767606079447908056273158100821121925095619737746620850607260757810475090761298368985457347165127292741149416721041763604554318162870073188139669710401755437336543329554381802695713970683311739285815308393954324848452546864769951685666179199289068909305178004397410295149311376425439705484363590459495756168578664275393922688788367880548439495847181119188944083027840106826213370117238970550579758483771977685103298862838157356674557927570444734669522686521909493182548890076736569028999930512445981063332018952636667544265880026543244955135283160882988948323600167958308411050
Enter a number to sign (-1 to stop): -1
Challenge: 385196064
```
Note: The first half of this is not from the same run as the second half. We could not capture that as sending in 1000+ primes overflowed the terminal buffer.

After injecting the primes, we use our second python script to create a mapping of the injected primes and their respective RSA signatures and attempt to factor the random number generated by the challenge. If the number is factorizable we can proceed. We have explained our script below

First, we use regular expressions to search our file for N, e, and the signatures of our primes.

```Python
import re

# parse primes 
primes = []
with open("primes1.txt") as file:
    for line in file:
        primes += [int(num) for num in line.split()]

# parse N, e, and signatures
text = open("data.txt").read()
N = [int(n) for n in re.findall(r'N:\s([0-9]+)', text)][0]
e = [int(e) for e in re.findall(r'e:\s([0-9]+)', text)][0]
signatures = [int(s) for s in re.findall(r'Signature:\s([0-9]+)', text)]

# create ref dict
ref = dict(zip(primes[0:len(signatures)],signatures))
```

Then, we attempt to factorize the challenge in terms of those primes.

```Python
# works for small n only
# hardcoded to limit to amount of cached primes
# so that failure is ensured if not factorizable
# in terms of said primes
def prime_fac(n):
    fac = {}
    for p in primes[0:len(signatures)]:
        while n % p == 0:
            n //= p
            if p in fac:
                fac[p] += 1
            else:
                fac.update({p:1})
    return fac

# get challenge value and attempt to factorize
value = int(input("input value: "))
value_fac = prime_fac(value)
```

If the factorization is not successful, the program aborts, and we must start over. Otherwise, we compute the RSA signature using its multiplicative properites.


```Python
# compute product of the "alleged factorization" of the challenge
product = 1
for k in value_fac.keys():
    product *= k ** value_fac[k]

# if the factorization has succeeded, compute the rsa signature
if product == value:
    print(value_fac)
    msg = 1
    # compute the rsa sig by the multiplicative
    # property of rsa, using the dictionary of
    # primes and their respective signatures
    for k in value_fac.keys():
        for i in range(0, value_fac[k]):
            msg *= ref[k]
            msg %= N
    print(msg)
else:
    print("factorization failed")
    print(value_fac)
```


In the other terminal we execute this script as follows.

Terminal 2:
```
$ python exploit.py
input value: 385196064
{17: 1, 2: 5, 3: 1, 43: 1, 11: 1, 499: 1}
15486554977210219256388039133715196553070795643379336975276692498842069230242667426214871008286822411285396168050269114686408339966162558629689153800261029418833721697324906302181066867409777389430177486151661270297240695918206258411949113708275025343713830583977988920352097926717174289542790538077651354230796249295245304464750118236233282194766726354743915632978103074007650305176805671464001528663812751319935260810661095957980922666379541298397204659141228399632711282887661507836260768021102725691900275964999855752941686062551325686275668300155452587243121830723515427560833495827809959063303951795823704582305
$  
```

Then, we copy the resulting signature and input it into terminal 1.

Terminal 1:
```
Enter the signature of the challenge: 15486554977210219256388039133715196553070795643379336975276692498842069230242667426214871008286822411285396168050269114686408339966162558629689153800261029418833721697324906302181066867409777389430177486151661270297240695918206258411949113708275025343713830583977988920352097926717174289542790538077651354230796249295245304464750118236233282194766726354743915632978103074007650305176805671464001528663812751319935260810661095957980922666379541298397204659141228399632711282887661507836260768021102725691900275964999855752941686062551325686275668300155452587243121830723515427560833495827809959063303951795823704582305
Congrats! Here is the flag: ad4b118a7296792be34a29ee5180daba
```

We usually have to repeat this process no more than 10 times to get it to work, a substantial improvement on a brute force or randomized search method. It would have been cool to get this process done in a single script. If anyone has information on how this two terminal system could be reduced to a single, one off python script, please contact us. We would love to hear of such a solution.

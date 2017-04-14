#!/usr/bin/python2 -u
from hashlib import sha256
from Crypto import Random
from Crypto.Random import random
from Crypto.Cipher import AES
from subprocess import check_output, STDOUT, CalledProcessError

BLOCK_SIZE = 16
R = Random.new()


def pad(m):
    o = BLOCK_SIZE - len(m) % BLOCK_SIZE
    return m + o * chr(o)

def unpad(p):
    return p[0:-ord(p[-1])]

def send_encrypted(KEY, m):
    IV = R.read(BLOCK_SIZE)
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    c = aes.encrypt(pad(m))
    print (IV + c).encode('hex')

def read_encrypted(KEY):
    data = raw_input("").decode('hex')
    IV, data = data[:BLOCK_SIZE], data[BLOCK_SIZE:]
    aes = AES.new(KEY, AES.MODE_CBC, IV)
    m = unpad(aes.decrypt(data))
    return m

p = 174807157365465092731323561678522236549173502913317875393564963123330281052524687450754910240009920154525635325209526987433833785499384204819179549544106498491589834195860008906875039418684191252537604123129659746721614402346449135195832955793815709136053198207712511838753919608894095907732099313139446299843
g = 41899070570517490692126143234857256603477072005476801644745865627893958675820606802876173648371028044404957307185876963051595214534530501331532626624926034521316281025445575243636197258111995884364277423716373007329751928366973332463469104730271236078593527144954324116802080620822212777139186990364810367977
    
print "Parameters:"
print "p = {}".format(p)
print "g = {}".format(g)

b = 7
B = pow(g, b, p)

print "B = {}".format(B)

A = int(raw_input("Please supply A: "))
K = pow(A, b, p)
print K

KEY = sha256(str(K)).digest()
print KEY

print "password"
print send_encrypted(KEY, 'password\n')
print "ThisIsMySecurePasswordPleaseGiveMeAShell\n"
print send_encrypted(KEY, 'ThisIsMySecurePasswordPleaseGiveMeAShell\n')
print "cat flag.txt"
print send_encrypted(KEY, 'cat flag.txt\n')

print "enter response"
print read_encrypted(KEY)

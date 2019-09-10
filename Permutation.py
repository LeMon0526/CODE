'''
Name: Permutation Cipher
Programmer: AI
Date: 2017-09-01
State: alpha
Note: 
Example:

import Cipher.Permutation

p = "gettheball"
k = "ccaeb"
c = Cipher.Permutation.Encrypt(p, k)
print(c)
print(Cipher.Permutation.Decrypt(c, k))

'''

def Encrypt(plaintext, key):
    ciphertext = ""
    table = _Sort(key)
    n = (len(key) - len(plaintext) % len(key)) % len(key)
    for i in range(n):
        plaintext += 'x'
    for i in range(0, len(plaintext), len(key)):
        for j in range(len(key)):
            ciphertext += plaintext[i + table[j]]
    return ciphertext

def Decrypt(ciphertext, key):
    plaintext = ""
    table = _Sort(key)
    for i in range(0, len(ciphertext), len(key)):
        for j in range(len(key)):
            plaintext += ciphertext[i + table.index(j)]
    return plaintext

def _Sort(key):
    table = []
    for i in range(ord('a'), ord('z') + 1):
        beg = 0
        while True:
            beg = key.find(chr(i), beg) + 1
            if beg != 0:
                table.append(beg - 1)
            else:
                break
    return table

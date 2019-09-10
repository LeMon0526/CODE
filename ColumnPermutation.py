'''
Name: Column Permutation Cipher
Programmer: AI
Date: 2017-09-01
State: alpha
Note: 
Example:

import Cipher.ColumnPermutation
p = "encryptionalgorithms"
k = "what"
c = Cipher.ColumnPermutation.Encrypt(p, k)
print(c)
print(Cipher.ColumnPermutation.Decrypt(c, k))

'''

def Encrypt(plaintext, key):
    ciphertext = ""
    table = _Sort(key)
    n = (len(key) - len(plaintext) % len(key)) % len(key)
    for i in range(n):
        plaintext += 'x'
    for i in table:
        for j in range(len(plaintext) // len(key)):
            ciphertext += plaintext[j * len(key) + i]
    return ciphertext

def Decrypt(ciphertext, key):
    plaintext = ""
    table = _Sort(key)
    for i in range(len(ciphertext) // len(key)):
        for j in range(len(key)):
            plaintext += ciphertext[(len(ciphertext) // len(key)) * table.index(j) + i]
    return plaintext

def _Sort(key):
    table = []
    for i in range(len(key)):
        k = 0
        for j in range(len(key)):
            if (ord(key[i]) == ord(key[j]) and i > j) or ord(key[i]) > ord(key[j]):
                k += 1
        table.append(k)
    return table

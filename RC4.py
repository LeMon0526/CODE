'''
Rivest Cipher 4(RC4)
Programmer: Ai Zhengpeng
Date: 2017-08-30
Function:
Encrypt(plaintext, key) -> ciphertext
Decrypt(ciphertext, key) -> ciphertext
_KSA(key) -> permutation
_PRG(permutation, i, j) -> z, i, j
'''

import base64

MODULO = 256

def Encrypt(plaintext, key):
    ciphertext = ""
    permutation = _KSA(key)
    i, j = 0, 0
    for letter in plaintext:
        z, i, j = _PRG(permutation, i, j)
        ciphertext += chr(ord(letter) ^ z)
    ciphertext = bytes.decode(base64.b64encode(str.encode(ciphertext)))
    return ciphertext

def Decrypt(ciphertext, key):
    plaintext = ""
    permutation = _KSA(key)
    i, j = 0, 0
    ciphertext = bytes.decode(base64.b64decode(str.encode(ciphertext)))

    for letter in ciphertext:
        z, i, j = _PRG(permutation, i, j)
        plaintext += chr(ord(letter) ^ z)
    return plaintext

def _KSA(key):
    permutation = []
    for i in range(MODULO):
        permutation.append(i)
    j = 0
    for i in range(MODULO):
        j = (j + permutation[i] + ord(key[i % len(key)])) % MODULO
        permutation[i], permutation[j] = permutation[j], permutation[i]
    return permutation

def _PRG(permutation, i, j):
    i = (i + 1) % MODULO
    j = (j + permutation[i]) % MODULO
    permutation[i], permutation[j] = permutation[j], permutation[i]
    z = permutation[(permutation[i] + permutation[j]) % MODULO]
    return z, i, j

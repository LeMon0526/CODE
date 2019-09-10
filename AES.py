'''
Name: Advanced Encryption Standard(AES)
Programmer: Ai
Date: 2017-09-01
Note: Key length must be 16, 24, 32 bytes.
Example:

import Cipher.AES
key = "Sixteen byte key"
plaintext = "Attack at dawn"
ciphertext = Cipher.AES.Encrypt(plaintext, key)
print(ciphertext)
print(Cipher.AES.Decrypt(ciphertext, key))

'''

from Crypto.Cipher import AES
from Crypto import Random

import base64

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS) 
unpad = lambda s : s[:-ord(s[len(s)-1:])]

def Encrypt(plaintext, key):
    plaintext = pad(plaintext)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return bytes.decode(base64.b64encode(iv + cipher.encrypt(plaintext)))

def Decrypt(ciphertext, key):
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:16]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return bytes.decode(unpad(cipher.decrypt(ciphertext[16:])))

#key = "Sixteen byte key"
#plaintext = "Attack at dawn"
#ciphertext = Cipher.AES.Encrypt(plaintext, key)
#print(ciphertext)
#print(Decrypt(ciphertext, key))

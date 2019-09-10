'''
Autokey Cipher - Ciphertext
Programmer: Ai Zhengpeng
Date: 2017-08-31
Function:
Encrypt(plaintext, key) -> ciphertext
Decrypt(ciphertext, key) -> plaintext
'''

def Encrypt(plaintext, key):
    ciphertext = ""
    i = 0
    for letter in plaintext:
        if letter.islower():
            ciphertext += chr((ord(letter) - ord('a') + ord(key[i].lower()) - ord('a')) % 26 + ord('a'))
            key += letter
            i += 1
        elif letter.isupper():
            ciphertext += chr((ord(letter) - ord('A') + ord(key[i].lower()) - ord('a')) % 26 + ord('A'))
            key += letter
            i += 1
        else:
            ciphertext += letter
    return ciphertext

def Decrypt(ciphertext, key):
    plaintext = ""
    i = 0
    for letter in ciphertext:
        if letter.islower():
            p = chr((ord(letter) - ord(key[i].lower()) + 26) % 26 + ord('a'))
            key += p
            plaintext += p
            i += 1
        elif letter.isupper():
            p = chr((ord(letter) - ord(key[i].upper()) + 26) % 26 + ord('A'))
            key += p
            plaintext += p
            i += 1
        else:
            plaintext += letter
    return plaintext

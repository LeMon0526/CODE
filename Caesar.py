'''
Caesar Cipher
Programmer: Ai Zhengpeng
Date: 2017-08-30
Function:
Encrypt(plaintext, key) -> ciphertext
Decrypt(ciphertext, key) -> plaintext
'''

def Encrypt(plaintext, key):
    ciphertext = ""
    for letter in plaintext:
        if letter.islower():
            ciphertext += chr((ord(letter) - ord('a') + key) % 26 + ord('a'))
        elif letter.isupper():
            ciphertext += chr((ord(letter) - ord('A') + key) % 26 + ord('A'))
        else:
            ciphertext += letter
    return ciphertext

def Decrypt(ciphertext, key):
    plaintext = ""
    for letter in ciphertext:
        if letter.islower():
            plaintext += chr((ord(letter) - ord('a') - key + 26) % 26 + ord('a'))
        elif letter.isupper():
            plaintext += chr((ord(letter) - ord('A') - key + 26) % 26 + ord('A'))
        else:
            plaintext += letter
    return plaintext

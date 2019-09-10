'''
Multiliteral Cipher
Programmer: Ai Zhengpeng
Date: 2017-09-01
Function:
Encrypt(plaintext, key) -> ciphertext
Decrypt(ciphertext, key) -> ciphertext
Note: The key must be five different letters.
Example:

import Cipher.Multiliteral
plaintext = "hat"
key = "codes"
ciphertext = Cipher.Multiliteral.Encrypt(plaintext, key)
print(ciphertext)
print(Cipher.Multiliteral.Decrypt(ciphertext, key))

'''

def Encrypt(plaintext, key):
    ciphertext = ""
    table = "abcdefghiklmnopqrstuvwxyz"
    for letter in plaintext:
        if letter.islower():
            if letter != 'j':
                ciphertext += key[table.find(letter) // 5].lower()
                ciphertext += key[table.find(letter) % 5].lower()
            else:
                ciphertext += key[table.find('i') // 5].lower()
                ciphertext += key[table.find('i') % 5].lower()
        elif letter.isupper():
            if letter != 'J':
                ciphertext += key[table.find(letter.lower()) // 5].upper()
                ciphertext += key[table.find(letter.lower()) % 5].upper()
            else:
                ciphertext += key[table.find('i') // 5].upper()
                ciphertext += key[table.find('i') % 5].upper()
        else:
            ciphertext += letter
    return ciphertext

def Decrypt(ciphertext, key):
    plaintext = ""
    table = "abcdefghiklmnopqrstuvwxyz"
    flag = -1
    for letter in ciphertext:
        if letter.isalpha() == False:
            plaintext += letter
        elif flag == -1:
            flag += 1
            flag += (key.find(letter.lower()) * 5)
        else:
            flag += key.find(letter.lower())
            if letter.islower():
                plaintext += table[flag]
            else:
                plaintext += table[flag].upper()
            flag = -1
    return plaintext

'''
Keyword Cipher
Programmer: Ai Zhengpeng
Date: 2017-08-30
Function:
Encrypt(plaintext, key) -> ciphertext
Decrypt(ciphertext, key) -> plaintext
'''

def Encrypt(plaintext, key):
    ciphertext = ""
    table = ""
    for letter in key:
        if letter.isalpha() and table.find(letter.lower()) == -1:
            table += letter.lower()
    for i in range(26):
        if table.find(chr(i + ord('a'))) == -1:
            table += chr(i + ord('a'))
    for letter in plaintext:
        if letter.islower():
            ciphertext += table[ord(letter) - ord('a')]
        elif letter.isupper():
            ciphertext += table[ord(letter) - ord('A')].upper()
        else:
            ciphertext += letter
    return ciphertext

def Decrypt(ciphertext, key):
    plaintext = ""
    table = ""
    for letter in key:
        if letter.isalpha() and table.find(letter.lower()) == -1:
            table += letter.lower()
    for i in range(26):
        if table.find(chr(i + ord('a'))) == -1:
            table += chr(i + ord('a'))
    for letter in ciphertext:
        if letter.islower():
            plaintext += chr(table.find(letter) + ord('a'))
        elif letter.isupper():
            plaintext += chr(table.find(letter.lower()) + ord('A'))
        else:
            plaintext += letter
    return plaintext

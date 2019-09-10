#GQY/Cipher/RSA
# need download lib first
# pip install rsa
# -*- coding: utf-8 -*-

import base64
import rsa

(publickey,privatekey) = rsa.newkeys(1024)

with open('public.pem','w') as f:
    f.write(publickey.save_pkcs1().decode())

with open('private.pem','w') as f:
    f.write(privatekey.save_pkcs1().decode())

with open('public.pem','r') as f:
    pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

with open('private.pem','r') as f:
    prikey = rsa.PrivateKey.load_pkcs1(f.read().encode())

#message = "Hello World!"

#ciphertext = rsa.encrypt(message.encode(),pubkey)

#plaintext = rsa.decrypt(ciphertext,prikey).decode() # the plaintext is bytes

#print (plaintext)

def Encrypt(plaintext):
    ciphertext = base64.b64encode(rsa.encrypt(plaintext.encode(), pubkey)).decode()
    return ciphertext

def Decrypt(ciphertext):
    plaintext = rsa.decrypt(base64.b64decode(ciphertext.encode()), prikey).decode()
    return plaintext
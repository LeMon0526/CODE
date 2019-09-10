#GQY/ECC/9.3
# -*- coding: UTF-8 -*- 
#y^2 = x^3 + a*x + b (mod p)
#public key that we got from google
# pip install sympy
# pip install numpy

# SM2 standard paramater

p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
G = [0,0]
G[0] = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
G[1] = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0

import sys
import sympy
import math
import numpy as np
import numpy.linalg as linalg
import random
import GlobalWindow

# C = {rG,Pm+rPa} Pa=kG
# creat 2 random num r,k

r = random.randint(100,1000)
k = random.randint(100,1000) # the k is private key

#ciphertext = ""

def ECC_Decrypt(C1,C2,add):
    # print ("Finishing Encrypt")
    C1[0] = int(int(C1[0])/r)
    C1[1] = int(int(C1[1])/r)
    tmp = G
    for i in range(k):
        tmp = Plus(tmp,G)

    tmp[0] = int(tmp[0])
    tmp[0] = r*(tmp[0])

    P = [0,0]
    P[0] = int(C2[0]) - tmp[0]
    # P[1] = C2[1] - tmp[1]
    #P = C2 - tmp # P is Pm

    Mx = P[0] - add
    GlobalWindow.result += chr(Mx)
    # print(chr(Mx))
    return GlobalWindow.result

def ECC_Encrypt(message,index):
    x = ord(message[index]) # char to int
    # C1 = C2 = Pa = Pm = [0,0]
    C1 = [0,0]
    C2 = [0,0]
    Pa = [0,0]
    Pm = [0,0]
    P = Get_P(x,0) # P(x,Py,k) k is the add num
    Pm[0] = P[0] + P[2] # Pm(x) x + k
    Pm[1] = P[1] # Pm(y)
    tmp = G
    for i in range(k): # k is global in the ECC
        tmp = Plus (tmp,G)
    # Pa = tmp
    Pa[0] = int(tmp[0])
    Pa[1] = int(tmp[1])
    # C1 = r*G
    C1[0] = r*G[0]
    C1[1] = r*G[1]
    # C2 = Pm + r*Pa
    C2[0] = Pm[0] + r*Pa[0]
    C2[1] = Pm[1] + r*Pa[1]
    return (C1,C2,P[2])


def y_square(x):
    return x**3 + a*x + b # mod p

def Plus(p1,p2): #p(x,y)
    p1[0] = int(p1[0])
    p1[1] = int(p1[1])
    p2[0] = int(p2[0])
    p2[1] = int(p2[1])
    if (p1[0] == 0)and(p1[1] == 0):
        return p2
    if (p2[0] == 0)and(p2[1] == 0):
        return p1
    if (p1[1] == -p2[1])and(p1[0] == p2[0]):
        return [0,0]
    if (p1[0] == p2[0])or(p1[1] == p2[1]):
        s = (3*p1[0]*p1[0] - p)/(2*p2[1])
        x = s - 2*p1[0]
        x = x%p
        y = p1[1] + s*(x-p1[0])
        y = y%p
        y = -y
        return [x,y]
    if (p1[0] != p2[0]):
        s = (p1[1] - p2[1])/(p1[0] - p2[0])
        x = s - p1[0] - p2[0]
        x = x%p
        y = p1[0] + s*(x - p1[0])
        y = y%p
        y = -y
        return [x,y]


def gcd(a,b):

    if b==0 :
        return a
    else:
        return gcd(b,a%b)


def fast_pow(a1, b1, p):
    """
    Return a to the power of b (mod p)
    """
    ans = 1
    while b1 :
        if int(b1)&1 :
            ans = ans*a1
            ans = ans % p
        b1>>=1
        a1 = a1*a1
        a1 = a1%p
    if ans < 0:
        ans = ans + p
    return ans


def Get_P(x,k): # the x come in is initial(k is the add num)
    # print ("Come into Get_x")
    while (1):
        y_2 = y_square(x+k)
        y_2 = y_2%p
        if (gcd(y_2,p) != 1):
            print ('Data is error')
            break
        if fast_pow(y_2, int(((p-1)/2)), p) != 1:
            k = k+1
            if k >= r:
                Py = Get_Py(y_2)
                return (x,Py,k)
            
            continue

        if fast_pow(y_2, int(((p-1)/2)), p) == 1:# we get the result
            # print ("we get k")
            Py = Get_Py(y_2)
            return (x,Py,k)


def Get_Py(p1):
#    print ("Come into cycle")
     result = int(math.sqrt(p1))%p
     
     return result    
 #    print ("Can not find the y")

def Encrypt(message):
    GlobalWindow.str_len = len(message)
    for i in range(len(message)):
        (M1,M2,add) = ECC_Encrypt(message,i)
        GlobalWindow.C1x.append(M1[0])
        GlobalWindow.C1y.append(M1[1])
        GlobalWindow.C2x.append(M2[0])
        GlobalWindow.C2y.append(M2[1])
        GlobalWindow.Add.append(add)
    for e in (GlobalWindow.C1x):
        e = str(e)
    for e in (GlobalWindow.C1y):
        e = str(e)
    for e in (GlobalWindow.C2x):
        e = str(e)
    for e in (GlobalWindow.C2y):
        e = str(e)


# input the ciphertext to get plaintext
def Decrypt_Point(P):
    # The P is a string includes space which divides 
    # to 5 points to decrypt (you should write correct points first)
    P = P.spilt()
    M1 = [int(P[0]),int(P[1])]
    M2 = [int(P[2]),int(P[3])]
    add = int(P[4])
    ECC_Decrypt(M1,M2,add)


        
def Decrypt():
    for e in (GlobalWindow.C1x):
        e = int(e)
    for e in (GlobalWindow.C1y):
        e = int(e)
    for e in (GlobalWindow.C2x):
        e = int(e)
    for e in (GlobalWindow.C2y):
        e = int(e)
    for i in range(GlobalWindow.str_len):
        M1 = [GlobalWindow.C1x[i],GlobalWindow.C1y[i]]
        M2 = [GlobalWindow.C2x[i],GlobalWindow.C2y[i]]
        add = GlobalWindow.Add[i]
        ECC_Decrypt(M1,M2,add)


def Enc_Dec(message):
    for i in range(len(message)):
        (M1,M2,add) = ECC_Encrypt(message,i)
        GlobalWindow.C1x.append(M1[0])
        GlobalWindow.C1y.append(M1[1])
        GlobalWindow.C2x.append(M2[0])
        GlobalWindow.C2y.append(M2[1])
        ECC_Decrypt(M1,M2,add)

def printCiphertext():
    ciphertext = ''
    for i in range(len(GlobalWindow.C1x)):
        ciphertext = ciphertext + str(GlobalWindow.C1x[i]) + ','
    for i in range(len(GlobalWindow.C1y)):
        ciphertext = ciphertext + str(GlobalWindow.C1y[i]) + ','
    for i in range(len(GlobalWindow.C2x)):
        ciphertext = ciphertext + str(GlobalWindow.C2x[i]) + ','
    for i in range(len(GlobalWindow.C2y)):
        ciphertext = ciphertext + str(GlobalWindow.C2y[i]) + ','
    return ciphertext

#print(ECC('HELLO'))

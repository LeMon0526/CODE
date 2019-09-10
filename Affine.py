'''-----------------------------------------------------------------------
文件名称：		Affine
文件描述：		实现Affine密码的加解密编写
操作系统：		win10
调试软件名称：  DeBug
编译环境：		VS2015
最后修改：		2017/8/30   <李远志>
函数注意项：    当遇到了非26个字母的其他字符，密文将保留这些字符
-------------------------------------------------------------------------'''

#--------------------------------------------模块引入------------------------------------------#
import fractions
import sys

#--------------------------------------------函数定义------------------------------------------#

'''-----------------------------------------------------------------------------------
函数定义	：    加密Affine密码
函数参数	：    plaintext(string)为明文,a,b取值范围[0,25],a与26互素
函数返回值  ：    加密后结果(string)
--------------------------------------------------------------------------------------'''
def Encrypt(plainText,key): #key = "a b"
    cipherText = ""

    i = 0
    for i in range(len(key)):
        if(key[i]==' '):
            break
        i += 1
    a = int(key[:i])
    b = int(key[i+1:])
    #判断a与b是否符合输入规则
    if IfPass(a,b) == False:
        sys.exit()
    else:
        for letter in plainText:
            if ord(letter) >= 97 and ord(letter) <= 122 :  #保留空格，标点符号等
                ordPaint    = ord(letter) - ord('a')
                ordCipher   = (ordPaint * a + b) % 26
                cipherText += chr(ordCipher + ord('a'))
            elif (ord(letter) >= 65 and ord(letter) <= 90):
                ordPaint    = ord(letter) - ord('A')
                ordCipher   = (ordPaint * a + b) % 26
                cipherText += chr(ordCipher + ord('A'))
            else:
                cipherText += letter
        return cipherText

'''-----------------------------------------------------------------------------------
函数定义	：    解密Affine密码
函数参数	：    ciphertext(string)为明文,a,b取值范围[0,25],a与26互素
函数返回值  ：    解密后结果(string)
--------------------------------------------------------------------------------------'''
def Decrypt(cipherText,key):
    plainText = ""

    i = 0
    for i in range(len(key)):
        if(key[i]==' '):
            break
        i += 1
    a = int(key[:i])
    b = int(key[i+1:])
    #判断a与b是否符合输入规则
    if IfPass(a,b) == False:
        sys.exit()
    else:
        for letter in cipherText:
            if ord(letter) >= 97 and ord(letter) <= 122:  #保留空格，标点符号等
                ordCipher   = ord(letter) - ord('a')
                ordPlain    = (Euclidean(a,26) * (ordCipher - b)) % 26
                plainText  += chr(ordPlain + ord('a'))
            elif (ord(letter) >= 65 and ord(letter) <= 90):
                ordPaint    = ord(letter) - ord('A')
                ordCipher   = (ordPaint * a + b) % 26
                cipherText += chr(ordCipher + ord('A'))
            else:
                plainText  += letter
        return plainText


'''-----------------------------------------------------------------------------------
函数定义	：    判断输入的a,b是否符合规则
函数参数	：    a,b取值范围[0,25],a与26互素
函数返回值  ：    True为符合规则，False为不符合
--------------------------------------------------------------------------------------'''
def IfPass(a,b):
    res = False
    if (type(a) != int) or (type(b) != int):
        print("a,b中有不为整形的数！")
    elif a>25 or a<0 or b>25 or b<0:
        print("a,b中有不在0到25之间的数！")
    elif fractions.gcd(a,26) != 1:
        print("a的值输入有误(不与26互素)")
    else:
        res = True
    return res

'''-----------------------------------------------------------------------------------
函数定义	：    求e对于f的逆元
函数参数	：    e为被求逆元的对象， f为要mol的数，
函数返回值  ：    e的逆元
--------------------------------------------------------------------------------------'''
def Euclidean(e,f):

    (X1,X2,X3) = (1,0,f)
    (Y1,Y2,Y3) = (0,1,e)
    while Y3 != 1:
        if Y3 == 0 :
            print("不存在逆元!")
            sys.exit()
        Q = X3 // Y3
        (T1,T2,T3) = (X1-Q*Y1,X2-Q*Y2,X3-Q*Y3)
        (X1,X2,X3) = (Y1,Y2,Y3)
        (Y1,Y2,Y3) = (T1,T2,T3)
    return Y2

'''-----------------------------------------------------------------------
main函数测试用：

from Cipher.Affine import Encrypt
from Cipher.Affine import Decrypt
plaintext = "hello world!"
a,b = 3,1
ciphertext = Encrypt(plaintext,"3 1")
print(ciphertext)
qwe = Decrypt(ciphertext,"3 1")
print(qwe)
-----------------------------------------------------------------------'''
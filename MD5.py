import math

#定义四个常量
A = 1732584193
B = -271733879
C = -1732584194
D = 271733878

#定义abcd的四个临时变量
ATemp = 0
BTemp = 0
CTemp = 0
DTemp = 0

#定义四个计算表达式
F = lambda x,y,z:((x&y)|((~x)&z))  
G = lambda x,y,z:((x&z)|(y&(~z)))  
H = lambda x,y,z:(x^y^z)  
I = lambda x,y,z:(y^(x|(~z))) 

# k是4294967296*abs( sin(i) ）的整数部分,用于16轮计算
k = [
	0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,
	0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,0x698098d8,
	0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,
	0xa679438e,0x49b40821,0xf61e2562,0xc040b340,0x265e5a51,
	0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
	0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,
	0xfcefa3f8,0x676f02d9,0x8d2a4c8a,0xfffa3942,0x8771f681,
	0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,
	0xbebfbc70,0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,
	0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,0xf4292244,
	0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,
	0xffeff47d,0x85845dd1,0x6fa87e4f,0xfe2ce6e0,0xa3014314,
	0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391 ];

#每一轮像左移位的次数
s = [ 7,12,17,22,7,12,17,22,7,12,17,22,7,
12,17,22,5,9,14,20,5,9,14,20,5,9,14,20,5,9,14,20,
4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,6,10,
15,21,6,10,15,21,6,10,15,21,6,10,15,21 ]

'''-----------------------------------------------------------------------------------
函数定义	：    加密MD5
--------------------------------------------------------------------------------------'''
def Encrypt(plainText):

    global ATemp,BTemp,CTemp,DTemp

    #初始化
    (ATemp,BTemp,CTemp,DTemp) = (A,B,C,D)

    plainText = AddPlainText(plainText)     #填充明文

    #对每512bit块做处理
    for num in range(len(plainText) // 64):
        M = [0] * 16    # M将512bit分成16个32bit

        #将这512bit分成16块存入M(M为int)
        for i in range(16):
            for j in range(4):
                plainText[4*i+3-j] = int(plainText[4*i+3-j],16)     #将16进制字符串转换为十进制整形
                M[i] = M[i] * 256 + plainText[4*i+3-j]              #将连续四个整形合并到M

        #进行4轮加密
        EncryptByFour(M)
        
    #变成十六进制且逆序
    res = ChangeHex(ATemp) + ChangeHex(BTemp) + ChangeHex(CTemp) + ChangeHex(DTemp)
    return res


'''-----------------------------------------------------------------------------------
函数定义	：    加密填充明文
--------------------------------------------------------------------------------------'''
def AddPlainText(plainText):

    length = len(plainText)
    plainText = list(map(hex,map(ord,plainText)))       #将明文转换为16进制列表
    for num in range(len(plainText)):
        plainText[num] = plainText[num][2:]             #除去前面的'0x'

    #补充100000.....000
    plainText.append('80')
    while (len(plainText)*8+64)%512 != 0:  
        plainText.append('00') 

    #加入原明文长度(左对齐)
    length = hex(length * 8)[2:]
    length = length.ljust(16,'0')
    lengthList = []
    for num in range(len(length)):
        if num % 2 == 0:
            lengthList.append(length[num] + length[num + 1])

    plainText.extend(lengthList)
    return plainText

'''-----------------------------------------------------------------------------------
函数定义	：    四轮加密
--------------------------------------------------------------------------------------'''
def EncryptByFour(M):
    global ATemp,BTemp,CTemp,DTemp,k,s
    (f,g) = (0,0)
    (a,b,c,d) = (ATemp,BTemp,CTemp,DTemp)
    for i in range(64):

        if i < 16 :
            f = F(b,c,d)
            g = i
        elif i < 32 :
            f = G(b, c, d)
            g = (5 * i + 1) % 16
        elif i < 48 :
            f = H(b, c, d)
            g = (3 * i + 5) % 16
        else:
            f = I(b, c, d)
            g = (7 * i) % 16

        tmp = d;d = c;c = b
        b = b + ShiftLeft(StayInt((a + f + k[i] + M[g])), s[i]);
        b = StayInt(b);a = tmp
        i += 1

    ATemp = StayInt(ATemp + a)
    BTemp = StayInt(BTemp + b)
    CTemp = StayInt(CTemp + c)
    DTemp = StayInt(DTemp + d)

'''-----------------------------------------------------------------------------------
函数定义	：    将int型变量左移n位
--------------------------------------------------------------------------------------'''
def ShiftLeft(num,n):
    for i in range(n):
        num = num << 1;

        #如果溢出(超过32位)
        if num >= 2**32:
            num = StayInt(num)
            num += 1

    return num

'''-----------------------------------------------------------------------------------
函数定义	：    将整形变量控制在32位
--------------------------------------------------------------------------------------'''
def StayInt(num):
    num = num & (2**32 - 1)
    return num

'''-----------------------------------------------------------------------------------
函数定义	：    变回十六进制并逆序排列
--------------------------------------------------------------------------------------'''
def ChangeHex(num):
    num = str(hex(num))[2:]

    #补全字符串至8位
    while len(num) < 8:
        num = '0' + num
    res = "0"*8
    for i in range(len(num)):
        if i % 2 == 0:
            res = res[:(6-i)] + num[i] + num[i+1] + res[(8-i):]
    return res



'''---------------------------------主函数测试用--------------------------------------------------
import sys
from Cipher.MD5 import*

a = Encrypt('hello world!')
print(a)
sys.exit()
正确结果为：fc3ff98e8c6a0d3087d515c0473f8677
------------------------------------主函数测试用--------------------------------------------------'''
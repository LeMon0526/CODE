'''-----------------------------------------------------------------------
文件名称：		PlayFair
文件描述：		实现PlayFair密码的加解密编写
操作系统：		win10
调试软件名称：  DeBug
编译环境：		VS2015
最后修改：		2017/8/31   <李远志>
-------------------------------------------------------------------------'''

#--------------------------------------------模块引入------------------------------------------#
import sys

#--------------------------------------------函数定义------------------------------------------#

'''-----------------------------------------------------------------------------------
函数定义	：    加密PlayFair密码
函数参数	：    plaintext(string)为明文,key为密钥(string)
函数返回值  ：    加密后结果(string)
--------------------------------------------------------------------------------------'''
def Encrypt(plainText,key):
    cipherText = ""
    (plainText,ifAdd) = Norm(plainText)             #规范明文格式
    keyList = makeKeyList(key)                      #生成密钥二维列表
    cipherText = Plain2Cipher(plainText,keyList)    #将明文加密成密文
    return cipherText

'''-----------------------------------------------------------------------------------
函数定义	：    加密PlayFair密码
函数参数	：    plaintext(string)为明文,key为密钥(string)
函数返回值  ：    加密后结果(string)
--------------------------------------------------------------------------------------'''
def Decrypt(cipherText,key):
    if len(cipherText) // 2 == 1:
        cipherText = cipherText + 'q'
    plainText = ""
    keyList = makeKeyList(key)                      #生成密钥二维列表
    plainText = Cipher2Plain(cipherText,keyList)    #将密文解密成明文
    plainText = DeNorm(plainText)                   #反规范明文格式
    return plainText


'''-----------------------------------------------------------------------------------
函数定义	：    规范明文格式（将可读的明文变为可加密的明文）
函数参数	：    plaintext(string)为明文
函数返回值  ：    (string)plainText :  规范后明文
                  (Bool)ifAdd       :  是否在尾部加入了'q'，是为true
规范方式    ：    当相连两个字母相同时，中间加'q'，如果这两个字母为q，则加't'
--------------------------------------------------------------------------------------'''
def Norm(plainText):

    numOfLetter = 0             #字符串中字母的数量(用于判断字母奇偶)
    while plainText.find('j') != -1:
        jLoc = plainText.find('j')
        plainText = plainText[:jLoc] + 'i' + plainText[jLoc+1:]
    #在两个相同字母之间加入'q'或't'
    i = 0
    while i < len(plainText) - 1:
        if not (plainText[i].islower() or plainText[i].isupper()):            #取到了非字母的值
            i += 1
            continue

        numOfLetter += 1               
        if plainText[i] == plainText[i+1]:                              
            if plainText[i] != 'q':
                plainText = plainText[:i+1] + 'q' + plainText[i+1:]       #插入'q'
            else:
                plainText = plainText[:i+1] + 't' + plainText[i+1:]       #插入't'
        i += 1

    if (plainText[-1].islower() or plainText[-1].isupper()):
        numOfLetter += 1
    if numOfLetter % 2 == 1:
        if plainText[-1:-1] != 'q':
            plainText = plainText + 'q'
        else:
            plainText = plainText + 't'
        return (plainText,True)

    else:
        return (plainText,False)

'''-----------------------------------------------------------------------------------
函数定义	：    反规范明文格式（将可加密的明文变为可读的明文）
函数参数	：    plaintext(string)为明文
函数返回值  ：    (string)plainText :  反规范后明文
规范方式    ：    当q两边字母相同时，删掉q。当最后一个字符为q时，删除q
--------------------------------------------------------------------------------------'''
def DeNorm(plainText):

    while plainText.find('j') != -1:
        jLoc = plainText.find('j')
        plainText = plainText[:jLoc] + 'i' + plainText[jLoc+1:]
    plainText = list(plainText)
    num = 1
    while num < len(plainText) - 1 :
        if plainText[num] == 'q' and plainText[num-1] == plainText[num+1]:
            del plainText[num]
        num += 1

    if plainText[-1] == 'q':
        del plainText[-1]
    plainText = ''.join(plainText)
    return plainText

'''-----------------------------------------------------------------------------------
函数定义	：    生成密钥二维列表
函数参数	：    key(string)密钥
函数返回值  ：    keyList(list)   :   密钥二维列表
--------------------------------------------------------------------------------------'''
def makeKeyList(key):
    keyList = [[0 for col in range(5)] for row in range(5)]     #生成5*5二维列表

    #将密钥写入二维数组
    for letter in key:
        if List2DFind(keyList,letter) == False:         #列表中无该字符
            Letter2List(keyList,letter)                 #插入字符到列表

    #补全剩余二维数组
    letter = 'a'
    while List2DFind(keyList,0) == True:

        if (letter > 'z'):                              #错误判断
            print("密钥生成错误！")
            sys.exit()

        if letter == 'j':
             letter = chr(ord(letter) + 1)
        if List2DFind(keyList,letter) == False:         #列表中无该字符
            Letter2List(keyList,letter)                 #插入字符到列表
        letter = chr(ord(letter) + 1)

    return keyList

'''-----------------------------------------------------------------------------------
函数定义	：    判断二维数组中是否存在某一字符
函数参数	：    keyList(list)    :   目标二维数组
                  letter(string)   :   目标字符
函数返回值  ：    存在：true ; 不存在：false
--------------------------------------------------------------------------------------'''
def List2DFind(keyList,letter):
    for i in range(len(keyList)):
        if letter in keyList[i]:
            return True
    return False

'''-----------------------------------------------------------------------------------
函数定义	：    将字符写入二维列表(写入位置为第一个未赋值的地方)
函数参数	：    keyList(list)    :   目标二维数组
                  letter(string)   :   目标字符
函数返回值  ：    存在：true ; 不存在：false
--------------------------------------------------------------------------------------'''
def Letter2List(keyList,letter):
    if List2DFind(keyList,0) == False:
        print("二维数组溢出!")
        sys.exit()
    for i in range(len(keyList)):
        for j in range(len(keyList[i])):
            if keyList[i][j] == 0:
                keyList[i][j] = letter
                return

'''-----------------------------------------------------------------------------------
函数定义	：    将明文加密成密文
函数参数	：    plainText(string)    :   明文
                  keyList(list)        :   密钥二维列表
函数返回值  ：    密文(string)
--------------------------------------------------------------------------------------'''
def Plain2Cipher(plainText,keyList):
    cipherText = []

    #判断是否为大写字母
    isUpper1 = False
    isUpper2 = False

    # 将密文长度与明文一致，并且初始化为0
    for i in range(len(plainText)):
        cipherText.append(0)

    exchange = 0
    for loc in range(len(plainText)):

        #如果不是字母，直接赋值给密文
        if (plainText[loc].islower() or plainText[loc].isupper()) == False:
             cipherText[loc] = plainText[loc]
             continue

         #如果是字母，依次分配给letter1和letter2
        if exchange == 0:
            if plainText[loc].isupper():
                isUpper1 = True
                letter1 = chr(ord(plainText[loc]) + 32)
            else:
                isUpper1 = False
                letter1 = plainText[loc]
            loc1 = loc
            exchange = 0.5
        elif exchange == 0.5:
            if plainText[loc].isupper():
                isUpper2 = True
                letter2 = chr(ord(plainText[loc]) + 32)
            else:
                isUpper2 = False
                letter2 = plainText[loc]
            loc2 = loc
            exchange = 1

        #将两个字母依据规则放到密文
        if exchange == 1:
            (letter1,letter2) = ChangeCipherText(letter1,letter2,keyList)
            if isUpper1 == True:
                letter1  = chr(ord(letter1) - 32)
            if isUpper2 == True:
                letter2 = chr(ord(letter2) - 32)
            cipherText[loc1] = letter1
            cipherText[loc2] = letter2
            exchange = 0;

    cipherTextstr = ''.join(cipherText)
    return cipherTextstr

'''-----------------------------------------------------------------------------------
函数定义	：    将密文解密成明文
函数参数	：    cipherText(string)   :   密文
                  keyList(list)        :   密钥二维列表
函数返回值  ：    明文(string)
--------------------------------------------------------------------------------------'''
def Cipher2Plain(cipherText,keyList):
    plainText = []

    #判断是否为大写字母
    isUpper1 = False
    isUpper2 = False

    # 将明文长度与密文一致，并且初始化为0
    for i in range(len(cipherText)):
        plainText.append(0)

    exchange = 0
    print(cipherText)
    print(type(cipherText))

    for loc in range(len(cipherText)):
        #如果不是字母，直接赋值给明文
        if (cipherText[loc].islower() or cipherText[loc].isupper()) == False:
             plainText[loc] = cipherText[loc]
             continue

         #如果是字母，依次分配给letter1和letter2
        if exchange == 0:
            if cipherText[loc].isupper():
                isUpper1 = True
                letter1 = chr(ord(cipherText[loc]) + 32)
            else:
                isUpper1 = False
                letter1 = cipherText[loc]
            loc1 = loc
            exchange = 0.5
        elif exchange == 0.5:
            if cipherText[loc].isupper():
                isUpper2 = True
                letter2 = chr(ord(cipherText[loc]) + 32)
            else:
                isUpper2 = False
                letter2 = cipherText[loc]
            loc2 = loc
            exchange = 1

        #将两个字母依据规则放到明文
        if exchange == 1:
            (letter1,letter2) = ChangePlainText(letter1,letter2,keyList)
            if isUpper1 == True:
                letter1  = chr(ord(letter1) - 32)
            if isUpper2 == True:
                letter2 = chr(ord(letter2) - 32)
            plainText[loc1] = letter1
            plainText[loc2] = letter2
            exchange = 0;

    plainTextstr = ''.join(plainText)
    return plainTextstr


'''-----------------------------------------------------------------------------------
函数定义	：    将两个字母依据规则变换成密文中的对应字母
函数参数	：    letter1,letter2(string)   :   两个字母
                  keyList(2Dlist)           ;   密钥二维数组
函数返回值  ：    密文中的对应的两个字母
--------------------------------------------------------------------------------------'''
def ChangeCipherText(letter1,letter2,keyList):

    #找到两个字母在密钥列表中的坐标
    (locx1,locy1) = FindLocOfList(letter1,keyList)
    (locx2,locy2) = FindLocOfList(letter2,keyList)

    #如果在同一行
    if locx1 == locx2:
        letter1 = keyList[locx1][(locy1 + 1) % 5]
        letter2 = keyList[locx2][(locy2 + 1) % 5]

    #如果在同一列
    elif locy1 == locy2:
        letter1 = keyList[(locx1 + 1) % 5][locy1]
        letter2 = keyList[(locx2 + 1) % 5][locy2]

    #如果既不在同一行也不再同一列
    else:
        letter1 = keyList[locx1][locy2]
        letter2 = keyList[locx2][locy1]
    return (letter1,letter2)

'''-----------------------------------------------------------------------------------
函数定义	：    将两个字母依据规则变换成明文中的对应字母
函数参数	：    letter1,letter2(string)   :   两个字母
                  keyList(2Dlist)           ;   密钥二维数组
函数返回值  ：    明文中的对应的两个字母
--------------------------------------------------------------------------------------'''
def ChangePlainText(letter1,letter2,keyList):

    #找到两个字母在密钥列表中的坐标
    (locx1,locy1) = FindLocOfList(letter1,keyList)
    (locx2,locy2) = FindLocOfList(letter2,keyList)

    #如果在同一行
    if locx1 == locx2:
        letter1 = keyList[locx1][(locy1 - 1) % 5]
        letter2 = keyList[locx2][(locy2 - 1) % 5]

    #如果在同一列
    elif locy1 == locy2:
        letter1 = keyList[(locx1 - 1) % 5][locy1]
        letter2 = keyList[(locx2 - 1) % 5][locy2]

    #如果既不在同一行也不再同一列
    else:
        letter1 = keyList[locx1][locy2]
        letter2 = keyList[locx2][locy1]
    return (letter1,letter2)

'''-----------------------------------------------------------------------------------
函数定义	：    找到一个字母在一个二维数组中的坐标
函数参数	：    letter1(string)   :   字母
                  keyList(2Dlist)   ;   二维数组
函数返回值  ：    坐标(x,y)
--------------------------------------------------------------------------------------'''
def FindLocOfList(letter,keyList):
    for i in range(len(keyList)):
        if letter in keyList[i]:
            return (i,keyList[i].index(letter))

'''-----------------------------------------主函数测试用------------------------------------------
from Cipher.PlayFair  import*
str = "hell world!"
key = "hello"
a = makeKeyList(key)
for list in a:
    print(list)
Encrypt(str,key)
---------------------------------------------主函数测试用-----------------------------------------'''

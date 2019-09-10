'''
Cipher: CA 
Principle: Stream Cipher
Types: one dimension, two dimension(moore neighbourhood)
Programmer: TSM
Date: 2017-09-01
Function:
Encrypt(plaintext, key)
Decrypt(ciphertext, key)  
'''
#加密函数
def Encrypt(plaintext, key):
    dimension = int(key[0])
    key = int(key[2:])
    if(dimension==1):
        ciphertext = OneDEncrypt(plaintext, key)
    elif(dimension==2):
        ciphertext = TwoDEncrypt(plaintext, key)
    else:
        print("!dimension 参数错误")
        return False
    return ciphertext

#一维CA加密
def OneDEncrypt(plaintext, key):
    ciphertext = ['\0',]*6400
    tempPlaintext = ['\0',]*6400
    tempCiphertext = ['\0',]*6400

    #处理原始明文字符串
    num = 0;    #有效明文字数
    for i in range(0,len(plaintext)):
        if(97<=ord(plaintext[i])<=122):  #原始明文为小写字母
            tempPlaintext[num] = plaintext[i]
            num += 1
        elif(65<=ord(plaintext[i])<=90): #原始明文为大写字母
            tempPlaintext[num] = chr(ord(plaintext[i])+32)
            num += 1

    #原始明文字母转换为0/1流
    plaintextStream = ""
    for i in range(0,num):
        tempStream = str(bin(ord(tempPlaintext[i])))
        tempStream = tempStream[2:]
        plaintextStream = plaintextStream + tempStream

    #加密规则
    key = int(key)
    ruleStr = str(bin(key))
    ruleStr = "0"*(10-len(ruleStr))+ruleStr[2:]
     
    #根据规则加密
    ciphertextStream = RuleEncrypt(ruleStr, plaintextStream)
    for i in range(0,int(len(ciphertextStream)/7)):
        tempC = ciphertextStream[i*7:(i+1)*7]
        tempC = ''.join(tempC)
        tempCiphertext[i] = chr(int(tempC,2))

    #转换密文字符串
    num = 0
    for i in range(0,len(plaintext)):
        if(97<=ord(plaintext[i])<=122):
            ciphertext[i] = tempCiphertext[num]
            num += 1
        elif(65<=ord(plaintext[i])<=90):
            ciphertext[i] = chr(ord(tempCiphertext[num])-32)
            num += 1
        else:
            ciphertext[i] = plaintext[i]
    ciphertext = ciphertext[:len(plaintext)]
    ciphertext = ''.join(ciphertext)
    return ciphertext

#规则加密函数
def RuleEncrypt(ruleStr, plaintextStream):
    ciphertextStream = ['\0',]*len(plaintextStream)
    for i in range(0,len(plaintextStream)):
        tempStream = plaintextStream[i-1] + plaintextStream[i] + plaintextStream[(i+1)%len(plaintextStream)]
        ciphertextStream[i] = ruleStr[int(tempStream,2)]
    return ciphertextStream

#二维CA加密
def TwoDEncrypt(plaintext, key):
    ciphertext = [([0] * len(plaintext)) for i in range(len(plaintext))]
    #加密规则
    ruleStr = str(bin(key))
    ruleStr = "0"*(8-len(ruleStr))+ruleStr[2:]

    X = input("请输入自定义X（0/1）:")
    for i in range(0,len(plaintext)):
        for j in range(0,len(plaintext)):
            ciphertext[i][j] = (int(ruleStr[0])*int(X))^(int(ruleStr[1])*plaintext[i][j])^(int(ruleStr[2])*plaintext[(i-1)%len(plaintext)][j])^(int(ruleStr[3])*plaintext[(i+1)%len(plaintext)][j])^(int(ruleStr[4])*plaintext[i][(j-1)%len(plaintext)])^(int(ruleStr[5])*plaintext[i][(j+1)%len(plaintext)])
    return ciphertext

#测试数据
#print(OneDEncrypt('hello','23'))
#plaintext = [[0,0,1],[0,0,0],[0,1,0]]
#print("Plaintext:")
#print(plaintext)
#ciphertext = TwoDEncrypt(plaintext,14)
#print("Ciphertext:")
#print(ciphertext)



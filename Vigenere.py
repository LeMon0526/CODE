'''
Cipher: VigenereCipher
Programmer: TSM
Date: 2017-08-30
Function:
Encrypt(plaintext, key)
Decrypt(ciphertext, key)  
'''
#加密函数
def Encrypt(plaintext, key):
    ciphertext = ['\0',]*6400
    tempPlaintext = ['\0',]*6400
    tempCiphertext = ['\0',]*6400
    #建立Vigenere Table
    table = [([0] * 26) for i in range(26)]
    for i in range(0,26):
        for j in range(0,26):
            table[i][j] = (i+j)%26
    #处理原始明文字符串
    num = 0;    #有效明文字数
    for i in range(0,len(plaintext)):
        if(97<=ord(plaintext[i])<=122):  #原始明文为小写字母
            tempPlaintext[num] = plaintext[i]
            num += 1
        elif(65<=ord(plaintext[i])<=90): #原始明文为大写字母
            tempPlaintext[num] = chr(ord(plaintext[i])+32)
            num += 1
    #有效明文字符串转换为密文
    for i in range(0,num):
        tempCiphertext[i] = chr(table[ord(key[i%len(key)])-97][ord(tempPlaintext[i])-97]+97)
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

#解密函数
def Decrypt(ciphertext, key):
    plaintext = ['\0',]*50
    tempPlaintext = ['\0',]*50
    tempCiphertext = ['\0',]*50
    #建立Vigenere Table
    table = [([0] * 26) for i in range(26)]
    for i in range(0,26):
        for j in range(0,26):
            table[i][j] = (i+j)%26
     #处理原始密文字符串
    num = 0;    #有效密文字数
    for i in range(0,len(ciphertext)):
        if(97<=ord(ciphertext[i])<=122):  #原始密文为小写字母
            tempCiphertext[num] = ciphertext[i]
            num += 1
        elif(65<=ord(ciphertext[i])<=90): #原始密文为大写字母
            tempCiphertext[num] = chr(ord(ciphertext[i])+32)
            num += 1
    #将有效密文字符串转换为明文
    for i in range(0,num):
        for j in range(0,26):
            if(table[ord(key[i%len(key)])-97][j]==ord(tempCiphertext[i])-97):
                tempPlaintext[i] = chr(j+97)
    #转换明文字符串
    num = 0
    for i in range(0,len(ciphertext)):
        if(97<=ord(ciphertext[i])<=122):
            plaintext[i] = tempPlaintext[num]
            num += 1
        elif(65<=ord(ciphertext[i])<=90):
            plaintext[i] = chr(ord(tempPlaintext[num])-32)
            num += 1
        else:
            plaintext[i] = ciphertext[i]
    plaintext = plaintext[:len(plaintext)]
    plaintext = ''.join(plaintext)
    return plaintext

#测试数据
#plaintext =Decrypt("dfaf asd","cds")
#print(plaintext)




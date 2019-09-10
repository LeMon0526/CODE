'''
DSA
Author: Dong
Date: 2017-09-04
Function:
    Sign(message, key)     :使用DSA算法产生签名.    key为元组(y,g,p,q,x)
    Verify(message, key, sig):验证签名，返回TRUE/FALSE.   key为元组(y,g,p,q)
    
    SHA1(message)          :实现SHA-1算法产生消息摘要
'''
from Crypto.Random from .import random
import Crypto
from Crypto.PublicKey import DSA
#from Crypto.Hash import SHA

class _DSAKey(object):
    def size(self):
        """Return the maximum number of bits that can be encrypted"""
        return size(self.p) - 1

    def has_private(self):
        return hasattr(self, 'x')

    def _sign(self, m, k):   # alias for _decrypt
        # SECURITY TODO - We _should_ be computing SHA1(m), but we don't because that's the API.
        if not self.has_private():
            raise TypeError("No private key")
        if not (1 < k < self.q):
            raise ValueError("k is not between 2 and q-1")
        inv_k = inverse(k, self.q)   # Compute k**-1 mod q
        r = pow(self.g, k, self.p) % self.q  # r = (g**k mod p) mod q
        s = (inv_k * (m + self.x * r)) % self.q
        return (r, s)

    def _verify(self, m, r, s):
        # SECURITY TODO - We _should_ be computing SHA1(m), but we don't because that's the API.
        if not (0 < r < self.q) or not (0 < s < self.q):
            return False
        w = inverse(s, self.q)
        u1 = (m*w) % self.q
        u2 = (r*w) % self.q
        v = (pow(self.g, u1, self.p) * pow(self.y, u2, self.p) % self.p) % self.q
        return v == r

'''
Implementation of SHA-1 algorithm
'''

def AddPlainText(plainText):

    length = len(plainText)
    plainText = list(map(hex,map(ord,plainText)))       #������ת��Ϊ16�����б�
    for num in range(len(plainText)):
        plainText[num] = plainText[num][2:]             #��ȥǰ���'0x'

    #����100000.....000
    plainText.append('80')
    while (len(plainText)*8+64)%512 != 0:  
        plainText.append('00') 

    #����ԭ���ĳ���(�����)
    length = hex(length * 8)[2:]
    length = length.rjust(16,'0')
    lengthList = []
    for num in range(len(length)):
        if num % 2 == 0:
            lengthList.append(length[num] + length[num + 1])

    plainText.extend(lengthList)
   # for i in range(56,64,4):
   #     plainText[i],plainText[i+1],plainText[i+2],plainText[i+3] = plainText[i+3],plainText[i+2],plainText[i+1],plainText[i]
    return plainText
           
def LeftRotate(num,bits):
    
    num = ((num<< bits)& 0xFFFFFFFF) | ((num) >> (32 - (bits))  )
    return num
#def leftrotate(word,bits):
 #   return ((word << bits) & 0xFFFFFFFF) | ((word) >> (32 - (bits)))


def ChangeHex(num):
    num = str(hex(num))[2:]

    #��ȫ�ַ�����8λ
    while len(num) < 8:
        num = '0' + num  
        '''
    res = "0"*8
    for i in range(len(num)):
        if i % 2 == 0:
            res = res[:(6-i)] + num[i] + num[i+1] + res[(8-i):]
    '''
    return num
               
def SHA1(message):
    h0 = 0x67452301
    h1 = 0xEFCDAB89
    h2 = 0x98BADCFE
    h3 = 0x10325476
    h4 = 0xC3D2E1F0
    h  = 0xFFFFFFFF
    plainText = AddPlainText(message)
    for num in range(len(plainText)*8//512):
        M = [0] * 16    # M��512bit�ֳ�16��32bit
        W = [0] * 80
         #����512bit�ֳ�16�����M(MΪint)
        for i in range(16):
            for j in range(4):
                plainText[64*num+4*i+j] = int(plainText[64*num + 4*i+j],16)     #��16�����ַ���ת��Ϊʮ��������
                M[i] = M[i] * 256 + plainText[64*num + 4*i+j]              #�������ĸ����κϲ���M
        for t in range(16):
                W[t] = M[t]
        for t in range (16,80):
            W[t] = LeftRotate(W[t-3]^W[t-8]^W[t-14]^W[t-16],1)
        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
       
        for j in range(0,80):
            if 0 <= j and j <= 19:
                #f =(b&c)|((~b)&d)&h
                f=d ^ (b & (c ^ d)) &h
                k = 0x5A827999
            else:
                if 20<=j and j<=39:
                    f = b^c^d&h
                    k = 0x6ED9EBA1
                else:
                    if 40 <= j and j <= 59:
                        f = (b & c) | (b & d) | (c & d)&h
                        k = 0x8F1BBCDC
                    else:
                        if 60 <= j and j <= 79:
                            f = b ^ c ^ d&h
                            k = 0xCA62C1D6
            temp = LeftRotate(a,5) + f + e + k + W[j]&h
            e = d
            d = c
            c = LeftRotate(b,30)
            b = a
            a = temp
        #Add this chunk's hash to result so far:
        h0 = h0 + a &h
        h1 = h1 + b &h
        h2 = h2 + c &h
        h3 = h3 + d &h
        h4 = h4 + e &h
    digest = ChangeHex(h0)+ ChangeHex(h1)+ ChangeHex(h2)+ ChangeHex(h3)+ ChangeHex(h4)
    return  bytes.fromhex(digest)


def generateKey(bits) :     # g,p,q,x,y
    key = DSA.generate(bits)
    return key

def constructKey(tup):    
    '''
        tup with 4 or 5 items in the following order:
        1. Public key (*y*).
        2. Sub-group generator (*g*).
        3. Modulus, finite field order (*p*).
        4. Sub-group order (*q*).
        5. Private key (*x*). Optional.
    
    '''
    key = DSA.construct(tup) 
    return key
def generateK(q) :
    k = random.StrongRandom().randint(1,q-1)
    return k


def DSA_Sign(message, key, k):
    dig = SHA1(message)
    sig = key.sign(dig, k)
    return sig 

def DSA_Verify(message, key, sig) :

    dig = SHA1(message)
    if key.verify(dig,sig):
        return True
    else:
        return False

def Sign(message, key):
    newKey = constructKey((key[0],key[1],key[2],key[3],key[4]))
    k = generateK(newKey.q)
    sig = DSA_Sign(message, newKey , k)
    str1 = str(sig[0])
    str2 = str(sig[1])
    lenstr = len(str1)
    sig_str = str1 + str2
    
    return sig_str

def Verify(message, sig, key):
    str1 = sig[0:48]
    str2 = sig[48:48*2]
    sig_int = (int(str1),int(str2))
    newKey = constructKey((key[0],key[1],key[2],key[3]))
    a = DSA_Verify(message, newKey , sig_int)
    return a

message = 'hello'
tup = (45765342401604687241128449772944733752990916022564027455790382055746256400541598197068931346511522461150446895744952616520086278134132978832871916005779068152320248430961052271558801557201924112195543438798171388390044569701508878757507381031997085133554835541412574591824296504065160930628980769756859931990,43376379741515098647985425804924879601418733263383850422598111312577593386358487364224325263259858969597179251430700334177085086070671449464377616596274930686913256608398943997830334161922260743497953638415364436460427838759705357463553196755185148779782007128058722284120672980828831033776489898432828082361,89884656743115797203643969326208167354925714643588468712364745929920911611342304769134404976757706776492814888985130026442956403037161947081508067139935189302454456558696954436501574072984903785582353419756739807211841909524953510682258535758101581242581094790592743585216465460932752002047977201839275936987,935386979343325361212450472438835748446251696899,157431932338196084657629305270682047200580952750)
sig = Sign(message,tup)

#a = Verify(message, sig, tup)
#print(a)


'''
message = 'hello'
key = generateKey(1024)
k = generateK(key.q)
sig = DSA_Sign(message, key , k)
a = DSA_Verify(message, key , sig)
print(a)
'''


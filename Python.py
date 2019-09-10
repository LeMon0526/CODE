# Python use C function dll
# UKey by C
# -*- coding: UTF-8 -*-

import os
from ctypes import *
import ctypes

a1 = 43376379741515098647985425804924879601418733263383850422598111312577593386358487364224325263259858969597179251430700334177085086070671449464377616596274930686913256608398943997830334161922260743497953638415364436460427838759705357463553196755185148779782007128058722284120672980828831033776489898432828082361
a2 = 89884656743115797203643969326208167354925714643588468712364745929920911611342304769134404976757706776492814888985130026442956403037161947081508067139935189302454456558696954436501574072984903785582353419756739807211841909524953510682258535758101581242581094790592743585216465460932752002047977201839275936987
a3 = 935386979343325361212450472438835748446251696899
a4 = 45765342401604687241128449772944733752990916022564027455790382055746256400541598197068931346511522461150446895744952616520086278134132978832871916005779068152320248430961052271558801557201924112195543438798171388390044569701508878757507381031997085133554835541412574591824296504065160930628980769756859931990

C = ctypes.CDLL("UKey.dll")
# C.Hello()

Disk_Num = C.GetNum()

# key = "This is the key"

# size = len(key)

c1 = str(a1)
c2 = str(a2)
c3 = str(a3)
c4 = str(a4)
len1 = len(c1) # 1024 bits
len2 = len(c3) # 160 bits

def Write(key,start,size):

    C.WriteDisk(key.encode('ASCII'),start,size,Disk_Num)
    # return len(key)

def Read(start,size):
    C.ReadDisk_P.restype = ctypes.c_char_p
    readbuf = C.ReadDisk_P(start,size,Disk_Num)
    result = str(readbuf)
    return result

"""
readbuf = C.ReadDisk_P(0x200,size,Disk_Num)

readbuf = ctypes.string_at(readbuf, -1)

result = readbuf.decode('utf-8')
"""
# result = result.value
# result = str(readbuf)

# str = Read(size)
# str = str[2:2 + size]

# print (str)

def Write_In():
    Write(c1,0x400,len1)
    Write(c2,0x600,len1)
    Write(c3,0x800,len2)
    Write(c4,0xA00,len1)

def Read_From():
    s1 = Read(0x400,len1)
    s2 = Read(0x600,len1)
    s3 = Read(0x800,len2)
    s4 = Read(0xA00,len1)
    s1 = s1[2:2+len1]
    s2 = s2[2:2+len1]
    s3 = s3[2:2+len2]
    s4 = s4[2:2+len1]
    result_1 = (int(s1),int(s2),int(s3),int(s4))
    result = (result_1[3],result_1[0],result_1[1],result_1[2])
    return result


# Write_In()
# key = Read_From() # key is tuple
# print (key)

"""
a1 = str(a)
size = len(a1)
# Write(a1)
str = Read(size)
str = str[2:2+size]
b = int(str)
print (b)
if a == b:
    print ("Hello World")
"""

"""
for i in range(len(result)):
    print (result[i])
"""
# print (result)
# print (readbuf)




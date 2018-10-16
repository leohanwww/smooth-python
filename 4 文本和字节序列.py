第四章 

人类使用文本，计算机使用字节序列

编码和解码
>>> s = 'café'
>>> len(s) # ➊
4 
>>> b = s.encode('utf8') # ➋ 把b编码成bytes对象
>>> b
b'caf\xc3\xa9' # ➌
>>> len(b) # ➍
5 >>> b.decode('utf8') # ➎ 把b解码成str对象
'café

bytes对象和bytearray对象
>>> c = bytes('café', encoding='utf8') #用bytes()编码
>>> c
b'caf\xc3\xa9'
>>> c[0] #bytes对象里的元素是range(256) 内的整数
99
>>> c[:2] #bytes对象的切片还是bytes对象
b'ca'
>>> c_arr = bytearray(c) #用bytearray()创建
>>> c_arr
bytearray(b'caf\xc3\xa9')
>>> c_arr[-2:] #切片还是bytearray对象
bytearray(b'\xc3\xa9')

二进制序列会显示成三种类型
ASCII范围内的字节，显示成ASCII本身，转义序列\t \n \r \\,其它的显示成字节符
如\x00是空字节
处理字符串的方法一样能处理二进制序列

编码错误处理
>>> city = 'São Paulo'
>>> city.encode('utf8')
b'S\xc3\xa3o Paulo' #正常
>>> city.encode('cp437') ➌
Traceback (most recent call last): #出现错误
File "<stdin>", line 1, in <module>
File "/.../lib/python3.4/encodings/cp437.py", line 12, in encode
return codecs.charmap_encode(input,errors,encoding_map)
UnicodeEncodeError: 'charmap' codec can't encode character '\xe3' in
position 1: character maps to <undefined>
>>> city.encode('cp437', errors='ignore') ➍
b'So Paulo'
>>> city.encode('cp437', errors='replace') ➎
b'S?o Paulo'
>>> city.encode('cp437', errors='xmlcharrefreplace') ➏
b'São Paulo'



>>> octets = b'Montr\xe9al'
>>> octets.decode('utf8')
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe9 in position 5: invalid continuation byte
>>> octets.decode('utf8', errors='replace')
'Montr�al' #无法显示的字符被替代了

处理文本文件


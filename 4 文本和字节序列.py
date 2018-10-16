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
>>> fp = open('cafe.txt', 'w', encoding='utf_8')
>>> fp ➊
<_io.TextIOWrapper name='cafe.txt' mode='w' encoding='utf_8'>
>>> fp.write('café')
4 ➋
>>> fp.close()
>>> import os
>>> os.stat('cafe.txt').st_size
5 ➌
>>> fp2 = open('cafe.txt')
>>> fp2 ➍
<_io.TextIOWrapper name='cafe.txt' mode='r' encoding='cp1252'>
>>> fp2.encoding ➎
'cp1252'
>>> fp2.read()
'cafÃ©' ➏
>>> fp3 = open('cafe.txt', encoding='utf_8') ➐
>>> fp3
<_io.TextIOWrapper name='cafe.txt' mode='r' encoding='utf_8'>
>>> fp3.read()
'café' ➑
>>> fp4 = open('cafe.txt', 'rb') ➒
>>> fp4
<_io.BufferedReader name='cafe.txt'> ➓
>>> fp4.read() ⓫
b'caf\xc3\xa9'
除非想判断编码，否则不要在二进制模式中打开文本文件；
即便如此，也应该使用 Charde
关于编码默认值的最佳建议是:自己设定编码类型

Unicode字符串规范化
>>> from unicodedata import normalize
>>> s1 = 'café' # 把"e"和重音符组合在一起
>>> s2 = 'cafe\u0301' # 分解成"e"和重音符
>>> len(s1), len(s2)
(4, 5)
>>> len(normalize('NFC', s1)), len(normalize('NFC', s2)) #NFC格式把字符和声标组合在一起
(4, 4)
>>> len(normalize('NFD', s1)), len(normalize('NFD', s2)) #NFD格式把字符和声标分开，所以有5个长度
(5, 5)
>>> normalize('NFC', s1) == normalize('NFC', s2)
True
>>> normalize('NFD', s1) == normalize('NFD', s2)
True

>>> from unicodedata import normalize, name
>>> half = '½'
>>> normalize('NFKC', half)
'1⁄2'
>>> four_squared = '4²'
>>> normalize('NFKC', four_squared) #兼容模式
'42'
>>> micro = 'μ'
>>> micro_kc = normalize('NFKC', micro)
>>> micro, micro_kc
('μ', 'μ')
>>> ord(micro), ord(micro_kc)
(181, 956)
>>> name(micro), name(micro_kc)
('MICRO SIGN', 'GREEK SMALL LETTER MU')
使用 '1/2' 替代 '½' 可以接受，微符号也确实是小写的希腊字母
'μ'，但是把 '4²' 转换成 '42' 就改变原意了。某些应用程序可以把
'4²' 保存为 '4<sup>2</sup>'，但是 normalize 函数对格式一无所
知。因此，NFKC 或 NFKD 可能会损失或曲解信息，但是可以为搜索和
索引提供便利的中间表述：用户搜索 '1 / 2 inch' 时，如果还能找到
包含 '½ inch' 的文档，那么用户会感到满意。
使用 NFKC 和 NFKD 规范化形式时要小心，而且只能在特
殊情况中使用，例如搜索和索引，而不能用于持久存储，因为这两
种转换会导致数据损失。
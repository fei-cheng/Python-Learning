import math

"""
    Requirements:
        input: A 2-gram string, letters belong to '0~9'. 10^2=100 kinds of permutaion
        output: A 2-gram string, letters belong to '0~9' and 'A~F'. (10+26)^2=1296 kinds of permutaion

    Author: fei.cheng
"""

PI = math.pi
BIAS = 3

def encryption(val):
    if len(val) != 2:
        return None
    val = int(val) + BIAS
    """ -1 <= cos_val <= 1 """
    cos_val = math.cos(val * PI / 180)
    """ 0 <= cos_val <= 1 """
    cos_val = (cos_val + 1) / 2
    """ 0 <= cos_val <= 1295 """
    cos_val = int(cos_val * 1295)
    result_st = ''
    result_lt = [cos_val/36, cos_val%36]
    for item in result_lt:
        if item < 10:
            result_st += str(item)
        else:
            result_st += chr(item - 10 + ord('A'))
    return result_st

def decryption(key):
    if len(key) != 2:
        return None
    num = 0
    for ch in key:
        if (ch >= 'A') and (ch <= 'Z'):
            ch = ord(ch) - ord('A') + 10
        else:
            ch = int(ch)
        num = num * 36 + ch
    num = (num * 2.0 / 1295) - 1
    dgr = math.acos(num) * 180 / PI
    return int(dgr) - BIAS     

def algorithm_validate():
    for val in range(100):
        val_str = str(val)
        if val < 10:
            val_str = '0' + val_str

        encode = encryption(val_str)
        decode = decryption(encode)

        if decode != val:
            print 'Error at: ', val, val_str, encode, decode

if __name__ == '__main__':
    #algorithm_validate()
    print 'Encode: 54 ---> ', encryption('54')
    print 'Decode: RS ---> ', decryption('RS')
    
        

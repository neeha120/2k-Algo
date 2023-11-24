import numpy as np
import random
from itertools import islice, cycle

# S-box Table
sbox_table = [[[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
		[0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
		[4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
		[15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],

		[[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
		[3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
		[0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
		[13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],

		[[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
		[13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
		[13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
		[1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],

		[[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
		[13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
		[10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
		[3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],

		[[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
		[14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
		[4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
		[11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],

		[[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
		[10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
		[9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
		[4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],

		[[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
		[13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
		[1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
		[6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],

		[[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
		[1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
		[7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
		[2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

def same_length(short, long):
    if len(short)<len(long):
        short = list(islice(cycle(short), len(long)))
    elif len(short)>len(long):
        short = list(islice(cycle(short), len(long)))

    return (''.join(short))

def key_stuff(key):
    key = str(key)
    if (len(key) % 6 == 1):
        key = key + (5*"1")
    elif (len(key) % 6 == 2):
        key = key + (4*"1")
    elif (len(key) % 6 == 3):
        key = key + (3*"1")
    elif (len(key) % 6 == 4):
        key = key + (2*"1")
    elif (len(key) % 6 == 5):
        key = key + (1*"1")
    
    return key

# split the key into length of key1 as summation (Expanding key2)
def parts(a, b):
    q, r = divmod(a, b)
    return [q + 1] * r + [q] * (b - r)

# convert to binary
def strToBinary(s):
	return ("".join(f"{ord(i):08b}" for i in s))

# decimal to binary
def decToBinary(n):
   return ("".join(format(n, '08b')))

def xor(a, b, n):
	ans = ""
	for i in range(n):
		if (a[i] == b[i]):
			ans += "0"
		else:
			ans += "1"
	return ans

def bin2dec(binary):
	binary1 = binary
	decimal, i, n = 0, 0, 0
	while(binary != 0):
		dec = binary % 10
		decimal = decimal + dec * pow(2, i)
		binary = binary//10
		i += 1
	return decimal

def dec2bin(num):
	res = bin(num).replace("0b", "")
	if(len(res) % 4 != 0):
		div = len(res) / 4
		div = int(div)
		counter = (4 * (div + 1)) - len(res)
		for i in range(0, counter):
			res = '0' + res
	return res

def sbox(x,k):
    sbox_str = ""
    for i in range(0, len(k)+1, 48):
        for j in range(0, 8):
            row = bin2dec(int(x[j * 6] + x[j * 6 + 5]))
            col = bin2dec(
                int(x[j * 6 + 1] + x[j * 6 + 2] + x[j * 6 + 3] + x[j * 6 + 4]))
            val = (sbox_table[j][row][col])
            sbox_str = sbox_str + dec2bin(val)

    return sbox_str

def decToStr(n):
    return chr(n)

def encrypt():
    plaintext = input("Enter plaintext: ")
    k1 = input("Enter key1: ")
    k2 = int(input("Enter numeric key: "))
    if (len(plaintext) % 4 == 3):
        plaintext = plaintext + (1*"x")
    elif (len(plaintext) % 4 == 2):
        plaintext = plaintext + (2*"x")
    elif (len(plaintext) % 4 == 1):
        plaintext = plaintext + (3*"x")
    k1 = same_length(k1,plaintext)
    k1 = key_stuff(k1)
    k3 = list(k1)
    random.Random(5).shuffle(k3)
    k3 = ''.join(k3)
    print(f"k3: {k3}")
    k4 = parts(k2,len(k3))
    k4 = ([str(i) for i in k4])
    k4 = [eval(i) for i in k4]
    k4_lst = []
    for i in range(len(k4)):
        k4_lst.append(decToBinary(k4[i]))

    k4 = ''.join(k4_lst)
    print(f"k4: {k4}")
    k3 = key_stuff(k3)
    k3_bin = (strToBinary(k3))
    k5 = xor(k3_bin,k4,len(k3_bin))
    print(f"k5: {k5}")
    plain_bin = strToBinary(plaintext)
    print(f"plain_bin: {plain_bin}")

    k6 = sbox(k5,k4)
    print(f"k6: {k6}")
    cipher = xor(k6,plain_bin,len(plain_bin))
    print(f"cipher: {cipher}")

    lst_cipher = list(cipher)
    cip_lst_bin = []
    for i in range(0, len(lst_cipher), 8):
        x = lst_cipher[i:i+8]
        x = ''.join(x)
        cip_lst_bin.append(x)

    cip_lst_dec = []
    for i in range(0, len(cip_lst_bin)):
        cip_lst_dec.append(bin2dec(int(cip_lst_bin[i])))


    print(cip_lst_dec)

    cip_lst_text = []
    for i in range(0, len(cip_lst_dec)):
        cip_lst_text.append(decToStr(cip_lst_dec[i]))

    ciphertext = ''.join(cip_lst_text)
    print(ciphertext)

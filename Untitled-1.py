
from token import RIGHTSHIFT


def binaryToDecimal(binary):    	
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * (2**i)
        binary = binary//10
        i += 1
    return decimal

binaryReg1 = "0011001010111001"


binaryReg1rs = 3*'0' + binaryReg1[0:-3]
# registers[reg1] = binaryToDecimal(int(binaryReg1rs))
print(binaryToDecimal(int(binaryReg1)))
print(binaryToDecimal(int(binaryReg1rs)))
print((binaryToDecimal(int(binaryReg1)))>>3)
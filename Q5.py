import math
cpuSize = 0
memorySpace = input("Enter the space in Memory: ")
print()
print("MENU -> Memory Addressing Types")
print("1. Bit Addressable Memory")
print("2. Nibble Addressable Memory")
print("3. Byte Addressable Memory")
print("4. Word Addressable Memory")
addressType = input("Choose the type of Addressable Memory: ")
if (addressType == '4'):
    cpuSize = int(input("Enter the number of bits of CPU: "))
print()



spacePrefix = {'K': 2**10, 'M' : 2**20, 'G': 2**30}
spaceUnit = {'B': 8, 'b': 1}

addressDecoding = {'1':1, '2':4, '3': 8, '4':cpuSize}
squares = spaceUnit[memorySpace[-1]]*spacePrefix[memorySpace[-2]]*int(memorySpace[:-2])
columns = addressDecoding[addressType]
rows = squares/columns
addressBits = math.log2(rows)

print("------------Query 1-------------")
# Query 1
def query1():
    lengthInstruction = int(input("Enter the length of one instruction in bits: "))
    lengthRegister = int(input("Enter the length of register in bits: "))
    opcodeBits = lengthInstruction-addressBits-lengthRegister
    fillerBits = lengthInstruction-2*lengthRegister-opcodeBits
    print()
    print("Minimum bits needed to represent an address in this architecture:", addressBits)
    print("Number of bits needed by opcode:", opcodeBits)
    print("Number of filler bits in Instruction Type 2:", fillerBits)
    print("Maximum no. of instructions this ISA can support:", 2**opcodeBits)
    print("Maximum no. of registers this ISA can support:", 2**lengthRegister)
    print()

query1()


# TYPE 1
print("----------Query 2--------------")
print("----------Type 1--------------")
def type1():
    cpusize_enhanced = int(input("Enter the number of bits of CPU: "))
    print()
    print("MENU -> Memory Addressing Types")
    print("1. Bit Addressable Memory")
    print("2. Nibble Addressable Memory")
    print("3. Byte Addressable Memory")
    print("4. Word Addressable Memory")
    addressType_enhanced = input("Choose the type of Addressable Memory by which the Current Addressable memory is to be enhanced with: ")
    print()

    addressDecoding_enhanced = {'1':1, '2':4, '3': 8, '4':cpusize_enhanced}

    columns_enhanced = addressDecoding_enhanced[addressType_enhanced]

    rows_enhanced = squares/columns_enhanced

    addressBits_enhanced = math.log2(rows_enhanced)
    pins = addressBits_enhanced-addressBits
    if (pins > 1):
        print("Pins required:", pins)
    else:
        print("Pins saved:", pins)
    print()

type1()

# TYPE 2
print("----------Type 2--------------")

def type2():
    cpuSize_type2 = int(input("Enter the number of bits of CPU: "))
    addressBits_type2 = int(input("Enter the number of address pins: "))
    print()
    print("MENU -> Memory Addressing Types")
    print("1. Bit Addressable Memory")
    print("2. Nibble Addressable Memory")
    print("3. Byte Addressable Memory")
    print("4. Word Addressable Memory")
    addressType_type2 = input("Choose the type of Addressable Memory: ")
    print()
    addressDecoding_type2 = {'1':1, '2':4, '3': 8, '4':cpuSize_type2}
    memorySpace_type2 = (2**addressBits_type2)*addressDecoding_type2[addressType_type2]
    memorySpace_type2 /= 8*(2**30)
    print("Size of Main Memory in bytes:",memorySpace_type2,"GB")
    print()

type2()
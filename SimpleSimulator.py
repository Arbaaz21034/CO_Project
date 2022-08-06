"""
Project Name:
    Computer Organization CSE112 - Q2: Simple Simulator

Project Authors:
    Arman Rajesh Ganjoo    (2021018)
    Chaitanya Arora        (2021033)
    Arbaaz Choudhari       (2021034)
"""
import matplotlib.pyplot as plt

DEBUG_MODE = False; # Keep this OFF when not in development or when pushing to Github

def debug(x):
    if (DEBUG_MODE):
        print(f"[DEBUG] {x}");

if (DEBUG_MODE):
    print("\nDEBUG mode is ON. Remember to turn it OFF before pushing code to Github.");





# Here I have tried to keep the same naming as Assembler to make our work easier.

# Initialising Memory
memory = ['0'*16]*256
programCounter = 0
halted = 0

# Declaring Dictionaries for decoding instructions

opcodes = {
    '10000' : 'add', '10001' : 'sub', '10011' : 'mov', '10010' : 'movimm','10100'  : 'ld',
    '10101'  : 'st', '10110' : 'mul', '10111' : 'div', '11000'  : 'rs', '11001'  : 'ls',
    '11010' : 'xor', '11011'  : 'or', '11100' : 'and', '11101' : 'not', '11110' : 'cmp', '11111' : 'jmp', 
    '01100' : 'jlt', '01101' : 'jgt', '01111'  : 'je', '01010' : 'hlt'
}
registers = { 
    '000' : 0, '001' : 0, '010' : 0, '011' : 0, '100' : 0, '101' : 0, '110' : 0, '111' : 0
}

# Flags Convention: v -> overflow flag, l -> lesser than flag, g -> greater than flag, e -> equal flag
flags = { 'v':0, 'l':0, 'g':0, 'e':0 }

instructionsList = [] # List contains all Instruction Objects derived from STDIN


# HELPER FUNCTIONS -------------------
# This function converts decimal numbers (with constraints) to 8-bit binary numbers
def decimalToBinary16bit(decimal):
    # Maximum value of decimal supported is 255. For dec=256, the binary result overflows to more than 8 bits
    binary = bin(decimal).replace('0b','')
    sixteenBitBinary = "0"*(16-len(binary)) + binary 

    return sixteenBitBinary

def decimalToBinary8bit(decimal):
    # Maximum value of decimal supported is 255. For dec=256, the binary result overflows to more than 8 bits
    binary = bin(decimal).replace('0b','')
    eightBitBinary = "0"*(8-len(binary)) + binary 

    return eightBitBinary

def decimalToSmallestBinary(decimal):
    binary = bin(decimal).replace('0b','')

    return binary


def decimalToBinary(decimal, bits):
    binary = bin(decimal).replace('0b','');
    binary = "0"*(bits - len(binary)) + binary;
    return binary;


# This function converts binary numbers to decimal equivalent.

def binaryToDecimal(binary):
	
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * (2**i)
        binary = binary//10
        i += 1
    return decimal


# Actual Implementation starts here -------------------


class Instruction:
    # Initiate the Instruction object with the assembly instruction derived from stdin
    def __init__(self, asmInstruction, lineNumber):
        self.instruction = asmInstruction
        self.lineNumber = lineNumber


    def executeInstruction(self):
        instructionName = opcodes[self.instruction[0:5]]
        
        allInstructions = ['var','add','sub','mov','movimm','ld','st','mul','div','rs','ls','xor','or',
        'and','not','cmp','jmp','jlt','jgt','je','hlt'] # list does not include labels as labels have custom names


        if (instructionName in allInstructions):
            if (instructionName in ["and","or","not"]): # Had to create a special way to execute and, or, not operations as they are keywords in python
                eval(f"self.{instructionName}Instruction()")
            else:
                eval(f"self.{instructionName}()") # Neat way of executing methods based on the variable name. Alternative would have been several lines.

    def resetFlags(self): # This function resets all the flags to zero.
        flags['v'] = 0
        flags['e'] = 0
        flags['g'] = 0
        flags['l'] = 0
        registers["111"] = 0


    # All Instruction Methods start here ------
    def add(self):
        
        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]
        registers[reg3] = registers[reg1] + registers[reg2] 
        
        if (registers[reg3] > 255): # Case of overflow
            debug("Encountered overflow in add");
            self.resetFlags()
            setFlag('v');
            registers[reg3] = registers[reg3] % (2**16)

        else:
            self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter+=1

    

    def sub(self):

        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]

        if (registers[reg2] > registers[reg1]):
            debug("Encountered underflow in sub");
            registers[reg3] = 0
            self.resetFlags()
            setFlag('v');
        else:
            registers[reg3] = registers[reg1] - registers[reg2] # Actually subtract the registers's values and dump in reg3's value
            self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter+=1



    def movimm(self):
        reg1 = self.instruction[5:8]
        immValue = binaryToDecimal(int(self.instruction[8:]))
        registers[reg1] = immValue
        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter+=1
        

    def mov(self):
        reg1 = self.instruction[10:13]
        reg2 = self.instruction[13:16]

        if (reg1 == '111'):
            registers[reg2] = binaryToDecimal(int(flags['v']+flags['l']+flags['g']+flags['e']))
            self.resetFlags()

        else:
            registers[reg2] = registers[reg1]
            self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter+=1
         

    def mul(self):
        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]
        registers[reg3] = registers[reg1] * registers[reg2]

        if (registers[reg3] > 255):
            debug("Encountered overflow in mul");
            self.resetFlags()
            setFlag('v');
            registers[reg3] = registers[reg3] % (2**16)

        else:
            self.resetFlags()
        
        global programCounter
        memoryAccessed.append(programCounter)
        programCounter+=1

    def div(self):

        reg3 = self.instruction[10:13]
        reg4 = self.instruction[13:16]

        registers['000'] = int(registers[reg3] / registers[reg4]) # quotient
        registers['001'] = registers[reg3] % registers[reg4] # remainder

        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter+=1


    def ld(self):
        
        reg1 = self.instruction[5:8]
        memAddress = binaryToDecimal(int(self.instruction[8:]))

        registers[reg1] = binaryToDecimal(int(memory[memAddress]))

        self.resetFlags()

        global programCounter
        global cycle
        memoryAccessed.append(programCounter)
        cycleNumber.append(cycle)
        memoryAccessed.append(memAddress)
        programCounter+=1


    def st(self):

        reg1 = self.instruction[5:8]
        memAddress = binaryToDecimal(int(self.instruction[8:]))

        memory[memAddress] = decimalToBinary16bit(registers[reg1])

        self.resetFlags()

        global programCounter
        global cycle
        memoryAccessed.append(programCounter)
        cycleNumber.append(cycle)
        memoryAccessed.append(memAddress)
        programCounter+=1



    def rs(self):
        reg1 = self.instruction[5:8]
        immValue = binaryToDecimal(int(self.instruction[8:]))
        binaryReg1 = decimalToBinary16bit(registers[reg1])
        binaryReg1rs = immValue*'0' + binaryReg1[0:-immValue]
        registers[reg1] = binaryToDecimal(int(binaryReg1rs))

        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter += 1


    def ls(self):

        reg1 = self.instruction[5:8]
        immValue = binaryToDecimal(int(self.instruction[8:]))
        binaryReg1 = decimalToBinary16bit(registers[reg1])
        binaryReg1ls = binaryReg1[immValue:] + immValue*'0'
        registers[reg1] = binaryToDecimal(int(binaryReg1ls))

        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter += 1




    def xor(self):

        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]

        binaryReg1 = decimalToBinary16bit(registers[reg1])
        binaryReg2 = decimalToBinary16bit(registers[reg2])
        binaryReg3 = ""
        for i in range(0,16):
            binaryReg3 += str(int(binaryReg1[i]) ^ int(binaryReg2[i]))

        registers[reg3] = binaryToDecimal(int(binaryReg3))   

        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter += 1



    def orInstruction(self):

        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]

        binaryReg1 = decimalToBinary16bit(registers[reg1])
        binaryReg2 = decimalToBinary16bit(registers[reg2])
        binaryReg3 = ""
        for i in range(0,16):
            binaryReg3 += str(int(binaryReg1[i]) or int(binaryReg2[i]))

        registers[reg3] = binaryToDecimal(int(binaryReg3))   

        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter += 1

    def andInstruction(self):

        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]

        binaryReg1 = decimalToBinary16bit(registers[reg1])
        binaryReg2 = decimalToBinary16bit(registers[reg2])
        binaryReg3 = ""
        for i in range(0,16):
            binaryReg3 += str(int(binaryReg1[i]) and int(binaryReg2[i]))

        registers[reg3] = binaryToDecimal(int(binaryReg3))   

        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter += 1

    def notInstruction(self):

        reg1 = self.instruction[10:13]
        reg2 = self.instruction[13:16]

        binaryReg1 = decimalToSmallestBinary(registers[reg1])
        binaryReg2 = ""

        for bit in binaryReg1:
            if (bit == "0"):
                binaryReg2 += "1"
            elif (bit == "1"):
                binaryReg2 += "0"

        registers[reg2] = binaryToDecimal(int(binaryReg2))

        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter += 1
    
    def cmp(self):
        
        reg1 = self.instruction[10:13]
        reg2 = self.instruction[13:16]

        self.resetFlags()

        if (registers[reg1] == registers[reg2]):
            setFlag('e');
        elif (registers[reg1] > registers[reg2]):
            setFlag('g');
        elif (registers[reg1] < registers[reg2]):
            setFlag('l');

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter += 1

    
    def jmp(self):
        debug("JMP'd to an instruction.")
        memAddress = binaryToDecimal(int(self.instruction[8:]))
        self.resetFlags()

        global programCounter
        memoryAccessed.append(programCounter)
        programCounter = memAddress

  


    def jlt(self):
        memAddress = binaryToDecimal(int(self.instruction[8:]))
        global programCounter
        memoryAccessed.append(programCounter)
        if (flags['l'] == 1):
            debug("JLT'd to an instruction.")
            programCounter = memAddress
        else: 
            programCounter+=1
        self.resetFlags()


    def jgt(self):
        memAddress = binaryToDecimal(int(self.instruction[8:]))
        global programCounter
        memoryAccessed.append(programCounter)
        if (flags['g'] == 1):
            debug("JGT'd to an instruction.")
            programCounter = memAddress
        else:
            programCounter+=1
        self.resetFlags()


    def je(self):
        memAddress = binaryToDecimal(int(self.instruction[8:]))
        global programCounter
        memoryAccessed.append(programCounter)
        if (flags['e'] == 1):
            debug("JE'd to an instruction.")
            programCounter = memAddress
        else:
            programCounter+=1   
        self.resetFlags()
    
    def hlt(self):
        global halted
        halted = 1
        self.resetFlags()
        global programCounter
        memoryAccessed.append(programCounter)

def setFlag(flagType):
    if (flagType.lower() == "e"):
        registers['111'] = 1;
        flags['e'] = 1;
    elif (flagType.lower() == "g"):
        registers["111"] = 2;
        flags['g'] = 1;
    elif (flagType.lower() == "l"):
        registers["111"] = 4;
        flags['l'] = 1;
    elif (flagType.lower() == "v"):
        registers["111"] = 8;
        flags['v'] = 1;
    else:
        debug("Weird behavior in setFlag()");




#####################################################################
##### Special Functions for handling Q4
#####################################################################

def floatToBinary(number):

    numberString = str(number);
    if '.' not in numberString:
        numberString += ".0";

    if '.' in numberString:
        wholeString, decimalString = numberString.split('.')
        whole = int(wholeString)
        wholeBinary = bin(whole).replace('0b','')

        decimal = int(decimalString)
        decimalBinary = ""
        counter = 0
        while(decimal):
            d = '0'+'.'+str(decimal)
            d = float(d)
            m = d*2

            mstring = str(m)
            decimalBinary += mstring[0]
            decimal = int(mstring[2:])
            counter += 1

            if (counter == 5):
                break
    
    return wholeBinary+'.'+ decimalBinary




def decimalToBinary(decimal, bits):
    binary = bin(decimal).replace('0b','');
    binary = "0"*(bits - len(binary)) + binary;
    return binary;


def binaryToDecimalAlt(binary):
    dec = 0;
    c = 0;
    for bit in binary[::-1]:
        a = int(bit) * (2**c);
        dec += a;
        c += 1;
    return dec;


def floatBinaryToDecimal(floatBinary):
    integerPart = 0;
    decimalPart = 0;

    decimalIndex = floatBinary.index('.');
    a = 0;
    for x in reversed(floatBinary[0:decimalIndex]):
        integerPart += int(x) * (2**a);
        a += 1;

    b = -1;
    for x in floatBinary[decimalIndex+1::]:
        decimalPart += int(x) * (2**b);
        b -= 1;

    decimal = integerPart + decimalPart;
    return decimal;


def binaryToCustomFormat(binary):
    binary = list(binary);
    exponent = 0;
    while (binary[1] != '.'):
        exponent += 1;
        decimalIndex = binary.index(".");
        tmp = str(binary[decimalIndex-1]);
        binary[decimalIndex-1] = '.';
        binary[decimalIndex] = tmp;
        
    mantissa = binary[2::];
    exponent = list(decimalToBinary(exponent,3));
    while (len(mantissa) < 5):
        mantissa.append('0');

    format = exponent + mantissa[0:5];
    return "".join(format);



def customFormatToFloat(format):
    exponentInBinary = format[0:3];
    mantissaInBinary = format[3::];

    exponent = binaryToDecimalAlt(exponentInBinary);
    fullMantissa = "1."+mantissaInBinary;
    fullMantissa = list(fullMantissa)
    
    c = 0;
    for x in range(exponent):        
        decimalIndex = fullMantissa.index(".");
        if (decimalIndex == len(fullMantissa) - 1):
            fullMantissa.append("0");
        if (c >= exponent):
            break;
        tmp = fullMantissa[decimalIndex+1];
        fullMantissa[decimalIndex+1] = '.';
        fullMantissa[decimalIndex] = tmp;
        c = c+1;

    if (fullMantissa[-1] == "."):
        fullMantissa.append("0");
    fullMantissa = "".join(fullMantissa);
    floatNumber = floatBinaryToDecimal(fullMantissa);


    return floatNumber;



def FLOAT_TO_CUSTOM_FORMAT(float):
    if (float >= 252.0):
        print("This number cannot be represented in the given 8-bit system.");
        exit()
    binary = floatToBinary(float);
    customFormat = binaryToCustomFormat(binary);
    return customFormat;
    

def CUSTOM_FORMAT_TO_FLOAT(format):
    if (len(format) != 8):
        print("The Float format must be 8 bits.");
        exit();
    float = customFormatToFloat(format);
    return float;


############################################################
############################################################
############################################################


# Main program loop which is responsible for handling the input
def main():
    i = 0
    instructionNumber = 0
    h = 0
    while 1:
        try:

            inputLine = input().strip()
            if (len(inputLine) == 0):
                continue
            memory[i] = inputLine
            i+=1

            if (not h):
                currentInstruction = Instruction(inputLine,instructionNumber) # Create an Instruction object
                instructionsList.append(currentInstruction)
                instructionNumber+=1
                if (currentInstruction.instruction[0:5] == '01010'):
                    h = 1
        
        except EOFError:
            break

def registerDump():
    for r in registers:
        reg = decimalToBinary16bit(registers[r])
        print(reg, end = " ")
    print()

def memoryDump():
    for i in range(0,256):
        print(memory[i])

cycle = 1
cycleNumber = []
memoryAccessed = []
def simExecution():
    global halted
    while(not halted):
        global cycle
        cycleNumber.append(cycle)
        global programCounter
        pc = decimalToBinary8bit(programCounter)
        instruction = instructionsList[programCounter]
        instruction.executeInstruction()
        print(pc, end = " ")
        registerDump()
        cycle+=1
    
    memoryDump()

main()
simExecution()


plt.scatter(cycleNumber, memoryAccessed)
plt.xlabel('Cycle Number')
plt.ylabel('Memory Address Accessed')
plt.show()
        
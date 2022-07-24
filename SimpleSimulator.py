"""
Project Name:
    Computer Organization CSE112 - Q2: Simple Simulator

Project Authors:
    Arman Rajesh Ganjoo    (2021018)
    Chaitanya Arora        (2021033)
    Arbaaz Choudhari       (2021034)
"""

# Here I have tried to keep the same naming as Assembler to make our work easier.

# Initialising Memory
memory = ['0'*16]*256

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



rawInstructionsList = [] # List contains all instrucions in raw text form derived from STDIN

instructionsList = [] # List contains all Instruction Objects derived from STDIN

# Actual Implementation starts here -------------------


class Instruction:
    # Initiate the Instruction object with the assembly instruction derived from stdin
    def __init__(self, asmInstruction, lineNumber):
        self.instruction = asmInstruction.split() # is a list 
        self.lineNumber = lineNumber


    def executeInstruction(self):
        instructionName = opcodes[self.instruction[0:5]]
        
        allInstructions = ['var','add','sub','mov','ld','st','mul','div','rs','ls','xor','or',
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


    # All Instruction Methods start here ------
    def add(self):
        
        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]
        registers[reg3] = registers[reg1] + registers[reg2] 
        
        if (registers[reg3] > 255): # Case of overflow
            self.resetFlags()
            flags['v'] = 1
            registers[reg3] = registers[reg3] % (2**16)

        else:
            self.resetFlags()

    

    def sub(self):

        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]

        if (registers[reg2] > registers[reg1]):
            registers[reg3] = 0
            self.resetFlags()
            flags['v'] = 1
        else:
            registers[reg3] = registers[reg1] - registers[reg2] # Actually subtract the registers's values and dump in reg3's value
            self.resetFlags()



    def movimm(self):
        reg1 = self.instruction[5:8]
        immValue = binaryToDecimal(int(self.instruction[8:]))
        registers[reg1] = immValue
        self.resetFlags()

    def mov(self):
        reg1 = self.instruction[10:13]
        reg2 = self.instruction[13:16]

        if (reg1 == '111'):
            registers[reg2] = binaryToDecimal(int(flags['v']+flags['l']+flags['g']+flags['e']))
            self.resetFlags()

        else:
            registers[reg2] = registers[reg1]
            self.resetFlags()
   
         

    def mul(self):
        reg1 = self.instruction[7:10]
        reg2 = self.instruction[10:13]
        reg3 = self.instruction[13:16]
        registers[reg3] = registers[reg1] * registers[reg2]
        if (reg3[1] > 255):
            self.resetFlags()
            flags['v'] = 1
            reg3[1] = reg3[1] % (2**16)
        else:
            self.resetFlags()

    def div(self):

        reg3 = self.instruction[10:13]
        reg4 = self.instruction[13:16]

        registers['000'] = int(registers[reg3] / registers[reg4]) # quotient
        registers['001'] = registers[reg3] % registers[reg4] # remainder

        self.resetFlags()


    def ld(self):
        pass


    def st(self):
        pass



    def rs(self):
        pass


    def ls(self):
        pass


    def xor(self):
        pass

    def orInstruction(self):
        pass

    def andInstruction(self):
        pass

    def notInstruction(self):
        pass

    
    def cmp(self):
        
        reg1 = self.instruction[10:13]
        reg2 = self.instruction[13:16]

        self.resetFlags()
        if (registers[reg1] == registers[reg2]):
            flags['e'] = 1
        elif (registers[reg1] > registers[reg2]):
            flags['g'] = 1
        elif (registers[reg1] < registers[reg2]):
            flags['l'] = 1

    def jmp(self):
        pass
  


    def jlt(self):
        pass


    def jgt(self):
        pass


    def je(self):
        pass



    
    def hlt(self):
        self.resetFlags()



# HELPER FUNCTIONS -------------------
# This function converts decimal numbers (with constraints) to 8-bit binary numbers
def convertDecimalToBinary(decimal):
    # Maximum value of decimal supported is 255. For dec=256, the binary result overflows to more than 8 bits
    binary = bin(decimal).replace('0b','')
    eightBitBinary = "0"*(8-len(binary)) + binary 

    return eightBitBinary

# This function converts binary numbers to decimal equivalent.

def binaryToDecimal(binary):
	
    decimal, i = 0, 0
    while(binary != 0):
        dec = binary % 10
        decimal = decimal + dec * (2**i)
        binary = binary//10
        i += 1
    return decimal

	



# Main program loop which is responsible for handling the input
def main():
    i = 0
    instructionNumber = 0
    halted = 0
    while 1:
        try:
            inputLine = input().strip()
            memory[i] = inputLine
            i+=1

            if (not halted):
                currentInstruction = Instruction(inputLine,instructionNumber) # Create an Instruction object
                instructionsList.append(currentInstruction)
                rawInstructionsList.append(inputLine)
               
                if (currentInstruction.instruction[0:5] == '01010'):
                    halted = 1
                    continue
        
                instructionNumber+=1
                


        except EOFError:
            break







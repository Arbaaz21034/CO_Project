"""
Project Name:
    Computer Organization CSE112 - Q1: Assembler for Midsem Evaluation 2022

Project Authors:
    Arman Rajesh Ganjoo    (2021018)
    Chaitanya Arora        (2021033)
    Arbaaz Choudhari       (2021034)

"""

# Declaring all the global variables here -------------------


opcodes = {
    'add' : '10000', 'sub' : '10001', 'mov' : '10011', 'movimm' : '10010',
    'ld'  : '10100', 'st'  : '10101', 'mul' : '10110', 'div' : '10111',
    'rs'  : '11000', 'ls'  : '11001', 'xor' : '11010', 'or'  : '11011', 
    'and' : '11100', 'not' : '11101', 'cmp' : '11110', 'jmp' : '11111', 
    'jlt' : '01100', 'jgt' : '01101', 'je'  : '01111', 'hlt' : '01010'
}

registers = {
    'r0' : ['000',0], # In the values of the keys, value[0] stands for the binary name (str) of the register and value[1] stands for its actual dynamic value (int) in the program
    'r1' : ['001',0], 'r2' : ['010',0], 'r3' : ['011',0],
    'r4' : ['100',0], 'r5' : ['101',0], 'r6' : ['110',0],
}

flags = {
    'v':0,  # overflow
    'l':0,  # less than
    'g':0,  # greater than
    'e':0   # equal
}

# For handling Special Case of C type instruction
flagsDictionary = {
    'flags': [111, 0]
}

instructionsList = [] # List contains all Instruction Objects derived from STDIN
rawInstructionsList = []; # List contains all instrucions in raw text form derived from STDIN
outputList = []  # List contains everything that needs to be outputted to STDOUT
lineCount = 0; # Keep a track of the instruction's line number (Needed for ErrorGen)


# Actual Implementation starts here -------------------


# This class forms the basis of the assembler. It contains all the error checks and everything else related to the instructions.
class Instruction:
    # Initiate the Instruction object with the assembly instruction derived from stdin
    def __init__(self, asmInstruction, lineNumber):
        self.instruction = asmInstruction.split(); # is a list 
        self.lineNumber = lineNumber;
        self.instructionLength = len(self.instruction); # Refers to the number of operands in the instruction (including instruction name)
        self.validInstruction = False; # All instructions are assumed to be invalid initally
        self.instructionType = None;
        self.isLabel = 0
        self.isVar = 0

    # This method checks the validity of the instruction name (i.e the first word of the instruction)
    def checkInstructionName(self):
        instructionName = self.instruction[0];
        validInstructionNames = ['var','add','sub','mov','ld','st','mul','div','rs','ls','xor','or',
        'and','not','cmp','jmp','jlt','jgt','je','hlt'];

        # Seeking errors
        if (instructionName not in validInstructionNames):
            if (not instructionName.endswith(":")): # Checks whether the instruction name is a label or not
                print(f"Typo in instruction name on line {self.lineNumber}");
                exit();
            

    def executeInstruction(self):
        instructionName = self.instruction[0];
        commonInstructions = ['var','add','sub','mov','ld','st','mul','div','rs','ls','xor','or',
        'and','not','cmp','jmp','jlt','jgt','je','hlt']; # list does not include labels as labels have custom names

        if (instructionName in commonInstructions):
            if (instructionName in ["and","or","not"]): # Had to create a special way to execute and, or, not operations as they are keywords in python
                eval(f"self.{instructionName}Instruction()");
            else:
                eval(f"self.{instructionName}()"); # Neat way of executing methods based on the variable name. Alternative would have been several lines.

        else: # This is a label instruction
            if (not (self.instruction[0][:-1].isalnum())):
                self.labelNameError()
            if (self.instruction[0][:-1] in dictVariables):
                self.misuseOfVariableAsLabel()

            self.isLabel = 1;
            instructionName = self.instruction[1];
            self.instruction = self.instruction[1::]; # Makes the instruction equivalent to the instruction on right of the label
            self.instructionLength = len(self.instruction);

            if (instructionName in ["and","or","not"]): 
                eval(f"self.{instructionName}Instruction()");
            else:
                eval(f"self.{instructionName}()"); 


    def resetFlags(self):
        flags['v'] = 0
        flags['e'] = 0
        flags['g'] = 0
        flags['l'] = 0
        # This function resets all the flags to zero.

    # All instruction methods

    def add(self):
        
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];

            reg3[1] = reg1[1] + reg2[1]; # Actually add the registers's values and dump in reg3's value
            if (reg3[1] > 255):
                self.resetFlags()
                flags['v'] = 1
                
                reg3[1] = 0
            else:
                self.resetFlags()

            self.validInstruction = True;
            self.instructionType = 'A';

        except KeyError: # This error is thrown when one of the register names is invalid
            self.typoError();  

    
    def sub(self):
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];


            if (reg2[1] > reg1[1]):
                reg3[1] = 0;
                self.resetFlags()
                flags['v'] = 1
    
            else:
                reg3[1] = reg1[1] - reg2[1]; # Actually subtract the registers's values and dump in reg3's value
                self.resetFlags()

            self.validInstruction = True;
            self.instructionType = 'A';


            
        except KeyError: # This error is thrown when one of the register names is invalid
            self.typoError();



    def mov(self):

        if (self.instructionLength != 3):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];

            if (self.instruction[2].startswith('$')): # Mov immediate
                immValue = int(self.instruction[2].replace('$',''));
                if (immValue > 255):
                    self.immError()
                reg1[1] = immValue

                self.resetFlags()
                self.instruction[0] = "movimm";
                self.validInstruction = True;
                self.instructionType = 'B';




            else: # Mov Register
                reg2 = registers[self.instruction[2].lower()];
                reg2[1] = reg1[1];

                self.resetFlags()
                self.validInstruction = True;
                self.instructionType = 'C';


        except KeyError:
            # complete this maybe
            if (self.instruction[1].lower() == "flags"):
                if (self.instruction[2].lower() in registers):

                    flags['v'] = convertDecimalToBinary(registers[self.instruction[2].lower()][1])[4]
                    flags['l'] = convertDecimalToBinary(registers[self.instruction[2].lower()][1])[5]
                    flags['g'] = convertDecimalToBinary(registers[self.instruction[2].lower()][1])[6]
                    flags['e'] = convertDecimalToBinary(registers[self.instruction[2].lower()][1])[7]
                    self.validInstruction = True;
                    self.instructionType = 'Special case of C';
                else:    
                    self.typoError();

            else:
                self.typoError();
            

    def mul(self):
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];

            reg3[1] = reg1[1] * reg2[1];
            if (reg3[1] > 255):
                self.resetFlags()
                flags['v'] = 1
                reg3[1] = 0
            else:
                self.resetFlags()

            self.validInstruction = True;
            self.instructionType = 'A';

        except KeyError: # This error is thrown when one of the register names is invalid
            self.typoError();

    def div(self):
        if (self.instructionLength != 3):
            self.syntaxError();
        
        try:
            reg3 = registers[self.instruction[1].lower()];
            reg4 = registers[self.instruction[2].lower()];


            # This might not be the right thing to do. FIXME: This may need a fix in future
            if (reg4[1] == 0): # Zero division error
                print(f'ZeroDivisionError on line {self.lineNumber}: You cannot divide by 0');
                exit();

            quotient = int(reg3[1] / reg4[1]);
            remainder = reg3[1] % reg4[1];

            registers['r0'][1] = quotient;
            registers['r1'][1] = remainder;

            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = 'C';
            

        except KeyError:
            self.typoError();


    def ld(self):
        if (self.instructionLength != 3):
            self.syntaxError()
        try:
            reg1 = registers[self.instruction[1].lower()]
            memAddr = self.instruction[2]
            global dictVariables
            if (memAddr not in dictVariables):
                self.varNotDeclaredError()

            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = 'D';

        except KeyError:
            self.typoError()

    def st(self):
        if (self.instructionLength != 3):
            self.syntaxError()
        try:
            reg1 = registers[self.instruction[1].lower()]
            memAddr = self.instruction[2]
            global dictVariables
            if (memAddr not in dictVariables):
                self.varNotDeclaredError()

            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = 'D';

        except KeyError:
            self.typoError()


    def rs(self):
        if (self.instructionLength != 3):
            self.syntaxError();
        
        try:
            reg1 = registers[self.instruction[1].lower()];
            immValue = int(self.instruction[2].replace('$',''));
            if (immValue > 255):
                self.immError()

            newValue = reg1[1] >> immValue;
            reg1[1] = newValue;

            self.validInstruction = True;
            self.instructionType = 'B';
            self.resetFlags()

        except KeyError:
            self.typoError();


    def ls(self):
        if (self.instructionLength != 3):
            self.syntaxError();
        
        try:
            reg1 = registers[self.instruction[1].lower()];
            immValue = int(self.instruction[2].replace('$',''));
            if (immValue > 255):
                self.immError()

            newValue = reg1[1] << immValue;
            reg1[1] = newValue;

            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = 'B';

        except KeyError:
            self.typoError();

    def xor(self):
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];

            reg3[1] = reg1[1] ^ reg2[1];

            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = 'A';
        
        except KeyError:
            self.typoError();


    # Could not name this method "or" as it's already a keyword in python. Sad. (Same for "and")
    def orInstruction(self):
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];

            reg3[1] = reg1[1] | reg2[1];
            
            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = 'A';
        
        except KeyError:
            self.typoError();



    def andInstruction(self):
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];

            reg3[1] = reg1[1] & reg2[1];

            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = 'A';
        
        except KeyError:
            self.typoError();


    # Stands for invert (not) instruction
    def notInstruction(self):
        if (self.instructionLength != 3):
            self.syntaxError();
        
        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];

            reg1[1] = ~reg2[1];

            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = "C";
            
        except KeyError:
            self.typoError();

    
    def cmp(self):
        if (self.instructionLength != 3):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];

            # these will be handled from the previous instruction no need to reset before(remove this block of comments)
            # not sure if the overflow flag will be reset here as well or not. For now, I'm not resetting it.
            # flags['v'] = 0;
            # flags['l'] = 0;
            # flags['g'] = 0;
            # flags['e'] = 0;
            self.resetFlags()
            if (reg1[1] == reg2[1]):
                flags['e'] = 1;
            elif (reg1[1] > reg2[1]):
                flags['g'] = 1;
            elif (reg1[1] < reg2[1]):
                flags['l'] = 1;
                

            self.validInstruction = True;
            self.instructionType = "C";

            # For debugging purposes. Comment the statement below when code is in production
            #print(flags);

        except KeyError:
            self.typoError();

    def jmp(self):
        if (self.instructionLength != 3):
            self.syntaxError()
        try:
            reg1 = registers[self.instruction[1].lower()]
            memAddr = self.instruction[2]
            global dictLabels
            if (memAddr not in dictLabels):
                if (memAddr in dictVariables):
                    self.misuseOfVariableAsLabel()
                else:
                    self.labelNotDeclaredError()
            
            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = "E";

        except KeyError:
            self.typoError()



    def jlt(self):
        if (self.instructionLength != 3):
            self.syntaxError()
        try:
            reg1 = registers[self.instruction[1].lower()]
            memAddr = self.instruction[2]
            global dictLabels
            if (memAddr not in dictLabels):
                if (memAddr in dictVariables):
                    self.misuseOfVariableAsLabel()
                else:
                    self.labelNotDeclaredError()

            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = "E";

        except KeyError:
            self.typoError()


    def jgt(self):
        if (self.instructionLength != 3):
            self.syntaxError()
        try:
            reg1 = registers[self.instruction[1].lower()]
            memAddr = self.instruction[2]
            global dictLabels
            if (memAddr not in dictLabels):
                if (memAddr in dictVariables):
                    self.misuseOfVariableAsLabel()
                else:
                    self.labelNotDeclaredError()
            
            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = "E";

        except KeyError:
            self.typoError()


    def je(self):
        if (self.instructionLength != 3):
            self.syntaxError()
        try:
            reg1 = registers[self.instruction[1].lower()]
            memAddr = self.instruction[2]
            global dictLabels
            if (memAddr not in dictLabels):
                if (memAddr in dictVariables):
                    self.misuseOfVariableAsLabel()
                else:
                    self.labelNotDeclaredError()
            
            self.resetFlags()
            self.validInstruction = True;
            self.instructionType = "E";

        except KeyError:
            self.typoError()

    def var(self):                          
        if (self.instructionLength != 2):
            self.syntaxError()
        
        if (not (self.instruction[1].isalnum())):
            self.varNameError()
        
        self.validInstruction = True
        self.instructionType = "V"
        self.isVar = 1

    
    def hlt(self):
        if (self.instructionLength != 1):
            self.syntaxError();
        if (rawInstructionsList[-1] != "hlt"): # Check if hlt is not used as the last instruction (which is illegal)
            self.hltError();

        self.validInstruction = True;
        self.instructionType = 'F';


    # All error methods

    def syntaxError(self):
        print(f"Syntax error on line {self.lineNumber}");
        exit();

    def hltError(self):
        print(f"hlt not used as the last instruction on line {lineCount}");
        exit();

    def typoError(self):
        print(f'Typo in register name on line {self.lineNumber}');
        exit();

    def varError(self):
        print(f"Error on line {self.lineNumber}: Variables not declared at the beginning")
        exit()

    def varNameError(self):
        print(f"Invalid variable name used on line {self.lineNumber}")
        exit()
    
    def labelNameError(self):
        print(f"Invalid label name used on line {self.lineNumber}")
        exit()
    
    def varNotDeclaredError(self):
        print(f"Use of undefined variable on line {self.lineNumber}")
        exit()

    def labelNotDeclaredError(self):
        print(f"Use of undefined label on line {self.lineNumber}")
        exit()

    def misuseOfVariableAsLabel(self):
        print(f"Misuse of Variable as Label on line {self.lineNumber}")
        exit()
    
    def immError(self):
        print(f"Illegal immediate value on line {self.lineNumber}")
        exit()

    



    # Solely for debugging purposes
    # This method is triggered when print(instructionObject) is called
    def __str__(self):
        return f'Instruction: {" ".join(self.instruction)} | Line: {self.lineNumber}';






# This function converts (i.e encodes) the instructions into machine code (which is a 16-bit binary)
def encode(instructionObject):
    instructionType = instructionObject.instructionType;
    binaryOutput = None;

    if (instructionType == 'A'): # 3 Registers type
        opcode = opcodes[instructionObject.instruction[0]];
        reg1 = registers[instructionObject.instruction[1].lower()];
        reg2 = registers[instructionObject.instruction[2].lower()];
        reg3 = registers[instructionObject.instruction[3].lower()];

        binaryOutput = f"{opcode}00{reg1[0]}{reg2[0]}{reg3[0]}"; # The zeroes in this binary output are unused/filler bits


    elif (instructionType == 'B'): # Register and Immediate type
        opcode = opcodes[instructionObject.instruction[0]];
        reg1 = registers[instructionObject.instruction[1].lower()];
        immValue = int(instructionObject.instruction[2].replace('$',''));
        immValueInBinary = convertDecimalToBinary(immValue); # Strictly 8-bits
        binaryOutput = f"{opcode}{reg1[0]}{immValueInBinary}";


    elif (instructionType == 'C'): # 2 Registers type
        opcode = opcodes[instructionObject.instruction[0]];
        reg1 = registers[instructionObject.instruction[1].lower()];
        reg2 = registers[instructionObject.instruction[2].lower()];

        binaryOutput = f"{opcode}00000{reg1[0]}{reg2[0]}";
    
    elif (instructionType == 'Special Case of C'): # mov Flags Ri
        opcode = opcodes[instructionObject.instruction[0]];
        reg1 = flagsDictionary[instructionObject.instruction[1].lower()]
        reg2 = registers[instructionObject.instruction[2].lower()];

        binaryOutput = f"{opcode}00000{reg1[0]}{reg2[0]}";


    elif (instructionType == 'D'): # Register and memoryAddress type
        opcode = opcodes[instructionObject.instruction[0]];
        reg1 = registers[instructionObject.instruction[1].lower()];
        memAddr = dictVariables[instructionObject.instruction[2]]

        binaryOutput = f"{opcode}{reg1[0]}{memAddr}";


    elif (instructionType == 'E'): # Only memoryAddress type
        opcode = opcodes[instructionObject.instruction[0]];
        memAddr = dictLabels[instructionObject.instruction[2]]

        binaryOutput = f"{opcode}000{memAddr}";


    elif (instructionType == 'F'): # Only for hlt instruction
        opcode = opcodes[instructionObject.instruction[0]];
        binaryOutput = f"{opcode}00000000000";

    elif (instructionType == 'V'): # For var instruction
        return;

    outputList.append(binaryOutput);


# This function converts decimal numbers (with constraints) to 8-bit binary numbers
def convertDecimalToBinary(decimal):
    # Maximum value of decimal supported is 255. For dec=256, the binary result overflows to more than 8 bits
    binary = bin(decimal).replace('0b','');
    eightBitBinary = "0"*(8-len(binary)) + binary; 



    return eightBitBinary;


# ---- Memory Management Operations -----
# counting variables declared.
def countVarInstructions(instruction, count):       # instruction is a string containing one line of instruction.
    if ((instruction[0]).lower() == 'var'):         # count is the current variable count which gets incremented every time a variable is declared.
        count+=1


currentVarCount = 0
# Storing Labels and Variables
dictLabels = {}             # This dictionary should contain label names given in Assembly code(key) and Memory address(value)
dictVariables = {}          # This dictionary should contain label names given in Assembly code(key) and Memory address(value)
allVarDeclared = 0;

# Main program loop which is responsible for handling the input
def main():
    while 1:
        try:
            inputLine = input().strip();
            global lineCount;
            lineCount += 1;

            # Don't add the instruction to the instructions list when the instruction is empty or a blank line
            if (len(inputLine) == 0):
                continue;
    
            global currentVarCount
            countVarInstructions(inputLine, currentVarCount)    # counting the number of variables declared.

            currentInstruction = Instruction(inputLine,lineCount); # Create an Instruction object
            instructionsList.append(currentInstruction);
            rawInstructionsList.append(inputLine);

        except EOFError:
            #print("\nAssembly input terminated. Generating your machine code.\n");
            break;


# Function which checks the instructions and tries to catch errors. If instruction is valid, it calls encode() to generate machien code (i.e 16-bit binaries)
def generateBinaries():
    if ('hlt' not in rawInstructionsList): # Check if hlt is missing
        print(f"Error: Missing hlt instruction at line {lineCount}");
        exit();

    if (rawInstructionsList.count('hlt') > 1):
        print(f"Error: Not allowed to have more than 1 hlt instruction");
        exit();

    if (len(instructionsList) > 256):
        print(f"Error: Exceeded the maximum amount (256) of instructions allowed");
        exit();

    instructionNumber = 0
    for instructionObject in instructionsList:
        if (instructionObject.instruction[0].lower() != 'var'):
            global allVarDeclared
            allVarDeclared = 1

        else:
            if (allVarDeclared):
                instructionObject.varError()

        #print(instructionObject); # DO NOT uncomment when in production
        instructionObject.checkInstructionName() # Checks the validity of the instruction's first work aka the instruction name
        instructionObject.executeInstruction();

        if (instructionObject.isVar):
            global dictVariables
            dictVariables[instructionObject.instruction[1]] = len(instructionsList) + currentVarCount
        
        if (instructionObject.isLabel):
            global dictLabels
            dictLabels[instructionObject.instruction[0][:-1]] = instructionNumber - currentVarCount   # Adds Label to the dictionary of labels

        if (instructionObject.validInstruction):
            encode(instructionObject);


# Function which generates the stored input. Only runs if the whole ASM code is error-free 
def output():
    for outputLine in outputList:
        print(outputLine);

    # For debugging purposes. In production, comment the line below.
    #print(registers);


# All basic functions are called here --------------------------

# Calling the main program function which will accept the input
main()
# Generating the binaries (if possible) and getting them ready for the STDOUT
generateBinaries()
# Calling the program which will output the 16-bit binaries line by line
output()
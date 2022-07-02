"""
Project Name:
    Computer Organization CSE112 - Q1: Assembler for Midsem Evaluation 2022


Project Authors:
    Arman Rajesh Ganjoo    (2021018)
    Chaitanya Arora        (2021033)
    Arbaaz Choudhari       (2021034)

"""

# Some notes to remember:
# Apparently, registers are 16 bits in Q1

# FIXME: Fix flag stuff (High Alert)




# Declaring all the global variables here -------------------


opcodes = {
    'add' : '10000', 'sub' : '10001', 'mov' : '10010', 'mov' : '10011',
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

    # This method checks the validity of the instruction name (i.e the first word of the instruction)
    def checkInstructionName(self):
        instructionName = self.instruction[0];
        validInstructionNames = ['var','add','sub','mov','ld','st','mul','div','rs','ls','xor','or',
        'and','not','cmp','jmp','jlt','jgt','je','hlt'];

        # Seeking errors
        if (instructionName.lower() not in validInstructionNames):
            if (not instructionName.endswith(":")): # Checks whether the instruction name is a label or not
                print(f"Typo in instruction name on line {self.lineNumber}");
                exit();


    # !!!!!!!!!!!! COMPLETE IT, CHECK THE TODO  !!!!!!!!!!!!!!!!!
    def executeInstruction(self):
        instructionName = self.instruction[0];
        commonInstructions = ['add','sub','mov','ld','st','mul','div','rs','ls','xor','or',
        'and','not','cmp','jmp','jlt','jgt','je','hlt']; # list does not include var and labels
        # TODO: Implement execution for var and labels as well

        if (instructionName.lower() in commonInstructions):
            if (instructionName.lower() in ["and","or","not"]): # Had to create a special way to execute and, or, not operations as they are keywords in python
                eval(f"self.{instructionName}Instruction()");
            else:
                eval(f"self.{instructionName}()"); # Neat way of executing methods based on the variable name. Alternative would have been several lines.





    # All instruction methods

    def add(self):
        
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];

            reg3[1] = reg1[1] + reg2[1]; # Actually add the registers's values and dump in reg3's value


            #TODO: handle overflow in addition. Figure out when it'll occur as well
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
                flags['v'] = 1;
            else:
                reg3[1] = reg1[1] - reg2[1]; # Actually subtract the registers's values and dump in reg3's value


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
                # complete later on for immediate/const values
                # TODO: Check if the immValue does not EXCEED 8 bits (or, is > 255 in dec)
                immValue = int(self.instruction[2].replace('$',''));
                reg1[1] = immValue;

                self.validInstruction = True;
                self.instructionType = 'B';




            else: # Mov Register
                reg2 = registers[self.instruction[2].lower()];
                reg2[1] = reg1[1];

                self.validInstruction = True;
                self.instructionType = 'C';


        except:
            # complete this maybe
            self.typoError();
            pass

    def mul(self):
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];


            #TODO: handle overflow in  mult. Figure out when it'll occur as well
            reg3[1] = reg1[1] * reg2[1];
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

            self.validInstruction = True;
            self.instructionType = 'C';

        except KeyError:
            self.typoError();


    # TODO: Create methods for LOAD (ld) and STORE (st)



    def rs(self):
        if (self.instructionLength != 3):
            self.syntaxError();
        
        try:
            reg1 = registers[self.instruction[1].lower()];
            immValue = int(self.instruction[2].replace('$',''));
            # TODO: Check if the imm value is 8 bit or not. Throw an error if it isn't. Do this for every function where an immediate value is used

            newValue = reg1[1] >> immValue;
            reg1[1] = newValue;
            self.validInstruction = True;
            self.instructionType = 'B';

        except KeyError:
            self.typoError();


    def ls(self):
        if (self.instructionLength != 3):
            self.syntaxError();
        
        try:
            reg1 = registers[self.instruction[1].lower()];
            immValue = int(self.instruction[2].replace('$',''));
            # TODO: Check if the imm value is 8 bit or not. Throw an error if it isn't. Do this for every function where an immediate value is used

            newValue = reg1[1] << immValue;
            reg1[1] = newValue;
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

            # not sure if the overflow flag will be reset here as well or not. For now, I'm not resetting it.
            flags['v'] = 0;
            flags['l'] = 0;
            flags['g'] = 0;
            flags['e'] = 0;

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
        pass


    def jlt(self):
        pass


    def jgt(self):
        pass


    def je(self):
        pass

    def var(self):                          
        if (self.instructionLength != 2):
            self.syntaxError()
        
        if (not (self.instruction[1].isalnum())):
            self.varNameError()
        
        self.validInstruction = True
        self.instructionType = "V"

    
    def hlt(self):
        # FIXME: Maybe the hlt keyword must be the last instruction
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
        print(f"Error on line {self.lineNumber}: Variables not declared at the begining")
        exit()

    def varNameError(self):
        print(f"Invalid variable name declared on line {self.lineNumber}")
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
        reg1 = registers[instructionObject.instruction[1]];
        reg2 = registers[instructionObject.instruction[2]];
        reg3 = registers[instructionObject.instruction[3]];

        binaryOutput = f"{opcode}00{reg1[0]}{reg2[0]}{reg3[0]}"; # The zeroes in this binary output are unused/filler bits


    elif (instructionType == 'B'): # Register and Immediate type
        opcode = opcodes[instructionObject.instruction[0]];
        reg1 = registers[instructionObject.instruction[1]];
        immValue = int(instructionObject.instruction[2].replace('$',''));
        immValueInBinary = convertDecimalToBinary(immValue); # Strictly 8-bits
        binaryOutput = f"{opcode}{reg1[0]}{immValueInBinary}";


    elif (instructionType == 'C'): # 2 Registers type
        opcode = opcodes[instructionObject.instruction[0]];
        reg1 = registers[instructionObject.instruction[1]];
        reg2 = registers[instructionObject.instruction[2]];

        binaryOutput = f"{opcode}00000{reg1[0]}{reg2[0]}";


    elif (instructionType == 'D'): # Register and memoryAddress type
        opcode = opcodes[instructionObject.instruction[0]];
        reg1 = registers[instructionObject.instruction[1]];
        memAddr = "~~~~~~~~"; # Replace the value of memAddr with the memAddr when it is implemented

        binaryOutput = f"{opcode}{reg1[0]}{memAddr}";


    elif (instructionType == 'E'): # Only memoryAddress type
        opcode = opcodes[instructionObject.instruction[0]];
        memAddr = "~~~~~~~~"; # Replace the value of memAddr with the memAddr when it is implemented

        binaryOutput = f"{opcode}000{memAddr}";


    elif (instructionType == 'F'): # Only for hlt instruction
        opcode = opcodes[instructionObject.instruction[0]];
        binaryOutput = f"{opcode}00000000000";


    elif (instructionType == None):
        print("ERROR: For some reason, the instruction type is None. Located error in encode(). Fix ASAP.");
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

# Storing Labels
dictLabels = {}             # This dictionary should contain label names given in Assembly code(key) and Memory address(value)



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

        """
        except Exception as e:
            print("An unknown error occured. The error message is given below.");
            print(e);
            break;
        """

allVarDeclared = 0
# Function which checks the instructions and tries to catch errors. If instruction is valid, it calls encode() to generate machien code (i.e 16-bit binaries)
def generateBinaries():
    if ('hlt' not in rawInstructionsList): # Check if hlt is missing
        print(f"Error: Missing hlt instruction at line {lineCount}");
        exit();

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

        if (instructionObject.validInstruction):
            encode(instructionObject);


# Function which generates the stored input. Only runs if the whole ASM code is error-free 
def output():
    for outputLine in outputList:
        print(outputLine);

    # For debugging purposes. In production, comment the line below.
    print(registers);
    





# All basic functions are called here --------------------------


# Calling the main program function which will accept the input
main()
# Generating the binaries (if possible) and getting them ready for the STDOUT
generateBinaries()
# Calling the program which will output the 16-bit binaries line by line
output()


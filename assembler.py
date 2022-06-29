"""
Project Name:
    Computer Organization CSE112 - Q1: Assembler for Midsem Evaluation 2022


Project Authors:
    Arman Rajesh Ganjoo    (2021018)
    Chaitanya Arora        (2021033)
    Arbaaz Choudhari       (2021034)

"""





import re


class Instruction:
    # Initiate the Instruction object with the assembly instruction derived from stdin
    def __init__(self, asmInstruction, lineNumber):
        self.instruction = asmInstruction.split(); # is a list 
        self.lineNumber = lineNumber;
        self.instructionLength = len(self.instruction); # Refers to the number of operands in the instruction (including instruction name)



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

        if (instructionName in commonInstructions):
            eval(f"self.{instructionName}()"); # Neat way of executing methods based on the variable name. Alternative would have been several lines.




    def add(self):
        
        if (self.instructionLength != 4):
            self.syntaxError();

        try:
            reg1 = registers[self.instruction[1].lower()];
            reg2 = registers[self.instruction[2].lower()];
            reg3 = registers[self.instruction[3].lower()];

            ## Note: continue from here

        except KeyError: # This error is thrown when one of the registers is invalid
            pass            

    
    def sub(self):
        pass


    def mov(self):
        pass
    
    
    def hlt(self):
        pass








    def syntaxError(self):
        print(f"Syntax error on line {self.lineNumber}");
        exit();



    # Solely for debugging purposes
    # This method is triggered when print(instructionObject) is called
    def __str__(self):
        return f'Instruction: {" ".join(self.instruction)} | Line: {self.lineNumber}';









opcodes = {
    'add' : '10000',
    'sub' : '10001',
    'mov' : '10010',
    'mov' : '10011',
    'ld'  : '10100',
    'st'  : '10101',
    'mul' : '10110',
    'div' : '10111',
    'rs'  : '11000', 
    'ls'  : '11001', 
    'xor' : '11010', 
    'or'  : '11011', 
    'and' : '11100', 
    'cmp' : '11110',
    'jmp' : '11111', 
    'jlt' : '01100', 
    'jgt' : '01101', 
    'je'  : '01111', 
    'hlt' : '01010'
}


registers = {
    'r0' : '000',
    'r1' : '001',
    'r2' : '010',
    'r3' : '011',
    'r4' : '100',
    'r5' : '101',
    'r6' : '110',
}

instructionsList = [] # List contains all instructions derived from STDIN
outputList = []  # List contains everything that needs to be outputted to STDOUT






lineCount = 0; # Keep a track of the instruction's line number (Needed for ErrorGen)

def main():
    while 1:
        try:
            inputLine = input().strip();
            global lineCount;
            lineCount += 1;

            # Don't add the instruction to the instructions list when the instruction is empty or a blank line
            if (len(inputLine) == 0):
                continue;

            currentInstruction = Instruction(inputLine,lineCount); # Create an Instruction object
            instructionsList.append(currentInstruction);

        except EOFError:
            print("\nAssembly input terminated. Generating your machine code.\n");
            break;

"""
        except Exception as e:
            print("An unknown error occured. The error message is given below.");
            print(e);
            break;
"""


def generateBinaries():
    for instructionObject in instructionsList:
        #print(instructionObject); # DO NOT uncomment when in production
        instructionObject.checkInstructionName() # Checks the validity of the instruction's first work aka the instruction name
        instructionObject.executeInstruction();


def output():
    for outputLine in outputList:
        pass;
    







# Calling the main program function which will accept the input
main()
# Generating the binaries (if possible) and getting them ready for the STDOUT
generateBinaries()
# Calling the program which will output the 16-bit binaries line by line
output()


"""
Project Name:
    Computer Organization CSE112 - Q1: Assembler for Midsem Evaluation 2022


Project Authors:
    Arman Rajesh Ganjoo    (2021018)
    Chaitanya Arora        (2021033)
    Arbaaz Choudhari       (2021034)

"""





class Instruction:
    # Initiate the Instruction object with the assembly instruction derived from stdin
    def __init__(self, asmInstruction, lineNumber):
        self.instruction = asmInstruction;
        self.lineNumber = lineNumber;

    # This method checks the validity of the instruction name (i.e the first word of the instruction)
    def checkInstructionName(self):
        instructionName = self.instruction.split()[0];
        validInstructionNames = ['var','add','sub','mov','ld','st','mul','div','rs','ls','xor','or',
        'and','not','cmp','jmp','jlt','jgt','je','hlt'];

        # Seeking errors
        if (instructionName.lower() not in validInstructionNames):
            if (not instructionName.endswith(":")): # Checks whether the instruction name is a label or not
                print(f"Typo in instruction name on line {self.lineNumber}");
                exit();





    # Solely for debugging purposes
    # This method is triggered when print(instructionObject) is called
    def __str__(self):
        return f"Instruction: {self.instruction} | Line: {self.lineNumber}";









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
    'R0' : '000',
    'R1' : '001',
    'R2' : '010',
    'R3' : '011',
    'R4' : '100',
    'R5' : '101',
    'R6' : '110',
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



def output():
    for outputLine in outputList:
        pass;
    







# Calling the main program function which will accept the input
main()
# Generating the binaries (if possible) and getting them ready for the STDOUT
generateBinaries()
# Calling the program which will output the 16-bit binaries line by line
output()


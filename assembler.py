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
    def __init__(self,asmInstruction):
        self.instruction = asmInstruction;

    def add(self):
        pass

    def printInstruction(self):
        print(self.instruction);






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








def main():
    while 1:
        try:
            inputLine = input().strip();

            # Don't add the instruction to the instructions list when the instruction is empty or a blank line
            if (len(inputLine) == 0):
                continue;

            instructionsList.append(inputLine);

        except EOFError:
            print("\nAssembly input terminated. Generating your machine code.\n");
            break;


        except Exception as e:
            print("An unknown error occured. The error message is given below.");
            print(e);
            break;



def output():
    
    for instructionLine in instructionsList:
        instruction = Instruction(instructionLine); # Create an Instruction Object
        instruction.printInstruction();








# Calling the main program function
main()
# Calling the program which will output binaries or errors
output()
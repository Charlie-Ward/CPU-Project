import json
import sys

# Register Setup
# print(f'Registers loading')
registers = ['00000000', '00000000', '00000000', '00000000']
IAR = 00000000  # Instruction Address Register
IR = 00000000  # Instruction Register
# print(f'Registers loaded')

# print("Register 1:", registers[0])
# print("Register 2:", registers[1])
# print("Register 3:", registers[2])
# print("Register 4:", registers[3])
# print('Instruction Address Register:', IAR)
# print('Instruction Register:', IR)

instructions_file = open('instructions.json')
instructions = json.load(instructions_file)


def error_gen(errorNumber, instructionNumber):
    print(f"ERROR AT INSTRUCTION NUMBER {instructionNumber}")
    print("Error Information:")
    match errorNumber:
        case 1:
            print('Too many bits present in instruction')
        case 2:
            print("Too many splits in instruction")
        case 3:
            print("Instructions OpCode is not supported")

    print("For documentation visit https://charlie-ward.info")  # ADD PROPER DOCUMENTATION
    sys.exit(errorNumber)


def load_instruction(instruction_number):
    global current_instruction
    current_instruction = (instructions[instruction_number])[str(instruction_number)]
    return current_instruction


def split_instruction(input_instruction):
    n = 4
    global split_instructions
    split_instructions = [(input_instruction[i:i + n]) for i in range(0, len(input_instruction), n)]
    return split_instructions


def op_code(input_instruction):
    global opCodeValue
    match input_instruction:
        case '0001':
            opCodeValue = 1
        case _:
            opCodeValue = 0
    return opCodeValue


for i in instructions:

    load_instruction(IAR)
    if len(current_instruction) != 8:
        error_gen(1, IAR)

    split_instruction(current_instruction)
    if len(split_instructions) != 2:
        error_gen(2, IAR)

    op_code(split_instructions[0])
    if opCodeValue == 0:
        error_gen(3, IAR)

    IAR += 1

instructions_file.close()

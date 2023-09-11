import json
import sys

# Register Setup
# print(f'Registers loading')
registers = ['0000', '0000', '0000', '0000']
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
            print('Not enough bits present in instruction')
        case 3:
            print("Too many splits in instruction")
        case 4:
            print("Instruction's OpCode is not supported")
        case 5:
            print("Sum of operation is too large to store")

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
            # Save Instruction Value to Register 0
            opCodeValue = 1
        case '0010':
            # Save Instruction Value to Register 1
            opCodeValue = 2
        case '0011':
            # Save Instruction Value to Register 2
            opCodeValue = 3
        case '0100':
            # Save Instruction Value to Register 3
            opCodeValue = 4
        case '0101':
            # Add two values from registers together
            opCodeValue = 5
        case '0110':
            # Subtract two values from registers together
            opCodeValue = 6
        case '0111':
            # Save sotred value of sum to register
            opCodeValue = 7
        case '1000':
            # Output register value to console
            opCodeValue = 8
        case '1111':
            # Halt program
            opCodeValue = 15
        case _:
            opCodeValue = 64
    return opCodeValue


def store_register(opCodeValue, instructionValue):
    match opCodeValue:
        case 1:
            registers[0] = instructionValue
        case 2:
            registers[1] = instructionValue
        case 3:
            registers[2] = instructionValue
        case 4:
            registers[3] = instructionValue


def add_registers(instructionValue):
    global sum_of_operation
    n = 2
    register_positions = [(instructionValue[i:i + n]) for i in range(0, len(instructionValue), n)]

    first_value = ''
    second_value = ''

    match register_positions[0]:
        case '00':
            first_value = registers[0]
        case '01':
            first_value = registers[1]
        case '10':
            first_value = registers[2]
        case '11':
            first_value = registers[3]
    match register_positions[1]:
        case '00':
            second_value = registers[0]
        case '01':
            second_value = registers[1]
        case '10':
            second_value = registers[2]
        case '11':
            second_value = registers[3]
    sum_of_operation = int(first_value) + int(second_value)
    return sum_of_operation


def subtract_registers(instructionValue):
    global sum_of_operation
    n = 2
    register_positions = [(instructionValue[i:i + n]) for i in range(0, len(instructionValue), n)]

    first_value = ''
    second_value = ''

    match register_positions[0]:
        case '00':
            first_value = registers[0]
        case '01':
            first_value = registers[1]
        case '10':
            first_value = registers[2]
        case '11':
            first_value = registers[3]
    match register_positions[1]:
        case '00':
            second_value = registers[0]
        case '01':
            second_value = registers[1]
        case '10':
            second_value = registers[2]
        case '11':
            second_value = registers[3]
    sum_of_operation = int(first_value) - int(second_value)
    return sum_of_operation


def store_sum(sum_of_operation, register_position, IAR):
    if len(str(sum_of_operation)) > 4:
        error_gen(5, IAR)
    sum_of_operation_str = str(sum_of_operation)
    if len(sum_of_operation_str) == 1:
        sum_of_operation_str = '000' + sum_of_operation_str
    elif len(sum_of_operation_str) == 2:
        sum_of_operation_str = '00' + sum_of_operation_str
    elif len(sum_of_operation_str) == 3:
        sum_of_operation_str = '0' + sum_of_operation_str
    match register_position:
        case '0000':
            registers[0] = sum_of_operation_str
        case '0001':
            registers[1] = sum_of_operation_str
        case '0010':
            registers[2] = sum_of_operation_str
        case '0011':
            registers[3] = sum_of_operation_str

def ouput_register_value(register_position):
    match register_position:
        case '0000':
            print(registers[0])
        case '0001':
            print(registers[1])
        case '0010':
            print(registers[2])
        case '0011':
            print(registers[3])

def run_cpu(IAR):
    load_instruction(IAR)
    if len(current_instruction) > 8:
        error_gen(1, IAR)
    elif len(current_instruction) < 8:
        error_gen(2, IAR)

    split_instruction(current_instruction)
    if len(split_instructions) != 2:
        error_gen(3, IAR)

    op_code(split_instructions[0])
    if opCodeValue == 0:
        error_gen(4, IAR)

    match opCodeValue:
        case 1:
            store_register(opCodeValue, split_instructions[1])
        case 2:
            store_register(opCodeValue, split_instructions[1])
        case 3:
            store_register(opCodeValue, split_instructions[1])
        case 4:
            store_register(opCodeValue, split_instructions[1])
        case 5:
            add_registers(split_instructions[1])
        case 6:
            subtract_registers(split_instructions[1])
        case 7:
            store_sum(sum_of_operation, split_instructions[1], IAR)
        case 8:
            ouput_register_value(split_instructions[1])
        case 15:
            print("PROGRAM HALT")
            print(f'Program halted at instruction number {IAR}')
            sys.exit(0)


for i in instructions:
    run_cpu(IAR)
    IAR += 1

instructions_file.close()
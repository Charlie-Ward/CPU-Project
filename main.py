import json
import sys

memory = ['0000', '0000', '0000', '0000']
cache = '0000'
IAR = 00000000  # Instruction Address Register
IR = 00000000  # Instruction Register

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
        case 6:
            print("Sum of operation is less than 0")
        case 7:
            print("Tried to store a value to large in memory")
        case 8:
            print("Cannot transfer memory values between itself")

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
            # Save Instruction Value to Memory Slot 0
            opCodeValue = 1
        case '0010':
            # Save Instruction Value to Memory Slot 1
            opCodeValue = 2
        case '0011':
            # Save Instruction Value to Memory Slot 2
            opCodeValue = 3
        case '0100':
            # Save Instruction Value to Memory Slot 3
            opCodeValue = 4
        case '0101':
            # Add two values from memory together
            opCodeValue = 5
        case '0110':
            # Subtract two values from memory together
            opCodeValue = 6
        case '0111':
            # Save stored value of sum to memory
            opCodeValue = 7
        case '1000':
            # Output memory value to console
            opCodeValue = 8
        case '1001':
            # Store a memory value into cache
            opCodeValue = 9
        case '1010':
            # Store cache into a memory slot
            opCodeValue = 10
        case '1011':
            # Print cache value
            opCodeValue = 11
        case '1100':
            # Place memory value into new piece of memory
            opCodeValue = 12
        case '1101':
            opCodeValue = 13
        case '1110':
            opCodeValue = 14
        case '1111':
            # Halt program
            opCodeValue = 15
        case _:
            opCodeValue = 16
    return opCodeValue


def store_memory(opCodeValue, instructionValue, IAR):
    if len(instructionValue) > 4:
        error_gen(7, IAR)
    match opCodeValue:
        case 1:
            memory[0] = instructionValue
        case 2:
            memory[1] = instructionValue
        case 3:
            memory[2] = instructionValue
        case 4:
            memory[3] = instructionValue


def get_values(memory_position_1, memory_position_2, memory):
    global first_value, second_value
    first_value = ''
    second_value = ''

    match memory_position_1:
        case '00':
            first_value = memory[0]
        case '01':
            first_value = memory[1]
        case '10':
            first_value = memory[2]
        case '11':
            first_value = memory[3]
    match memory_position_2:
        case '00':
            second_value = memory[0]
        case '01':
            second_value = memory[1]
        case '10':
            second_value = memory[2]
        case '11':
            second_value = memory[3]

    return first_value, second_value, memory


def add_memory(instructionValue):
    global sum_of_operation
    n = 2
    memory_positions = [(instructionValue[i:i + n]) for i in range(0, len(instructionValue), n)]
    get_values(memory_positions[0], memory_positions[1], memory)
    sum_of_operation = int(first_value) + int(second_value)
    return sum_of_operation


def subtract_memory(instructionValue, IAR):
    global sum_of_operation
    n = 2
    memory_positions = [(instructionValue[i:i + n]) for i in range(0, len(instructionValue), n)]
    get_values(memory_positions[0], memory_positions[1], memory)
    sum_of_operation = int(first_value) - int(second_value)
    if sum_of_operation < 0:
        error_gen(6, IAR)
    return sum_of_operation


def store_sum(sum_of_operation, memory_position, IAR):
    if len(str(sum_of_operation)) > 4:
        error_gen(5, IAR)
    sum_of_operation_str = str(sum_of_operation)
    if len(sum_of_operation_str) == 1:
        sum_of_operation_str = '000' + sum_of_operation_str
    elif len(sum_of_operation_str) == 2:
        sum_of_operation_str = '00' + sum_of_operation_str
    elif len(sum_of_operation_str) == 3:
        sum_of_operation_str = '0' + sum_of_operation_str
    match memory_position:
        case '0000':
            memory[0] = sum_of_operation_str
        case '0001':
            memory[1] = sum_of_operation_str
        case '0010':
            memory[2] = sum_of_operation_str
        case '0011':
            memory[3] = sum_of_operation_str


def output_memory_value(memory_position):
    match memory_position:
        case '0000':
            print(memory[0])
        case '0001':
            print(memory[1])
        case '0010':
            print(memory[2])
        case '0011':
            print(memory[3])

def store_in_cache(memory_position, cache, memory):
    match memory_position:
        case '0000':
            cache = memory[0]
        case '0001':
            cache = memory[1]
        case '0010':
            cache = memory[2]
        case '0011':
            cache = memory[3]
    return cache

def save_from_cache(memory_position, cache, memory):
    match memory_position:
        case '0000':
            memory[0] = cache
        case '0001':
            memory[1] = cache
        case '0010':
            memory[2] = cache
        case '0011':
            memory[3] = cache
    return memory

def print_cache(cache):
    print(cache)

def swap_memory(instructionValue, IAR, memory):
    n = 2
    firstposition = 0
    secondposition = 0
    memory_positions = [(instructionValue[i:i + n]) for i in range(0, len(instructionValue), n)]
    match memory_positions[0]:
        case '00':
            firstposition = 0
        case '01':
            firstposition = 1
        case '10':
            firstposition = 2
        case '11':
            firstposition = 3
    match memory_positions[1]:
        case '00':
            secondposition = 0
        case '01':
            secondposition = 1
        case '10':
            secondposition = 2
        case '11':
            secondposition = 3
    if firstposition == secondposition:
        error_gen(8, IAR)

    memory[secondposition] = memory[firstposition]

    return memory



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

    match opCodeValue:
        case 1:
            store_memory(opCodeValue, split_instructions[1], IAR)
        case 2:
            store_memory(opCodeValue, split_instructions[1], IAR)
        case 3:
            store_memory(opCodeValue, split_instructions[1], IAR)
        case 4:
            store_memory(opCodeValue, split_instructions[1], IAR)
        case 5:
            add_memory(split_instructions[1])
        case 6:
            subtract_memory(split_instructions[1], IAR)
        case 7:
            store_sum(sum_of_operation, split_instructions[1], IAR)
        case 8:
            output_memory_value(split_instructions[1])
        case 9:
            store_in_cache(split_instructions[1], cache, IAR)
        case 10:
            save_from_cache(split_instructions[1], cache, IAR)
        case 11:
            print_cache(cache)
        case 12:
            swap_memory(split_instructions[1], IAR, memory)
        case 13:
            error_gen(4, IAR)
        case 14:
            error_gen(4, IAR)
        case 15:
            print("PROGRAM HALT")
            print(f'Program halted at instruction number {IAR}')
            sys.exit(0)
        case _:
            error_gen(4, IAR)
for i in instructions:
    run_cpu(IAR)
    IAR += 1

instructions_file.close()

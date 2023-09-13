#  CPU SIM
#### This is a small CPU simulator

### How to use
##### This simulator uses an external file called instructions.json to import it's instructions. This json file must follow the rules of the simulator.
##### An instruction is built out of two parts first the opCode this is the first 4 bits of the instruction and tells the program what you want it to do. The next 4 bits are the parameters of this opCode
#### When creating an instruction you must also include a key before the instruction value.
#### When you need to input two memory values this will be done in the parameters. Use the binary value of the memory slot you want to use. For example if you want to use memory slot 3 use "11". So if you want to add memory slot 1 and 3 together your parameter would be 0111. If only one memory slot is require place the value of the slot at the end of the parameters so if you wanted slot 1 you would write "0001".
#### Beware that using opCode "1100" (Place memory slot value into a new memory slot) will erase the current value of the memory slot you are transferring into if you want to save this value first store it to cache and then store it to a new memory slot
| Memory Slot | Binary Code |
|-------------|-------------|
| 0           | 00          |
| 1           | 01          |
| 2           | 10          |
| 3           | 11          |
### Example Instruction
#### { <- Opener
#### "1" <- Key this must be the next number following your last instruction. This must start at 0
#### : <- Seperator
#### " <- Speech marks open
#### 0110 <- OpCode
#### 1101 <- Parameters
#### "} <- Closing
### So in your file the instruction would look like this
#### {"1" : "01101101"}

### Instruction Database

| OpCode | Description                                    | Parameters                                                                              |
|--------|------------------------------------------------|-----------------------------------------------------------------------------------------|
| "0001" | Store value into memory slot 1                 | Number to store in base 10 form                                                         |
| "0010" | Store value into memory slot 2                 | Number to store in base 10 form                                                         |
| "0011" | Store value into memory slot 3                 | Number to store in base 10 form                                                         |
| "0100" | Store value into memory slot 4                 | Number to store in base 10 form                                                         |
| "0101" | Add two memory slots together                  | Binary value of both the memory slots (Two bits each)                                   |
| "0110" | Subtract two memory slots from each other      | Binary value of both the memory slots (Two bits each)                                   |
| "0111" | Store value of sum to memory                   | Binary value of memory position with two zeros at the front                             |
| "1000" | Output value of a memory slot                  | Binary value of memory position with two zeros at the front                             |
| "1001" | Store a memory slot to cache                   | Binary value of memory position with two zeros at the front                             |
| "1010" | Store cache to a memory slot                   | Binary value of memory position with two zeros at the front                             |
| "1011" | Print cache value                              | N/A                                                                                     |
| "1100" | Place memory slot value into a new memory slot | Binary Value of memory slot to take from THEN binary value of memory slot to place into |
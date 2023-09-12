#  CPU SIM
#### This is a small CPU simulator

### How to use
##### This simulator uses an external file called instructions.json to import it's instructions. This json file must follow the rules of the simulator.
##### An instruction is built out of two parts first the opCode this is the first 4 bits of the instruction and tells the program what you want it to do. The next 4 bits are the parameters of this opCode
#### When creating an instruction you must also include a key before the instruction value.
#### When you need to input two memory values this will be done in the parameters. Use the binary value of the memory slot you want to use. For example if you want to use memory slot 3 use "11". So if you want to add memory slot 1 and 3 together your parameter would be 0111
### Example Instruction
#### { <- Opener
#### "1" <- Key this must be the next number following your last instruction. This must start at 0
#### : <- Seperator
#### " <- Speech marks open
#### 0110 <- OpCode
#### 1101 <- Parameters
#### "} <- Closing
### So in your file the instruction would look like this
#### {"1" : "01101101}

### Instruction Database

| OpCode | Description                    | Parameters |
|--------|--------------------------------|------------|
| "0001" | Store value into memory slot 1 |Number to store in base 10 form |
| "0010" | Store value into memory slot 2 |Number to store in base 10 form |
| "0011" | Store value into memory slot 3 |Number to store in base 10 form |
| "0100" | Store value into memory slot 4 |Number to store in base 10 form |
| "0101"| Add two memory slots together | Binary value of both the memory slots (Two bits each) |
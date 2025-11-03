# Machine Code Formats (MIPS)

## R Format Instructions

### Machine Language

* Code is converted into machine language (0s and 1s)
* Example:
  * add R8, R17, R18
  * 00000010 00110010 01000000 00100000
* Format
  * First 6 Bits is an operation code
  * Second 5 bits is rs
  * Third 5 bits is rt
  * fourth 5 bits is rd
  * fifth 5 bits is shamt
  * sixth 6 bits is funct

* Opcode (Operation Code)
  * The type of operation we are doing
  * Add
  * LW
* RS (Source 1):
  * The first input
  * The register of the first input
* RT (Source 2):
  * The second input
* RD (Destination):
  * The destination register
* Shamt
  * Shift amount (Used for shift instructions)
* Funct:
  * Function selector (Add = 32, sub = 34, etc)

* How many bits do you need to specify the register
  * 5 Bits for each register
  * There are 32 regiseters hence we need 5 bits

* Which register is 01000
  * This is register 8 which is $t0 in mips.
* What does 000000 10001 10010 01000 00000 100000 mean?
  * 000000 = R type of instruction
  * 10001 = Register 17 ($s1)
  * 10010 = Register 18
  * 01000 = Register 8
  * 00000 = we are not shifting so its 0
  * 100000 = Add
  * Register 17 + Register 18 into Register 8

### R Type Instruction

* Example:

```mips
add $t8, $t3, $zero
```

1. Convert register names to register numbers
	```mips
	add $8, $11, $8
	```

2. Assign parts to section
3. add = funct 100000
4. $8 = rd(dest) = 01000
5. $11 = rs(src1) = 01011
6. $0 = rt (src2) = 00000
7. Operation code is R type so its 000000
8. YOu don't have to memorize the codes they will be provided to you on exams

```
000000 01011 00000 01000 00000 100000
```

* Q: Under what circumstances will you use the shift
  * A shift right is essentially subtracting 6
  * Can be used to jump between registers very quicky

### I Format

* Now that we've seen an R format instruction, we will look at the i format.
* I format are all the operations that have constants (addi, li, etc)
* How can we support this in the processor?
* We have constants inside the instruction
* BUt theres a problem instructions only have 32 bits
* We store the constant data in the instruction, not the register file.
* I format does not use rd (second parameter), does not use shhmt (shifts), and does not use funct. It uses all those 16 bits for the address

* I Format:
 1. First 6 bits are for the operation
 2. 2nd 5 bits are for the first param
 3. 3rd 5 bits are for the storage location
 4. next 16 bits are for the input value
 5. That gives us 32 bits

* Example of I machine code:
  * 001000 00000 00011 0000000000000011
 1. 001000 = addi
 2. 00000 = $zero
 3. 00011 = $3 (Storage location)
 4. 0000000000000011 = 3

* Example 2: lw $3, 4($5)
  * 100011 (lw)
  * 00101 = 4($5)
  * 00000 = $3

* Example 3: sw $5, 8($3)

 1. 101011 = sw operation code
 2. 00011 = register 3 ( parameter register)
 3. 00101 = register 5 ( where its going to be stored)
 4. 0000000000001000 = Constant 8
 5. 101011 00011 00101 0000000000001000

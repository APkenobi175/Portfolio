def sumN(a):
    x = 0
    for i in a:
        x += i
    return x

# so to do this in mips assembly, we need to follow these steps:
# 1. Set up the stack frame
# 2. Initialize a sum variable to 0
# 3. Loop through the array, adding each element to the sum
# 4. Return the sum
# Here is the MIPS assembly code for the sumN function:
""" 
    .data
newline: .asciiz "\n"
prompt: .asciiz "The sum is: "
    .text
    .globl main
main:
    # Sample array and its length
    li $t0, 5              # length of the array
    la $a0, array          # load address of the array  
    jal sumN               # call sumN function
    # Print the result
    li $v0, 4              # syscall for print string
    la $a0, prompt         # load address of prompt
    syscall
    li $v0, 1              # syscall for print integer
    move $a0, $v0         # move result to $a0 for printing
    syscall
    li $v0, 4              # syscall for print string
    la $a0, newline        # load address of newline
    syscall
    li $v0, 10             # syscall for exit
    syscall
sumN:

"""
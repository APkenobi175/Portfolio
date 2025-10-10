.data
a: .word 4 # a=4
b: .word 7 # b = 7
c: .word 10 # c = 10
result: .space 4 # result


.text
.globl main

main:
	# First we need to load the data into the registers
	lw $t0, a # load a into $t0 register
	lw $t1, b # load b into $t1 register
	lw $t2, c # load c into $t2 register
	
	# Now we need to do the addition
	add $t3, $t0, $t1 # A + B = Temp $t3
	add $t3, $t2, $t3 # add the temp with $t2(c)
	sw $t3, result # now store $t3 back into memory into result
	
	
	# Now that the math is done we need to print the result
	# To do this we need to change the syscall code to code 1
	li $v0, 1 # load 1 into systcall register
	move $a0, $t3 # move result variable into $a0
	syscall # Print the result
	
	
	

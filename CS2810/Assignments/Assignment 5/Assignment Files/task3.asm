.data
	a: .word 1
	b: .word 1
	c: .word 1
	d: .word 1
	divisor: .word 4 # hard coded
	
	sum: .space 4
	average: .space 4
	
.text
.globl main


main:
	# Load words into registers
	lw $t0, a # load a
	lw $t1, b # load b
	lw $t2, c # load c
	lw $t3, d # load d 
	lw $t6, divisor # load divisor
	
	# Compute the sum $t4 = temp var/solution
	add $t4, $t0, $t1 # a + b = temp
	add $t4, $t4, $t2 # temp + c = temp 
	add $t4, $t4, $t3 # temp + d = temp
	
	# Compute the average $t5 = average
	div $t5, $t4, $t6 # average = a+b+c+d/4
	
	# store sum and average in memory
	sw $t4, sum
	sw $t5, average
	
	# exit
	li $v0, 10
	syscall 
	
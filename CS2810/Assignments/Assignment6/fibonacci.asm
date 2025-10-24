.data
userPrompt: .asciiz "Please enter a number: "
newline: .asciiz "\n"

.text
.globl main

main:
	# Print the prompt message
	li $v0, 4 # print string
	la $a0, userPrompt
	syscall
	
	# read the integer input
	li $v0, 5 # read integer
	syscall 
	move $t0, $v0 # store the user input into the $t0 register
	
	
	# Initialize the fibonacci variables
	li $t1, 0 # first num = 0
	li $t2, 1 # second num = 1
	
	# Initialize loop index
	move $t3, $zero # i = 0
	
	
loop:
	beq $t3, $t0, exit # If i >=n exit program
	
	# print current fibb number
	li $v0, 1 # print int
	move $a0, $t1
	syscall
	
	# print a new line
	li $v0, 4 # print string
	la $a0, newline
	syscall
	
	# Calculate the next fib number
	add $t4, $t1, $t2 # $t4 = $t1 + $t2
	move $t1, $t2
	move $t2, $t4 
	
	addi $t3, $t3, 1 # increment the index (i++)
	j loop # loop until done
	
	
	
exit:
	li $v0, 10 # Exit program
	syscall
	

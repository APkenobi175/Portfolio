.data 
userInput: .asciiz "Enter a number: "
newLine: .asciiz "\n"


.text
.globl main

main:
	li $v0, 4 # print string
	la $a0, userInput
	syscall
	
	
	li $v0, 5 # read int
	syscall
	move $t0, $v0
	
	li $t1, 0 # start at 0
	
	addi $t2, $t0, 1 # user input + 1 is when the loop will end
	
loop:
	beq $t1, $t2, exit # once we hit the number the user entered, stop the loop
	li $v0, 1 # print int
	move $a0, $t1
	syscall
	
	li $v0, 4 # print string
	la $a0, newLine # print a new line
	syscall
	
	
	addi $t1, $t1, 1 # i++
	j loop
	
	
exit:
	li $v0, 10
	syscall
	
	

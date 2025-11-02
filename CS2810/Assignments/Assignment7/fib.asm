.data 
.align 2
array: .space 128 #(32 words = 32*4 = 128)
prompt: .asciiz "Please Enter How Many Fibonacci Numbers You Would Like:  "
newLine: .asciiz "\n"
space: .asciiz " "




.text
.globl main

main:
	li $v0, 4 #prnt string
	la $a0, prompt
	syscall
	
	li $v0, 5
	syscall
	move $s2, $v0
	
	
LoopSetup:
	li $s1, 0 # i = 0
	la $s3, array 
	la $s0, array # save address for the array
	
Loop:
	slt $t4, $s1, $s2 
	beq $t4, $zero, LoopDone # if i>=n you are done
	
	move $a0, $s1
	jal Fib
	sw $v0, 0($s3)
	
	# print first i+1 elements
	move $a0, $s0 # base address
	addi $a1, $s1, 1 # size = i + 1
	jal PrintArray
	
	addi $s1, $s1, 1 # i++
	addi $s3, $s3, 4 # offset +4
	j Loop
	
LoopDone:
	j Exit
	

Exit:
	li $v0, 10
	syscall
	


### PRINT ARRAY FUNCTION ###
PrintArray:
	addi $sp, $sp, -12 # Make room in the stack for arguments and $ra
	sw $ra, 8($sp) # store ra
	sw $a1, 4($sp) # save size of the array
	sw $a0, 0($sp) # save base address of the array
	
	move $t0, $a0 # move the base address to a temp register
	li $t1, 0 # i = 0 initialize i
	move $t2, $a1 # n
	addi $t3, $a1, -1 # n-1
	
PrntArrLoop:
	slt $t4, $t1, $t2 
	beq $t4, $zero, PrntArrDone # if i >= n you are done 
	
	# print i
	lw $a0, 0($t0)
	li $v0, 1 # print int
	syscall
	
	# if you are at the lest element, don't print space
	beq $t1, $t3, skipSpace
	
	# print comma
	li $v0, 4 # print string
	la $a0, space
	syscall
	
skipSpace:
	addi $t1, $t1, 1 # i++
	addi $t0, $t0, 4 # increment offset
	j PrntArrLoop # loop until done
	
PrntArrDone:
	li $v0, 4 # print string
	la $a0, newLine
	syscall # print a new line
	
	# restore all your things and return to $ra
	lw $a0, 0($sp)
	lw $a1, 4($sp)
	lw $ra, 8($sp)
	addi $sp, $sp, 12 # return sp back to normal
	jr $ra # go back to ra
### END PRINT ARRAY FUNCTION ###


### FIB FUNCTION ###
Fib:
	addi $sp, $sp, -12 # add some space in the stack
	sw $ra, 8($sp) # save ra
	sw $a0, 0($sp) # save n
	
	# if n==0 return 0 base case 1
	beq $a0, $zero, fibZero

	# if n == 1 return 1 base case 2
	
	li $t0, 1
	beq $a0, $t0, fibOne
	
	# Else do recursive case
	# find fib(n-1)
	addi $a0, $a0, -1
	jal Fib
	sw $v0, 4($sp) # save fib(n-1)
	
	
	# find fib (n-2)
	lw $a0, 0($sp) # restore original n
	addi $a0, $a0, -2
	jal Fib
	
	# do fib(n-1) + fib(n-2)
	lw $t1, 4($sp) 
	add $v0, $v0, $t1 # return register 0 = fib(n-2) + fib(n-1)
	j fibDone

	
fibZero:
	# Return 0
	li $v0, 0
	j fibDone 
fibOne:
	# Return 1
	li $v0, 1
	j fibDone
	
fibDone:
	# Restore the stack and return to ra
	lw $a0, 0($sp)
	lw $ra, 8($sp)
	addi $sp, $sp, 12
	jr $ra
	
### END FIB FUNCTION ###

	

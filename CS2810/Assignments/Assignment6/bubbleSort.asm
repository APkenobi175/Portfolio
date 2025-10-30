.data
	array: .word 8,2,6,0,1,3,10,45,4 # Hard Coded Array
	beforeSort: .asciiz "Before Bubble Sort: "
	afterSort: .asciiz "After Bubble Sort: "
	newLine: .asciiz "\n"
	n: .word 9 # length of array ( Hard coded )
	comma: .asciiz ", "

.text
.globl main

main:
	la $t3, array # base address of array A and offset
	lw $t0, n # load n
	subi $t2, $t0, 1 # N - 1


	li $v0, 4 # print string
	la $a0, beforeSort
	syscall

	# Now we have to loop through all the items in the array
	li $t1, 0 # init i = 0

Loop1:
	bge $t1, $t0, printNewLine
	li $v0, 1 # print int
	lw $a0, 0($t3)
	syscall
	
	
	
	beq $t2, $t1, skipComma # if its the last number don't put a comma at the end
	
	li $v0, 4 # print stringa
	la $a0, comma # print a comma
	syscall
	
	skipComma:
		addi $t1, $t1, 1 # inncrement i
		addi $t3, $t3, 4 # increment offset
	
	j Loop1
	
printNewLine:
	li $v0, 4 # print string
	la $a0, newLine
	syscall
	
	
# START BUBBLE SORT
BeforeLoop:
	li $t7, 0 # swapped = 0, initialize. 
	li $t1, 0 # gonna reuse this i = 0 (i will reuse this same index later too)
	move $t3, $zero # return offset back to 0
	la $t3, array
	
Loop2:
	bge $t1, $t2, AfterLoop
	lw $t4, 0($t3) # array[i]
	lw $t5, 4($t3) # array[i + 1]
	
	# if a[i] > a[i+1] then swap
	slt $t6, $t5, $t4   
	beq $t6, $zero, SkipSwap # if $t6 is zero then don't swap
	j Swap # otherwise swap

	
Swap:
	sw $t5, 0($t3) # swap a[i] and a[i+1]
	sw $t4, 4($t3)
	li $t7, 1  #($t7 will be our swapped indicator), swapped = True
	
SkipSwap:
	addi $t1, $t1, 1 # increment i
	addi $t3, $t3, 4 # increment offset
	j Loop2 # do it again
	
AfterLoop:
	beq $t7, $zero, DoneSorting # if there are no swaps then you are done sorting, exit early
	addi $t2, $t2, -1 # the next pass of the array will be sortened by 1
	bgt $t2, $zero, BeforeLoop # If more elements remain repeat
# BUBBLE SORT IS FINISHED
DoneSorting:
	la $t3, array # base address of array A and offset
	lw $t0, n # load n
	subi $t2, $t0, 1 # N - 1


	li $v0, 4 # print string
	la $a0, afterSort
	syscall

	# Now we have to loop through all the items in the array, exact same as before
	li $t1, 0 # init i = 0

Loop3:
	bge $t1, $t0, Exit
	li $v0, 1 # print int
	lw $a0, 0($t3)
	syscall
	
	
	
	beq $t2, $t1, skipComma2 # if its the last number don't put a comma at the end
	
	li $v0, 4 # print string
	la $a0, comma # print a comma
	syscall
	
	skipComma2:
		addi $t1, $t1, 1 # inncrement i
		addi $t3, $t3, 4 # increment offset
	
	j Loop3

Exit:
	# Print a new line just for fun
	li $v0, 4
	la $a0, newLine
	syscall
	# Now exit
	li $v0, 10 # exit
	syscall	

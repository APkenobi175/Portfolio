.data
array: .word 8,2,6,0,1,3,10,45,4
beforeSort: .asciiz "Before Bubble Sort: "
afterSort: .asciiz "After Bubble Sort: "
newLine: .asciiz "\n"
n: .word 9 # length of array
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

loop1:
	bge $t1, $t0, printNewLine
	li $v0, 1 # print int
	lw $a0, 0($t3)
	syscall
	
	
	
	beq $t2, $t1, skipComma # if its the last number don't put a comma at the end
	
	li $v0, 4 # print string
	la $a0, comma # print a comma
	syscall
	
	skipComma:
		addi $t1, $t1, 1 # inncrement i
		add $t3, $t3, 4 # increment offset
	
	j loop1
	
printNewLine:
	li $v0, 4 # print string
	la $a0, newLine
	syscall
	
	
	
OuterPass:
	li $t7, 0 # swapped = 0tf is 
	li $t1, 0 # gonna reuse this i = 0
	move $t3, $zero # return offset back to 0
	
loop2:
	bge $t1, $t2, nextStep
	
	
	

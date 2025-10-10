.data
### Strings
stringA: .asciiz "Enter a: "
stringB: .asciiz "Enter b: "
stringC: .asciiz "Enter c: "
minusString: .asciiz " - "
plusString: .asciiz " + "
equalsString: .asciiz " = "


.text
.globl main

main:

	## A ##
	# Prompt the user (print the string)
	li $v0, 4 #syscall 4 is for printing strings
	la $a0, stringA
	syscall
	li $v0, 5 #syscall 5 is for reading integers
	syscall 
	move $t0, $v0 # move the user's input into register $t0
	li $v0, 11 #syscall 11 is for printing chars
	la $a0, 10 # \n
	syscall
	
	
	
	## B ##
	# Same thing as A but for B
	li $v0, 4 #print string
	la $a0, stringB
	syscall
	
	li $v0, 5 #syscall 5 is for reading integers
	syscall 
	move $t1, $v0 # move the user's input into register $t1
	li $v0, 11 #print char
	la $a0, 10 # \n
	syscall
	
	
	
	
	## C ##
	# Same thing as A but for C
	li $v0, 4 #syscall 4 is for printing strings
	la $a0, stringC
	syscall

	li $v0, 5 #syscall 5 is for reading integers
	syscall 
	move $t2, $v0 # move the user's input into register $t2
	
	li $v0, 11 #print char
	la $a0, 10 # \n
	syscall
	
	
	
	
	# Compute A - B + C
	sub $t3, $t0, $t1 # A-b=temp
	add $t3, $t2, $t3 # temp + C
	
	
	# Print the result
	
	# Print A
	li $v0, 1 # print int
	move $a0, $t0 # a
	syscall
	# Print -
	li $v0, 4 # print string
	la $a0, minusString # -
	syscall
	# Print B
	li $v0, 1 # print int
	move $a0, $t1 # B
	syscall
	# Print +
	li $v0, 4 # print string
	la $a0, plusString # +
	syscall
	# Print C
	li $v0, 1 # print int
	move $a0, $t2 # C
	syscall
	# Print =
	li $v0, 4 # print string
	la $a0, equalsString # =
	syscall
	# Print result
	li $v0, 1 # print int
	move $a0, $t3 # result
	syscall
	
	# Exit without dropping off the bottom
	li $v0, 10 # syscall 10 is exit
	syscall
	
	
	
	
	
	
	
	
	
	
	
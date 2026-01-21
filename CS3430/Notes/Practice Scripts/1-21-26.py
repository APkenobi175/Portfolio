import numpy as np

A = np.array([[2.0, 1.0],
              [5.0, 3.0]]) # Coefficient matrix

B = np.array([1.0, 2.0]) # Constant terms (answers) 

# Numpy will automatically convert them to floats, so manually setting to float is good practice

# Solve for X in AX = B

X = np.linalg.solve(A, B) # Wow thats fucking easy what the hell. Numpy is powerful wow

print(X) # [ 1. -1.] # The commas turn into periods when printed because numpy arrays are weird like that

Ax = A@X # Matrix multiplication using @ operator

np.matmul(A, X) # Another way to do matrix multiplication
print(Ax) # [1. 2.] # Confirms that AX = B
print(Ax - B) # Ax what we have obtained, B is what we have been given. 

# Prints out [-2.22222222220e^-16, 0.000000000000e+00] which is effectively 0 due to floating point precision

error = np.linalg.norm(Ax - B) # This is how we compute the error between what we have and what we want
# In numpy norm computes the Euclidean norm.
print(f"Error: {error}") # Error: 2.449293598294706e-16



import numpy as np

detA = np.linalg.det(A) # Determinant of A
rankA = np.linalg.matrix_rank(A) # Rank of A

if rankA == A.shape[1]: # A.shape[1] is the number of columns in A
    print("System is solvable")
else:
    print("System is not solvable")

C = np.array([[1.0, 2.0],
              [2.0, 4.0]]) # Another coefficient matrix

bro = np.linalg.matmul(A, C)
print(bro)
# prints out [[4. 8.][11. 22. ]]


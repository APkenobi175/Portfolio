def fizz_buzz(n):
    result = ""
    for x in range(1,n+1):
        if x % 3 == 0 and x % 5 == 0:
            result += "fizzbuzz\n"
        elif x % 3 == 0:
            result += "fizz\n"
        elif x % 5 == 0:
            result += "buzz\n"
        else:
            result +=f"{x}\n"
    return result


## All middleware has the following shape (middleware factory function)

def constraint_middleware_Factory(next):# this is the function that creates the middleware function (higher order function)
    def middleware(n): # should match your main function (Fizzbuzz)
        if n > 0 and n <=100:
            return next(n)
        else:
            return "Number was out of bounds bro ham must be between 1 and 100"
    return middleware

# YOu can compose as many middleware as you'd like

def capitalize_middleware_factory(next):
    def middleware(n):
        result = next(n)
        return result.upper()
    return middleware

# call them in reverse order in part of the chain
middleware_chain = capitalize_middleware_factory(fizz_buzz)
middleware_chain = constraint_middleware_Factory(fizz_buzz)

num = int(input("Enter a number"))

print(middleware_chain(num))
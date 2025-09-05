def find(data, conditionFunction):
    for x in data:
        if conditionFunction(x):
            return True
    return False



myData = [1,2,3,4,5,6,76,8]


def myConditionFunction(num):
    return num > 50

print(find(myData, myConditionFunction))

def printHello():
    print("Hello!")

a = printHello

a()
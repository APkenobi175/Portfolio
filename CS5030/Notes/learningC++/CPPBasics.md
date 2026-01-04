# Basics of C++

## First Program in C++

* When we start a C++ program we need to include the libraries we want to use, similar to import in python
* In the program below we use `#include <iostream>` to include the standard C++ library
* Now that we have our library we can use features from it
* First we will define the main function, this is where our program starts executing
* Insude the main function we will type `std::cout << "Hello World";` to output "Hello World" to the console
* std is short for standard library
* :: allows to access features of that library
* cout is short for character out, not console out
* << is used to output one or more characters
* Together this line is called a statement, and we terminate statements with a `;`
* Finally we return 0 to make sure our function executed correctly, we return an int because thats what we define our functions output as in `int main ()`

```cpp
#include <iostream> // This is importing the standard C++ library

int main () {
    // first type std, which is short for standard library
    // second, type ::. this allows us to use features of the standard library
    // third, type cout. This is short for character out, not console out
    // Using cout we can output one or more characters, to do this we want to use <<
    // This line is called a statment. We terminate statements with a ;
    std::cout << "Hello World";
    return 0;
    // we return 0 to make sure our function executed correctly
    // we return an int because thats what we define our functions output as 
}
```

## Variables

* When we declare our variables we need to specify the type of variable it is
* this helps in memory allocation and type checking
* Then we can initialize our variable with a value
* The following program intializes an int variable named file size and then outputs it to the console

```cpp
int main(){
    int file_size = 100; 
    std::cout << file_size;
    return 0;
}
```

## Data Types

* C++ is a statically typed language, meaning we need to declare the type of variable when we create it
* Here are some common data types in C++
  * int - integer values
  * float - floating point numbers
  * double - double precision floating point numbers
  * char - single characters
  * bool - boolean values (true or false)
  * string - sequence of characters (requires including the string library)

## Macros

* Macros are a way to define code that can be reused throughout your program
* They are defined using the `#define` directive
* Here is an example of a macro that outputs a value to the console

```cpp
#include <iostream>
#define LOG(x) std::cout << x << std::endl; // this is a macro defintion, it replaces LOG(x) with std::cout << x << std::endl;
int main(){
    int file_size = 100; 
    LOG(file_size) // this will be replaced with std::cout << file_size << std::endl;
    return 0;
}
```

* Macros can make your code more readable and easier to maintain

## Pointers

* Pointers are variables that store the memory address of another variable
* They are declared using the `*` operator
* Here is an example of how to use pointers in C++
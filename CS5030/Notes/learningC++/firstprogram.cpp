#include <iostream> // This is importing the standard C++ library

int main () {
    // first type std, which is short for standard library
    // second, type ::. this allows us to use features of the standard library
    // third, type cout. This is short for character out, not console out
    // Using cout we can output one or more characters, to do this we want to use <<
    // This line is called a statment. We terminate statements with a ;
    std::cout << "Hello World";

    for (int i = 0; i < 5; i++) {
        std::cout << "\nThis is line number " << i;
    }
    return 0;
    // we return 0 to make sure our function executed correctly
    // we return an int because thats what we define our functions output as 
}
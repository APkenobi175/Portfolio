#include <iostream>
#include <cstring> // for memset

#define LOG(x) std::cout << x << std::endl; // this is a macro defintion, it replaces LOG(x) with std::cout << x << std::endl; so I can use LOG to output text easily
// this is cool and all but ill create a print function because python is so cool

// Pointer example
//
// int main() {
    // int var = 8; // normal integer variable, this variable has a memory address, we want to store that address

    // void* ptr = &var; // the & operator gets the memory address of var, we store that address in ptr. ptr is a pointer variable, it stores a memory address. We use void* to define a pointer that can point to any data type
    // // What this does is it initializes a variable var, and then stores the memory address of var in the pointer variable ptr
    // // std::cin.get(); // what cin does is wait for user input. It will wait until the user presses enter
    // // since we are using a void pointer, we need to cast it to the correct data type before dereferencing it
    // LOG("The value of var is: " << *(static_cast<int*>(ptr))); // this will output the value of var by dereferencing the pointer ptr after casting it to an int pointer
    // std::cout << "The memory address of var is: " << ptr << std::endl; // this will output the memory address of var
    // return 0;
//}
// what is wrong with this code?
// we are using a void pointer, which means we cannot dereference it directly to get the value stored at that memory address
// to dereference a void pointer, we need to cast it to the correct data type first


// Using pointers

// int main(){
//     char* buffer = new char[8]; // this creates a new character pointer that allocates 8 bytes of memory on the heap
//     // this is similar to mips when you offset the stack pointer to allocate space on the stack
//     // this is basically creating an array of 8 chars
//     memset(buffer, 0, 8); // this sets all 8 bytes of memory to 0
//     // I need to import memset from the cstring library

//     char** ptr = &buffer; // this creates a pointer to a pointer, ptr stores the memory address of buffer

//     delete[] buffer; // this frees the memory allocated for buffer
// }




// Here is something I create for fun, an implementation of a dynamic array using pointers




void print(auto arg){ // auto allows us to accept any data type as an argument
    std::cout << arg << std::endl; // std::endl adds a new line after the output
}
int main(){
    int size = 2; // this is the size of the array
    int* arr = new int[size]; // this is an interger pointer that allocates an array of integers on the heap, it has size 2 
    arr[0] = 1; // set first element to 1
    arr[1] = 2; // set second element to 2
    LOG("Array elements before resizing:"); // use the log macro to output text
    for(int i = 0; i < size; i++){ // from 0 to size loop through the array
        LOG(arr[i]); // output each element of the array
    }
    // now we want to resize the array to size 4
    int newSize = 4; // new size of the array
    int* newArr = new int[newSize]; // this is a new pointer that allocates memory for the new array of new size which is 4
    // now we will copy the old array into the new array
    for(int i = 0; i < size; i++){ // from 0 to size loop through the old array
        newArr[i] = arr[i]; // copy each element from the old array to the new array
    }
    delete[] arr; // free the memory allocated for the old array
    arr = newArr; // point arr to the new array, what this does is makes our arr pointer point to the new array rather than the old array.
    size = newSize; // update the size variable to the new size
    LOG("Array elements after resizing:"); // use the log macro to output text
    for(int i = 0; i < size; i++){ // from 0 to size loop through the array
        LOG(arr[i]); // output each element of the array
    }
    print("Hello World");
    print(1 + 1);
    print(3.14);

}





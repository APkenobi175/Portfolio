# Complexity

Big-O Notation:

Fastest to Slowest:

O(1), O(log n), O(n), O(nlog n), O(n^2), O(n^3), O(2^n), O(n!)

Its easier to come up with an upper bound than come up with a lower bound or a tight bound
Thats why we use Big O!

If you have to go through the entire list exactly one time worst-case is O(n)

An algorithm that requires 2n + 1 operations to complete its task on n data is said to have linear runtime



#### Why don't we worry about constants?
Because they don't matter!

As N gets large, the constant becomes unimportant



## Master Theorem

#### A= Number of recursive calls
#### B= Factory by which the problem size decreases
#### K= Total amount of work in a single call

Assume T(n) = [a(T(n/b))] Recursion + [O(n^k)] Work before recursive call

#### if a>b^k The complexity is O(n^logb(A))
#### if a=b^k the complexity is O(n^k log n)
#### if a<b^k the complexity is O(n^k)

This formula only works on recursive functions!

This formula also only works if it decreases by a factor

if its linear (n-1) it is commonly O(n^2)

### Example 1
```java

public static void doit(int n){
    if (n<=1)return;
    x++;
    doit(n/2);
}
```

#### A=1
#### B=2
#### K=0 (Does no work that depends on N)

1 = 2^0 so complexity is O(n^0 log n) which equals **O(log(n))**

### Example 2
```java

public static void doit(int n){
    if (n<=1)return;
    x++;
    doit(n/2);
    doit(n/2);
}
```
##### A=2
##### B=2
##### K=0

1 > 2^0 so complexity is O(nlog2(2)) =
**O(n)** (I think)

## Expiremental Data

**O(1)** - Constant

**O(logn)** - Grows slowly by a constant

**O(n)** doubles between entries

**O(nlogn)** - Slightly more than doubles between entries

**O(n^2)** - Quadruples between entries

**O(2^n)** - grows exponentially

**Note** - This is the real world and numbers aren't perfect. So complexity could be O(n) and the "Doubles" might not be perfect

### Example

| n | T(n) |
|---|------|
| 2 | 10   |
| 4 |17|
|8|32|
|16|66|
|32|130|

The complexity of this data is **O(n)** even though the numbers aren't exactly doubled


## Binary Search Trees

Nodes always get added at a leaf

**Definition** 
- Key in the root of the right subtree is greater than the root
- Key in the root of the left subtree is less than or equal too the root
- Left and right subtrees are binary search trees


### Comparable Objects

The Comparable<T> interface defines a standard
way to compare objects using relations less than,
equal to, and greater than.
The interface defines a single method
public interface Comparable<T>
```Java
{
int compareTo(T item);
}
```

The method compareTo() returns an integer
value that is negative, zero, or positive (no specific
return values required as long as sign is correct). The
value compares the value of an attributes of
the object (obj) with another object (obj2) of
the same type

```Java
public class BinarySearchTree<E extends Comparable<? super E>>
{
private BinaryNode<E> root; // no one outside class has access
public void insert( E x )
{
root = insert( x, root );
}

private BinaryNode<E> insert( E x, BinaryNode<E> t )
    {if( t == null )
            return new BinaryNode<>( x, null, null );
        int compareResult = x.compareTo( t.element );
        if( compareResult < 0 )
            t.left = insert( x, t.left );
        else if( compareResult > 0 )
            t.right = insert( x, t.right );
        else
            ; // Duplicate; do nothing
        return t;
    }
```
The SYNTAX IS HORRIBLE

This is how you insert a node into a comparable binary search tree. E means generic
The public version calls the private version. Why do we need 2? We call them the same because we are lazy and java lets us. We have to pass in the root but the main program didn't know about the root.







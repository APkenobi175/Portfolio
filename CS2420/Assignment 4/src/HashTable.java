import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

// QuadraticProbing Hash table class
//
// CONSTRUCTION: an approximate initial size or default of 101
//
// ******************PUBLIC OPERATIONS*********************
// bool insert( x )       --> Insert x
// bool remove( x )       --> Remove x
// bool contains( x )     --> Return true if x is present
// void makeEmpty( )      --> Remove all items


/**
 * Probing table implementation of hash tables.
 * Note that all "matching" is based on the equals method.
 * @author Mark Allen Weiss
 */
public class HashTable<E>
{   private static final int DEFAULT_TABLE_SIZE = 101;
    private HashEntry<E>[] array; // array of elements
    private int occupiedCt; // Number of occupied cells
    private int currentActiveEntries; // Number of active elements
    private int totalProbes; // track total probes
    private boolean useBetterHash = false;
    /**
     * Construct the hash table.
     */
    public HashTable( )
    {
        this( DEFAULT_TABLE_SIZE );
    }

    public void setUseBetterHash(boolean useBetterHash){
        this.useBetterHash = useBetterHash;
    }

    /**
     * Construct the hash table.
     * @param size the approximate initial size.
     */
    public HashTable( int size )
    {
        allocateArray( size );
        doClear( );
    }

    /**
     * Insert into the hash table. If the item is
     * already present, do nothing.
     * Implementation issue: This routine doesn't allow you to use a lazily deleted location.  Do you see why?
     * @param x the item to insert.
     */
    public boolean insert(E x) {
        int currentPos = findPos(x);
        if (isActive(currentPos)) {
            array[currentPos].element = x;  // Replace the existing value
            return true;
        }

        // Insert new element
        array[currentPos] = new HashEntry<>(x, true);
        currentActiveEntries++;

        // Rehash if the table is half full
        if (++occupiedCt > array.length / 2) {
            rehash();
        }

        return true;
    }

    public String toString (int limit){
        StringBuilder sb = new StringBuilder();
        int ct=0;
        for (int i=0; i < array.length && ct < limit; i++){
            if (array[i]!=null && array[i].isActive) {
                sb.append( i + ": " + array[i].element + "\n" );
                ct++;
            }
        }
        return sb.toString();
    }

    /**
     * Expand the hash table.
     */
    private void rehash( )
    {
        HashEntry<E> [ ] oldArray = array;

        // Create a new double-sized, empty table
        allocateArray( 2 * oldArray.length );
        occupiedCt = 0;
        currentActiveEntries = 0;

        // Copy table over
        for( HashEntry<E> entry : oldArray )
            if( entry != null && entry.isActive )
                insert( entry.element );
    }

    /**
     * Method that performs quadratic probing resolution.
     * @param x the item to search for.
     * @return the position where the search terminates.
     * Never returns an inactive location.
     */
    private int findPos(E x) {
        int offset = 1;
        int currentPos = myhash(x);
        Object key = getKey(x);  // Extract key from the element
        int probes = 1;

        while (array[currentPos] != null &&
                !getKey(array[currentPos].element).equals(key)) {
            currentPos += offset;  // Quadratic probing
            offset += 2;
            if (currentPos >= array.length) {
                currentPos -= array.length;
            }
            probes++;
        }
        totalProbes += probes;
        return currentPos;
    }
    private Object getKey(E element){
        if ( element instanceof Pair){
            return ((Pair<?, ?>) element).get1(); // Get the key (first value)
        }
        return element;
    }


    /**
     * Remove from the hash table.
     * @param x the item to remove.
     * @return true if item removed
     */
    public boolean remove(E x) {
        int currentPos = findPos(x);
        if (isActive(currentPos) &&
                getKey(array[currentPos].element).equals(getKey(x))) {
            array[currentPos].isActive = false;
            currentActiveEntries--;
            return true;
        }
        return false;
    }

    /**
     * Get current size.
     * @return the size.
     */
    public int size( )
    {
        return currentActiveEntries;
    }

    /**
     * Get length of internal table.
     * @return the size.
     */
    public int capacity( )
    {
        return array.length;
    }

    /**
     * Find an item in the hash table.
     * @param x the item to search for.
     * @return true if item is found
     */
    public boolean contains(E x) {
        int currentPos = findPos(x);
        return isActive(currentPos) &&
                getKey(array[currentPos].element).equals(getKey(x));
    }

    /**
     * Find an item in the hash table.
     * @param x the item to search for.
     * @return the matching item.
     */
    public E find( E x )
    {
        int currentPos = findPos( x );
        if (!isActive( currentPos )) {
            return null;
        }
        else {
            return array[currentPos].element;
        }
    }

    /**
     * Return true if currentPos exists and is active.
     * @param currentPos the result of a call to findPos.
     * @return true if currentPos is active.
     */
    private boolean isActive( int currentPos )
    {
        return array[ currentPos ] != null && array[ currentPos ].isActive;
    }

    /**
     * Make the hash table logically empty.
     */
    public void makeEmpty( )
    {
        doClear( );
    }

    private void doClear( )
    {
        occupiedCt = 0;
        for( int i = 0; i < array.length; i++ )
            array[ i ] = null;
    }

    private int myhash(E x) {
        int hashVal;
        if (x instanceof ColorMap && useBetterHash) {
            hashVal = ((ColorMap) x).betterHashCode();  // Use mod hash code
        } else {
            hashVal = x.hashCode();  // Use original hash function
        }

        hashVal %= array.length;
        if (hashVal < 0) {
            hashVal += array.length;
        }
        return hashVal;
    }

    private static class HashEntry<E>
    {
        public E  element;   // the element
        public boolean isActive;  // false if marked deleted

        public HashEntry( E e )
        {
            this( e, true );
        }

        public HashEntry( E e, boolean i )
        {
            element  = e;
            isActive = i;
        }
    }
    // Current size

    /**
     * Internal method to allocate array.
     * @param arraySize the size of the array.
     */
    private void allocateArray( int arraySize )
    {
        array = new HashEntry[ nextPrime( arraySize ) ];
    }

    /**
     * Internal method to find a prime number at least as large as n.
     * @param n the starting number (must be positive).
     * @return a prime number larger than or equal to n.
     *
     */
    private static int nextPrime( int n )
    {
        if( n % 2 == 0 )
            n++;

        for( ; !isPrime( n ); n += 2 )
            ;

        return n;
    }

    /**
     * Internal method to test if a number is prime.
     * Not an efficient algorithm.
     * @param n the number to test.
     * @return the result of the test.
     */
    private static boolean isPrime( int n )
    {
        if( n == 2 || n == 3 )
            return true;

        if( n == 1 || n % 2 == 0 )
            return false;

        for( int i = 3; i * i <= n; i += 2 )
            if( n % i == 0 )
                return false;

        return true;
    }

    public ArrayList<E> getAll(){
        ArrayList<E> items = new ArrayList<>();
        for (HashEntry<E> entry : array) {
            if (entry != null && entry.isActive) {
                items.add( entry.element );
            }
        }
        Collections.sort(items, Comparator.comparing(Object::toString));
        return items;
    }

    public void printAverageProbes(){
        System.out.print(Math.round((double)totalProbes/currentActiveEntries ));
    }


    // Simple main
    public static void main( String [ ] args ) {
        HashTable<Pair<String, Integer>> H = new HashTable<>();

        // Insert TEST
        H.insert(new Pair<>("Jimmy", 66));
        H.insert(new Pair<>("Jim", 67));
        H.insert(new Pair<>("Jom", 90));

        // PRINT TABLE CONTENTS
        System.out.println("Table contents:");
        System.out.println(H.getAll());

        //FIND
        System.out.println("Contains Jimmy? " + H.contains(new Pair<>("Jimmy", 66)));
        //DELET
        H.remove(new Pair<>("Jim", 67));
        System.out.println("After deleting Jim:");
        System.out.println(H.getAll());

        //CHANGE VALUE
        H.remove(new Pair<>("Jom", 90));
        H.insert(new Pair<>("Jom", 100));
        System.out.println("After modifying Jom:");
        System.out.println(H.getAll());

        // Print average probe count
        H.printAverageProbes();
    }
}


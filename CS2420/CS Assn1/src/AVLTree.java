 // AvlTree class
//
// CONSTRUCTION: with no initializer
//
// ******************PUBLIC OPERATIONS*********************
// void insert( x )       --> Insert x
// void remove( x )       --> Remove x (unimplemented)
// boolean contains( x )  --> Return true if x is present
// boolean remove( x )    --> Return true if x was present
// Comparable findMin( )  --> Return smallest item
// Comparable findMax( )  --> Return largest item
// boolean isEmpty( )     --> Return true if empty; else false
// void makeEmpty( )      --> Remove all items
// void printTree( )      --> Print tree in sorted order
// ******************ERRORS********************************
// Throws UnderflowException as appropriate

/**
 * Implements an AVL tree.
 * Note that all "matching" is based on the compareTo method.
 * @author Mark Allen Weiss
 */
public class AVLTree<AnyType extends Comparable<? super AnyType>>
{
    /**
     * Construct the tree.
     */
    public AVLTree( )
    {
        root = null;
    }

    /**
     * @param value the item to insert.
     */
    public void insert( AnyType value )
    {
        root = insert( value, root );
    }

    /**
     * Remove from the tree. Nothing is done if x is not found.
     * @param value the item to remove.
     */
    public void remove( AnyType value )
    {
        root = remove( value, root );
    }


    /**
     * Internal method to remove from a subtree.
     * @param value the item to remove.
     * @param currentNode the node that roots the subtree.
     * @return the new root of the subtree.
     */
    private AvlNode<AnyType> remove( AnyType value, AvlNode<AnyType> currentNode )
    {
        // Base case - If node is null not found
        if( currentNode == null )
            return currentNode;   // Item not found; do nothing
        // Compare item to remove to the current node's value
        int compareResult = value.compareTo( currentNode.element );
        // If the value is smaller, go to the left subtree, if its greater go to the right sub tree
        if( compareResult < 0 )
            currentNode.left = remove( value, currentNode.left );
        else if( compareResult > 0 )
            currentNode.right = remove( value, currentNode.right );

        else if( currentNode.left != null && currentNode.right != null ) // Two children
        {
            currentNode.element = findMin( currentNode.right ).element; // Node has two cildren so replace it with the smallest item in the right sub tree
            currentNode.right = remove( currentNode.element, currentNode.right ); // remove replaced item
        }
        else // If the node has one or no children replace it with its non-null child :)
            currentNode = ( currentNode.left != null ) ? currentNode.left : currentNode.right;
        return balance( currentNode ); // rebalance after deletion
    }

    /**
     * Find the smallest item in the tree.
     * @return smallest item or null if empty.
     */
    public AnyType findMin( )
    {
        if( isEmpty( ) )
            throw new RuntimeException( );
        return findMin( root ).element;
    }

    public  void  deleteMin( ){
        if (root ==null){
            throw new RuntimeException("Error: Empty Tree");

        }

        root = deleteMin(root); // Remove smallest node and rebalance

    }

    /**
     * Method to delete the smallest item in a subtree
     * @param currentNode - The root of the subtree that we will delete the minimum node
     * @return the new root of the tree after deletion
     */
    private AvlNode<AnyType> deleteMin( AvlNode<AnyType> currentNode )
    {
        // Base case - if current node has no left child its actually, fun fact, the smallest node
        if (currentNode.left == null){
            return currentNode.right;
        }
        // Recursively move to the left to find the smallest node
        currentNode.left = deleteMin( currentNode.left );
        // AFter deletion is completet rebalance the tree
        return balance( currentNode );
    }

    /**
     * Find the largest item in the tree.
     * @return the largest item of null if empty.
     */
    public AnyType findMax( )
    {
        if( isEmpty( ) )
            throw new RuntimeException( );
        return findMax( root ).element;
    }

    /**
     * Find an item in the tree.
     * @param searchItem the item to search for.
     * @return true if x is found.
     */
    public boolean contains( AnyType searchItem )
    {
        return contains( searchItem, root );
    }

    /**
     * Make the tree logically empty.
     */
    public void makeEmpty( )
    {
        root = null;
    }

    /**
     * Test if the tree is logically empty.
     * @return true if empty, false otherwise.
     */
    public boolean isEmpty( )
    {
        return root == null;
    }

    /**
     * Print the tree contents in sorted order.
     */
    public void printTree( String label)
    {
        System.out.println(label);
        if( isEmpty( ) )
            System.out.println( "Empty tree" );
        else
            printTree( root,"" );
    }

    private static final int ALLOWED_IMBALANCE = 1;

    // Assume t is either balanced or within one of being balanced
    private AvlNode<AnyType> balance( AvlNode<AnyType> currentNode )
    {
        if( currentNode == null ) // Don't follow null references, there is nothing to balance if node is null
            return currentNode;
        // if the left subtree is heavier, do some rotations!
        if( height( currentNode.left ) - height( currentNode.right ) > ALLOWED_IMBALANCE )
            if( height( currentNode.left.left ) >= height( currentNode.left.right ) )
                currentNode = rightRotation( currentNode);
            else
                currentNode = doubleRightRotation( currentNode );
        else
            // if the right subtree is heavier do some rotations!
        if( height( currentNode.right ) - height( currentNode.left ) > ALLOWED_IMBALANCE )
            if( height( currentNode.right.right ) >= height( currentNode.right.left ) )
                currentNode = leftRotation( currentNode );
            else
                currentNode = doubleLeftRotation( currentNode );
        // after rotations are done update the height of the current Node
        currentNode.height = Math.max( height( currentNode.left ), height( currentNode.right ) ) + 1;
        return currentNode;
    }

    public void checkBalance( )
    {
        checkBalance( root );
    }

    private int checkBalance( AvlNode<AnyType> nodeToCheck )
    {
        if( nodeToCheck == null )
            return -1;

        if( nodeToCheck != null )
        {
            int heightLeft = checkBalance( nodeToCheck.left );
            int heightRight = checkBalance( nodeToCheck.right );
            if( Math.abs( height( nodeToCheck.left ) - height( nodeToCheck.right ) ) > 1 ||
                    height( nodeToCheck.left ) != heightLeft || height( nodeToCheck.right ) != heightRight )
                System.out.println( "\n\n***********************OOPS!!" );
        }

        return height( nodeToCheck );
    }


    /**
     * Internal method to insert into a subtree.  Duplicates are allowed
     * @param insertedItem the item to insert.
     * @param currentNode the node that roots the subtree.
     * @return the new root of the subtree.
     */
    private AvlNode<AnyType> insert( AnyType insertedItem, AvlNode<AnyType> currentNode )
    {
        if( currentNode == null )
            return new AvlNode<>( insertedItem, null, null );

        int compareResult = insertedItem.compareTo( currentNode.element );

        if( compareResult < 0 )
            currentNode.left = insert( insertedItem, currentNode.left );
        else
            currentNode.right = insert( insertedItem, currentNode.right );

        return balance( currentNode );
    }

    /**
     * Internal method to find the smallest item in a subtree.
     * @param currentNode the node that roots the tree.
     * @return node containing the smallest item.
     */
    private AvlNode<AnyType> findMin( AvlNode<AnyType> currentNode )
    {
        if( currentNode == null )
            return currentNode;

        while( currentNode.left != null )
            currentNode = currentNode.left;
        return currentNode;
    }



    /**
     * Internal method to find the largest item in a subtree.
     * @param currentNode the node that roots the tree.
     * @return node containing the largest item.
     */
    private AvlNode<AnyType> findMax( AvlNode<AnyType> currentNode )
    {
        if( currentNode == null )
            return currentNode;

        while( currentNode.right != null )
            currentNode = currentNode.right;
        return currentNode;
    }

    /**
     * Internal method to find an item in a subtree.
     * @param target is item to search for.
     * @param currentNode the node that roots the tree.
     * @return true if x is found in subtree.
     */
    private boolean contains( AnyType target, AvlNode<AnyType> currentNode )
    {
        while( currentNode != null ) // Traverse tree until we find a null thats node
        {
            int compareResult = target.compareTo( currentNode.element );
            // if the target node is smaller, move it to the left child, if its
            // bigger move it to the right child
            if( compareResult < 0 )
                currentNode = currentNode.left;
            else if( compareResult > 0 )
                currentNode = currentNode.right;
            // if the target and currentNode are the same then return true
            else
                return true;    // Match
        }
// Item isn't in the tree
        return false;   // No match
    }

    /**
     * Internal method to print a subtree in sorted order.
     * @param currentNode the node that roots the tree.
     */
    private void printTree( AvlNode<AnyType> currentNode, String indent )
    {
        if( currentNode != null )
        { // Recursively print the right subtree
            printTree( currentNode.right, indent+"   " );
            // recursively print the nodes value
            System.out.println( indent+ currentNode.element + "("+ currentNode.height  +")" );
            printTree( currentNode.left, indent+"   " ); // print the left subtree
        }
    }

    /**
     * Return the height of node t, or -1, if null.
     */
    private int height( AvlNode<AnyType> currentNode )
    {   if (currentNode==null) return -1;
        return currentNode.height;
    }

    /**
     * Rotate binary tree node with left child.
     * For AVL trees, this is a single rotation for case 1.
     * Update heights, then return new root.
     */
    private AvlNode<AnyType> rightRotation(AvlNode<AnyType> currentNode )
    {// The left cild of the current node will become the new root
        AvlNode<AnyType> theLeft = currentNode.left;
        // Move te right subtree of the left child to the left of the current node
        currentNode.left = theLeft.right;
        // set the current node as the right child
        theLeft.right = currentNode;
        // update the height of the currentNode which is the old root
        currentNode.height = Math.max( height( currentNode.left ), height( currentNode.right ) ) + 1;
        // now we update the height of the new root which is the left child
        theLeft.height = Math.max( height( theLeft.left ), currentNode.height ) + 1;
        // return the new root
        return theLeft;
    }

    /**
     * Rotate binary tree node with right child.
     * For AVL trees, this is a single rotation for case 4.
     * Update heights, then return new root.
     */
    private AvlNode<AnyType> leftRotation(AvlNode<AnyType> currentNode )
    { // the right child of the current node will become the new root
        AvlNode<AnyType> theRight = currentNode.right;
        // move left subtree of right child to right of current node
        currentNode.right = theRight.left;
        // set current node as left child of new root
        theRight.left = currentNode;
        // update the height of the current node
        currentNode.height = Math.max( height( currentNode.left ), height( currentNode.right ) ) + 1;
        // update the height of the new root
        theRight.height = Math.max( height( theRight.right ), currentNode.height ) + 1;
        // return the new root
        return theRight;
    }

    /**
     * Double rotate binary tree node: first left child
     * with its right child; then node k3 with new left child.
     * For AVL trees, this is a double rotation for case 2.
     * Update heights, then return new root.
     */
    private AvlNode<AnyType> doubleRightRotation( AvlNode<AnyType> currentNode )
    { // first do a left rotation, and then do a right rotation
        currentNode.left = leftRotation( currentNode.left );
        return rightRotation( currentNode );

    }

    /**
     * Double rotate binary tree node: first right child
     * with its left child; then node k1 with new right child.
     * For AVL trees, this is a double rotation for case 3.
     * Update heights, then return new root.
     */
    private AvlNode<AnyType> doubleLeftRotation(AvlNode<AnyType> currentNode )
    { // firrst do a right rotation, and then do a left rotation
        currentNode.right = rightRotation( currentNode.right );
        return leftRotation( currentNode );
    }

    private static class AvlNode<AnyType>
    {
        // Constructors
        AvlNode( AnyType theElement )
        {
            this( theElement, null, null );
        }

        AvlNode( AnyType theElement, AvlNode<AnyType> leftTree, AvlNode<AnyType> rightTree )
        {
            element  = theElement;
            left     = leftTree;
            right    = rightTree;
            height   = 0;
        }

        AnyType           element;      // The data in the node
        AvlNode<AnyType>  left;         // Left child
        AvlNode<AnyType>  right;        // Right child
        int               height;       // Height
    }

    /** The tree root. */
    private AvlNode<AnyType> root;


    // Test program
    public static void main( String [ ] args ) {
        // Test AVL tree with integer values
        AVLTree<Integer> integerTree = new AVLTree<>();
        // Test AVL tree with dwarf objects
        AVLTree<Dwarf> dwarfTree = new AVLTree<>();
        // Insert list of dwarfs and test tree
        String[] nameList = {"Snowflake", "Sneezy", "Doc", "Grumpy", "Bashful", "Dopey", "Happy", "Doc", "Grumpy", "Bashful", "Doc", "Grumpy", "Bashful"};
        for (int i=0; i < nameList.length; i++)
            dwarfTree.insert(new Dwarf(nameList[i]));
        // Print the tree
        dwarfTree.printTree( "The Tree" );
        // Remove bashful from the tree
        dwarfTree.remove(new Dwarf("Bashful"));
        // print the tree again to test removal
        dwarfTree.printTree( "The Tree after delete Bashful" );
        // Test deleteMin
        for (int i=0; i < 8; i++) {
            dwarfTree.deleteMin();
            dwarfTree.printTree( "\n\n The Tree after deleteMin" );
        }
    }

}


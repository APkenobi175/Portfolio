// ******************ERRORS********************************
// Throws UnderflowException as appropriate
import java.util.Queue;
import java.util.LinkedList;
import java.util.List;
class UnderflowException extends RuntimeException {
    /**
     * Construct this exception object.
     *
     * @param message the error message.
     */
    public UnderflowException(String message) {
        super(message);
    }
}

public class Tree {
    private BinaryNode root;  // Root of tree
    private String treeName;     // Name of tree

    /**
     * Create an empty tree
     * @param label Name of tree
     */
    public Tree(String label) {
        treeName = label;
        root = null;
    }

    /**
     * Create tree from list
     * @param arr   List of elements
     * @param label Name of tree
     * @ordered true if we want an ordered tree
     */
    public Tree(Integer[] arr, String label, boolean ordered) {
        treeName = label;
        if (ordered) {
            root = null;
            for (int i = 0; i < arr.length; i++) {
                bstInsert(arr[i]);
            }
        } else root = buildUnordered(arr, 0, arr.length - 1);
    }


    /**
     * Build a NON BST tree by inorder
     * @param arr nodes to be added
     * @return new tree
     */
    private BinaryNode buildUnordered(Integer[] arr, int low, int high) {
        if (low > high) return null;
        int mid = (low + high) / 2;
        BinaryNode curr = new BinaryNode(arr[mid], null, null);
        curr.left = buildUnordered(arr, low, mid - 1);
        curr.right = buildUnordered(arr, mid + 1, high);
        return curr;
    }


    /**
     * Change name of tree
     * @param name new name of tree
     */
    public void changeName(String name) {
        this.treeName = name;
    }

    /**
     * Return a string displaying the tree contents as a single line
     */
    public String toString() {
        if (root == null)
            return treeName + " Empty tree";
        else
            return treeName + "\n" + toString(root, 0);



    }

    public String toString(BinaryNode node, int depth) {
        if(node == null){
            return""; //  Base case: Return empty string if null

        }

        // In order to match the desired output we need to create an indendation based on the depth of the node.

        String tree = " ".repeat(depth) + node.element + "\n"; // Then go to a new line

        // Traverse right subtree, then left subtree
        tree += toString(node.right, depth + 1);
        tree += toString(node.left, depth + 1);

        return tree;
    }
    /**
     * Return a string displaying the tree contents as a single line
     */
    public String toString2() {
        if (root == null)
            return treeName + " Empty tree";
        else
            return treeName + " " + toString2(root);
    }

    /**
     * Internal method to return a string of items in the tree in order
     * This routine runs in O(??)
     *
     * @param t the node that roots the subtree.
     */
    public String toString2(BinaryNode t) {
        if (t == null) return "";
        StringBuilder sb = new StringBuilder();
        sb.append(toString2(t.left));
        sb.append(t.element.toString() + " ");
        sb.append(toString2(t.right));
        return sb.toString();
    }


    /**
     * The complexity of finding the deepest node is O(n) Every node is processed once
     */

    public Integer deepestNode() {
        if(root == null){
            return null; // DON'T FOLLOW NULL NODES!!!!!!!!
        }
        Queue<BinaryNode> queue = new LinkedList<>(); // Using java's builtin queue and linked list implementations
        queue.add(root); // Start with root
        BinaryNode currentNode = null; // initiate

        while(!queue.isEmpty()){
            currentNode = queue.poll(); // dequeue node and enqueue the left and right children if they exist

            if(currentNode.left != null){
                queue.add(currentNode.left);

            }
            if(currentNode.right != null){
                queue.add(currentNode.right);
            }
            // We will keep dequeuing and enqueuing until the node is null, once that happens we have reached the deepest node
        }
        return currentNode.element; // This is the value of the deepest node

    }

    /**
     * The complexity of finding the flip is O(n) because we visit each node once
     * reverse left and right children recursively
     */
    public void flip() {
        flip(root); // Start at the root
    }
    private void flip(BinaryNode t){
        if(t == null){
            return; // base case never follow a null node :)))
        }

        //Swap left and right children

        BinaryNode temp = t.left; // Temporary Node
        t.left = t.right; //set the left node to the right node
        t.right = temp; // set the right node back to our temp node to finish swapping

        // Recursively do this for all the nodes
        flip(t.left);
        flip(t.right);
    }

    /**
     * Counts number of nodes in specified level
     * The complexity of nodesInLevel is O(n) because we have to visit every node in the tree
     * @param level Level in tree, root is zero
     * @return count of number of nodes at specified level
     */
    public int nodesInLevel(int level) {
        return nodesInLevel(root, level); // Recursion

    }

    private int nodesInLevel(BinaryNode node, int level) {
        if(node == null){
            return 0; // Base case if null there are no nodes
        }
        if(level==0){
            return 1; //if we reach level 0 that means we reached the desired level, we'll keep subtracting by 1 til we get here
        }

        //Recursively count nodes in left and right subtrees
        return nodesInLevel(node.left, level-1) + nodesInLevel(node.right, level-1);

    }

    /**
     * Print all paths from root to leaves
     * The complexity of printAllPaths is O(n) because we look at every node
     */
    public void printAllPaths() {
        int[] path = new int[10000000]; //we prolly won't exceed this number I bet you
        printAllPaths(root, path, 0);
    }

    private void printAllPaths(BinaryNode node, int[] path, int length) {
        if(node == null){
            return; // If node is null return base case
        }
        path[length] = node.element; // Add current node to path
        length++; // Keep track of length of path

        //if its a leaf node print the path
        if(node.left == null && node.right == null){
            printPath(path, length);
        } else{
            printAllPaths(node.left, path, length);
            printAllPaths(node.right, path, length);
        }
    }

    // Function to print array path
    private void printPath(int[] path, int length) {
        for(int i = 0; i<length; i++){
            System.out.print(path[i]+ " ");
        }
        System.out.println();
    }

    private int bstCount=0;
    /**
     * Counts all non-null binary search trees embedded in tree
     *  The complexity of countBST depends on tree. if its balanced its O(logn) if its not balanced its O(n)
     * @return Count of embedded binary search trees
     */

    public Integer countBST() {
        bstCount=0;
        countBSTHelper(root, Integer.MIN_VALUE, Integer.MAX_VALUE);
        return bstCount;
    }

    private boolean countBSTHelper(BinaryNode node, int min, int max) {
        if(node == null){
            return true; // empty subtree is a bst

        }
        // check if crrent node viilates BST properties

        if(node.element <= min || node.element >= max){
            return false;
        }

        boolean isLeftBST = countBSTHelper(node.left, min, node.element);
        boolean isRightBST = countBSTHelper(node.right, node.element, max);

        if(isLeftBST && isRightBST){
            bstCount++;
            return true;
        }
        return false;


    }

    /**
     * Insert into a bst tree; duplicates are allowed
     * The complexity of bstInsert depends on the tree.  If it is balanced the complexity is O(log n)
     * @param x the item to insert.
     */
    public void bstInsert(Integer x) {

        root = bstInsert(x, root);
    }

    /**
     * Internal method to insert into a subtree.
     * In tree is balanced, this routine runs in O(log n)
     * @param x the item to insert.
     * @param t the node that roots the subtree.
     * @return the new root of the subtree.
     */
    private BinaryNode bstInsert(Integer x, BinaryNode t) {
        if (t == null)
            return new BinaryNode (x, null, null);
        int compareResult = x.compareTo(t.element);
        if (compareResult < 0) {
            t.left = bstInsert(x, t.left);
        } else {
            t.right = bstInsert(x, t.right);
        }
        return t;
    }

    /**
     * Determines if item is in tree
     * @param item the item to search for.
     * @return true if found.
     */
    public boolean contains(Integer item) {
        return contains(item, root);
    }

    /**
     * Internal method to find an item in a subtree.
     * This routine runs in O(log n) as there is only one recursive call that is executed and the work
     * associated with a single call is independent of the size of the tree: a=1, b=2, k=0
     *
     * @param x is item to search for.
     * @param t the node that roots the subtree.
     * @return node containing the matched item.
     */
    private boolean contains(Integer x, BinaryNode t) {
        if (t == null)
            return false;

        int compareResult = x.compareTo(t.element);

        if (compareResult < 0)
            return contains(x, t.left);
        else if (compareResult > 0)
            return contains(x, t.right);
        else {
            return true;    // Match
        }
    }
    /**
     * Remove all paths from tree that sum to less than given value
     * @param sum: minimum path sum allowed in final tree
     *           This is also O(n) because we have to visit every node
     */
    public void pruneK(Integer sum) {
        root = pruneK(root, 0, sum);
    }

    private BinaryNode pruneK(BinaryNode t, int sum, int minSum) {
        if(t == null){
            return null; // nothing to prune
        }
        sum += t.element; // add current node to level value

        // recursively prune left and right subtrees
        t.left = pruneK(t.left, sum, minSum);
        t.right = pruneK(t.right, sum, minSum);

        //if node is a leaf and sum is less than K, prune it!
        if (t.left == null && t.right == null && sum < minSum){
            return null; // - Prune the node
        }
        return t; // otherwise keep it in the tree
    }

    /**
     * Build tree given inOrder and preOrder traversals.  Each value is unique
     * @param inOrder  List of tree nodes in inorder
     * @param preOrder List of tree nodes in preorder
     */
    public void buildTreeFromTraversals(Integer[] inOrder, Integer[] preOrder) {
        root = null;
    }

    /**
     * Find the least common ancestor of two nodes
     * @param a first node
     * @param b second node
     * @return String representation of ancestor
     */

    public BinaryNode lca(BinaryNode  t,Integer a, Integer b) {
        if(!nodeExists(t, a) || !nodeExists(t, b)){
            return null; // Was having issues because node 62
            // doesn't exist in treeOne but
            // it was still finding an LCA,
            // this prevents that from happening.
            // It does return null though, so I am not
            // sure what the most correct way to go about this was

        }

        if(t ==null){
            return null;
        }

        // if both a and b are smaller than current node go left
        if(a<t.element && b<t.element){
            return lca(t.left,a,b);
        }

        //if both a and b are greater than current node go right
        if(a>t.element && b>t.element){
            return lca(t.right,a,b);
        }

        // return t if t is the LCA because a and b are on different sides
        return t;
    }
    public Integer sumAll(){
        BinaryNode  r =   root;
        return sumAll(r);
    }
    public Integer sumAll(BinaryNode  t){
        if (t==null) return 0;
        return t.element + sumAll(t.left) + sumAll(t.right);
    }

    public Integer lca(Integer a, Integer b) {

        BinaryNode  l  = lca(root,a,b);
        if (l==null) return null;
        return l.element;

    }
    private boolean nodeExists(BinaryNode t, Integer key){
        if(t == null){
            return false;

        }
        if(t.element.equals(key)) {
            return true;
        }
        if (key< t.element){
            return nodeExists(t.left, key);
        }else{
            return nodeExists(t.right, key);
        }

    }
    /**
     * Balance the tree - do not use rotations,
     * Instead rebuild the tree
     */
    public void balanceTree() {
        // Collect elements in sorted list
        List<Integer> sortedList = new LinkedList<>();
        TraverseCollect(root, sortedList); // Helper method

        // Rebuild the tree as balanced binary search tree
        root = buildBalancedBST(sortedList, 0, sortedList.size()-1);
    }

    private void TraverseCollect(BinaryNode root, List<Integer> sortedList) {
        if (root == null) return;
        // traverse left subtree
        TraverseCollect(root.left, sortedList);
        // add element
        sortedList.add(root.element);
        // traverse right
        TraverseCollect(root.right, sortedList);

    }
    private BinaryNode buildBalancedBST(List<Integer> sortedList, int start, int end) {
        if (start > end) return null;

        // calculate middle index
        int mid = (start + end) / 2;

        // create a node with the middle element (root)\
        BinaryNode node = new BinaryNode(sortedList.get(mid));

        // recursively build left and right subtrees
        node.left = buildBalancedBST(sortedList, start, mid - 1);
        node.right = buildBalancedBST(sortedList, mid + 1, end);
        return node;
    }

    /**
     * In a BST, keep only nodes between range
     *
     * @param a lowest value
     * @param b highest value
     */
    public void keepRange(Integer a, Integer b) {
        root = keepRange(root, a, b);
    }

    private BinaryNode keepRange(BinaryNode root, Integer a, Integer b) {
        if (root == null) return null;
        // if current node value less than a, discard node
        if(root.element<a){
            return keepRange(root.right, a, b);

        }
        if(root.element>b){
            return keepRange(root.left, a, b);
        }
        root.left = keepRange(root.left, a, b);
        root.right = keepRange(root.right, a, b);
        return root;
    }

    // Basic node stored in unbalanced binary  trees
    public static class BinaryNode  {
        Integer element;            // The data in the node
        BinaryNode left;   // Left child
        BinaryNode  right;  // Right child

        // Constructors
        BinaryNode(Integer theElement) {
            this(theElement, null, null);
        }

        BinaryNode(Integer theElement, BinaryNode lt, BinaryNode rt) {
            element = theElement;
            left = lt;
            right = rt;
        }

        // toString for BinaryNode
        public String toString() {
            StringBuilder sb = new StringBuilder();
            sb.append("Node:");
            sb.append(element);
            return sb.toString();
        }

    }


}

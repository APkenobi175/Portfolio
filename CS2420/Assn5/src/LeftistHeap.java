public class LeftistHeap<T extends Comparable<T>> {
    private class Node {
        T data;
        Node left, right;
        int nullpathlength;

        Node(T data) {
            this.data = data;
            this.left = null;
            this.right = null;
            this.nullpathlength = 0;
        }
    }

    private Node root;

    public LeftistHeap() {
        this.root = null;
    }

    // Merge the heaps at h1 and h2
    private Node merge(Node h1, Node h2) {
        if (h1 == null) return h2;
        if (h2 == null) return h1;

        // make sure that h1 is the smaller root
        if (h1.data.compareTo(h2.data) > 0) {
            Node tempnode = h1;
            h1 = h2;
            h2 = tempnode;
        }

        // Merge h1s right child with h2
        h1.right = merge(h1.right, h2);

        // Enforce leftistism by swapping children if need be
        if (getNPL(h1.left) < getNPL(h1.right)) {
            Node tempnode = h1.left;
            h1.left = h1.right;
            h1.right = tempnode;
        }

        // Update null path length
        h1.nullpathlength = getNPL(h1.right) + 1;

        return h1;
    }

    // Insert values into heap
    public void insert(T data) {
        Node newNode = new Node(data);
        root = merge(root, newNode);
    }

    // Delete and return min value from heap
    public T deleteMin() throws Exception {
        if (root == null) throw new Exception("Heap is EMPTY !!!!!111!!!!1!!!!11!!!!!!!!!!!");
        T minData = root.data;
        root = merge(root.left, root.right);
        return minData;
    }

    // Get null path length, return 0 for null nodes
    private int getNPL(Node n) {
        return (n == null) ? 0 : n.nullpathlength;
    }

    // Method to check if the heap is empty
    public boolean isEmpty() {
        return root == null;
    }
}

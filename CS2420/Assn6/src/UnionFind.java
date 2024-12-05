import java.util.Arrays;

public class UnionFind {
    private int[] parent;
    private int[] size;


    // Constructor, initialize the arrays
    public UnionFind(int n) {
        parent = new int[n];
        size = new int[n];
        for (int i = 0; i < n; i++) {
            parent[i] = i;
            size[i] = 1;
        }
    }

    // FIND
    public int find(int x) {
        if (parent[x] != x) {
            parent[x] = find(parent[x]); // path compression

        }
        return parent[x];
    }


    // Union by size
    public void union(int x, int y) {
        int rootX = find(x);
        int rootY = find(y);

        if (rootX != rootY) {
            // Attatch the smaller tree underneatht he larger tree
            if (size[rootX] < size[rootY]) {
                parent[rootX] = rootY;
                size[rootX] += size[rootY];

            }else{
                parent[rootY] = rootX;
                size[rootY] += size[rootX];
            }
        }
    }
    // Print the arrays that you have for testing
    public void printTheArrays(){
        System.out.println("Parent: " + Arrays.toString(parent));
        System.out.println("Size: " + Arrays.toString(size));



    }

    // return parent pls
    public int getParent(int index){
        return parent[index];
    }
}

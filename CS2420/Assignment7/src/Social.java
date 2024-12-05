import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;

public class Social {
    private int size;
    private int pathLength[][];
    private int inter[][];
    private int ctPaths[];
    private double betweenNess[];
    boolean DEBUG;
    int MAX=10;

    private ArrayList<String> nodes;

    public Social(String nodeFile, String edgeFile) {
        System.out.println("\n\n****" + nodeFile);
        size = 0;

        try {

            File file = new File(
                    nodeFile);
            BufferedReader br
                    = new BufferedReader(new FileReader(file));
            String st;
            nodes = new ArrayList<>();
            while ((st = br.readLine()) != null) {
                String anode = st.split(":")[0];
                nodes.add(anode);
            }
            size = nodes.size();
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }
        Collections.sort(nodes);
        DEBUG = nodes.size() < MAX;

        this.pathLength = new int[size][size];
        inter = new int[size][size];
        for (int[] row : pathLength) {
            Arrays.fill(row, size);
        }
        for (int[] row : inter) {
            Arrays.fill(row, -1);
        }
        for (int i = 0; i < size; i++)
            pathLength[i][i] = 0;

        try {

            File file = new File(edgeFile);
            BufferedReader br
                    = new BufferedReader(new FileReader(file));
            String st;
            int edgeCt = 0;
            while ((st = br.readLine()) != null) {
                edgeCt++;
                String edgeData[] = st.split(":");
                int node1 = nodes.indexOf(edgeData[0]);
                int node2 = nodes.indexOf(edgeData[1]);
                if (legal(node1) && legal(node2)) {
                    pathLength[node1][node2] = 1;
                    pathLength[node2][node1] = 1;
                    // if (DEBUG) System.out.println("EDGE " + node1 + " " + node2); (Used this to debug)
                } else System.out.println("Illegal " + node1 + " " + node2 + " size " + size);
            }
            System.out.println("Nodes " + size + " Edges " + edgeCt);
        } catch (Exception e) {
            System.out.println(e.getMessage());
        }

    }

    boolean legal(int n) {
        return (n >= 0) && (n < size);
    }


    public void printMatrix(String label, int[][] length, int[][] inter) {
        StringBuffer sb = new StringBuffer();
        sb.append(label + "\n");
        for (int i = 0; i < size; i++) {
            sb.append(String.format("%3d", i));
            sb.append(":");
            for (int j = 0; j < size; j++) {
                sb.append(String.format("%3d(%3d)", length[i][j], inter[i][j]));
                //sb.append(String.format("%3d", length[i][j])); idk what this is I think it was here when I started
            }
            sb.append("\n");
        }
        System.out.println("Path "+sb.toString());

    }

    public void computeShortestPaths() {
        for (int k = 0; k < size; k++) { // Intermediate node
            for (int i = 0; i < size; i++) { // Start node
                for (int j = 0; j < size; j++) { // End node
                    // If going through k gives a shorter path
                    if (pathLength[i][k] + pathLength[k][j] < pathLength[i][j]) {
                        pathLength[i][j] = pathLength[i][k] + pathLength[k][j];
                        inter[i][j] = k; // Update the intermediate node
                    }
                }
            }
        }
        if (DEBUG) {
            printMatrix("Lengths", inter, inter);
        }
    }





    public String findInter(int from, int to, boolean addDirect) {
        if (inter[from][to] == -1) {
            //  System.out.println("Direct path from " + from + " to " + to); (used this to DEBUG)
             return addDirect ? " " + to : "";
        }
        int mid = inter[from][to];
        // System.out.println("Path from " + from + " to " + to + " goes through " + mid); (used to DEBUG)
        return findInter(from, mid, true) + findInter(mid, to, true);
    }


    public void findBetweenness() {
        ctPaths = new int[size];
        betweenNess = new double[size];

        // Iterate through all pairs of nodes
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                if (i != j) {
                    // Get the intermediate nodes for the path from i to j
                    String path = findInter(i, j, true);
                    String[] nodesOnPath = path.trim().split(" ");

                    // Increment the count for each intermediate node
                    for (String node : nodesOnPath) {
                        int nodeIndex = Integer.parseInt(node.trim());
                        if (nodeIndex != i && nodeIndex != j) { // Ignore start and end nodes
                            ctPaths[nodeIndex]++;
                        }
                    }
                }
            }
        }

        // Figure out the  Betweenness Centrality
        int totalPairs = size * (size - 1);
        for (int k = 0; k < size; k++) {
            betweenNess[k] = (double) ctPaths[k] / totalPairs; // we want it to be decimals
        }

        // Print betweeness
        System.out.println("Betweenness:"); // match output from the assignment document
        for (int k = 0; k < size; k++) {
            System.out.printf("Node %d: %.2f%n", k, betweenNess[k]); // Rounds the betweeness to two decimal places

        }
    }







    public static void main(String[] args) {
        String[] nodes = {"NodeEx.txt", "Nodes0.txt", "Nodes1.txt", "Nodes2.txt", "crisis-nodes.txt", "got-nodes.txt"};
        String[] edges = {"EdgeEx.txt", "Edges0.txt", "Edges1.txt", "Edges2.txt", "crisis-edges.txt", "got-edges.txt"};
        int[] to = {4, 2, 6, 0, 50, 63};
        int[] from = {2, 4, 1, 4, 1, 105};

        for (int i = 0; i < nodes.length; i++) {
            Social s = new Social(nodes[i], edges[i]);

            // find shortest paths
            s.computeShortestPaths();

            // find Betweenness Centrality
            s.findBetweenness();

            // display paths
            String path = from[i] + s.findInter(from[i], to[i], false);
            System.out.println(nodes[i] + " Path: " + path);
        }
    }



}





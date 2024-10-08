import java.util.*;
import java.util.ArrayList;

public class Flooding {
    int[][] terrain;
    GridLocation[] sources;
    boolean[][] flooded;
    int height;
    int rows;
    int cols;
    int[][] whenFlood;

    Flooding(int[][] terrain, GridLocation[] sources, int height) {
        this.terrain = terrain;
        this.sources = sources;
        this.height = height;
        rows = terrain.length;
        cols = terrain[0].length;
    }
    // WhenFlood using priority queue
    public int[][] whenFlood(){
        int insertCt = 0;

        // Once again initialize whenFlood matrix with large values
        whenFlood = new int[rows][cols];
        for (int i = 0; i< rows; i++) {
            for (int j = 0; j< cols; j++) {
                whenFlood[i][j] = Integer.MAX_VALUE;
            }
        }

        // Create AVLTree to keep track of cells to process instead of an arraylist
        AVLTree<GridLocation> toDoList = new AVLTree<>();

        // Add water sources to the to-do list
        for (GridLocation source : sources) {
            int row = source.row;
            int col = source.col;
            whenFlood[row][col] = terrain[row][col];
            source.whenFlood = terrain[row][col];
            toDoList.insert(source);
            insertCt++;
        }

        // Process to do list

        while (!toDoList.isEmpty()){
            GridLocation current = toDoList.findMin();
            toDoList.deleteMin();
            int currentRow = current.row;
            int currentCol = current.col;
            int currentFloodTime = whenFlood[currentRow][currentCol];


            for (GridLocation neighbor : getNeighbors(currentRow, currentCol)) {
                int neighborRow = neighbor.row;
                int neighborCol = neighbor.col;
                int newFloodTime = Math.max(terrain[neighborRow][neighborCol], currentFloodTime);

                if (newFloodTime < whenFlood[neighborRow][neighborCol]){
                    whenFlood[neighborRow][neighborCol] = newFloodTime;
                    neighbor.whenFlood = newFloodTime;
                    toDoList.insert(neighbor);
                    insertCt++;
                }
            }
        }

        // Print the total number of nodes added to the to-do list
        System.out.println("PQ Nodes " + String.format("%,5d", insertCt));

        // Return the whenFlood matrix
        return whenFlood;




    }
    public int[][] whenFloodExhaustive(){
        int insertCount = 0;

        // Initialize the whenFlood matrix with large values that are cells that are not flood initially
        whenFlood = new int[rows][cols];
        for (int i = 0; i< rows; i++){
            for (int j = 0; j< cols; j++){
                whenFlood[i][j] = Integer.MAX_VALUE; // all cells are unflooded initially

            }
        }

        // TO DO LIST TO KEEP TRACK OF CELLS
        ArrayList<GridLocation> toDoList = new ArrayList<>();

        // Add all initial water sources to the to do list
        for (GridLocation source : sources){
            int row = source.row;
            int col = source.col;
            whenFlood[row][col] = terrain[row][col]; // the flood level is its terrain level
            toDoList.add(source); // Add source to to-do list
            insertCount++;
        }
       // Processing the to do list:
        while(!toDoList.isEmpty()){
            // Get the next item from the to do list
            GridLocation current = toDoList.remove(0);
            int currentRow = current.row;
            int currentCol = current.col;
            int currentFloodTime = whenFlood[currentRow][currentCol];

            // Get the neighbors of the current cell using getNeighbors helper method
            for (GridLocation neighbor : getNeighbors(currentRow, currentCol)){
                int neighborRow = neighbor.row;
                int neighborCol = neighbor.col;

                // calculate potential new flood time
                int newFloodTime = Math.max(terrain[neighborRow][neighborCol], currentFloodTime);
                if (newFloodTime < whenFlood[neighborRow][neighborCol]){
                    whenFlood[neighborRow][neighborCol] = newFloodTime;
                    toDoList.add(neighbor);
                    insertCount++;
                }
            }

        }
        // Print the total number of nodes in the to do list
        System.out.println("Exhaustive Nodes " + String.format("%5d", insertCount));
        return whenFlood;
    }
    private ArrayList<GridLocation> getNeighbors(int row, int col){
        ArrayList<GridLocation> neighbors = new ArrayList<>();
        if (row > 0) {
            neighbors.add(new GridLocation(row - 1, col)); // Up
        }
        if (row < rows - 1) {
            neighbors.add(new GridLocation(row + 1, col)); // Down
        }
        if (col > 0) {
            neighbors.add(new GridLocation(row, col - 1)); // Left
        }
        if (col < cols - 1) {
            neighbors.add(new GridLocation(row, col + 1)); // Right
        }

        return neighbors;
    }


    public boolean[][] markFloodedR() {
        System.out.println("Flooded in Regions Recursive");
        flooded = new boolean[rows][cols];
        for (int i = 0; i < rows; i++)
            Arrays.fill(flooded[i], false);
        for (GridLocation g : sources) {
            markFloodedR(g);

        }
        return flooded;
    }

    void markFloodedR(GridLocation g) {
        try {

            // Check conditions
          if(!validNeighbor(g) || flooded[g.row][g.col] || terrain[g.row][g.col] > height){
              return; // out of bounds, already flooded, or too high tto flood
          }

          //Mark current location as flooded

            flooded[g.row][g.col] = true;

          // check all four neighbors using this cool thing called recursion

            markFloodedR(new GridLocation(g.row -1, g.col)); //up
            markFloodedR(new GridLocation(g.row +1, g.col)); //down
            markFloodedR(new GridLocation(g.row, g.col -1)); // left
            markFloodedR(new GridLocation(g.row, g.col +1)); // right

        } catch (StackOverflowError e) {
            System.err.println("Stack Overflow");
            System.exit(0);
        }


    }

    public boolean[][] markFlooded() {
        flooded = new boolean[rows][cols];
        for (int i = 0; i < rows; i++)
            Arrays.fill(flooded[i], false); //  no flooded areas at start
        // create the queue as per the psudeocode
        Queue<GridLocation> queue = new LinkedList<>();

        // enqueue all water sources that are at or below water level
        for (GridLocation g : sources) {
            if (terrain[g.row][g.col] <= height) {
                flooded[g.row][g.col] = true; // it flooded whoopsies
                queue.add(g);
            }
        }

        //cardinal directions

        int[] CardinalRow = {-1, 1, 0, 0};
        int[] CardinalCol = {0, 0, -1, 1}; // up down, left right to find neighbors

        while(!queue.isEmpty()) {
            GridLocation current = queue.poll(); // dequeue the next flooded location (psudeocode)

            // check all four neighbors using the cardinal directions

            for (int i = 0; i < 4; i++) {
                int newRow = current.row + CardinalRow[i];
                int newCol = current.col + CardinalCol[i];

                GridLocation neighbor = new GridLocation(newRow, newCol);

                // if the neighbor is valid, not already flooded, and at or below the water level then its FLOODED!!!!! so flood it and add it to the queue

                if (validNeighbor(neighbor) && !flooded[newRow][newCol] && terrain[newRow][newCol] <= height) {

                    flooded[newRow][newCol] = true;
                    queue.add(neighbor);
                }
            }
        }

        return flooded;
    }

    boolean validNeighbor(GridLocation g) {
        int row = g.row;
        int col = g.col;
        return (row >= 0 && col >= 0 && row < rows && col < cols);
    }


}

import java.util.*;

public class Flooding {
    int[][] terrain;
    GridLocation[] sources;
    boolean[][] flooded;
    int height;
    int rows;
    int cols;

    Flooding(int[][] terrain, GridLocation[] sources, int height) {
        this.terrain = terrain;
        this.sources = sources;
        this.height = height;
        rows = terrain.length;
        cols = terrain[0].length;
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

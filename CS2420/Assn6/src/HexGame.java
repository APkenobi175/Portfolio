import java.io.*;
import java.util.*;

public class HexGame {
    private static final int RED = 1;
    private static final int BLUE = 2;
    private static final int NONE = 0;

    private final int size;
    private final UnionFind unionFind;
    private final int[][] board; // Tracks color of each cell (none, red and bklue)
    private final int topRed, bottomRed, leftBlue, rightBlue; // Virtual nodes of top bottom left and right

    // ANSI color codes
    private static final String ANSI_RESET = "\u001B[0m"; // Reset colors
    private static final String ANSI_RED = "\u001B[31m"; // 1 string 2 string Red string
    private static final String ANSI_BLUE = "\u001B[34m"; // Blue string

    private int redMoves = 0; // how many moves each color has made
    private int blueMoves = 0;

    public HexGame(int size) {
        this.size = size;
        this.unionFind = new UnionFind(size * size + 4); // union find with extra space for virtual nodes
        this.board = new int[size][size];

        // edge connections
        this.topRed = size * size;       // Virtual node for Red TOP
        this.bottomRed = size * size + 1; // Virtual node for Red BOTTOM
        this.leftBlue = size * size + 2;  // Virtual node for BLue LEFT
        this.rightBlue = size * size + 3; // Virtual node for Blue RIGHT
    }

    // move for the specified player at the given cell
    public boolean playMove(int player, int cell) {
        int row = (cell - 1) / size;
        int col = (cell - 1) % size;

        // Validate the move
        if (board[row][col] != NONE) {
            System.out.println("Invalid move: Cell " + cell + " is already occupied.");
            return false;
        }

        // Place the player's marker down
        board[row][col] = player;
        if (player == RED) redMoves++;
        else blueMoves++;

        // Union with neighbors of the same color
        int cellIndex = cell - 1;
        for (int neighbor : getNeighbors(cellIndex)) {
            int neighborRow = neighbor / size;
            int neighborCol = neighbor % size;
            if (neighbor >= 0 && neighbor < size * size && board[neighborRow][neighborCol] == player) {
                unionFind.union(cellIndex, neighbor);
            }
        }

        // Union with the virtual nodes for the edge connections
        if (player == RED) {
            if (row == 0) unionFind.union(cellIndex, topRed); // Connect top row to TOP
            if (row == size - 1) unionFind.union(cellIndex, bottomRed); // Connect bottom row to BOTTOM
        } else if (player == BLUE) {
            if (col == 0) unionFind.union(cellIndex, leftBlue); // Connect left column to LEFT
            if (col == size - 1) unionFind.union(cellIndex, rightBlue); // Connect right column to RIGHT
        }

        return true;
    }

    // Check if the player has won
    public boolean checkWin(int player) {
        if (player == RED) {
            return unionFind.find(topRed) == unionFind.find(bottomRed);
        } else if (player == BLUE) {
            return unionFind.find(leftBlue) == unionFind.find(rightBlue);
        }
        return false;
    }

    // Getter method for neighbors fof a cell index
    private List<Integer> getNeighbors(int cellIndex) {
        int row = cellIndex / size;
        int col = cellIndex % size;
        List<Integer> neighbors = new ArrayList<>();

        // Offsets for neighbors in NW NE W E SW SE directions
        int[] offsets = {-size, -size + 1, -1, 1, size - 1, size};

        for (int offset : offsets) {
            int neighbor = cellIndex + offset;
            int neighborRow = neighbor / size;
            int neighborCol = neighbor % size;

            // make sure the neighbor is within bounds
            if (neighbor >= 0 && neighbor < size * size &&
                    Math.abs(neighborRow - row) <= 1 &&
                    Math.abs(neighborCol - col) <= 1) {
                neighbors.add(neighbor);
            }
        }

        return neighbors;
    }

    // Print the game board
    public void printBoard() {
        for (int row = 0; row < board.length; row++) {
            // Indent each row to create hex layout
            for (int i = 0; i < row; i++) {
                System.out.print("  ");
            }
            for (int col = 0; col < board[row].length; col++) {
                if (board[row][col] == RED) {
                    System.out.print(ANSI_RED + "R " + ANSI_RESET);
                } else if (board[row][col] == BLUE) {
                    System.out.print(ANSI_BLUE + "B " + ANSI_RESET);
                } else {
                    System.out.print("0 ");
                }
            }
            System.out.println();
        }
    }

    // Play moves from a file
    public void playFromFile(String filename) {
        try (BufferedReader reader = new BufferedReader(new FileReader(filename))) {
            String line;
            int currentPlayer = BLUE;
            int totalMoves = 0;

            while ((line = reader.readLine()) != null) {
                int move = Integer.parseInt(line.trim());
                if (playMove(currentPlayer, move)) {
                    totalMoves++;
                    printBoard();
                    if (checkWin(currentPlayer)) {
                        System.out.println("----->" + (currentPlayer == RED ? ANSI_RED + "RED" : ANSI_BLUE + "BLUE") + ANSI_RESET + " has won after " + totalMoves + " attempted moves!");
                        System.out.println("RED moves: " + redMoves + ", BLUE moves: " + blueMoves); // print out how many moves each team used
                        return;
                    }
                    currentPlayer = (currentPlayer == RED ? BLUE : RED);
                }
            }
            System.out.println("No winner yet!");
        } catch (IOException e) {
            System.err.println("Error reading moves from file: " + e.getMessage()); // if no file
        }
    }

    // main
    public static void main(String[] args) {
        HexGame game = new HexGame(11);
        game.playFromFile("moves2.txt"); // this is where you can change between moves.txt and moves2.txt
    }
}

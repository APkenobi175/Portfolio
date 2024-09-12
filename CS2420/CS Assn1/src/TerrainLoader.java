import java.io.*;
import java.util.*;
public class TerrainLoader {

    public static Terrain loadTerrain(File filename) throws IOException {
        try (var br = new FileInputStream(filename)) {
            return loadTerrain(br);
        }
    }

    private static int nextInt(Scanner s) throws IOException {
        if (!s.hasNextInt()) throw new IOException("Malformed file.");
        return s.nextInt();
    }

    private static Terrain loadTerrain(InputStream stream) throws IOException {
        try (var input = new Scanner(stream)) {
            /* Read the terrain size. */
            int numRows = nextInt(input);
            int numCols = nextInt(input);
            var heights = new int[numRows][numCols];
            int min  = Integer.MAX_VALUE;
            int max = Integer.MIN_VALUE;

            /* Read the water sources. */
            int numSources = nextInt(input);
            var sources = new GridLocation[numSources];
            for (int i = 0; i < numSources; i++) {
                int row = nextInt(input);
                int col = nextInt(input);
                sources[i] = new GridLocation(row, col);
            }

            /* Read the height data. */
            for (int row = 0; row < numRows; row++) {
                for (int col = 0; col < numCols; col++) {
                    heights[row][col] = nextInt(input);
                    if (heights[row][col]>max)
                        max = heights[row][col];
                    if (heights[row][col]<min)
                        min = heights[row][col];
                }
            }

            return new Terrain(heights, sources,min,max);
        } catch (RuntimeException e) {
            throw new IOException("Error reading terrain.", e);
        }
    }

}

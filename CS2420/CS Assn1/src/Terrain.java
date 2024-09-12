import java.util.*;

public class Terrain {
    public int[][] heights;
    public GridLocation[] waterSources;
    public int min;
    public int max;

    public Terrain(int[][] heights, GridLocation[] sources,int min, int max) {
        this.heights = heights;
        this.waterSources = sources;
        this.min = min;
        this.max = max;

    }

    @Override public String toString() {
        return Arrays.deepToString(heights) + Arrays.deepToString(waterSources);
    }
}

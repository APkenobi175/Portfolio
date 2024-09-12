import javax.swing.*;
import java.awt.*;

public class Display extends JPanel {
    /* Terrain data */
    private int[][] heights;
    private GridLocation[] sources;

    /* Which cells are flooded; can change. */
    private boolean[][] flooded;

    /* Min and max height; used to interpolate heights to colors. */
    private int minHeight, maxHeight;
    boolean wantSourceShown= false;  // If set to true, will show source as a white square
    public int getMinHeight(){
        return minHeight;
    }
    public int getMaxHeight(){
        return maxHeight;
    }

    /* Color of flooded cells. */
    private static final Color UNDERWATER_COLOR = new Color(0, 49, 83); // Prussian blue

    /* The rest of the map is colored according to the following scheme. The heights are mapped
     * to real numbers between 0 and 1. Those real numbers are then used to interpolate between
     * a fixed series of color points marked off at various intervals.
     *
     * The RGBPoint type represents a particular RGB color annotated with a threshold value
     * between 0 and 1 indicating where that color sits.
     */
    private static final class RGBPoint {
        public final int red, green, blue;
        public final double threshold;

        public RGBPoint(int r, int g, int b, double t) {
            red = r;
            green = g;
            blue = b;
            threshold = t;
        }
    }

    /* Background color */
    private static final Color BACKGROUND_COLOR = new Color(102, 2, 60); // Tyrian purple


    /* The actual colors to use to draw the map, annotated with their threshold values.
     * We will scale the height to be a ratio between 0 (minimum) and 1 (maximum).
     * The threshold allows us to pick the colors unequally.  So anything between
     * .25 and .4 (in scale) will be between Maize and Metallic gold */

    private static final RGBPoint[] COLORS = new RGBPoint[]{
            new RGBPoint(0, 102, 0, 0.0),   // Pakistan green
            new RGBPoint(154, 205, 50, 0.1),   // Chartreuse
            new RGBPoint(251, 236, 93, 0.25),   // Maize
            new RGBPoint(212, 175, 55, 0.4),   // Metallic gold
            new RGBPoint(153, 76, 0, 0.75),   // LightBrown
            new RGBPoint(51, 25, 0, 1.01)    // Sienna. The 1.01 here is to ensure we cover rounding errors.
    };


    /* Initial dimensions. */
    private static final int DEFAULT_WIDTH = 800;
    private static final int DEFAULT_HEIGHT = 640;
    public Display() {
        setPreferredSize(new Dimension(DEFAULT_WIDTH, DEFAULT_HEIGHT));
    }

    String toStringGrid(int[][] d){
        StringBuffer sb = new StringBuffer();
        for (int i=0; i < d.length; i++) {
            for (int j = 0; j < d[0].length; j++) {
                sb.append(String.format("%4d", d[i][j]));
            }
            sb.append("\n");
        }
        return sb.toString();
    }

    public void setTerrain(Terrain t) {
        /* Stash the terrain. */
        this.heights = t.heights;
        this.sources = t.waterSources;

        /* Clear flooding, since the terrain has changed. */
        this.flooded = null;

        minHeight = t.min;
        maxHeight = t.max;
        if (heights.length<50 )
            System.out.println(toStringGrid(heights));

        //System.out.println("Set Terrain Max Height " + maxHeight + " Min Height " + minHeight);
    }

    public void setFlooding(boolean[][] flooded) {
        this.flooded = flooded;
    }

    /**
     *
     * @param value to be scaled
     * @param min  lowest value can take on
     * @param max  highest value cane take on
     * @param newMin lowest of converted range
     * @param newMax highest of converted range
     * @return a scaled value between newMin and newMax
     */
    private static double scaleIt(double value, double min, double max, double  newMin, double newMax) {
        return (value - min) / (max - min + 0.000001) * (newMax - newMin) + newMin;
    }

    /**
     * @param row
     * @param col
     * @return the color for the terrain at cell at row,col
     */
    private Color colorFor(int row, int col) {
        if(wantSourceShown && isSource(row,col)) return Color.WHITE;
        /* Water always draws blue. */
        if (flooded!=null && flooded[row][col]) return UNDERWATER_COLOR;

        /* Map  height to a value in the interval [0, 1) */
        double alpha = scaleIt((double) heights[row][col], (double) minHeight, (double) maxHeight, 0.0, 1.0);

        /* Figure out which points we're between. */
        for (int i = 1; i < COLORS.length; i++) {
            if (alpha <= COLORS[i].threshold) {
                /* Progress is measured by how far between the two points we are. 0.0 means
                 * "completely at the left end. 1.0 means "completely at the right end."
                 */
                double progress = (alpha - COLORS[i - 1].threshold) /
                        (COLORS[i].threshold - COLORS[i - 1].threshold);

                /* Interpolate between those color points to get our overall color. */
                int red = (int) scaleIt(progress, 0, 1, COLORS[i - 1].red, COLORS[i].red);
                int green = (int) scaleIt(progress, 0, 1, COLORS[i - 1].green, COLORS[i].green);
                int blue = (int) scaleIt(progress, 0, 1, COLORS[i - 1].blue, COLORS[i].blue);

                return new Color(red, green, blue);
            }
        }
        System.out.println( row + " "+ col + " Alpha "+ alpha + " Terrain "  + heights[row][col] +" Min " + minHeight + "  max " + maxHeight);
        return Color.WHITE;
        //throw new RuntimeException("Color For Impossible.");
    }

    public boolean isSource(int row, int col){
        for (GridLocation g:sources){
            if (g.row == row && g.col==col) return true;
        }
        return false;
    }

    @Override
    public void paint(Graphics g) {
        /* Draw the background. */
        g.setColor(BACKGROUND_COLOR);
        g.fillRect(0, 0, getWidth(), getHeight());

        if (heights == null){
            //System.out.println("Missing terrain ");
            return;
        }

        /* Compute our aspect ratio. */
        double width = getWidth();
        double height = getHeight();

        double aspectRatio = (double) heights[0].length / heights.length;

        /* Aspect ratio is too wide. Bring the width down. */
        if (width / height > aspectRatio) {
            width = height * aspectRatio;
        }
        /* Aspect ratio is too tall. Bring the height down. */
        else {
            height = width / aspectRatio;
        }

        int baseX = (int) ((getWidth() - width) / 2.0);
        int baseY = (int) ((getHeight() - height) / 2.0);

        for (int x = baseX; x < baseX + width; x++) {
            for (int y = baseY; y < baseY + height; y++) {
                int col = (int)scaleIt((double)x, (double)baseX,  (baseX + width+1), 0.0, (double) heights[0].length);
                int row = (int)scaleIt((double)y, (double)baseY,  (baseY + height+1), 0.0, (double) heights.length);

                g.setColor(colorFor(row, col));
                g.fillRect(x, y, 1, 1);
            }
        }
    }
}
